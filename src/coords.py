class Coords:
    @staticmethod
    def centered_label(screen_width_and_height, label):
        screen_width, screen_height = screen_width_and_height
        label_width, label_height = label.get_size()
        x = screen_width - label_width
        y = (screen_height / 2) - label_height
        return x, y

    @staticmethod
    def bottom_left_label(screen_width_and_height, label):
        screen_width, screen_height = screen_width_and_height
        label_width, label_height = label.get_size()
        padding = 10
        x = padding
        y = screen_height - label_height - padding
        return x, y