from lib.services.AssetSerice import AssetService
import numpy as np
from PIL import Image
from math import degrees, tan
import lib.LightingDetector as lighting


class Makeover:
    def __init__(self, pil_image, feature_map):
        self.image = pil_image
        self.feature_map = feature_map
        self.asset_service = AssetService()
        self.head_tilt = self.calculate_head_tilt()

        # calculate lighting direction from grayscale image
        # commented out because it adds a lot to the run time and is not currently adding shadows
        # self.grayscale_np_image = np.asarray(pil_image.convert('L'))
        # self.lighting_map = lighting.get_lighting_map(self.grayscale_np_image)
        # self.lighting_percentiles_map = lighting.get_lighting_percentage(
        # self.lighting_map, np.asarray(pil_image))

    def calculate_head_tilt(self):
        adjacent = self.get_eye_width()
        rightmost_eye_point_x, rightmost_eye_point_y = self.get_rightmost_eye_point()
        leftmost_eye_point_x, leftmost_eye_point_y = self.get_leftmost_eye_point()
        opposite = np.max(rightmost_eye_point_y - leftmost_eye_point_y)
        head_tilt = degrees(tan(opposite / adjacent))
        return head_tilt

    def get_leftmost_eye_point(self):
        left_eye_feature_points = self.feature_map['left_eye']
        leftmost_eye_point_x, leftmost_eye_point_y = left_eye_feature_points.max(
            axis=0)
        return leftmost_eye_point_x, leftmost_eye_point_y

    def get_rightmost_eye_point(self):
        right_eye_feature_points = self.feature_map['right_eye']
        rightmost_eye_point_x, rightmost_eye_point_y = right_eye_feature_points.min(
            axis=0)
        return rightmost_eye_point_x, rightmost_eye_point_y

    def get_eye_width(self):
        leftmost_eye_point_x, leftmost_eye_point_y = self.get_leftmost_eye_point()
        rightmost_eye_point_x, rightmost_eye_point_y = self.get_rightmost_eye_point()

        eye_width = leftmost_eye_point_x - rightmost_eye_point_x
        return eye_width

    def get_feature_width(self, feature):
        feature_points = self.feature_map[feature]
        leftmost_point = feature_points.max(axis=0)
        rightmost_point = feature_points.min(axis=0)
        # subtract x points
        width = leftmost_point[0] - rightmost_point[0]
        return width

    def get_image_rescale_width(self, image, width):
        # shape is [x_size, y_size, ...]
        shape = np.shape(image)
        y_ratio = shape[1] / shape[0]
        size = width, np.round(width / y_ratio)
        return size

    def add_glasses(self, glasses_type):
        glasses = self.asset_service.get_asset(
            'glasses/' + glasses_type + '.png')

        eye_width = self.get_eye_width()
        # make glasses bigger than the eye width
        glasses_width = np.round(eye_width * 1.4)

        # resize glasses and keep aspect ratio
        size = self.get_image_rescale_width(glasses, glasses_width)
        glasses.thumbnail(size, Image.ANTIALIAS)

        # need to rotate glasses to match rotation of head in image
        foreground = glasses.rotate(self.head_tilt, expand=1)

        # get center eye point
        left_eye_feature_points = self.feature_map['left_eye']
        right_eye_feature_points = self.feature_map['right_eye']
        full_eye_list = np.append(
            right_eye_feature_points, left_eye_feature_points, axis=0)
        average_eye_coord_x, average_eye_coord_y = full_eye_list.mean(axis=0)

        # move x and y half the width and height of the glasses being added
        glasses_y, glasses_x, glasses_color = np.shape(glasses)
        average_eye_coord_x = average_eye_coord_x - glasses_x * .5
        # glasses should sit slightly higher than average point
        average_eye_coord_y = average_eye_coord_y - glasses_y * .5 - glasses_y * .1
        offset = tuple([int(average_eye_coord_x), int(average_eye_coord_y)])

        # apply shadows based on lighting percentile map
        # not implemented correctly yet so commented out
        # convert foreground to numpy array
        # np_glasses = np.array(foreground)
        # multiple by scalar to darken based on shadows of image
        # for x in range(len(np_glasses)):
        #     for y in range(len(np_glasses[x])):
        #         # get location in actual image
        #         x_loc = x + offset[0]
        #         y_loc = y + offset[1]
        #         color_diff = 150
        #         # only scale the rgb, not alpha channel
        #         np_glasses[x, y] = [np_glasses[x, y][0] +
        #                             (self.lighting_percentiles_map[x_loc, y_loc] - .5) * color_diff, np_glasses[x, y][1] +
        #                             (self.lighting_percentiles_map[x_loc, y_loc] - .5) * color_diff, np_glasses[x, y][2] +
        #                             (self.lighting_percentiles_map[x_loc, y_loc] - .5) * color_diff, np_glasses[x, y][3]]

        # foreground = Image.fromarray(np_glasses)
        # paste glasses onto the image
        self.image.paste(foreground, offset, foreground)

    def add_beard(self, beard_type):
        beard = self.asset_service.get_asset(
            'facial_hair/' + beard_type + '.png')

        # rescale beard to 2x eye width
        eye_width = self.get_eye_width()
        size = self.get_image_rescale_width(beard, eye_width * 1.7)
        beard.thumbnail(size, Image.ANTIALIAS)

        # place around average mouth point
        mouth_map = self.feature_map['mouth']
        average_mouth_x, average_mouth_y = mouth_map.mean(axis=0)

        beard = beard.rotate(self.head_tilt, expand=1)

        beard_size_x, beard_size_y = np.size(beard)

        average_mouth_x = average_mouth_x - .5 * beard_size_x
        average_mouth_y = average_mouth_y - .4 * beard_size_y
        offset = tuple([int(average_mouth_x), int(average_mouth_y)])

        self.image.paste(beard, offset, beard)

    def add_mustache(self, mustache_type):
        mustache = self.asset_service.get_asset(
            'facial_hair/' + mustache_type + '.png')

        # rescale to mouth width
        mouth_width = self.get_feature_width('mouth')
        size = self.get_image_rescale_width(mustache, mouth_width * 2)
        mustache.thumbnail(size, Image.ANTIALIAS)

        mustache = mustache.rotate(self.head_tilt, expand=1)

        # place slightly above and in center of mouth
        mouth_map = self.feature_map['mouth']
        average_mouth_x, average_mouth_y = mouth_map.mean(axis=0)

        mustache_size_x, mustache_size_y = np.size(mustache)

        average_mouth_x = average_mouth_x - .5 * mustache_size_x
        average_mouth_y = average_mouth_y - .6 * mustache_size_y
        offset = tuple([int(average_mouth_x), int(average_mouth_y)])

        self.image.paste(mustache, offset, mustache)

    def add_earings(self, earing_type):
        earing = self.asset_service.get_asset(
            'earings/' + earing_type + '.png')

        # rescale earing size
        if earing_type == 'earing1':
            earing_width = self.get_eye_width() / 1.5
        if earing_type == 'earing2':
            earing_width = self.get_eye_width() / 5

        size = self.get_image_rescale_width(earing, earing_width)
        earing.thumbnail(size, Image.ANTIALIAS)

        jaw_map = self.feature_map['jaw']

        earing = earing.rotate(self.head_tilt, expand=1)

        max_jaw_coord_x_left, max_jaw_coord_y_left = jaw_map.max(axis=0)
        max_jaw_coord_x_right, max_jaw_coord_y_right = jaw_map.max(axis=0)

        earing_size_x, earing_size_y = np.size(earing)

        if earing_type == 'earing1':
            # person's left ear earing
            max_jaw_coord_x = max_jaw_coord_x_left - .4 * earing_size_x
            max_jaw_coord_y = max_jaw_coord_y_left - 2.43 * earing_size_y
            offset = tuple([int(max_jaw_coord_x), int(max_jaw_coord_y)])
            self.image.paste(earing, offset, earing)

            # person's right ear earing
            max_jaw_coord_x = max_jaw_coord_x_right - 2.8 * earing_size_x
            max_jaw_coord_y = max_jaw_coord_y_right - 2.43 * earing_size_y
            offset = tuple([int(max_jaw_coord_x), int(max_jaw_coord_y)])
            self.image.paste(earing, offset, earing)

        # was having trouble sizing both earing styles the same so its hard coded for both earings right now
        if earing_type == 'earing2':
            # person's left ear earing
            max_jaw_coord_x = max_jaw_coord_x_left - .2 * earing_size_x
            max_jaw_coord_y = max_jaw_coord_y_left - 6.1 * earing_size_y
            offset = tuple([int(max_jaw_coord_x), int(max_jaw_coord_y)])
            self.image.paste(earing, offset, earing)

            # person's right ear earing
            max_jaw_coord_x = max_jaw_coord_x_right - 8 * earing_size_x
            max_jaw_coord_y = max_jaw_coord_y_right - 6.1 * earing_size_y
            offset = tuple([int(max_jaw_coord_x), int(max_jaw_coord_y)])
            self.image.paste(earing, offset, earing)

    def add_nose_stud(self, stud_type):
        nose_stud = self.asset_service.get_asset(
            'nose_studs/' + stud_type + '.png')

        # blue stud case
        if stud_type == 'nose_stud1':
            stud_width = self.get_eye_width() / 2.5

        # shiny stud case
        if stud_type == 'nose_stud2':
            stud_width = self.get_eye_width() / 8

        size = self.get_image_rescale_width(nose_stud, stud_width)
        nose_stud.thumbnail(size, Image.ANTIALIAS)
        nose_map = self.feature_map['nose']
        nose_stud = nose_stud.rotate(self.head_tilt, expand=1)
        average_nose_x, average_nose_y = nose_map.mean(axis=0)
        nose_stud_size_x, nose_stud_size_y = np.size(nose_stud)
        # blue stud case
        if stud_type == 'nose_stud1':
            average_nose_x = average_nose_x - .7 * nose_stud_size_x
            average_nose_y = average_nose_y - .6 * nose_stud_size_y
            offset = tuple([int(average_nose_x), int(average_nose_y)])
            self.image.paste(nose_stud, offset, nose_stud)
        # shiny stud case
        if stud_type == 'nose_stud2':
            average_nose_x = average_nose_x - 1.2 * nose_stud_size_x
            average_nose_y = average_nose_y - .6 * nose_stud_size_y
            offset = tuple([int(average_nose_x), int(average_nose_y)])
            self.image.paste(nose_stud, offset, nose_stud)

    def add_necklace(self, necklace_type):
        necklace = self.asset_service.get_asset(
            'necklaces/' + necklace_type + '.png')

        necklace_width = self.get_eye_width() * 1.54
        size = self.get_image_rescale_width(necklace, necklace_width)
        necklace.thumbnail(size, Image.ANTIALIAS)

        jaw_map = self.feature_map['jaw']
        necklace = necklace.rotate(self.head_tilt, expand=1)
        average_jaw_x, average_jaw_y = jaw_map.mean(axis=0)
        necklace_size_x, necklace_size_y = np.size(necklace)

        average_jaw_x = average_jaw_x - .44 * necklace_size_x
        average_nose_y = average_jaw_y + .25 * necklace_size_y
        offset = tuple([int(average_jaw_x), int(average_nose_y)])
        self.image.paste(necklace, offset, necklace)

    def get_makeover(self):
        # return makeover image with any extra processing needed
        return self.image
