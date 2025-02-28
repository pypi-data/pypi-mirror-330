#!/usr/bin/env python3

"""
TalkLink All Videos Page Generator

This script generates the All Videos page for the TalkLink website based on a template.
It uses Jinja2 for templating and includes all videos from the index map.

Usage:
    python generate_all_videos_page.py [--pages PAGES_PATH] [--output OUTPUT_PATH] [--create_isolated_html] [--styles_file_path STYLES_PATH]

Arguments:
    --pages: Path to the folder containing channel data (default: current directory)
    --output: Path to the output HTML file (default: talklink/resources/all_videos/all_videos.html)
    --create_isolated_html: Include CSS and JS directly in the HTML file
    --styles_file_path: Path to the CSS file (default: ../table_of_contents/styles.css)

Example:
    python generate_all_videos_page.py --pages /path/to/channels --output resources/all_videos/all_videos.html

Author: TalkLink Team
"""

import os
import argparse
import datetime
import json

from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

def generate_all_videos_page(index_map, channelIdMap, create_isolated_html=False, styles_file_path="../table_of_contents/styles.css") -> str:
    """
    Generate the All Videos page for TalkLink.
    
    Args:
        index_map: Dictionary mapping channels to videos
        channelIdMap: Dictionary mapping channel names to channel IDs
        create_isolated_html: Whether to include CSS and JS directly in the HTML file
        styles_file_path: Path to the CSS file
        
    Returns:
        str: The generated HTML content
    """
    templates_path = os.path.join(pkg_resources.files('talklink'), 'resources/all_videos')
    env = Environment(loader=FileSystemLoader(templates_path))
    
    # Define social links
    social_links = [
        {"icon": "fab fa-twitter", "url": "#"},
        {"icon": "fab fa-github", "url": "#"},
        {"icon": "fab fa-linkedin", "url": "#"}
    ]
    
    # Get current year for copyright
    current_year = datetime.datetime.now().year
    
    template = env.get_template('template.md')
    all_videos_content = template.render(
        index_map=index_map,
        channelIdMap=channelIdMap,
        social_links=social_links,
        current_year=current_year,
        home_link="../table_of_contents/toc.html",
        about_link="../about/about.html",
        create_isolated_html=create_isolated_html,
        styles_file_path=styles_file_path
    )
    
    return all_videos_content

def load_index_map(folder_path=""):
    """
    Load the index map and channel ID map from video info files.
    
    Args:
        folder_path: Path to the folder containing channel data
        
    Returns:
        tuple: (index_map, channelIdMap)
    """
    if folder_path == "":
        folder_path = "."
        
    index_map = {}
    channelIdMap = {}
    
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
                    else:
                        title = video_id
                        duration = "00:00:00"
                        upload_date = "January 1, 1000"
                        upload_date_int = 10000101
                        channel_id = channel
                        
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
    
    return index_map, channelIdMap

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate TalkLink All Videos Page')
    parser.add_argument('--pages', type=str, default="", help='Path to the folder containing channel data')
    parser.add_argument('--output', type=str, default="talklink/resources/all_videos/all_videos.html", help='Path to the output file')
    parser.add_argument('--create_isolated_html', action='store_true', help='Create HTML with embedded CSS and JS')
    parser.add_argument('--styles_file_path', required=False, default="../table_of_contents/styles.css", help='Path to the style file')
    args = parser.parse_args()

    # Load the index map
    index_map, channelIdMap = load_index_map(args.pages)
    
    # Generate the All Videos page
    all_videos_page = generate_all_videos_page(
        index_map=index_map,
        channelIdMap=channelIdMap,
        create_isolated_html=args.create_isolated_html, 
        styles_file_path=args.styles_file_path
    )
    
    # Get the output directory from the output file path
    output_dir = os.path.dirname(args.output)
    
    # Only try to create the directory if there is a directory path
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(args.output, "w") as all_videos_file:
        all_videos_file.write(all_videos_page)
    
    print(f"All Videos page generated successfully at {args.output}") 