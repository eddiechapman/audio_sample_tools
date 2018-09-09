# bit_depth_converter.py
#
# Prepares the bit depth and filename length of audio files for use on the MPC 1000
#
# Converts a directory of wav files to 16 bit depth. Directory structure and
# filenames are maintained. Any filenames longer than 16 characters are exported
# in a text file for future renaming.


import os
import csv

import pathlib
from subprocess import Popen, PIPE


def main():

    root = 'julez_jadon_drums'
    path = os.path.join(root, '/home/eddie/Music/Samples')
    sample_info = []
    categories = set()

    # TODO: first create list of (dirpath, filename) to then iterate over

    for dirpaths, dirnames, filenames in os.walk(path):
        os.chdir(dirpaths)
        wav_files = [file for file in filenames if file.endswith('.wav')]
        wav_files.sort()
        for i, file in enumerate(wav_files):
            sample = {}
            file_bits = file.split('_')
            path_bits = dirpaths.split('/')

            index = str(i)
            # pads zeros to left of index number
            sample['sample_id'] = index.zfill(5)

            sample['filename'] = file

            sample['kit'] = path_bits[5]

            sample['subdir'] = path_bits[6]

            sample['category'] = file_bits[0]
            categories.add(file_bits[0])

            sample['name'] = file_bits[1]

            if 'wet' or 'Wet' or 'FX' or 'Delay' in file_bits[2:]:
                sample['effect'] = 'Wet'
            elif 'dry' or 'Dry' in file_bits[2:]:
                sample['effect'] = 'Dry'

            if 'filter' or 'Filter' in file_bits[2:]:
                sample['filter'] = 'Filter'

            if 'BPM' in file_bits:
                sample['loop'] = 'True'
            else:
                sample['loop'] = 'False'

            if 'L' in file_bits[2:]:
                sample['rl'] = 'L'

            elif 'R' in file_bits[2:]:
                sample['rl'] = 'R'

            sample_info.append(sample)
    cat_list = [cat for cat in categories]
    cat_list.sort()
    for cat in cat_list:
        print(cat)




    with open('sample_info.csv', 'w') as outfile:
        os.chdir('/home/eddie/Music/Samples')
        writer = csv.writer(outfile)
        writer.writerows(sample_info)
        print(os.path.abspath('sample_info.csv'))
        print(len('sample_info.csv'))
main()
    # for
    #
    # p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    # p.stdout.close()
    # p.wait()


# def convert_bit_depth(file):
#     for f in file:
#          sox stuff
#
#             print
#             os.path.join(root, file)