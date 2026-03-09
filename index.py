import qrcode
import qrcode.image.svg
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

url = input("Enter the URL to generate QR code: ")
logo_path = input("Enter logo path (press Enter to skip): ").strip()
print("Available formats: PNG, JPG, SVG, PDF")
format_choice = input("In which format do you want to download? [default: png]: ").lower() or "png"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def add_logo_to_qr(qr_img, logo_path):
    qr_img = qr_img.convert('RGB')
    logo = Image.open(logo_path)
    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size))
    pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_img.paste(logo, pos)
    return qr_img

if format_choice == "svg":
    if logo_path:
        print("Logo not supported with SVG format")
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url, image_factory=factory)
    filename = f"qrcode_{timestamp}.svg"
    img.save(filename)
elif format_choice == "pdf":
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f"qrcode_{timestamp}.pdf"
    c = canvas.Canvas(filename)
    c.drawImage(ImageReader(buffer), 100, 600, width=200, height=200)
    c.save()
elif format_choice == "jpg" or format_choice == "jpeg":
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    else:
        img = img.convert('RGB')
    filename = f"qrcode_{timestamp}.jpg"
    img.save(filename)
else:
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    filename = f"qrcode_{timestamp}.png"
    img.save(filename)

print(f"QR code saved as {filename}")