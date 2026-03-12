let currentQRImage = null;
let logoData = null;

document.getElementById('logo').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            logoData = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

function changeQRType() {
    const qrType = document.getElementById('qrType').value;
    
    // Hide all forms
    document.querySelectorAll('.qr-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show selected form
    document.getElementById(qrType + 'Form').style.display = 'block';
}

async function generateQR() {
    const qrType = document.getElementById('qrType').value;
    const fillColor = document.getElementById('fillColor').value;
    const backColor = document.getElementById('backColor').value;
    const size = document.getElementById('size').value;
    const errorLevel = document.getElementById('errorLevel').value;

    let data = {
        type: qrType,
        fillColor: fillColor,
        backColor: backColor,
        size: size,
        errorLevel: errorLevel,
        logo: logoData
    };

    // Add type-specific data
    if (qrType === 'url') {
        const url = document.getElementById('url').value;
        if (!url) {
            alert('Please enter a URL or text');
            return;
        }
        data.url = url;
    } else if (qrType === 'phone') {
        const phone = document.getElementById('phoneNumber').value;
        if (!phone) {
            alert('Please enter a phone number');
            return;
        }
        data.phone = phone;
    } else if (qrType === 'email') {
        const email = document.getElementById('emailAddress').value;
        if (!email) {
            alert('Please enter an email address');
            return;
        }
        data.email = email;
        data.subject = document.getElementById('emailSubject').value;
        data.body = document.getElementById('emailBody').value;
    } else if (qrType === 'sms') {
        const phone = document.getElementById('smsPhone').value;
        if (!phone) {
            alert('Please enter a phone number');
            return;
        }
        data.phone = phone;
        data.message = document.getElementById('smsMessage').value;
    } else if (qrType === 'wifi') {
        const ssid = document.getElementById('wifiSSID').value;
        const password = document.getElementById('wifiPassword').value;
        if (!ssid) {
            alert('Please enter WiFi name (SSID)');
            return;
        }
        data.ssid = ssid;
        data.password = password;
        data.encryption = document.getElementById('wifiEncryption').value;
    } else if (qrType === 'vcard') {
        const name = document.getElementById('vcardName').value;
        const phone = document.getElementById('vcardPhone').value;
        const email = document.getElementById('vcardEmail').value;
        if (!name || !phone) {
            alert('Please enter at least name and phone number');
            return;
        }
        data.name = name;
        data.phone = phone;
        data.email = email;
        data.organization = document.getElementById('vcardOrg').value;
        data.website = document.getElementById('vcardWebsite').value;
    }

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        currentQRImage = result.image;

        const preview = document.getElementById('preview');
        preview.innerHTML = `<img src="${result.image}" alt="QR Code">`;
        
        document.getElementById('downloadSection').style.display = 'block';
    } catch (error) {
        alert('Error generating QR code');
        console.error(error);
    }
}

async function downloadQR() {
    if (!currentQRImage) {
        alert('Please generate a QR code first');
        return;
    }

    const format = document.getElementById('format').value;

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: currentQRImage,
                format: format
            })
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `qrcode_${Date.now()}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        alert('Error downloading QR code');
        console.error(error);
    }
}
