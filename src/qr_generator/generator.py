import qrcode
import uuid
import os

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    qr_id = str(uuid.uuid4())
    qr_codes_dir = os.getenv('QR_CODES_DIR', "/app/qr_codes")
    os.makedirs(qr_codes_dir, exist_ok=True)
    img_path = os.path.join(qr_codes_dir, f"{qr_id}.png")
    img.save(img_path)
    
    return img_path, qr_id
