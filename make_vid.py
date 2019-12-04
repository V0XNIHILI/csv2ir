import sys

from Imgs2vid import Imgs2vid

# Default output and input names
input_dir_name = './ir/'
output_dir_name = 'video.avi'
fps = 15

# Check if CLI parameters are present
if len(sys.argv) == 4:
    input_dir_name = sys.argv[1]
    output_file_name = sys.argv[2]
    fps = sys.argv[3]

Imgs2vid.create_video(input_dir_name, output_file_name, fps)
