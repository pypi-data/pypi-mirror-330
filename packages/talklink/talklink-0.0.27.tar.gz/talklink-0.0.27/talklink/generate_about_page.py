#!/usr/bin/env python3
"""
TalkLink About Page Generator

This script generates the About page for the TalkLink website based on a template.
It uses Jinja2 for templating and includes dynamic content such as features, team members,
and support options.

Usage:
    python generate_about_page.py [--output OUTPUT_PATH] [--create_isolated_html] [--styles_file_path STYLES_PATH]

Arguments:
    --output: Path to the output HTML file (default: talklink/resources/about/about.html)
    --create_isolated_html: Include CSS and JS directly in the HTML file
    --styles_file_path: Path to the CSS file (default: ../table_of_contents/styles.css)

Example:
    python generate_about_page.py --output resources/about/about.html

Author: TalkLink Team
"""

import os
import argparse
import datetime

from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

def generate_about_page(create_isolated_html=False, styles_file_path="TODO_REPLACE_WITH_STYLES_FILE_PATH", script_file_path="TODO_REPLACE_WITH_SCRIPT_FILE_PATH") -> str:
    """
    Generate the About page for TalkLink.
    
    Args:
        create_isolated_html: Whether to include CSS and JS directly in the HTML file
        styles_file_path: Path to the CSS file
        
    Returns:
        str: The generated HTML content
    """
    templates_path = os.path.join(pkg_resources.files('talklink'), 'resources/about')
    env = Environment(loader=FileSystemLoader(templates_path))
    
    # Define the features
    features = [
        {
            "icon": "fas fa-search",
            "title": "Searchable Transcripts",
            "description": "Quickly find specific moments in videos by searching the transcript."
        },
        {
            "icon": "fas fa-comment-alt",
            "title": "Interactive Timestamps",
            "description": "Click on any part of the transcript to jump to that exact moment in the video."
        },
        {
            "icon": "fas fa-tag",
            "title": "Claim Identification",
            "description": "Identify different types of claims made in videos with our color-coded system."
        },
        {
            "icon": "fas fa-share-alt",
            "title": "Shareable Links",
            "description": "Share specific moments from videos with timestamped links."
        },
        {
            "icon": "fas fa-moon",
            "title": "Dark Mode",
            "description": "Comfortable viewing experience in any lighting condition."
        },
        {
            "icon": "fas fa-keyboard",
            "title": "Keyboard Shortcuts",
            "description": "Navigate efficiently with intuitive keyboard controls."
        }
    ]
    
    # Define how it works steps
    how_it_works = [
        {
            "title": "Browse our collection",
            "description": "of videos with interactive transcripts"
        },
        {
            "title": "Search for specific content",
            "description": "within videos using our powerful search feature"
        },
        {
            "title": "Click on any part of the transcript",
            "description": "to jump to that moment in the video"
        },
        {
            "title": "Identify different types of claims",
            "description": "with our color-coded system"
        },
        {
            "title": "Share specific moments",
            "description": "with timestamped links"
        }
    ]
    
    '''
    # Define team members
    team_members = [
        {
            "name": "David Schneck",
            "role": "Founder & Lead Developer",
            "image": "https://randomuser.me/api/portraits/men/32.jpg",
            "social_links": [
                {"icon": "fab fa-twitter", "url": "#"},
                {"icon": "fab fa-github", "url": "#"},
                {"icon": "fab fa-linkedin", "url": "#"}
            ]
        }
    ]
    '''
    # Define support options
    support_options = [
        {
            "html": 'Buying us a coffee through our <a href="https://buymeacoffee.com/talklink" target="_blank">Buy Me A Coffee</a> page'
        },
        {
            "html": 'Sharing TalkLink with your friends and colleagues'
        },
        {
            "html": 'Providing feedback and suggestions for improvement'
        }
    ]
    
    # Define social links
    social_links = [
        {"icon": "fab fa-twitter", "url": "#"},
        {"icon": "fab fa-github", "url": "#"},
        {"icon": "fab fa-linkedin", "url": "#"}
    ]
    
    # Get current year for copyright
    current_year = datetime.datetime.now().year
    
    template = env.get_template('template.md')
    about_content = template.render(
        features=features,
        how_it_works=how_it_works,
        #team_members=team_members,
        support_options=support_options,
        social_links=social_links,
        contact_email="contact@talklink.com",
        home_link="/",
        about_link="/about.html",
        current_year=current_year,
        create_isolated_html=create_isolated_html,
        styles_file_path=styles_file_path,
        script_file_path=script_file_path
    )
    
    return about_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate TalkLink About Page')
    parser.add_argument('--output', type=str, required=False, default="", help='Path to the output file')
    parser.add_argument('--create_isolated_html', action='store_true', help='Create HTML with embedded CSS and JS')
    parser.add_argument('--styles_file_path', required=False, default="TODO_REPLACE_WITH_STYLES_FILE_PATH", help='Path to the style file')
    parser.add_argument('--script_file_path', required=False, default="TODO_REPLACE_WITH_SCRIPT_FILE_PATH", help='Path to the script file')
    args = parser.parse_args()

    about_page = generate_about_page(
        create_isolated_html=args.create_isolated_html, 
        styles_file_path=args.styles_file_path,
        script_file_path=args.script_file_path
    )
    
    output_dir = os.path.dirname(args.output) if args.output else '.'
    
    with open(args.output, "w") as about_file:
        about_file.write(about_page)
    
    print(f"About page generated successfully at {args.output}") 