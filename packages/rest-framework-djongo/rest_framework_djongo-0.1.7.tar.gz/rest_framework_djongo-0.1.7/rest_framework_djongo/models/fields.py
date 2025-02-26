import typing

from django.core.exceptions import ValidationError
from djongo.models.fields import FormedField as DjongoFormedField, ArrayField as DjongoArrayField


class CustomSaveValueThruFieldsMixin:
    def _save_value_thru_fields(self,
                                func_name: str,
                                value: dict,
                                *other_args):
        processed_value = {}

        errors = {}
        for field in self.model_container._meta.get_fields():
            try:
                try:
                    field_value = value.get(field.attname, field.get_default())
                except KeyError:
                    raise ValidationError(f'Value for field "{field}" not supplied')
                processed_value[field.attname] = getattr(field, func_name)(field_value, *other_args)
            except ValidationError as e:
                errors[field.name] = e.error_list

        if errors:
            e = ValidationError(errors)
            raise ValidationError(str(e))


class EmbeddedField(CustomSaveValueThruFieldsMixin, DjongoFormedField):
    pass


class BaseArrayField(CustomSaveValueThruFieldsMixin, DjongoArrayField, ):
    pass


class ArrayField(BaseArrayField):
    def _save_value_thru_fields(self,
                                func_name: str,
                                value: typing.Union[list, dict],
                                *other_args):
        processed_value = []
        for pre_dict in value:
            post_dict = super()._save_value_thru_fields(func_name,
                                                        pre_dict,
                                                        *other_args)
            processed_value.append(post_dict)
        return processed_value
