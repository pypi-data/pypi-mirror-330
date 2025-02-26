import argparse
import os
import importlib.resources as pkg_resources
from talklink.models import ClaimsData, Transcript, load_claims_from_json, load_transcript_from_json
from jinja2 import Environment, FileSystemLoader

def format_timestamp(start_time: float):
    timestamp = int(float(start_time))
    hours, remainder = divmod(timestamp, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_timestamp = f"{hours}:{minutes:02}:{seconds:02}"
    return formatted_timestamp

def generate_talklink_page(transcript: Transcript, claims: ClaimsData, video_id: str, speakers: str, video_title="Talk Link", toc_path="TODO_REPLACE_WITH_TOC_PATH", create_isolated_html=False, styles_file_path="TODO_REPLACE_WITH_STYLES_FILE_PATH", script_file_path="TODO_REPLACE_WITH_SCRIPT_FILE_PATH"):
    if video_title == "":
        video_title = "Talk Link"

    newColors = ["#D52941", "#B3EFB2", "#DC5E42", "#058ED9", "#CEBACF", "#9cd08f", "#CEA0AE", "#DAA588", "#3F4531", "#214F4B"]
    templates_path = os.path.join(pkg_resources.files('talklink'), 'resources/talklink_page')
    env = Environment(loader=FileSystemLoader(templates_path))

    speakers = speakers.split(",")
    
    # Define colors for different claim types
    claimTypeColors = {
        "fact": "#4285F4",       # Blue
        "opinion": "#EA4335",    # Red
        "prediction": "#FBBC05", # Yellow
        "question": "#34A853",   # Green
        "general": "#9AA0A6",    # Gray (default)
        "argument": "#8E24AA",   # Purple
        "evidence": "#00ACC1",   # Cyan
        "anecdote": "#FF6D00",   # Orange
        "definition": "#3949AB", # Indigo
        "statistic": "#00897B"   # Teal
    }

    data = {
        "video_id": video_id,
        "transcript": transcript,
        "claims": claims,
        "speakers": speakers,
        "format_timestamp": format_timestamp,
        "badgeColor": {speaker: newColors[i % len(newColors)] for i, speaker in enumerate(speakers)},
        "claimTypeColors": claimTypeColors,
        "toc": toc_path,
        "video_title": video_title,
        "create_isolated_html": create_isolated_html,
        "styles_file_path": styles_file_path,
        "script_file_path": script_file_path
    }

    template = env.get_template("template.md")
    html_content = template.render(data)

    return html_content

def main():
    parser = argparse.ArgumentParser(description='Generate HTML from transcript with links.')
    parser.add_argument('--input_file_path', type=str, required=True, help='Path to the input transcript file')
    parser.add_argument('--video_url', type=str, required=True, help='YouTube video URL')
    parser.add_argument('--speakers', type=str, required=True, help='Comma-separated list of speakers')
    parser.add_argument('--is_json', action='store_true', help='Indicates if the input transcript is in JSON format')
    parser.add_argument('--create_isolated_html', action='store_true', help='Create HTML with external CSS and JS links')
    parser.add_argument('--styles_file_path', required=False, default="TODO_REPLACE_WITH_STYLES_FILE_PATH", help='Path to the style file')
    parser.add_argument('--script_file_path', required=False, default="TODO_REPLACE_WITH_SCRIPT_FILE_PATH", help='Path to the script file')
    args = parser.parse_parse_args()

    transcript = load_transcript_from_json(args.input_file_path)
    claims = load_claims_from_json(args.input_file_path)

    html_output = generate_talklink_page(transcript, claims, args.video_url, args.speakers, create_isolated_html=args.create_isolated_html, styles_file_path=args.styles_file_path, script_file_path=args.script_file_path)

    with open('talklink_page.html', 'w') as html_file:
        html_file.write(html_output)

    print(f"HTML output saved to: talklink_page.html")

if __name__ == "__main__":
    main()
