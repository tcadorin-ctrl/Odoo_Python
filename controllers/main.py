def _check_token(request):
    # lee token desde System Parameters (si no existe, usa fallback '12345-TEST-TOKEN-LOCAL')
    token = request.env['ir.config_parameter'].sudo().get_param('gentefit.api_token', default='12345-TEST-TOKEN-LOCAL')
    auth = request.httprequest.headers.get('Authorization', '')  # 'Bearer ...'
    if not auth.startswith('Bearer '):
        return False, 'Missing or invalid Authorization header \'Bearer <token>\''
    provided = auth.split(' ', 1)[1].strip()
    if provided != token:
        return False, 'Missing or invalid Authorization header \'Bearer <token>\''
    return True, None

class GenteFitController(http.Controller):

    @http.route('/gentefit/api/import', type='http', auth='public', methods=['POST'], csrf=False)
    def import_xml(self, **kwargs):
        ok, err = _check_token(request)
        if not ok:
            return Response({"error": err}, status=401, content_type='application/json')

        # archivo multipart 'file'
        uploaded = request.httprequest.files.get('file')
        if not uploaded:
            return Response({"error": "Missing file"}, status=400, content_type='application/json')

        content = uploaded.read()
        # opcional: validar con XSD si existe
        xsd_path = os.path.join(MODULE_DIR, '..', 'data', 'genteFit_schema.xsd')
        try:
            if os.path.exists(xsd_path):
                schema_doc = etree.parse(xsd_path)
                schema = etree.XMLSchema(schema_doc)
                doc = etree.fromstring(content)
                schema.assertValid(doc)  # lanzará excepción si invalido

            # Guardar raw xml en un registro custom gentefit.file
            vals = {
                'name': uploaded.filename or 'imported.xml',
                'filename': uploaded.filename or 'imported.xml',
                'raw_xml': base64.b64encode(content).decode('utf-8'),
            }
            rec = request.env['gentefit.file'].sudo().create(vals)

            return Response({"ok": True, "saved": rec.name}, status=200, content_type='application/json')
        except etree.DocumentInvalid as e:
            return Response({"error": "XML invalid: " + str(e)}, status=400, content_type='application/json')
        except Exception as e:
            return Response({"error": str(e)}, status=500, content_type='application/json')

    @http.route('/gentefit/api/export', type='http', auth='public', methods=['GET'], csrf=False)
    def export_xml(self, **params):
        ok, err = _check_token(request)
        if not ok:
            return Response({"error": err}, status=401, content_type='application/json')

        table = params.get('table', 'Usuarios')
        # Simplificación: si hay registros gentefit.file, devolver el último raw_xml;
        # si no, construir un XML mínimo o devolver 404.
        files = request.env['gentefit.file'].search([], order='create_date desc', limit=1)
        if files:
            raw_b64 = files.raw_xml
            try:
                raw = base64.b64decode(raw_b64)
                return Response(raw, status=200, content_type='application/xml')
            except Exception:
                return Response({"error":"Cannot decode stored XML"}, status=500, content_type='application/json')
        else:
            # como fallback devolver un XML mínimo con Batch
            sample = b'<?xml version="1.0" encoding="utf-8"?><GenteFitExport><Batch><BatchId>test</BatchId><Date>2025-11-30T12:00:00Z</Date><Origin>GenteFit</Origin></Batch></GenteFitExport>'
            return Response(sample, status=200, content_type='application/xml')