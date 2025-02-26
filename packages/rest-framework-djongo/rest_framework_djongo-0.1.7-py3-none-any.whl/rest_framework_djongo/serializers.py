from bson import ObjectId
from bson.errors import InvalidId
from django.db import models
from django.utils.encoding import smart_str, is_protected_type
from django.utils.translation import gettext_lazy as _
from djongo import models as djo_models
from rest_framework import fields as drf_fields
from rest_framework import serializers


class ObjectIdField(serializers.Field):
    """ Field for ObjectId values """

    def to_internal_value(self, value):
        try:
            return ObjectId(smart_str(value))
        except InvalidId:
            raise serializers.ValidationError("'%s' is not a valid ObjectId" % value)

    def to_representation(self, value):
        return smart_str(value)


class EmbeddedField(serializers.Field):
    default_error_messages = {
        'not_a_dict': serializers.DictField.default_error_messages['not_a_dict'],
        'undefined_model': _('Document `{doc_cls}` has not been defined.'),
        'missing_class': _('Provided data has not `_cls` item.')
    }

    def to_internal_value(self, value):
        return value

    # def value_from_object(self, obj):
    #     if isinstance(obj, dict):
    #         return obj.get(self.attname)
    #     return getattr(obj, self.attname)

    def to_representation(self, value):
        return value


class GenericDjongoSerializer(serializers.ModelSerializer):
    """
    Serializer for GenericDjongoModel.
    """
    serializer_field_mapping = {
        models.AutoField: drf_fields.IntegerField,
        models.BigIntegerField: drf_fields.IntegerField,
        models.BooleanField: drf_fields.BooleanField,
        models.CharField: drf_fields.CharField,
        models.CommaSeparatedIntegerField: drf_fields.CharField,
        models.DateField: drf_fields.DateField,
        models.DateTimeField: drf_fields.DateTimeField,
        models.DecimalField: drf_fields.DecimalField,
        models.DurationField: drf_fields.DurationField,
        models.EmailField: drf_fields.EmailField,
        models.Field: drf_fields.ModelField,
        models.FileField: drf_fields.FileField,
        models.FloatField: drf_fields.FloatField,
        models.ImageField: drf_fields.ImageField,
        models.IntegerField: drf_fields.IntegerField,
        models.NullBooleanField: drf_fields.BooleanField,
        models.PositiveIntegerField: drf_fields.IntegerField,
        models.PositiveSmallIntegerField: drf_fields.IntegerField,
        models.SlugField: drf_fields.SlugField,
        models.SmallIntegerField: drf_fields.IntegerField,
        models.TextField: drf_fields.CharField,
        models.TimeField: drf_fields.TimeField,
        models.URLField: drf_fields.URLField,
        models.UUIDField: drf_fields.UUIDField,
        models.GenericIPAddressField: drf_fields.IPAddressField,
        models.FilePathField: drf_fields.FilePathField,

        djo_models.ObjectIdField: ObjectIdField,
        djo_models.EmbeddedField: EmbeddedField,
        # djo_models.ArrayField: EmbeddedField,
        djo_models.GenericObjectIdField: ObjectIdField,
        djo_models.JSONField: drf_fields.JSONField,
        # djo_models.ArrayField: drfd_fields.ObjectIdField,
        # djo_models.ArrayReferenceField: drf_djo_fields.ObjectIdField,

    }

    def get_default_field_names(self, declared_fields, model_info):
        return (
                list(declared_fields.keys())
                + list(model_info.fields_and_pk.keys())
        )


class EmbeddedSerializer(GenericDjongoSerializer):
    """
    Serializer for Embedded.
    """
    _saving_instances = False

    def validate(self, attrs):
        pk_field = self.Meta.model._meta.pk
        if pk_field.name not in attrs and pk_field.auto_created:
            attrs[pk_field.name] = pk_field.get_default()
        return attrs

    def get_unique_together_validators(self):
        # skip the valaidators
        return []
