#!/usr/local/bin/python3

import multiprocessing as mp

import os

import csv

import sys

import png
from numpy import percentile, array, concatenate, amin, amax, append, zeros, uint8

# Designed and forged from the ground up by Douwe den Blanken

class Csv2ir:
    @staticmethod
    def create_images(input_folder_name, output_folder_name):
        # Make sure that the output folder is created, in case it did not yet exist
        if os.path.exists(output_folder_name) == False:
            os.mkdir(output_folder_name)

        pool = mp.Pool(mp.cpu_count())

        process_counter = 0

        for file_name in os.listdir(input_folder_name):
            if file_name.endswith('.csv') == False:
                raise Exception('The file with name"' +
                                file_name + '" is not a CSV file!')
            else:
                with open(input_folder_name + '/' + file_name) as csv_file:
                    file_with_commas = csv_file.read()

                    # Make sure that all of the commas have been replaced by dots, while also all of
                    # the trailing ;'s, which cause numpy to comply as these entries in the list are
                    # of type string instead of type number, are removed
                    file_with_dots = file_with_commas.replace(
                        ',', '.').replace(';\n', '\n')

                    # A list needs to made out of the CSV module ouptut, because the value returned
                    # by csv.reader is an iterator over the rows
                    # Also, the ; is used as delimiter and by using .QUOTE...NNUMERIC we convert all
                    # of the list values, which normally would be of type string, into number
                    csv_2d_file = list(csv.reader(
                        file_with_dots.splitlines(), delimiter=';', quoting=csv.QUOTE_NONNUMERIC))

                    pool.apply_async(Csv2ir.create_ir_image, args=(
                        process_counter, csv_2d_file, file_name, output_folder_name), callback=Csv2ir.write_image)

                    process_counter += 1

        pool.close()
        pool.join()

    @staticmethod
    def create_ir_image(file_index, temp_2d_list, file_name, output_folder):
        img_width = len(temp_2d_list[0])
        img_height = len(temp_2d_list)

        temp_values_1d = array(temp_2d_list).flatten()

        lowest_temp = amin(temp_values_1d)  # for 2D: 7.6
        highest_temp = amax(temp_values_1d)  # for 2D: 12.1
        half_percentile_temp = percentile(
            temp_values_1d, 50, axis=0)  # for 2D: 9.85

        # 1D color array, in the form of: R, G, B, R, G, B ....
        # if not set to uint8, and bitdepth=8 at png.Writer() line, the image will not show up
        # correctly
        rgb_values = zeros((img_height*img_width*3,), dtype=uint8)

        min_color = [0, 0, 255]
        max_color = [255, 255, 0]
        middle_color = [255, 0, 0]

        for index in range(0, len(temp_values_1d)):
            temp_rgb = []

            current_temp = temp_values_1d[index]
            if current_temp > half_percentile_temp:
                temp_rgb = Csv2ir.interpolate_color(
                    middle_color, max_color, half_percentile_temp, highest_temp, current_temp)
            elif current_temp < half_percentile_temp:
                temp_rgb = Csv2ir.interpolate_color(
                    min_color, middle_color, lowest_temp, half_percentile_temp, current_temp)
            else:   # if current_temp == half_percentile_temp, the least possible occurence so we
                    # only put it at the end
                temp_rgb = middle_color

            rgb_fill_index = index*3

            for color in temp_rgb:
                rgb_values[rgb_fill_index] = color
                rgb_fill_index += 1

        return(file_index, [png.Writer(width=img_width, height=img_height, bitdepth=8, alpha=False,
                                       transparent=None, greyscale=False), rgb_values, file_name, output_folder])

    @staticmethod
    def write_image(result):
        create_ir_image_result = result[1]

        writer = create_ir_image_result[0]
        rgb_values = create_ir_image_result[1]

        image_file_name = create_ir_image_result[2].replace('.csv', '.png')
        folder_name = create_ir_image_result[3]

        image_file = open(folder_name + '/' +
                          image_file_name, 'wb')  # wb = write bytes

        writer.write_array(image_file, rgb_values)

        image_file.close()

    @staticmethod
    def interpolate_color(rgb_1, rgb_2, min, max, value):
        min_max_diff = max - min
        value_min_diff = value - min

        factor = value_min_diff/min_max_diff

        r_diff = rgb_2[0] - rgb_1[0]
        g_diff = rgb_2[1] - rgb_1[1]
        b_diff = rgb_2[2] - rgb_1[2]

        return([rgb_1[0] + int(factor*r_diff), rgb_1[1] + int(factor*g_diff), rgb_1[2] + int(factor*b_diff)])
