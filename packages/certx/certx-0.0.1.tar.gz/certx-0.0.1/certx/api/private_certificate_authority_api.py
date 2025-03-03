from flask import request
from flask_restx import Resource

from marshmallow.exceptions import ValidationError
from oslo_log import log as logging

from certx.api.model import model as api_model
from certx.common import exceptions
from certx import rest_api
from certx.service import certificate_authority_service
from certx.utils import algorithm_util

logger = logging.getLogger(__name__)

ca_ns = rest_api.namespace('', description='Private Certificate Authority')


@ca_ns.route('/v1/private-certificate-authorities')
class PrivateCertificateAuthoritiesResource(Resource):
    @ca_ns.doc('ListPrivateCertificateAuthorities')
    def get(self):
        query_option = api_model.ListPrivateCertificateAuthorityParameter().load(request.args.to_dict())
        logger.debug('query parameter: %s', query_option)
        cas = certificate_authority_service.list_certificate_authorities(query_option)
        return {'private_certificate_authorities': api_model.PrivateCertificateAuthority().dump(cas, many=True)}

    @ca_ns.doc('CreatePrivateCertificateAuthority')
    @ca_ns.expect(api_model.CreatePrivateCertificateAuthorityRequestBody, validate=True)
    def post(self):
        try:
            req_body = api_model.CreatePrivateCertificateAuthorityRequestBody().load(rest_api.payload)
            ca_dict = req_body['certificate_authority']
        except ValidationError as e:
            return {'message': 'Validation error', 'errors': e.messages}, 400

        if not algorithm_util.validate_key_and_signature_algorithm(ca_dict.get('key_algorithm'),
                                                                   ca_dict.get('signature_algorithm')):
            msg = 'unmatched key_algorithm {} and signature_algorithm {}'.format(
                ca_dict.get('key_algorithm').value, ca_dict.get('signature_algorithm').value)
            logger.error(msg)
            raise exceptions.InvalidInput(msg)

        logger.info('Create private CA with params: {}'.format(ca_dict))
        ca = certificate_authority_service.create_certificate_authority(ca_option=ca_dict)
        return {'private_certificate_authority': api_model.PrivateCertificateAuthority().dump(ca)}


@ca_ns.route('/v1/private-certificate-authorities/<ca_id>')
class PrivateCertificateAuthorityResource(Resource):
    @ca_ns.doc('ShowPrivateCertificateAuthority')
    def get(self, ca_id):
        ca = certificate_authority_service.get_certificate_authority(ca_id)
        return {'private_certificate_authority': api_model.PrivateCertificateAuthority().dump(ca)}

    @ca_ns.doc('DeletePrivateCertificateAuthority')
    def delete(self, ca_id):
        logger.info('Delete private CA %s', ca_id)
        certificate_authority_service.delete_certificate_authority(ca_id)
        return '', 204


@ca_ns.route('/v1/private-certificate-authorities/<ca_id>/export')
class PrivateCertificateAuthorityExportResource(Resource):
    @ca_ns.doc('ExportPrivateCertificateAuthority')
    def post(self, ca_id):
        content = certificate_authority_service.export_certificate_authority(ca_id)
        return api_model.PrivateCertificateAuthorityContent().dump(content)
