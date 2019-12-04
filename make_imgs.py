import multiprocessing as mp

import sys

from Csv2ir import Csv2ir

# Test that has to be ran if this script needs to be executed on Windows. Without this check and without 
# mp.freeze_support() following right after this check, Windows will not be able to properly run multicore
# Python functionality
# This check evaluates to True when you are running this file as python make_imgs.py
if __name__ == "__main__":
    mp.freeze_support()

    # Default folder names
    input_dir_name = 'csv'
    output_dir_name = 'ir'

    # Check if CLI parameters are present
    if len(sys.argv) == 3:
        input_dir_name = sys.argv[1]
        output_dir_name = sys.argv[2]

    Csv2ir.create_images(input_dir_name, output_dir_name)