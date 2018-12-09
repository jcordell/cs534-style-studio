from PIL import Image


class AssetService:
    def __init__(self):
        # should load assets into memory
        return

    def load_asset(self, path):
        # load asset into memory, remove white edges
        # example: the glasses1.png width should be the width of the glasses
        # not the width of the entire picture since there is whitespace
        return

    def get_asset(self, asset_path):
        # example asset_path: glasses/glasses1
        return self.pil_load_image('assets/' + asset_path)

    def pil_load_image(self, path):
        return Image.open(path)
