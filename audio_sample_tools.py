# bit_depth_converter.py
#
# Prepares the bit depth and filename length of audio files for use on the MPC 1000
#
# Converts a directory of wav files to 16 bit depth. Directory structure and
# filenames are maintained. Any filenames longer than 16 characters are exported
# in a text file for future renaming.

import json
import os.path
import re


ROOT = '/home/eddie/Music/Samples/JULEZ JADON DRUMS'

def parse_directory(ROOT):
    sample_info = []
    for directory, sub_directories, files in os.walk(ROOT):
        for file in files:
            if file.endswith('.wav'):
                sample = {
                    'file': file,
                    'filename': file.split('.')[0],
                    'filetype': file.split('.')[1],
                    'kit': directory.split('/')[-2],
                    'sub_kit': directory.split('/')[-1]
                }
                sample_info.append(sample)
    return sample_info


def extract_filename_info(sample):
    sample['filename_info'] = sample['filename'].split('_')


def categorize_sound(sample):
    sample['category'] = sample['filename_info'][0]


def find_name(sample):
    sample['name'] = sample['filename_info'][1]


def find_bpm(sample):
    pattern = re.compile(r'\d{2,3}\.?\d?BPM')
    possible_bpm_locations = sample['file'] + sample['sub_kit']
    results = pattern.search(possible_bpm_locations)
    if results:
        sample['BPM'] = results.group().replace('BPM', '')
        sample['loop'] = 'True'
    else:
        sample['loop'] = 'False'
        sample['BPM'] = 'N/A'

def find_effect(sample):
    pass

def find_filter(sample):
    pass

def find_key(sample):
    pattern = re.compile(r'([A-G])#?(maj|min)')
    possible_key_locations = sample['file'] + sample['sub_kit']
    results = pattern.search(possible_key_locations)
    if results:
        sample['key'] = results.group(0)    # (0): pattern uses matching so result groups must be joined


def main():
    sample_info = parse_directory(ROOT)
    for sample in sample_info:
        extract_filename_info(sample)
        find_name(sample)
        categorize_sound(sample)
        find_bpm(sample)
        find_effect(sample)
        find_filter(sample)
        find_key(sample)
        print(json.dumps(sample, indent=1))

main()

