from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor, QPen
import rawpy
import numpy as np
import qimage2ndarray


class ImageProcessor:

    def __init__(self, main_window, events_processor):

        self.events_processor = events_processor
        self.main_window = main_window

        self.img_scroll_area = self.main_window.image_scroll_area

        self.proc_blk_pic_btn = self.main_window.process_blk_btn
        self.proc_wht_pic_btn = self.main_window.process_wht_btn

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
        self.proc_blk_pic_btn.clicked.connect(self.blk_btn_handler)
        self.proc_wht_pic_btn.clicked.connect(self.wht_btn_handler)

    def blk_btn_handler(self):
        # get image path:
        pic_path = self.events_processor.files_loader.blk_pic_path
        if pic_path is None:
            self.raise_err_window('Black')
            return

        # get rgb thresholds
        rgb_thresholds = self.events_processor.rgb_thr_processor.get_thresholds()

        # load img
        raw_img = rawpy.imread(str(pic_path))
        rgb = raw_img.postprocess()

        broken_pixel_coordinates = self.find_broken_pixels(rgb, rgb_thresholds, 'blk')

        qt_image = QImage(qimage2ndarray.array2qimage(rgb))

        miniature_pixmap = QPixmap.fromImage(qt_image)
        miniature_pixmap = self.highlight_broken_pixels(miniature_pixmap, broken_pixel_coordinates, miniature=True)
        self.image_preview_label.setPixmap(miniature_pixmap)

        pixmap = QPixmap.fromImage(qt_image)
        pixmap = self.highlight_broken_pixels(pixmap, broken_pixel_coordinates)
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(self.img_label.pixmap().size())

        self.print_info(broken_pixel_coordinates)

    def wht_btn_handler(self):
        # get image path:
        pic_path = self.events_processor.files_loader.wht_pic_path
        if pic_path is None:
            self.raise_err_window('White')
            return

        # get rgb thresholds
        rgb_thresholds = self.events_processor.rgb_thr_processor.get_thresholds()

        # load img
        raw_img = rawpy.imread(str(pic_path))
        rgb = raw_img.postprocess()

        broken_pixel_coordinates = self.find_broken_pixels(rgb, rgb_thresholds, 'wht')

        qt_image = QImage(qimage2ndarray.array2qimage(rgb))

        miniature_pixmap = QPixmap.fromImage(qt_image)
        miniature_pixmap = self.highlight_broken_pixels(miniature_pixmap, broken_pixel_coordinates, miniature=True, img_type='wht')
        self.image_preview_label.setPixmap(miniature_pixmap)

        pixmap = QPixmap.fromImage(qt_image)
        pixmap = self.highlight_broken_pixels(pixmap, broken_pixel_coordinates, img_type='wht')
        self.img_label.setPixmap(pixmap)
        self.img_label.resize(self.img_label.pixmap().size())

        self.print_info(broken_pixel_coordinates)

    def raise_err_window(self, image_name):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f'{image_name} image was not chosen! Please, select an image')
        msg.setWindowTitle("Error")
        msg.exec()

    @staticmethod
    def find_broken_pixels(image, thresholds, pic_type):
        broken_pixel_coordinates = []
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

            broken_pixel_coordinates.append(coordinates)

        return broken_pixel_coordinates

    @staticmethod
    def highlight_broken_pixels(pixmap, broken_pixels_coordinates, miniature=False, img_type='blk'):

        colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

        painter = QPainter()
        painter.begin(pixmap)

        for (color, pixel_coordinates) in zip(colors, broken_pixels_coordinates):
            for pixel_coordinate in pixel_coordinates:
                cur_color = QColor(color[0], color[1], color[2]) if not miniature else (QColor(255, 255, 255) if img_type == 'blk' else QColor(0, 0, 0))
                line_weight = 1 if not miniature else 20
                painter.setPen(QPen(cur_color, line_weight))
                diameter = int(100) if not miniature else int(300)
                painter.drawEllipse(pixel_coordinate[1] - diameter // 2, pixel_coordinate[0] - diameter // 2, diameter, diameter)
        painter.end()

        return pixmap

    def print_info(self, broken_pixel_coordinates):
        all_ch_bad_pixels_set = set(broken_pixel_coordinates[0])
        all_ch_bad_pixels_set = all_ch_bad_pixels_set & set(broken_pixel_coordinates[1])
        all_ch_bad_pixels_set = all_ch_bad_pixels_set & set(broken_pixel_coordinates[2])
        info_str = f'Number of bad pixels:\nR channel: {len(broken_pixel_coordinates[0])}\n' \
            f'G channel: {len(broken_pixel_coordinates[1])}\n' \
            f'B channel: {len(broken_pixel_coordinates[2])}\n\n' \
            f'Number of bad pixels in all 3 channels: {len(all_ch_bad_pixels_set)}'

        self.info_label.setText(info_str)