"""QR code generation and encoding/decoding for member identification.

QR data format: SPOOL:{base64(SALT + member_id)}
- Only this app knows the SALT and PREFIX; other scanners see meaningless text.
"""

import base64
import os

import qrcode
from qrcode.image.styledpil import StyledPilImage


SALT = "swimpool2026"
PREFIX = "SPOOL:"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
QR_DIR = os.path.join(DATA_DIR, "qr_codes")


def _ensure_qr_dir():
    os.makedirs(QR_DIR, exist_ok=True)


def encode_member_qr(member_id):
    """Encode a member ID into the QR data string.

    Returns a string like: SPOOL:c3dpbXBvb2wyMDI2U1AwMDAwMDE=
    """
    raw = SALT + member_id
    encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
    return PREFIX + encoded


def decode_member_qr(qr_data):
    """Decode a scanned QR data string back to a member ID.

    Returns the member ID string, or None if the data is invalid
    (i.e. not from this app).
    """
    if not qr_data or not isinstance(qr_data, str):
        return None
    qr_data = qr_data.strip()
    if not qr_data.startswith(PREFIX):
        return None
    try:
        encoded = qr_data[len(PREFIX):]
        raw_bytes = base64.b64decode(encoded)
        raw = raw_bytes.decode("utf-8")
        if raw.startswith(SALT):
            return raw[len(SALT):]
    except (ValueError, UnicodeDecodeError):
        pass
    return None


def generate_qr_image(member_id, save=True):
    """Generate a QR code image for a member.

    If save=True, writes to data/qr_codes/qr_{member_id}.png and returns the path.
    If save=False, returns the PIL Image object.
    """
    data = encode_member_qr(member_id)
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    if save:
        _ensure_qr_dir()
        path = os.path.join(QR_DIR, f"qr_{member_id}.png")
        img.save(path)
        return path
    return img


def get_qr_path(member_id):
    """Return the expected file path for a member's QR code image."""
    return os.path.join(QR_DIR, f"qr_{member_id}.png")
