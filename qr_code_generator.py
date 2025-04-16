
@frappe.whitelist()
def get_qr_code(data: str) -> str:
    """Generate QR Code data

    Args:
        data (str): The information used to generate the QR Code

    Returns:
        str: The QR Code.
    """
    qr_code_bytes = get_qr_code_bytes(data)
    base_64_string = bytes_to_base64_string(qr_code_bytes)

    return add_file_info(base_64_string)

def add_file_info(data: str) -> str:
    """Add info about the file type and encoding."""
    return f"data:image/png;base64, {data}"

def get_qr_code_bytes(data: bytes | str) -> bytes:
    """Create a QR code and return the bytes without using BytesIO."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_array = np.array(img)
    
    img_pil = Image.fromarray(img_array)
    
    bytes_list = []
    img_pil.save(BytesArrayEncoder(bytes_list), format='PNG')
    
    return b''.join(bytes_list)

def bytes_to_base64_string(data: bytes) -> str:
    """Convert bytes to a base64 encoded string."""
    return base64.b64encode(data).decode("utf-8")

class BytesArrayEncoder:
    def __init__(self, byte_list):
        self.byte_list = byte_list
        
    def write(self, b):
        self.byte_list.append(b)
