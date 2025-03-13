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
    qr_codes_dir = "/app/qr_codes"
    os.makedirs(qr_codes_dir, exist_ok=True)
    img_path = f'{qr_codes_dir}/{qr_id}.png'
    img.save(img_path)
    
    return img_path, qr_id
