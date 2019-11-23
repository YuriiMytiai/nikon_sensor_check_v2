from files_loader import FilesLoader
from rgb_thr_processor import RGBThreshProcessor
from image_processor import ImageProcessor


class EventsProcessor:

    """
    It just connects all parts together
    """

    def __init__(self, main_window):

        self.main_window = main_window

        self.files_loader = FilesLoader(self.main_window)

        self.rgb_thr_processor = RGBThreshProcessor(self.main_window)

        self.image_processor = ImageProcessor(self.main_window, self)
