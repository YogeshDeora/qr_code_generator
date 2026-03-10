import qrcode
import qrcode.image.svg
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

url = input("Enter the URL to generate QR code: ")

# Color customization
print("\n--- Color Options ---")
print("Examples: black, white, red, blue, green, #FF5733, #000000")
fill_color = input("QR code color [default: black]: ").strip() or "black"
back_color = input("Background color [default: white]: ").strip() or "white"

# Size selection
print("\n--- Size Options ---")
print("1. Small (box_size=5, border=2)")
print("2. Medium (box_size=10, border=4)")
print("3. Large (box_size=15, border=6)")
size_choice = input("Choose size [default: 2]: ").strip() or "2"
size_map = {"1": (5, 2), "2": (10, 4), "3": (15, 6)}
box_size, border = size_map.get(size_choice, (10, 4))

# Error correction
print("\n--- Error Correction Level ---")
print("L - 7% recovery")
print("M - 15% recovery")
print("Q - 25% recovery")
print("H - 30% recovery (recommended for logos)")
error_level = input("Choose level (L/M/Q/H) [default: H]: ").strip().upper() or "H"
error_map = {
    "L": qrcode.constants.ERROR_CORRECT_L,
    "M": qrcode.constants.ERROR_CORRECT_M,
    "Q": qrcode.constants.ERROR_CORRECT_Q,
    "H": qrcode.constants.ERROR_CORRECT_H
}
error_correction = error_map.get(error_level, qrcode.constants.ERROR_CORRECT_H)

logo_path = input("\nEnter logo path (press Enter to skip): ").strip()

print("\n--- Available Formats ---")
print("PNG, JPG, SVG, PDF, WEBP, EPS")
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
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border, image_factory=factory)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    filename = f"qrcode_{timestamp}.svg"
    img.save(filename)
elif format_choice == "eps":
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    filename = f"qrcode_{timestamp}.eps"
    img.save(filename, "EPS")
elif format_choice == "pdf":
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f"qrcode_{timestamp}.pdf"
    c = canvas.Canvas(filename)
    c.drawImage(ImageReader(buffer), 100, 600, width=200, height=200)
    c.save()
elif format_choice == "webp":
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    else:
        img = img.convert('RGB')
    filename = f"qrcode_{timestamp}.webp"
    img.save(filename, "WEBP")
elif format_choice == "jpg" or format_choice == "jpeg":
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    else:
        img = img.convert('RGB')
    filename = f"qrcode_{timestamp}.jpg"
    img.save(filename)
else:
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if logo_path and os.path.exists(logo_path):
        img = add_logo_to_qr(img, logo_path)
    filename = f"qrcode_{timestamp}.png"
    img.save(filename)

print(f"\n✓ QR code saved as {filename}")