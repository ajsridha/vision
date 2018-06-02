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
from PIL.PngImagePlugin import PngImageFile
from io import BytesIO


class Receipt(object):
    def __init__(self, image):
        self.image = Image.open(BytesIO(image))
        self.width, self.height = self.image.size
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.offset_x = 0
        self.offset_y = 0

        degrees = self.calculate_rotation()
        self.rotate(degrees)

    def rotate(self, degrees):
        original_width = self.width
        original_height = self.height

        self.image = self.image.rotate(degrees, expand=True)

        self.width, self.height = self.image.size

        self.offset_x = (self.width - original_width) / 2
        self.offset_y = (self.height - original_height) / 2

        self.rotation_degrees = degrees
        self.rotation_radians = 0
        if degrees == 90:
            self.rotation_radians = radians(90)
        elif degrees == 180:
            self.rotation_radians = radians(90)
        elif degrees == 270:
            self.rotation_radians = radians(90)

    def calculate_rotation(self):
        self.orientation_known = False
        if not hasattr(self.image, '_getexif') or self.image._getexif() is None:
            return 0

        for orientation in ExifTags.TAGS.keys() :
            if ExifTags.TAGS[orientation]=='Orientation' : break
        exif = dict(self.image._getexif().items())

        if orientation not in exif:
            self.orientation_known = False
            return 0
        elif exif[orientation] == 3 :
            return 180
        elif exif[orientation] == 6 :
            return 270
        elif exif[orientation] == 8 :
            return 90

        return 0

    def preview(self, boxes=None):
        image = self.image.copy()
        if boxes:
            self._draw_boxes(boxes, image)

        image.show()

    def _draw_boxes(self, boxes, image):
        draw = ImageDraw.Draw(image)
        for box in boxes:
            vertices = box['vertices']
            draw.polygon([
                vertices[0]['x'], vertices[0]['y'],
                vertices[1]['x'], vertices[1]['y'],
                vertices[2]['x'], vertices[2]['y'],
                vertices[3]['x'], vertices[3]['y']], None, "red")
