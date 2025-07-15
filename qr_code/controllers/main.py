# -*- coding: utf-8 -*-
import base64
import io
import qrcode
from odoo import http

class QRSystrayController(http.Controller):
    """Declares a controller to handle QR code generation"""
    @http.route('/qr_systray/generate', type='json', auth='user')
    def generate_qr(self, text):
        """Generates the QR code based on the text from the dropdown"""
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "image": f"data:image/png;base64,{img_str}"
        }

