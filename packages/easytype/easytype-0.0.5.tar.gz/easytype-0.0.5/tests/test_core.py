import pytest
import datetime
import typing

from easytype.core import resolve_type, TypeBuilder, parse_unresolved_type, parse_from_dict, TypeReference
from easytype.core import PrimitiveType, UserDefinedType, InlineType, ParameterizedType, EnumType, FieldDefinition
from typing import Union, Optional


def test_resolve_type_reference():
    assert resolve_type('myType') == TypeReference(name='myType')
    assert resolve_type(TypeReference(name='myType')) == TypeReference(name='myType')


def test_resolve_primitive_type():
    assert resolve_type(int) == PrimitiveType(name='int')
    assert resolve_type(float) == PrimitiveType(name='float')
    assert resolve_type(str) == PrimitiveType(name='str')
    assert resolve_type(bool) == PrimitiveType(name='bool')
    assert resolve_type(list) == PrimitiveType(name='list')
    assert resolve_type(dict) == PrimitiveType(name='dict')
    assert resolve_type(tuple) == PrimitiveType(name='list')
    assert resolve_type(typing.Any) == PrimitiveType(name='any')

    cmt = 'this is a comment'
    assert resolve_type(int).with_comment(cmt) == PrimitiveType(name='int', comment=cmt)
    assert resolve_type(float).with_comment(cmt) == PrimitiveType(name='float', comment=cmt)
    assert resolve_type(str).with_comment(cmt) == PrimitiveType(name='str', comment=cmt)
    assert resolve_type(bool).with_comment(cmt) == PrimitiveType(name='bool', comment=cmt)
    assert resolve_type(list).with_comment(cmt) == PrimitiveType(name='list', comment=cmt)
    assert resolve_type(dict).with_comment(cmt) == PrimitiveType(name='dict', comment=cmt)
    assert resolve_type(tuple).with_comment(cmt) == PrimitiveType(name='list', comment=cmt)
    assert PrimitiveType.create_from_class_or_none(set) is None


def test_resolve_parameterized_type():
    assert resolve_type(list[int]) == ParameterizedType(name='list', params=[PrimitiveType(name='int')])
    assert resolve_type(list[float]) == ParameterizedType(name='list', params=[PrimitiveType(name='float')])
    assert resolve_type(list[str]) == ParameterizedType(name='list', params=[PrimitiveType(name='str')])
    assert resolve_type(list[bool]) == ParameterizedType(name='list', params=[PrimitiveType(name='bool')])
    assert resolve_type(list[dict]) == ParameterizedType(name='list', params=[PrimitiveType(name='dict')])

    assert resolve_type(Optional[int]) == ParameterizedType(name='optional', params=[PrimitiveType(name='int')])
    assert resolve_type(Optional[float]) == ParameterizedType(name='optional', params=[PrimitiveType(name='float')])
    assert resolve_type(Optional[str]) == ParameterizedType(name='optional', params=[PrimitiveType(name='str')])
    assert resolve_type(Optional[bool]) == ParameterizedType(name='optional', params=[PrimitiveType(name='bool')])
    assert resolve_type(Optional[dict]) == ParameterizedType(name='optional', params=[PrimitiveType(name='dict')])

    assert resolve_type(Union[str, int]) == ParameterizedType(name='union', params=[
        PrimitiveType(name='str'), PrimitiveType(name='int')
    ])

    assert resolve_type(dict[str, int]) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='int')
    ])
    assert resolve_type(dict[str, float]) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='float')
    ])
    assert resolve_type(dict[str, str]) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='str')
    ])
    assert resolve_type(dict[str, bool]) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='bool')
    ])
    assert resolve_type(dict[str, dict]) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='dict')
    ])

    assert resolve_type(tuple[str, dict, int]) == ParameterizedType(name='tuple', params=[
        PrimitiveType(name='str'), PrimitiveType(name='dict'), PrimitiveType(name='int')
    ])

    cmt = 'this is a comment'
    assert (resolve_type(list[dict]).with_comment(cmt) ==
            ParameterizedType(name='list', params=[PrimitiveType(name='dict')], comment=cmt))


def test_resolve_enum_type():
    assert resolve_type(['a', 'b', 'c']) == EnumType(choices=['a', 'b', 'c'])

    cmt = 'this is a comment'
    assert resolve_type(['a', 'b', 'c']).with_comment(cmt) == EnumType(choices=['a', 'b', 'c'], comment=cmt)


def test_resolve_inline_type():
    assert resolve_type(dict(
        x=int
    )) == InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])
    assert resolve_type(dict(
        x=int
    )).with_comment('c') == InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ], comment='c')


def test_resolve_user_defined_type():
    assert TypeBuilder.create('X', x=int) == UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])

    assert TypeBuilder.create('X', x=int).with_comment('c') == UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ], comment='c')


def test_resolve_resolved_type():
    assert resolve_type(EnumType(choices=['a', 'b', 'c'])) == EnumType(choices=['a', 'b', 'c'])
    assert resolve_type(PrimitiveType(name='int')) == PrimitiveType(name='int')
    assert resolve_type(ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='bool')
    ])) == ParameterizedType(name='dict', params=[
        PrimitiveType(name='str'), PrimitiveType(name='bool')
    ])
    assert resolve_type(InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])) == InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])
    assert resolve_type(UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])) == UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))
    ])


def test_resolve_edge_cases():
    assert ParameterizedType.get_parameterized_type_or_none(list, None) is None
    assert parse_unresolved_type(datetime.datetime) == PrimitiveType(name='any')
    assert parse_unresolved_type(typing.Callable[[int], int]) == PrimitiveType(name='any')


