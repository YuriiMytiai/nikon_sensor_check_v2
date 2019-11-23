from functools import partial


class RGBThreshProcessor:

    def __init__(self, main_window):
        self.rgb_layout = main_window.rgb_thresh_Vlayout

        self.r_slider = main_window.r_slider
        self.g_slider = main_window.g_slider
        self.b_slider = main_window.b_slider

        self.sliders = (self.r_slider, self.g_slider, self.b_slider)

        self.r_label = main_window.r_label
        self.g_label = main_window.g_label
        self.b_label = main_window.b_label

        self.labels = (self.r_label, self.g_label, self.b_label)

        self.setup_ranges()

        self.connect_value_change_events()

    def setup_ranges(self):
        for slider in (self.sliders):
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.setSingleStep(1)
            slider.setValue(200)

            if slider == self.r_slider:
                color = 'red'
            elif slider == self.g_slider:
                color = 'green'
            elif slider == self.b_slider:
                color = 'blue'

            slider.setStyleSheet(f"QSlider::handle:horizontal {{background: {color};}}")

            self.slider_value_changed_handler(slider)

    def connect_value_change_events(self):
        [slider.valueChanged.connect(partial(self.slider_value_changed_handler, slider)) for slider in self.sliders]

    def get_thresholds(self):
        thresholds = [slider.value() for slider in self.sliders]
        return thresholds

    def slider_value_changed_handler(self, slider):

        slider_value = slider.value()

        if slider == self.r_slider:
            self.r_label.setText(f'R: {slider_value}')
        elif slider == self.g_slider:
            self.g_label.setText(f'G: {slider_value}')
        elif slider == self.b_slider:
            self.b_label.setText(f'B: {slider_value}')
