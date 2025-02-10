from typing import Any, Union

from sqlalchemy import (
    JSON,
    Delete,
    MetaData,
    Select,
    Update,
)
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%"
            "(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    type_annotation_map = {dict[int | str, Any]: JSON}


class FilterMixin:
    @classmethod
    def _filter_field(
        cls,
        query: Union[Select[Any], Delete, Update],
        field_name: str,
        field_value: str | int | bool,
    ) -> Union[Select[Any], Delete, Update]:
        field_name, expr = field_name.split("__")
        if expr == "eq":
            query = query.where(getattr(cls, field_name) == field_value)
        elif expr == "ne":
            query = query.where(getattr(cls, field_name) != field_value)
        elif expr == "gt":
            query = query.where(getattr(cls, field_name) > field_value)
        elif expr == "ge":
            query = query.where(getattr(cls, field_name) >= field_value)
        elif expr == "lt":
            query = query.where(getattr(cls, field_name) < field_value)
        elif expr == "le":
            query = query.where(getattr(cls, field_name) <= field_value)
        else:
            query = query.where(getattr(cls, field_name) == field_value)
        return query

    @classmethod
    def filter(
        cls,
        query: Union[Select[Any], Delete, Update],
        filter_fields: dict,
    ) -> Union[Select[Any], Delete, Update]:
        for field, value in filter_fields.items():
            query = cls._filter_field(query, field, value)
        return query
