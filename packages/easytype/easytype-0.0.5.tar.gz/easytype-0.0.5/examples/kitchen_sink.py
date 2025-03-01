from easytype import TypeBuilder
import typing
import json

at = TypeBuilder.create(
    'AnotherType',
    some_value=int,
)
t = TypeBuilder.create(
    'Example',

    # type ref
    recursive_value='Example',

    #     primitive types
    int_value=int,
    float_value=float,
    str_value=str,
    bool_value=bool,
    list_value=list,
    dict_value=dict,
    any_value=typing.Any,

    #     inline types
    inline_value=dict(
        int_value=int,
        float_value=float,
        str_value=str,
        bool_value=bool,
        list_value=list,
        dict_value=dict,
        any_value=typing.Any,
    ),

    #     enum type
    enum_value=['apple', 'ornage'],

    #    user defined type
    another_type_value=at,

    #    parameterized
    list_of_int_value=list[int],
    list_of_float_value=list[float],
    list_of_str_value=list[str],
    list_of_bool_value=list[bool],
    list_of_list_value=list[list],
    list_of_dict_value=list[dict],
    list_of_any_value=list[typing.Any],
    optional_of_int_value=typing.Optional[int],
    optional_of_float_value=typing.Optional[float],
    optional_of_str_value=typing.Optional[str],
    optional_of_bool_value=typing.Optional[bool],
    optional_of_list_value=typing.Optional[list],
    optional_of_dict_value=typing.Optional[dict],
    optional_of_any_value=typing.Optional[typing.Any],
    dict_of_int_value=dict[str, int],
    dict_of_float_value=dict[str, float],
    dict_of_str_value=dict[str, str],
    dict_of_bool_value=dict[str, bool],
    dict_of_list_value=dict[str, list],
    dict_of_dict_value=dict[str, dict],
    dict_of_any_value=dict[str, typing.Any],
    tuple_of_bool_str_dict_value=tuple[bool, str, dict],
    tuple_of_int_list_value=tuple[int, list],
    tuple_of_bool_dict_value=tuple[bool, dict],
    tuple_of_float_list_bool_value=tuple[float, list, bool],
    tuple_of_str_bool_dict_value=tuple[str, bool, dict],
    union_of_dict_list_value=typing.Union[dict, list],
    union_of_int_float_value=typing.Union[int, float],
    union_of_int_list_value=typing.Union[int, list],
    union_of_float_dict_value=typing.Union[float, dict],
    union_of_list_dict_value=typing.Union[list, dict],
)

print(json.dumps(t.to_dict(), indent=2))
