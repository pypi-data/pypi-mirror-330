import argparse
import json
import tiktoken
from typing import Dict, Any, List, Protocol, Optional, Type
from abc import ABC, abstractmethod
from openai import OpenAI
from talklink.models import ClaimsData, Transcript, load_transcript_from_json

# Optimized system prompt - more concise while maintaining clarity
SYSTEM_PROMPT = """
You are an AI assistant specialized in extracting claims from conversation transcripts. Extract precise, contextually complete, and self-contained claims.

Claim Types:
1. opinion - Subjective statements
2. fact - Verifiable statements based on objective reality
3. prediction - Assertions about future events
4. evaluation - Judgments or assessments
5. cause-and-effect - Statements asserting causation
6. comparison - Statements comparing two or more things
7. conditional - Statements about what would happen under certain conditions
8. prescriptive - Statements about what should be done
9. definitional - Statements about what something is or means
10. existential - Assertions that something exists or does not exist
11. miscellaneous - Other claims not fitting above categories

Guidelines:
- Extract contextually complete claims that can stand alone
- Convert to third-person perspective where applicable
- Classify each claim accurately
- Use timestamps in "MM:SS" format when available
- IMPORTANT: Only include utterances that contain at least one claim - DO NOT include utterances with empty claims arrays
- Don't include the speaker name in the claim text, refer to them as "they" or "them"

Output Format:
{
  "utterances": [
    {
      "time_range": "MM:SS - MM:SS",
      "speaker": "Speaker Name",
      "claims": [
        {
          "type": "claim_type",
          "text": "Complete, self-contained claim text",
        }
      ]
    }
  ]
}
"""

# Abstract base class for model providers
class ModelProvider(ABC):
    @abstractmethod
    def extract_claims(self, transcript_chunk: Transcript, system_prompt: str) -> ClaimsData:
        """Extract claims from a transcript chunk using the model provider's API"""
        pass
    
    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """Get the token count for the given text"""
        pass
    
    @abstractmethod
    def get_max_tokens(self) -> int:
        """Get the maximum token limit for this model provider"""
        pass

# OpenAI model provider implementation
class OpenAIProvider(ModelProvider):
    def __init__(self, model_name: str = "gpt-4o"):
        self.client = OpenAI()
        self.model_name = model_name
        self.encoder = tiktoken.encoding_for_model(model_name)
    
    def extract_claims(self, transcript_chunk: Transcript, system_prompt: str) -> ClaimsData:
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript_chunk.model_dump_json()}
                ],
                response_format=ClaimsData
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            print(f"Error extracting claims: {e}")
            return ClaimsData(utterances=[])
    
    def get_token_count(self, text: str) -> int:
        return len(self.encoder.encode(text))
    
    def get_max_tokens(self) -> int:
        # Different models have different token limits
        if "gpt-4o" in self.model_name:
            return 8000
        elif "gpt-4o-mini" in self.model_name:
            return 8000
        else:
            return 4000  # Default for other models

# Factory for creating model providers
class ModelProviderFactory:
    @staticmethod
    def create_provider(provider_type: str, **kwargs) -> ModelProvider:
        if provider_type.lower() == "openai":
            return OpenAIProvider(**kwargs)
        # Add more providers as needed
        # elif provider_type.lower() == "anthropic":
        #     return AnthropicProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")

# Main claim extraction logic
class ClaimExtractor:
    def __init__(self, model_provider: ModelProvider, system_prompt: str = SYSTEM_PROMPT):
        self.model_provider = model_provider
        self.system_prompt = system_prompt
    
    def chunk_transcript(self, transcript: Transcript) -> List[Transcript]:
        """Splits transcript into chunks that fit within the model's token limit."""
        max_tokens = self.model_provider.get_max_tokens()
        prompt_tokens = self.model_provider.get_token_count(self.system_prompt)
        available_tokens = max_tokens - prompt_tokens - 500  # Reserve tokens for the response
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for utterance in transcript.utterances:
            utterance_json = json.dumps(utterance.model_dump())
            utterance_tokens = self.model_provider.get_token_count(utterance_json)
            
            if current_tokens + utterance_tokens > available_tokens:
                if current_chunk:
                    chunks.append(Transcript(content_url=transcript.content_url, utterances=current_chunk))
                    current_chunk = []
                    current_tokens = 0
            
            current_chunk.append(utterance)
            current_tokens += utterance_tokens
        
        if current_chunk:
            chunks.append(Transcript(content_url=transcript.content_url, utterances=current_chunk))
        
        return chunks
    
    def batch_process_chunks(self, chunks: List[Transcript], batch_size: int = 5) -> List[ClaimsData]:
        """Process chunks in batches to optimize API calls."""
        results = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}...")
            
            # Process each chunk in the batch
            batch_results = []
            for chunk in batch:
                claims = self.model_provider.extract_claims(chunk, self.system_prompt)
                batch_results.append(claims)
            
            results.extend(batch_results)
        
        return results
    
    def extract_claims(self, transcript: Transcript) -> ClaimsData:
        """Extract claims from a full transcript, handling chunking if needed."""
        print(f"Processing {len(transcript.utterances)} utterances...")
        
        # Split transcript into manageable chunks
        chunks = self.chunk_transcript(transcript)
        print(f"Split into {len(chunks)} chunks")
        
        # Process chunks in batches
        claims_data_list = self.batch_process_chunks(chunks)
        
        # Combine results
        combined_claims = ClaimsData(utterances=[])
        for claims_data in claims_data_list:
            combined_claims.utterances.extend(claims_data.utterances)
        
        # Filter out utterances with empty claims
        filtered_claims = self._filter_empty_claims(combined_claims)
        
        print(f"Finished processing {len(filtered_claims.utterances)} utterances with claims.")
        return filtered_claims
    
    def _filter_empty_claims(self, claims_data: ClaimsData) -> ClaimsData:
        """Filter out utterances with empty claims arrays."""
        filtered_utterances = [u for u in claims_data.utterances if u.claims and len(u.claims) > 0]
        return ClaimsData(utterances=filtered_utterances)

def main(transcript_path: str, output_path: str, provider_type: str = "openai", model_name: str = "gpt-4o-mini"):
    # Load transcript
    transcript = load_transcript_from_json(transcript_path)
    
    # Create model provider and claim extractor
    model_provider = ModelProviderFactory.create_provider(provider_type, model_name=model_name)
    claim_extractor = ClaimExtractor(model_provider)
    
    # Extract claims
    claims_data = claim_extractor.extract_claims(transcript)
    
    # Save results
    with open(output_path, "w") as file:
        json.dump(claims_data.model_dump(), file, indent=4)
    
    print(f"Claims extracted and saved to {output_path}")

# Convenience function for backward compatibility
def extract_claims_from_transcript(transcript: Transcript, 
                                  provider_type: str = "openai", 
                                  model_name: str = "gpt-4o-mini") -> ClaimsData:
    """Simple function to extract claims from a transcript using default settings."""
    model_provider = ModelProviderFactory.create_provider(provider_type, model_name=model_name)
    claim_extractor = ClaimExtractor(model_provider)  # Uses default SYSTEM_PROMPT
    return claim_extractor.extract_claims(transcript)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract claims from a transcript.")
    parser.add_argument("--transcript", required=True, help="Path to the transcript JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file for extracted claims.")
    parser.add_argument("--provider", default="openai", help="Model provider to use (e.g., openai)")
    parser.add_argument("--model", default="gpt-4o", help="Model name to use")
    args = parser.parse_args()
    
    main(args.transcript, args.output, args.provider, args.model)
