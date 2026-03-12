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

async function generateQR() {
    const url = document.getElementById('url').value;
    const fillColor = document.getElementById('fillColor').value;
    const backColor = document.getElementById('backColor').value;
    const size = document.getElementById('size').value;
    const errorLevel = document.getElementById('errorLevel').value;

    if (!url) {
        alert('Please enter a URL or text');
        return;
    }

    const data = {
        url: url,
        fillColor: fillColor,
        backColor: backColor,
        size: size,
        errorLevel: errorLevel,
        logo: logoData
    };

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