def test_field_comment():
    assert (
            FieldDefinition(fieldKey='x', fieldType=PrimitiveType(name='int')).with_comment('c') ==
            FieldDefinition(fieldKey='x',
                            fieldType=PrimitiveType(
                                name='int'), comment='c')
    )


def test_to_dict():
    assert PrimitiveType(name='int').to_dict() == {'type': 'PrimitiveType', 'name': 'int'}
    assert ParameterizedType(name='optional', params=[PrimitiveType(name='int')]).to_dict() == {
        'type': 'ParameterizedType', 'name': 'optional', 'params': [{'type': 'PrimitiveType', 'name': 'int'}]}
    assert EnumType(choices=['a', 'b', 'c']).to_dict() == {'type': 'EnumType', 'choices': ['a', 'b', 'c']}
    assert InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))]).to_dict() == {
               'type': 'InlineType',
               'fields': [{'fieldKey': 'x', 'fieldType': {'type': 'PrimitiveType', 'name': 'int'}}]}
    assert UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))]).to_dict() == {
               'type': 'UserDefinedType', 'name': 'X',
               'fields': [{'fieldKey': 'x', 'fieldType': {'type': 'PrimitiveType', 'name': 'int'}}]}


def test_to_dict_with_comment():
    cmt = 'this is a comment'
    # Testing PrimitiveType.
    assert PrimitiveType(name='int', comment=cmt).to_dict() == {
        'type': 'PrimitiveType', 'name': 'int', 'comment': 'this is a comment'
    }
    # Testing ParameterizedType.
    assert ParameterizedType(name='optional', params=[PrimitiveType(name='int', comment=cmt)],
                             comment=cmt).to_dict() == {
               'type': 'ParameterizedType', 'name': 'optional',
               'params': [{'type': 'PrimitiveType', 'name': 'int', 'comment': 'this is a comment'}],
               'comment': 'this is a comment'
           }
    # Testing EnumType.
    assert EnumType(choices=['a', 'b', 'c'], comment=cmt).to_dict() == {
        'type': 'EnumType', 'choices': ['a', 'b', 'c'], 'comment': 'this is a comment'
    }

    assert EnumType(choices=['a', 'b', 'c'], comment=cmt).with_name('N').to_dict() == {
        'type': 'EnumType', 'choices': ['a', 'b', 'c'], 'comment': 'this is a comment', 'name': 'N'
    }

    # Testing InlineType.
    assert InlineType(fields=[FieldDefinition('x', PrimitiveType(name='int', comment=cmt))], comment=cmt).to_dict() == {
        'type': 'InlineType',
        'fields': [
            {'fieldKey': 'x', 'fieldType': {'type': 'PrimitiveType', 'name': 'int', 'comment': 'this is a comment'}}],
        'comment': 'this is a comment'
    }
    # Testing UserDefinedType.
    assert UserDefinedType(name='X', fields=[FieldDefinition('x', PrimitiveType(name='int', comment=cmt))],
                           comment=cmt).to_dict() == {
               'type': 'UserDefinedType', 'name': 'X',
               'fields': [
                   {'fieldKey': 'x',
                    'fieldType': {'type': 'PrimitiveType', 'name': 'int', 'comment': 'this is a comment'}}],
               'comment': 'this is a comment'
           }

    assert FieldDefinition('x', fieldType=PrimitiveType(name='int')).with_comment(cmt).to_dict() == {
        'fieldKey': 'x',
        'fieldType': {'type': 'PrimitiveType', 'name': 'int'},
        'comment': 'this is a comment'
    }


def test_to_dict_from_dict():
    t = TypeReference(name='int')
    assert t == parse_from_dict(t.to_dict())

    t = PrimitiveType(name='int')
    assert t == parse_from_dict(t.to_dict())

    t = ParameterizedType(name='optional', params=[PrimitiveType(name='int')])
    assert t.to_dict() == parse_from_dict({
        'type': 'ParameterizedType', 'name': 'optional',
        'params': [{'type': 'PrimitiveType', 'name': 'int'}]}).to_dict()

    t = EnumType(choices=['a', 'b', 'c'])
    assert t == parse_from_dict({'type': 'EnumType', 'choices': ['a', 'b', 'c']})

    t = InlineType(fields=[
        FieldDefinition('x', PrimitiveType(name='int'))])
    assert t == parse_from_dict({
        'type': 'InlineType', 'fields': [{'fieldKey': 'x', 'fieldType': {'type': 'PrimitiveType', 'name': 'int'}}]})

    t = UserDefinedType(name='X', fields=[
        FieldDefinition('x', PrimitiveType(name='int'))])
    assert t == parse_from_dict({
        'type': 'UserDefinedType', 'name': 'X',
        'fields': [{'fieldKey': 'x', 'fieldType': {'type': 'PrimitiveType', 'name': 'int'}}]})

    with pytest.raises(ValueError) as err:
        parse_from_dict({
            'type': 'NotAType', 'name': 'X',
        })

    assert str(err.value) == f'Unexpected type NotAType'


def test_helpers():
    assert {'int', 'float', 'str', 'bool', 'list', 'dict', 'any'} == set(PrimitiveType.supported_types())


def test_create_from_dict():
    assert TypeBuilder.create('X', x=int) == TypeBuilder.create_from_dict('X', dict(x=int))


if __name__ == '__main__':
    pytest.main()
