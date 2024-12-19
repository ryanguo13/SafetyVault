from luma.core.interface.serial import spi
from luma.oled.device import ssd1309

# 初始化 SPI 接口
serial = spi(device=0, port=0, gpio_DC=22 ,gpio_RST=27)
device = ssd1309(serial)

# 显示文本
device.text("Hello, SPI!", (5, 10))
device.show()
