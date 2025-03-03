from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from oslo_config import cfg

from certx import app

database_conf = cfg.CONF.database

app.config['SQLALCHEMY_DATABASE_URI'] = database_conf.url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = database_conf.enable_track_modifications

db = SQLAlchemy(app)


class PrivateCertificateAuthorityModel(db.Model):
    __tablename__ = 'private_certificate_authority'

    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    path_length = db.Column(db.Integer, nullable=False, default=0)
    issuer_id = db.Column(db.String(36), nullable=True)
    key_algorithm = db.Column(db.String(32), nullable=False)
    signature_algorithm = db.Column(db.String(32), nullable=False)
    serial_number = db.Column(db.String(64), nullable=False)
    not_before = db.Column(db.DateTime, nullable=False)
    not_after = db.Column(db.DateTime, nullable=False)
    common_name = db.Column(db.String(192), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    state = db.Column(db.String(384), nullable=True)
    locality = db.Column(db.String(384), nullable=True)
    organization = db.Column(db.String(192), nullable=True)
    organization_unit = db.Column(db.String(192), nullable=True)
    uri = db.Column(db.String(128))  # 用于定位证书文件保存位置
    password = db.Column(db.String(1024))  # 密钥口令
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True, default=None)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)


class PrivateCertificateModel(db.Model):
    __tablename__ = 'private_certificate'

    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.String(32), nullable=False)
    issuer_id = db.Column(db.String(36), nullable=True)
    key_algorithm = db.Column(db.String(32), nullable=False)
    signature_algorithm = db.Column(db.String(32), nullable=False)
    serial_number = db.Column(db.String(64), nullable=False)
    not_before = db.Column(db.DateTime, nullable=False)
    not_after = db.Column(db.DateTime, nullable=False)
    common_name = db.Column(db.String(192), nullable=False)
    country = db.Column(db.String(2), nullable=False)
    state = db.Column(db.String(384), nullable=True)
    locality = db.Column(db.String(384), nullable=True)
    organization = db.Column(db.String(192), nullable=True)
    organization_unit = db.Column(db.String(192), nullable=True)
    uri = db.Column(db.String(128))  # 用于定位证书文件保存位置
    password = db.Column(db.String(1024))  # 密钥口令
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=True, default=None)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)


class CertificateResourceModel(db.Model):
    __tablename__ = 'certificate_resource'

    id = db.Column(db.String(36), primary_key=True)
    certificate_type = db.Column(db.String(32), nullable=False)  # CA, CERTIFICATE
    certificate_data = db.Column(db.LargeBinary)
    private_key_data = db.Column(db.LargeBinary)
