import argparse
import assemblyai as aai
import os
import json
from talklink.models import Transcript, TranscriptUtterance
import math
import librosa
import soundfile as sf
import tempfile
import subprocess
import shutil

def speed_up_audio_ffmpeg(file_path, speed_factor=1.0):
    """
    Speed up an audio file by the given factor using FFmpeg.
    
    Args:
        file_path: Path to the audio file
        speed_factor: Factor to speed up the audio (e.g., 1.5 for 1.5x speed)
        
    Returns:
        Path to the sped-up audio file (temporary file)
    """
    print(f"Speeding up audio by {speed_factor}x using FFmpeg")
    if speed_factor == 1.0:
        return file_path
    
    # Check if ffmpeg is available
    if shutil.which("ffmpeg") is None:
        print("FFmpeg not found. Falling back to librosa implementation.")
        return speed_up_audio_librosa(file_path, speed_factor)
    
    # Create a temporary file for the sped-up audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    
    # Use FFmpeg to speed up the audio
    # The atempo filter can only handle speed factors between 0.5 and 2.0
    # For higher speed factors, we chain multiple atempo filters
    atempo_chain = ""
    remaining_factor = speed_factor
    
    while remaining_factor > 2.0:
        atempo_chain += "atempo=2.0,"
        remaining_factor /= 2.0
    
    atempo_chain += f"atempo={remaining_factor}"
    
    cmd = [
        "ffmpeg",
        "-i", file_path,
        "-filter:a", atempo_chain,
        "-y",  # Overwrite output file if it exists
        temp_file.name
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return temp_file.name
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
        print("Falling back to librosa implementation.")
        return speed_up_audio_librosa(file_path, speed_factor)

def speed_up_audio_librosa(file_path, speed_factor=1.0):
    """
    Speed up an audio file by the given factor using librosa.
    
    Args:
        file_path: Path to the audio file
        speed_factor: Factor to speed up the audio (e.g., 1.5 for 1.5x speed)
        
    Returns:
        Path to the sped-up audio file (temporary file)
    """
    print(f"Speeding up audio by {speed_factor}x using librosa")
    if speed_factor == 1.0:
        return file_path
        
    # Load the audio file with librosa
    y, sr = librosa.load(file_path, sr=None)
    
    # Speed up the audio using librosa's time_stretch
    y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    
    # Create a temporary file for the sped-up audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    sf.write(temp_file.name, y_fast, sr, format='wav')
    
    return temp_file.name

# Default to FFmpeg implementation, with librosa as fallback
speed_up_audio = speed_up_audio_ffmpeg

def transcribe_audio(file_url, output_path, speed_factor=1.0, use_ffmpeg=True) -> Transcript:
    """
    Transcribe an audio file with optional speed adjustment to reduce costs.
    
    Args:
        file_url: URL or path to the audio file
        output_path: Path to save the transcript
        speed_factor: Factor to speed up the audio before transcription (e.g., 1.5 for 1.5x speed)
        use_ffmpeg: Whether to use FFmpeg (True) or librosa (False) for audio processing
        
    Returns:
        Transcript object
    """
    # Choose the appropriate speed-up function
    speed_up_func = speed_up_audio_ffmpeg if use_ffmpeg else speed_up_audio_librosa
    
    # Speed up the audio if requested
    processed_file = file_url
    if speed_factor > 1.0:
        print(f"Speeding up audio by {speed_factor}x to reduce transcription costs")
        processed_file = speed_up_func(file_url, speed_factor)
    
    print("Setting up AssemblyAI")
    # Set up AssemblyAI
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speaker_labels=True)
    config.speech_model = aai.SpeechModel.nano
    transcriber = aai.Transcriber()
    
    # Transcribe the audio
    transcript = transcriber.transcribe(
        processed_file,
        config=config
    )
    print(f"Transcription complete. Utterances saved to {output_path}")

    transcript_utterances = []
    
    # Process the transcript and adjust timestamps if needed
    for utterance in transcript.utterances:
        words = utterance.words
        while len(words) > 0:
            if len(words) > 160:
                cutoff_index = 150
                
                while cutoff_index < 200 and words[cutoff_index - 1].text[-1] not in ['.', '?', '!']:
                    cutoff_index += 1
                
                if cutoff_index >= len(words):
                    cutoff_index = len(words)
                
                new_statement = ' '.join(word.text for word in words[:cutoff_index])
                
                # Adjust timestamps if audio was sped up
                start_time = math.floor(words[0].start / 1000)
                end_time = math.floor(words[cutoff_index - 1].end / 1000)
                
                if speed_factor > 1.0:
                    start_time = math.floor(start_time * speed_factor)
                    end_time = math.floor(end_time * speed_factor)
                
                transcript_utterances.append(TranscriptUtterance(
                    start_time=start_time,
                    end_time=end_time,
                    text=new_statement,
                    speaker=f"Unknown {utterance.speaker}"
                ))
                words = words[cutoff_index:]
            else:
                new_statement = ' '.join(word.text for word in words)
                
                # Adjust timestamps if audio was sped up
                start_time = math.floor(words[0].start / 1000)
                end_time = math.floor(words[-1].end / 1000)
                
                if speed_factor > 1.0:
                    start_time = math.floor(start_time * speed_factor)
                    end_time = math.floor(end_time * speed_factor)
                
                transcript_utterances.append(TranscriptUtterance(
                    start_time=start_time,
                    end_time=end_time,
                    text=new_statement,
                    speaker=f"Unknown {utterance.speaker}"
                ))
                words = []

    print(f"Writing transcript to file {output_path}")

    transcript_data = Transcript(content_url=file_url, utterances=transcript_utterances)

    with open(output_path, 'w') as f:
        json.dump(transcript_data.model_dump(), f, indent=4)
    
    # Clean up temporary file if created
    if processed_file != file_url and os.path.exists(processed_file):
        os.unlink(processed_file)

    return transcript_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transcribe audio using AssemblyAI.')
    parser.add_argument('--audio', required=True, help='The path of the audio file to transcribe')
    parser.add_argument('--output', required=True, help='The path to save the output file')
    parser.add_argument('--speed', type=float, default=1.0, help='Speed factor to apply to audio (e.g., 1.5 for 1.5x speed)')
    parser.add_argument('--use-librosa', action='store_true', help='Use librosa instead of FFmpeg for audio processing')
    args = parser.parse_args()

    transcribe_audio(args.audio, args.output, args.speed, not args.use_librosa)


