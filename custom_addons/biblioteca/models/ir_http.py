from odoo import http, models
from odoo.http import request
from odoo.exceptions import AccessDenied

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_api_key(cls):
        api_key = (
            request.httprequest.headers.get('X-Odoo-API-Key')
            or request.httprequest.headers.get('api_key')
        )

        if not api_key:
            raise AccessDenied()

        uid = request.env['res.users.apikeys']._check_credentials(
            scope='rpc',
            key=api_key,
        )

        if not uid:
            raise AccessDenied()

        request.update_env(user=uid)