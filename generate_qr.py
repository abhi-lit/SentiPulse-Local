import qrcode

url = "https://represent-try-manga-cycle.trycloudflare.com"
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("static/qr_code.png")
print("High-speed Cloudflare QR Code generated at static/qr_code.png")
