import qrcode
import qrcode.image.svg
from datetime import datetime
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

url = input("Enter the URL to generate QR code: ")
print("Available formats: PNG, JPG, SVG, PDF")
format_choice = input("In which format do you want to download? [default: png]: ").lower() or "png"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

if format_choice == "svg":
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url, image_factory=factory)
    filename = f"qrcode_{timestamp}.svg"
    img.save(filename)
elif format_choice == "pdf":
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f"qrcode_{timestamp}.pdf"
    c = canvas.Canvas(filename)
    c.drawImage(ImageReader(buffer), 100, 600, width=200, height=200)
    c.save()
elif format_choice == "jpg" or format_choice == "jpeg":
    img = qrcode.make(url)
    rgb_img = img.convert('RGB')
    filename = f"qrcode_{timestamp}.jpg"
    rgb_img.save(filename)
else:
    img = qrcode.make(url)
    filename = f"qrcode_{timestamp}.png"
    img.save(filename)

print(f"QR code saved as {filename}")