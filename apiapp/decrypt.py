import base64
from Crypto.Cipher import AES
import frappe
import qrcode
import io
import base64
from openlocationcode import openlocationcode

def pad(s):
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def unpad(s):
    return s[:-ord(s[len(s) - 1:])]

def decrypt(ciphertext, key):
    key = key.ljust(32)[:32]  # Ensure key is 32 bytes (256 bits) for AES-256
    iv = 'This is an IV456'  # AES requires a 16-byte IV
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    return unpad(decrypted.decode('utf-8'))

@frappe.whitelist()
def decrypt_qr_code(encrypted_text, key):
    try:
        decrypted_text = decrypt(encrypted_text, key)
        return {
            'decrypted_text': decrypted_text
        }
    except Exception as e:
        frappe.throw(f"Error decrypting QR code: {str(e)}")



# @frappe.whitelist()
# def generate_qr_code(doc, method):
#     # Create a QR code based on the document name
#     if doc.document_barcode:
#         # Create QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=6,
#             border=2,
#         )
#         qr.add_data(str(doc.document_barcode))
#         qr.make(fit=True)

#         # Generate the image
#         img = qr.make_image(fill_color="black", back_color="white")
        
#         # Save the QR code image to a buffer
#         buffer = io.BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)

#         # Prepare the file for ERPNext
#         file_doc = frappe.get_doc({
#             "doctype": "File",
#             "file_name": f"{doc.name}_qr_code.png",
#             "is_private": 0,
#             "content": buffer.getvalue(),  # Use buffer.getvalue() instead of buffer.read()
#             "attached_to_doctype": doc.doctype,
#             "attached_to_name": doc.name,
#         })
#         file_doc.save(ignore_permissions=True)

#         # Update the QR code field with the attached file URL
#         doc.db_set("custom_qr_code_field", file_doc.file_url)



# Install the library if you haven't already
@frappe.whitelist()
def shortloc(doc,method=None):
    if doc.custom_latitude and doc.custom_post_office_latitude:
        latitude = float(doc.custom_latitude)
        longitude = float(doc.custom_longitude)
        code = openlocationcode.encode(latitude, longitude)
        # Decode the code to get detailed information
        decoded_location = openlocationcode.decode(code)
        reference_latitude= float(doc.custom_post_office_latitude)
        reference_longitude =float(doc.custom_post_office_longitude)
        short_code = openlocationcode.shorten(code, reference_latitude, reference_longitude)
        # print(f"Shortened code: {short_code}")
        full_code = openlocationcode.recoverNearest(short_code, reference_latitude, reference_longitude)# Check if this matches the expected longer code
        doc.pincode=short_code