from math import (
    cos,
    sin,
    radians
)
from PIL import (
    Image,
    ImageDraw,
    ExifTags
)
from io import BytesIO


class Receipt(object):
    def __init__(self, image):
        self.image = Image.open(BytesIO(image))
        width, height = self.image.size
        self.center_x = width / 2
        self.center_y = height / 2

        for orientation in ExifTags.TAGS.keys() :
            if ExifTags.TAGS[orientation]=='Orientation' : break
        exif = dict(self.image._getexif().items())

        self.rotation_degrees = 0
        if exif[orientation] == 3 :
            self.rotation_degrees = 180
        elif exif[orientation] == 6 :
            self.rotation_degrees = 270
        elif exif[orientation] == 8 :
            self.rotation_degrees = 90

        self.rotation_radians = radians(self.rotation_degrees)
        self.image.rotate(self.rotation_degrees, expand=True)
        new_width, new_height = self.image.size

        self.offset_x = (new_width - width) / 2
        self.offset_y = (new_height - height) / 2

    def preview(self, boxes=None):
        self.image.show()

    def _rotate_word(self, word):
        pass

    def _rotate_point(x, y):
        new_x = self.center_x + (
            ((x - self.center_x) * cos(self.rotation_radians))
            - ((y - self.center_y) * sin(self.rotation_radians))
        )
        new_y = self.center_y + (
            ((x - self.center_x) * sin(self.rotation_radians))
            + ((y - self.center_y) * cos(self.rotation_radians))
        )
        return new_x + self.offset_x, new_y + self.offset_y

