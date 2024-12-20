from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from luma.core.render import canvas



class foureyes:
    device = None

    def __init__(self):
        serial = spi(device=0, port=0, gpio_DC=22 ,gpio_RST=27)
        self.device = ssd1309(serial)

    def display_text(self, x, y, text):
        with canvas(self.device) as draw:
            draw.text((x, y), text, fill="white", font_size = 7)



