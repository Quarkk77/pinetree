#!/usr/bin/env python3

import os
import sys
import subprocess
import configparser
import curses
import argparse

# Configuration file path under ~/.config/pinetree
CONF_DIR = os.path.expanduser("~/.config/pinetree")
CONF_FILE = os.path.join(CONF_DIR, 'audio_converter.conf')

# Ensure ~/.config/pinetree exists
if not os.path.exists(CONF_DIR):
    os.makedirs(CONF_DIR)

# Create default configuration if it doesn't exist
def create_default_config():
    config = configparser.ConfigParser()
    config['SUPPORTED_FILETYPES'] = {
        'input_types': 'flac,wav,aac,ogg,mp4,m4a',
        'output_types': 'mp3,wav,ogg'
    }
    with open(CONF_FILE, 'w') as configfile:
        config.write(configfile)

# Read supported file types from the configuration
def read_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONF_FILE):
        create_default_config()
    config.read(CONF_FILE)
    input_types = config['SUPPORTED_FILETYPES']['input_types'].split(',')
    output_types = config['SUPPORTED_FILETYPES']['output_types'].split(',')
    return input_types, output_types

# Arrow key navigation for selecting input/output formats
def select_format(screen, options, title):
    current_selection = 0
    while True:
        screen.clear()
        screen.bkgd(curses.color_pair(0))  # Use the default terminal background color
        screen.addstr(0, 0, f"Select {title}:")
        for i, option in enumerate(options):
            if i == current_selection:
                screen.addstr(i + 1, 0, f"> {option}", curses.A_REVERSE)
            else:
                screen.addstr(i + 1, 0, f"  {option}")
        key = screen.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(options) - 1:
            current_selection += 1
        elif key == ord('\n'):
            return options[current_selection]

# Recursively convert audio files
def convert_files(input_ext, output_ext, start_directory):
    for root, _, files in os.walk(start_directory):
        for file in files:
            if input_ext == "*" or file.endswith(f".{input_ext}"):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, f"{os.path.splitext(file)[0]}.{output_ext}")
                if not os.path.exists(output_file):
                    print(f"Converting {input_file} to {output_file}")
                    subprocess.run([
                        'ffmpeg', '-i', input_file, '-codec:a', 'libmp3lame' if output_ext == 'mp3' else 'copy',
                        '-map_metadata', '0', output_file
                    ])
                else:
                    print(f"Skipping {input_file}, output file already exists.")

# Main function
def main(screen, start_directory):
    input_types, output_types = read_config()
    input_types.append("*")  # Add option to convert all supported input types
    input_ext = select_format(screen, input_types, "input file type")
    output_ext = select_format(screen, output_types, "output file type")

    if input_ext == "*":
        for input_type in input_types[:-1]:
            convert_files(input_type, output_ext, start_directory)
    else:
        convert_files(input_ext, output_ext, start_directory)

# Argument parsing for starting directory
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Pinetree Audio Converter")
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help='Starting directory')
    args = parser.parse_args()

    # Launch curses-based UI for format selection
    curses.wrapper(main, args.directory)
