from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from PIL import Image
from datetime import datetime
import io
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['QR_FOLDER'] = 'static/qrcodes'

def generate_wifi_qr(ssid, password, encryption):
    return f"WIFI:T:{encryption};S:{ssid};P:{password};;"

def generate_vcard_qr(name, phone, email, organization, website):
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{phone}
EMAIL:{email}
ORG:{organization}
URL:{website}
END:VCARD"""
    return vcard

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json
    qr_type = data.get('type', 'url')
    fill_color = data.get('fillColor', 'black')
    back_color = data.get('backColor', 'white')
    size = data.get('size', 'medium')
    error_level = data.get('errorLevel', 'H')
    logo_data = data.get('logo')
    
    # Generate QR data based on type
    if qr_type == 'url':
        qr_data = data.get('url')
    elif qr_type == 'phone':
        qr_data = f"tel:{data.get('phone')}"
    elif qr_type == 'email':
        email = data.get('email')
        subject = data.get('subject', '')
        body = data.get('body', '')
        qr_data = f"mailto:{email}?subject={subject}&body={body}"
    elif qr_type == 'sms':
        phone = data.get('phone')
        message = data.get('message', '')
        qr_data = f"SMSTO:{phone}:{message}"
    elif qr_type == 'wifi':
        qr_data = generate_wifi_qr(
            data.get('ssid'),
            data.get('password'),
            data.get('encryption', 'WPA')
        )
    elif qr_type == 'vcard':
        qr_data = generate_vcard_qr(
            data.get('name'),
            data.get('phone'),
            data.get('email'),
            data.get('organization', ''),
            data.get('website', '')
        )
    else:
        qr_data = data.get('url')
    
    size_map = {'small': (5, 2), 'medium': (10, 4), 'large': (15, 6)}
    box_size, border = size_map.get(size, (10, 4))
    
    error_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    error_correction = error_map.get(error_level, qrcode.constants.ERROR_CORRECT_H)
    
    qr = qrcode.QRCode(version=1, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    
    if logo_data:
        try:
            logo_bytes = base64.b64decode(logo_data.split(',')[1])
            logo = Image.open(io.BytesIO(logo_bytes))
            qr_width, qr_height = img.size
            logo_size = qr_width // 4
            logo = logo.resize((logo_size, logo_size))
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, pos)
        except:
            pass
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({'image': f'data:image/png;base64,{img_base64}'})

@app.route('/download', methods=['POST'])
def download_qr():
    data = request.json
    img_data = data.get('image')
    format_type = data.get('format', 'png')
    
    img_bytes = base64.b64decode(img_data.split(',')[1])
    img = Image.open(io.BytesIO(img_bytes))
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qrcode_{timestamp}.{format_type}"
    filepath = os.path.join(app.config['QR_FOLDER'], filename)
    
    if format_type == 'jpg' or format_type == 'jpeg':
        img = img.convert('RGB')
        img.save(filepath, 'JPEG')
    elif format_type == 'webp':
        img.save(filepath, 'WEBP')
    elif format_type == 'eps':
        img.save(filepath, 'EPS')
    else:
        img.save(filepath, 'PNG')
    
    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['QR_FOLDER'], exist_ok=True)
    app.run(debug=True)
