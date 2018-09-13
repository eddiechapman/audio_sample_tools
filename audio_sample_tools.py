# bit_depth_converter.py
#
# Prepares the bit depth and filename length of audio files for use on the MPC 1000
#
# Converts a directory of wav files to 16 bit depth. Directory structure and
# filenames are maintained. Any filenames longer than 16 characters are exported
# in a text file for future renaming.

import csv
import json
import os
import re


ROOT = '/home/eddie/Music/Samples/JULEZ JADON DRUMS'

def parse_directory(ROOT):
    """Store the name and location of all wav files in a folder of folders"""
    sample_info = []
    for directory, sub_directories, files in os.walk(ROOT):
        for file in files:
            if file.endswith('.wav'):
                sample = {
                    'file': file,
                    'directory': directory
                }
                sample_info.append(sample)
    return sample_info


def seperate_kit_sub_kit(sample):
    """Save the name of the folder and subfolder the sample was found in"""
    sample['kit'] = sample['directory'].split('/')[-2]
    sample['sub_kit'] = sample['directory'].split('/')[-1]


def seperate_filename_extension(sample):
    """Save the name and extension of the file separately"""
    sample['filename'] = os.path.splitext(sample['file'])[0]
    sample['filetype'] = os.path.splitext(sample['file'])[1]


def filename_spaces_to_underscores(sample):
    """Replace any spaces in filename with underscores"""
    sample['filename'] = sample['filename'].replace(' ', '_')


def extract_filename_info(sample):
    """List components of filename that are separated by an underscore"""
    sample['filename_info'] = sample['filename'].split('_')


def categorize_sound(sample):
    """Save the sample category using the first filename component"""
    sample['category'] = sample['filename_info'][0]


def find_name(sample):
    """Save the description of the sample using the second filename component"""
    sample['name'] = sample['filename_info'][1]


def find_variant(sample):
    """Save the number at the end of the sample name as the variation number"""
    pattern = re.compile(r'\d$')
    results = pattern.search(sample['filename_info'][1])
    if results:
        sample['variant'] = results.group()


def find_parent(sample):
    """Save the sample name minus the variation number"""
    if 'variant' in sample:
        sample['parent'] = sample['name'].replace(sample['variant'], '')


def find_bpm(sample):
    """Find and store the beats per minute value"""
    pattern = re.compile(r'\d{2,3}\.?\d?BPM')
    possible_bpm_locations = sample['file'] + sample['sub_kit']
    results = pattern.search(possible_bpm_locations)
    if results:
        sample['bpm'] = results.group().replace('BPM', '')
    else:
        sample['bpm'] = 'N/A'


def find_effect(sample):
    """Determine if sample is wet or dry"""
    if 'Wet' in sample['filename_info']:
        sample['effect'] = 'Wet'
    elif 'Dry' in sample['filename_info']:
        sample['effect'] = 'Dry'

def find_filter(sample):
    pass


def find_key(sample):
    """Find and store the key or pitch of the sample"""
    pattern = re.compile(r'([A-G])#?(maj|min)')
    possible_key_locations = sample['file'] + sample['sub_kit']
    results = pattern.search(possible_key_locations)
    if results:
        sample['key'] = results.group(0)    # (0): pattern uses matching so result groups must be joined
    else:
        sample['key'] = 'N/A'


def find_808_key(sample):
    """Find the key or pitch for 808 files"""
    if sample['category'] == 808 or '808':
        pattern = re.compile(r'([A-G])#?\d?$')
        results = pattern.search(sample['filename_info'][-1])
        if results:
            sample['key'] = results.group(0)


def write_csv(sample_info):
    """Output the contents to a CSV file"""
    with open('sample_info.csv', 'w') as csv_file:
        #column_names = sample_info[0].keys()
        column_names = ['file', 'directory', 'filename', 'filetype', 'kit', 'sub_kit', 'filename_info', 'category', 'name', 'parent', 'variant', 'effect', 'bpm', 'key']
        print(column_names)
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(sample_info)


def main():
    sample_info = parse_directory(ROOT)
    for sample in sample_info:
        seperate_filename_extension(sample)
        seperate_kit_sub_kit(sample)
        filename_spaces_to_underscores(sample)
        extract_filename_info(sample)
        find_name(sample)
        find_variant(sample)
        find_parent(sample)
        categorize_sound(sample)
        find_bpm(sample)
        find_effect(sample)
        find_filter(sample)
        find_key(sample)
        find_808_key(sample)
        print(json.dumps(sample, indent=1))
    write_csv(sample_info)

main()

