from pathlib import Path
from PyQt5.QtWidgets import QFileDialog
from functools import partial


class FilesLoader:

    def __init__(self, main_window):
        self.main_window = main_window

        self.files_select_layout = main_window.files_selection_Hlayout

        self.blk_img_btn = main_window.blk_img_sel_btn
        self.wht_img_btn = main_window.wht_img_sel_btn
        self.test_img_btn = main_window.test_img_sel_btn

        self.blk_img_path_label = main_window.blk_img_path_label
        self.wht_img_path_label = main_window.wht_img_path_label
        self.test_img_path_label = main_window.test_img_path_label

        self.blk_pic_path = None
        self.wht_pic_path = None
        self.test_pic_path = None

        self.connect_btns_events()

    def connect_btns_events(self):
        self.blk_img_btn.clicked.connect(partial(self.open_file_name_dialog, 'blk'))
        self.wht_img_btn.clicked.connect(partial(self.open_file_name_dialog, 'wht'))
        self.test_img_btn.clicked.connect(partial(self.open_file_name_dialog, 'test'))

    def open_file_name_dialog(self, img_type):
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "Select NEF file", "", "NEF(*.nef, *.NEF)")

        file_name = Path(file_name)
        if not file_name.exists():
            return

        if img_type == 'blk':
            self.blk_pic_path = file_name
            self.blk_img_path_label.setText(str(file_name))
        elif img_type == 'wht':
            self.wht_pic_path = file_name
            self.wht_img_path_label.setText(str(file_name))
        elif img_type == 'test':
            self.test_pic_path = file_name
            self.test_img_path_label.setText(str(file_name))
