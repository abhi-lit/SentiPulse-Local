import qrcode

url = "https://da9f9dc8c58aa3.lhr.life"
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("static/qr_code.png")
print("QR Code generated at static/qr_code.png")
