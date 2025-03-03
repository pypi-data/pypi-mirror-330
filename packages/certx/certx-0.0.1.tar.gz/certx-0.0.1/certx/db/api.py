from certx.db.model.models import db
from certx.db.model.models import PrivateCertificateAuthorityModel


def list_all_ca():
    return PrivateCertificateAuthorityModel.query.all()


def query_by_id(resource_id, resource_cls):
    return resource_cls.query.get(resource_id)


def delete_by_id(resource_id, resource_cls):
    obj = query_by_id(resource_id, resource_cls)
    db.session.delete(obj)
    db.session.commit()


def save_object(obj):
    db.session.add(obj)
    db.session.commit()
