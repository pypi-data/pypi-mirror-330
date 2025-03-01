import os
import json
import argparse
import datetime

from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

def generate_index(folder_path: str, create_isolated_html=False, styles_file_path="TODO_REPLACE_WITH_STYLES_FILE_PATH", script_file_path="TODO_REPLACE_WITH_SCRIPT_FILE_PATH") -> str:
    if folder_path == "":
        folder_path = "."
    templates_path = os.path.join(pkg_resources.files('talklink'), 'resources/table_of_contents')
    env = Environment(loader=FileSystemLoader(templates_path))

    index_map = {}
    channelIdMap = {}
    todays_videos = {}  # Dictionary to hold today's videos
    yesterdays_videos = {}  # New dictionary to hold yesterday's videos
    
    # Get today's and yesterday's dates
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    today_date = today.strftime("%B %d, %Y")
    yesterday_date = yesterday.strftime("%B %d, %Y")

    for channel in os.listdir(folder_path):
        channel_path = os.path.join(folder_path, channel)
        if os.path.isdir(channel_path):
            index_map[channel] = {}
            for video_id in os.listdir(channel_path):
                video_path = os.path.join(channel_path, video_id)
                if os.path.isdir(video_path):
                    talklink_file = os.path.abspath(os.path.join(video_path, "talklink_page.html"))
                    video_info_file = os.path.join(video_path, "video_info.json")
                    if os.path.isfile(talklink_file) and os.path.isfile(video_info_file):
                        with open(video_info_file, 'r') as f:
                            video_info = json.load(f)
                            title = video_info.get("title", video_id)
                            channel_id = video_info.get("channel_id", channel)
                            duration = video_info.get("duration_string", "00:00:00")
                            upload_date = video_info.get("upload_date", "10000101")
                            upload_date_int = int(upload_date)
                            if isinstance(upload_date, str) and len(upload_date) == 8:
                                upload_date = datetime.datetime.strptime(upload_date, "%Y%m%d").strftime("%B %d, %Y")
                                
                                # Check if the upload date is today or yesterday
                                if upload_date == today_date:
                                    todays_videos[video_id] = {
                                        "title": title,
                                        "talklink_file": talklink_file,
                                        "duration": duration,
                                        "upload_date": upload_date,
                                        "upload_date_int": upload_date_int,
                                        "channel": channel
                                    }
                                elif upload_date == yesterday_date:
                                    yesterdays_videos[video_id] = {
                                        "title": title,
                                        "talklink_file": talklink_file,
                                        "duration": duration,
                                        "upload_date": upload_date,
                                        "upload_date_int": upload_date_int,
                                        "channel": channel
                                    }
                    else:
                        title = video_id
                        duration = "00:00:00"
                        upload_date = "January 1, 1000"
                        upload_date_int = 10000101
                    index_map[channel][video_id] = {
                        "id": video_id,
                        "title": title,
                        "talklink_file": talklink_file,
                        "duration": duration,
                        "upload_date": upload_date,
                        "upload_date_int": upload_date_int
                    }
                    channelIdMap[channel] = f"https://www.youtube.com/channel/{channel_id}"
    
    # Sort the videos by upload_date for each channel in reverse order
    for channel in index_map:
        index_map[channel] = dict(sorted(index_map[channel].items(), key=lambda item: item[1]["upload_date_int"], reverse=True))
    
    template = env.get_template('template.md')
    index_content = template.render(
        index_map=index_map, 
        channelIdMap=channelIdMap, 
        todays_videos=todays_videos,
        yesterdays_videos=yesterdays_videos,
        today_date=today_date,
        yesterday_date=yesterday_date,
        create_isolated_html=create_isolated_html,
        styles_file_path=styles_file_path,
        script_file_path=script_file_path
    )
    
    return index_content
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Talklink Index')
    parser.add_argument('--pages', type=str, default="", help='Path to the folder containing channel data')
    parser.add_argument('--output', type=str, help='Path to the output file')
    parser.add_argument('--create_isolated_html', action='store_true', help='Create HTML with external CSS and JS links')
    parser.add_argument('--styles_file_path', required=False, default="TODO_REPLACE_WITH_STYLE_FILE_PATH", help='Path to the style file')
    parser.add_argument('--script_file_path', required=False, default="TODO_REPLACE_WITH_SCRIPT_FILE_PATH", help='Path to the script file')
    args = parser.parse_args()

    index = generate_index(args.pages, create_isolated_html=args.create_isolated_html, styles_file_path=args.styles_file_path, script_file_path=args.script_file_path)
    
    # Get the output directory from the output file path
    output_dir = os.path.dirname(args.output) if args.output else '.'
    
    with open(args.output, "w") as index_file:
        index_file.write(index)