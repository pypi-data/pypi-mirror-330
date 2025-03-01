import typing
from dataclasses import dataclass, field
from typing import get_args, get_origin, Optional, Union


@dataclass
class UserDefinedType:
    name: str
    fields: list['FieldDefinition']
    comment: Optional[str] = None
    reference_types: list['UserDefinedType'] = field(default_factory=list)

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='UserDefinedType',
            name=self.name,
            fields=[x.to_dict() for x in self.fields],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        if self.reference_types and len(self.reference_types) > 0:
            ret['includeTypes'] = [
                t.to_dict() for t in self.reference_types
            ]

        return ret

    def reference(self, t: 'UserDefinedType') -> 'UserDefinedType':
        self.reference_types.append(t)
        return self


@dataclass
class TypeReference:
    name: str

    def to_dict(self):
        ret = dict(
            type='TypeReference',
            name=self.name,
        )

        return ret


@dataclass
class PrimitiveType:
    """
    Supported types:
    int
    float
    str
    bool
    list
    dict
    any
    """
    name: str
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    @staticmethod
    def supported_types():
        return [
            'int',
            'float',
            'str',
            'bool',
            'list',
            'dict',
            'any',
        ]

    @staticmethod
    def create_from_class_or_none(clz) -> Optional['PrimitiveType']:

        if clz is int:
            return PrimitiveType(name='int')

        elif clz is float:
            return PrimitiveType(name='float')

        elif clz is bool:
            return PrimitiveType(name='bool')

        elif clz is str:
            return PrimitiveType(name='str')

        elif clz is list:
            return PrimitiveType(name='list')

        elif clz is dict:
            return PrimitiveType(name='dict')

        elif clz is tuple:
            return PrimitiveType(name='list')

        elif clz is typing.Any:
            return PrimitiveType(name='any')

        return None

    def to_dict(self):
        ret = dict(
            type='PrimitiveType',
            name=self.name,
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


@dataclass
class InlineType:
    fields: list['FieldDefinition']
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='InlineType',
            fields=[x.to_dict() for x in self.fields],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


@dataclass
class ParameterizedType:
    """
    Supported types:
        * List
        * Dict
        * Tuple
        * Union
        * Optional
    """
    name: str
    params: list['ResolvedType']
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='ParameterizedType',
            name=self.name,
            params=[x.to_dict() for x in self.params],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret

    @staticmethod
    def get_parameterized_type_or_none(clz, origin):
        name = None

        if origin is list or origin is typing.List:
            name = 'list'
        elif origin is dict or origin is typing.Dict:
            name = 'dict'
        elif origin is tuple or origin is typing.Tuple:
            name = 'tuple'
        elif origin is typing.Union:
            # note: typing.Optional also has origin Union
            name = 'union'

        if name is not None:
            args = get_args(clz)

            if name == 'union':
                if len(args) == 2 and args[-1] is type(None):
                    # recast union of A | None to Optional[None]
                    name = 'optional'
                    args = [args[0]]

            if name in ['list', 'optional']:
                assert len(args) == 1

            if name in ['dict']:
                assert len(args) == 2

            children = [resolve_type(a) for a in args]
            return ParameterizedType(name=name, params=children)

        # In all other case, we will return none, and let caller handle this.
        return None


@dataclass
class EnumType:
    choices: list[str]
    comment: Optional[str] = None
    name: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def to_dict(self):
        ret = dict(
            type='EnumType',
            choices=[x for x in self.choices],
        )

        if self.comment is not None:
            ret['comment'] = self.comment

        if self.name is not None:
            ret['name'] = self.name

        return ret


ResolvedType = Union[UserDefinedType, InlineType, PrimitiveType, ParameterizedType, EnumType, TypeReference]


@dataclass
class FieldDefinition:
    fieldKey: str
    fieldType: ResolvedType
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            fieldKey=self.fieldKey,
            fieldType=self.fieldType.to_dict(),
        )

        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


def is_resolved_type(type_def):
    if isinstance(type_def, UserDefinedType):
        return True
    if isinstance(type_def, InlineType):
        return True
    if isinstance(type_def, PrimitiveType):
        return True
    if isinstance(type_def, ParameterizedType):
        return True
    if isinstance(type_def, EnumType):
        return True
    if isinstance(type_def, TypeReference):
        return True
    return False


class TypeBuilder:
    @staticmethod
    def create(_name: str, **kwargs) -> UserDefinedType:
        return UserDefinedType(
            name=_name,
            fields=[
                FieldDefinition(fieldKey=k, fieldType=resolve_type(v)) for k, v in kwargs.items()
            ]
        )

    @staticmethod
    def create_from_dict(_name: str, kwargs: dict) -> UserDefinedType:
        return UserDefinedType(
            name=_name,
            fields=[
                FieldDefinition(fieldKey=k, fieldType=resolve_type(v)) for k, v in kwargs.items()
            ]
        )


def is_list_of_strings(variable):
    return isinstance(variable, list) and all(isinstance(item, str) for item in variable)


def parse_unresolved_type(type_def) -> Union[PrimitiveType, ParameterizedType, EnumType]:
    """
    unresolved_type can be a primitive type or parameterizedType
    """
    origin = get_origin(type_def)
    if origin is not None:
        # Load things like List[xxx], Dict[A,B]
        pt = ParameterizedType.get_parameterized_type_or_none(type_def, origin)
        if pt is not None:
            return pt
    else:
        pt = PrimitiveType.create_from_class_or_none(type_def)
        if pt is not None:
            return pt

    return PrimitiveType(name='any')


def resolve_type(type_def) -> ResolvedType:
    if is_resolved_type(type_def):
        return type_def
    elif isinstance(type_def, str):
        return TypeReference(name=type_def)
    elif isinstance(type_def, dict):
        return InlineType(
            fields=[
                FieldDefinition(fieldKey=k, fieldType=resolve_type(v)) for k, v in type_def.items()
            ]
        )
    elif is_list_of_strings(type_def):
        return EnumType(choices=type_def)
    else:
        return parse_unresolved_type(type_def)


def parse_field_from_dict(data) -> FieldDefinition:
    return FieldDefinition(
        fieldKey=data['fieldKey'],
        comment=data.get('comment', None),
        fieldType=parse_from_dict(data['fieldType']),
    )


def parse_from_dict(data):
    type_type = data['type']
    if type_type == 'UserDefinedType':
        return UserDefinedType(
            name=data['name'],
            fields=[parse_field_from_dict(f) for f in data['fields']],
            comment=data.get('comment', None),
            reference_types=data.get('referenceTypes', []),
        )
    elif type_type == 'TypeReference':
        return TypeReference(name=data['name'])
    elif type_type == 'PrimitiveType':
        return PrimitiveType(
            name=data['name'],
            comment=data.get('comment', None),
        )
    elif type_type == 'InlineType':
        return InlineType(
            fields=[parse_field_from_dict(f) for f in data['fields']],
            comment=data.get('comment', None),
        )
    elif type_type == 'ParameterizedType':
        return ParameterizedType(
            name=data['name'],
            params=[parse_from_dict(x) for x in data['params']],
            comment=data.get('comment', None),
        )
    elif type_type == 'EnumType':
        return EnumType(
            name=data.get('name', None),
            choices=data['choices'],
            comment=data.get('comment', None),
        )
    else:
        raise ValueError(f'Unexpected type {type_type}')
