import pico_vault.vault_util.udevrunner.udevrunner as testclass

mynewclass = testclass.udevrunner()


mynewclass.connect("/dev/ttyACM0")
result = mynewclass.query_connected_info()
print(result)
"""
import pyotp
import qrcode


PRIVATE_KEY = pyotp.random_base32()

hotp = pyotp.HOTP(PRIVATE_KEY)
hotp_registry = hotp.provisioning_uri(name="my test app", issuer_name="what does this mean", initial_count=0)

print(hotp_registry)

img = qrcode.make(hotp_registry)
img.show()
"""