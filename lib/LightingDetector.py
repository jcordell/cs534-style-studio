import numpy as np
from scipy import ndimage
import cv2
from PIL import Image
from tqdm import tqdm

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


# takes an image as input, returns the degree direction of lighting
def get_lighting_direction(np_image):
    # image should already be in grayscale
    for row in np_image:
        diff = np.diff(row) / row[:-1] * 100.
        print(diff)
        break
    return 1


def get_lighting_map(grayscale_np_image, box_size=9):
    # get average pixel value around each pixel
    result = grayscale_np_image
    result = ndimage.generic_filter(
        grayscale_np_image, np.nanmean, size=box_size, mode='constant', cval=np.NaN)
    return result


def calculate_color_distance(color1, color2):
    color1_rgb = sRGBColor(color1[0], color1[1], color1[2])
    color2_rgb = sRGBColor(color2[0], color2[1], color2[2])

    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return delta_e


def get_lighting_percentage(lighting_map, np_image, comparison_width=40):
    lighting_percentile_map = np.empty(np.shape(lighting_map))
    size_x, size_y = np.shape(lighting_map)
    # coun
    for row in tqdm(range(len(lighting_map))):

        # for each pixel, count how many pixels left and right are greater than current pixel
        for current_pixel in range(len(lighting_map[row])):
            brighter_pixels = 0
            darker_pixels = 0

            # only look between (current_pixel - 80) - (current_pixel + 80)
            start_pixel = np.amax([current_pixel - comparison_width, 0])
            end_pixel = np.amin(
                [current_pixel + comparison_width, len(lighting_map[row])])

            for comparison_pixel_indx in range(start_pixel, end_pixel):

                comparison_pixel = lighting_map[row][comparison_pixel_indx]

                # only compare pixels if pixel colors are similar
                if calculate_color_distance(np_image[row, comparison_pixel], np_image[row, current_pixel]) < 50:
                    if lighting_map[row, comparison_pixel] > lighting_map[row, current_pixel]:
                        brighter_pixels += 1
                    else:
                        darker_pixels += 1

            lighting_avg = darker_pixels / size_x
            lighting_percentile_map[row, current_pixel] = lighting_avg
    # denormalize between 0 to 255 (already between 0 and 1)
    result = lighting_percentile_map * 255
    image = Image.fromarray(result)
    image.show()
    return lighting_percentile_map
