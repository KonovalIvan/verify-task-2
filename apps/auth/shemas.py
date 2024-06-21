from marshmallow import fields, Schema, validate, validates, ValidationError

from apps.auth.models import User


class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=120))
    surname = fields.String(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.String(required=True, validate=validate.Length(min=6, max=121))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6, max=121))
    phone = fields.String(validate=validate.Length(max=25))
    csrf_token = fields.String(load_only=True)

    @validates('email')
    def validate_email(self, value):
        if User.query.filter_by(email=value).first():
            raise ValidationError('Email already exists.')

    @validates('phone')
    def validate_phone(self, value):
        if value and User.query.filter_by(phone=value).first():
            raise ValidationError('Phone number already exists.')
