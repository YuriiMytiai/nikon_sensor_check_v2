from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor, QPen
import rawpy
import numpy as np
import qimage2ndarray
from functools import partial


class ImageProcessor:

    def __init__(self, main_window, events_processor):

        self.events_processor = events_processor
        self.main_window = main_window

        self.broken_pixel_coordinates = []
        self.image_sizes = {}

        self.img_scroll_area = self.main_window.image_scroll_area

        self.proc_blk_pic_btn = self.main_window.process_blk_btn
        self.proc_wht_pic_btn = self.main_window.process_wht_btn
        self.proc_test_pic_btn = self.main_window.process_test_btn

        self.info_label = self.main_window.info_label

        self.image_preview_label = main_window.image_preview
        self.image_preview_label.setScaledContents(True)

        self.img_label = QLabel()

        self.setup_img_label()

        self.connect_btns_with_handlers()

    def setup_img_label(self):
        self.img_label.setBackgroundRole(QPalette.Base)
        self.img_label.setScaledContents(True)

        self.img_scroll_area.setBackgroundRole(QPalette.Dark)
        self.img_scroll_area.setWidget(self.img_label)

    def connect_btns_with_handlers(self):
        self.proc_blk_pic_btn.clicked.connect(partial(self.btns_handler, 'blk'))
        self.proc_wht_pic_btn.clicked.connect(partial(self.btns_handler, 'wht'))
        self.proc_test_pic_btn.clicked.connect(self.apply_mask)

    def btns_handler(self, img_type):
        # get image path:
        pic_path = self.events_processor.files_loader.blk_pic_path if img_type == 'blk' else self.events_processor.files_loader.wht_pic_path
        if pic_path is None:
            img_name = 'Black' if img_type == 'blk' else 'White'
            self.raise_err_window(img_name)
            return

        # get rgb thresholds
        rgb_thresholds = self.events_processor.rgb_thr_processor.get_thresholds()

        # load img
        raw_img = rawpy.imread(str(pic_path))

        if not self.check_sizes(raw_img, img_type):
            return

        rgb = raw_img.postprocess()

        self.find_broken_pixels(rgb, rgb_thresholds, img_type)

        qt_image = QImage(qimage2ndarray.array2qimage(rgb))

        self.show_pictures(qt_image, img_type)

        self.print_info()

    def apply_mask(self):
        pic_path = self.events_processor.files_loader.test_pic_path
        if pic_path is None:
            self.raise_err_window('Test')
            return

        img_type = 'test'

        # load img
        raw_img = rawpy.imread(str(pic_path))

        if not self.check_sizes(raw_img, img_type):
            return

        rgb = raw_img.postprocess()

        qt_image = QImage(qimage2ndarray.array2qimage(rgb))

        self.show_pictures(qt_image, img_type)

    def show_pictures(self, qt_image, img_type):
        miniature_pixmap = QPixmap.fromImage(qt_image)
        miniature_pixmap = self.highlight_broken_pixels(miniature_pixmap, miniature=True, img_type=img_type)
        self.image_preview_label.setPixmap(miniature_pixmap)

        pixmap = QPixmap.fromImage(qt_image)
        pixmap = self.highlight_broken_pixels(pixmap, img_type=img_type)
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(self.img_label.pixmap().size())

    def check_sizes(self, raw_img, img_type):
        img_size = (raw_img.sizes.width, raw_img.sizes.height)
        for v in self.image_sizes.values():
            if img_size != v:
                self.raise_err_window(img_type.upper(), 'wrong_pic_size')
                return False
        self.image_sizes[img_type] = img_size
        return True

    @staticmethod
    def raise_err_window(image_name, err_type='file_error'):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if err_type == 'file_error':
            msg.setText(f'{image_name} image was not chosen! Please, select an image')
        elif err_type == 'wrong_pic_size':
            msg.setText(f'Picture size of {image_name} image is different from other images')
        msg.setWindowTitle("Error")
        msg.exec()

    def find_broken_pixels(self, image, thresholds, pic_type):
        self.broken_pixel_coordinates = []

        for channel in range(0, 3):
            chan_img = image[:, :, channel]
            chan_threshold = thresholds[channel]

            if pic_type == 'blk':
                chan_broken_pixel_idxs = np.nonzero(chan_img > chan_threshold)
            elif pic_type == 'wht':
                chan_broken_pixel_idxs = np.nonzero(chan_img < chan_threshold)

            coordinates = []
            for i in range(0, chan_broken_pixel_idxs[0].shape[0]):
                coordinates.append((chan_broken_pixel_idxs[0][i], chan_broken_pixel_idxs[1][i]))

            self.broken_pixel_coordinates.append(coordinates)

    def highlight_broken_pixels(self, pixmap, miniature=False, img_type='blk'):

        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

        painter = QPainter()
        painter.begin(pixmap)

        for (color, pixel_coordinates) in zip(colors, self.broken_pixel_coordinates):
            for pixel_coordinate in pixel_coordinates:
                cur_color = QColor(color[0], color[1], color[2]) if not miniature else (QColor(255, 255, 255) if img_type == 'blk' else QColor(255, 0, 0))
                line_weight = 1 if not miniature else 20
                painter.setPen(QPen(cur_color, line_weight))
                diameter = int(100) if not miniature else int(300)
                painter.drawEllipse(pixel_coordinate[1] - diameter // 2, pixel_coordinate[0] - diameter // 2, diameter, diameter)
        painter.end()

        return pixmap

    def print_info(self):
        all_ch_bad_pixels_set = set(self.broken_pixel_coordinates[0])
        all_ch_bad_pixels_set = all_ch_bad_pixels_set & set(self.broken_pixel_coordinates[1])
        all_ch_bad_pixels_set = all_ch_bad_pixels_set & set(self.broken_pixel_coordinates[2])
        info_str = f'Number of bad pixels:\nR channel: {len(self.broken_pixel_coordinates[0])}\n' \
            f'G channel: {len(self.broken_pixel_coordinates[1])}\n' \
            f'B channel: {len(self.broken_pixel_coordinates[2])}\n\n' \
            f'Number of bad pixels in all 3 channels: {len(all_ch_bad_pixels_set)}'

        self.info_label.setText(info_str)
