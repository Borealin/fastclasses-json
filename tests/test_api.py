from dataclasses import dataclass, field
from typing import Optional, List, Dict

import pytest

from fastclasses_json.api import dataclass_json


def test_decorator():

    @dataclass_json
    @dataclass
    class A:
        x: int

    assert A.from_dict
    assert A(1).from_dict

    assert A.to_dict
    assert A(1).to_dict

    @dataclass_json()
    @dataclass
    class B:
        x: int

    assert B.from_dict
    assert B(1).from_dict

    assert B.to_dict
    assert B(1).to_dict


def test_to_dict():

    @dataclass_json
    @dataclass
    class A:
        x: int
        y: str

    assert A(5, 'hi').to_dict() == {'x': 5, 'y': 'hi'}


def test_from_dict():

    @dataclass_json
    @dataclass
    class A:
        x: int
        y: str

    assert A.from_dict({'x': 5, 'y': 'hi'}) == A(5, 'hi')


def test_to_json():

    @dataclass_json
    @dataclass
    class A:
        x: int
        y: str

    assert A(5, 'hi').to_json() == '{"x":5,"y":"hi"}'
    import textwrap
    assert A(5, 'hi').to_json(indent=2) == textwrap.dedent(
        """\
        {
          "x": 5,
          "y": "hi"
        }"""
    )


def test_from_json():

    @dataclass_json
    @dataclass
    class A:
        x: int
        y: str

    assert A.from_json('{"x":5,"y":"hi"}') == A(5, 'hi')


def test_to_dict__optional():

    @dataclass_json
    @dataclass
    class A:
        x: Optional[int]

    assert A(None).to_dict() == {}
    assert A(1).to_dict() == {'x': 1}


def test_from_dict__optional():

    @dataclass_json
    @dataclass
    class A:
        x: Optional[int]

    assert A.from_dict({}) == A(None)


def test_to_dict__nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: A

    assert B(A('xxx')).to_dict() == {
        'a': {
            'a': 'xxx'
        }
    }


def test_from_dict__nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: A

    assert B.from_dict({
        'a': {
            'a': 'xxx'
        }
    }) == B(A('xxx'))


def test_to_dict__list_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: List[A]

    assert B([A('xxx'), A('yyy')]).to_dict() == {
        'a': [{
            'a': 'xxx',
        }, {
            'a': 'yyy',
        }]
    }


def test_from_dict__list_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: List[A]

    assert B.from_dict({
        'a': [{
            'a': 'xxx',
        }, {
            'a': 'yyy',
        }]
    }) == B([A('xxx'), A('yyy')])


def test_to_dict__optional_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: Optional[A]

    assert B(A('xxx')).to_dict() == {
        'a': {
            'a': 'xxx'
        }
    }
    assert B(None).to_dict() == {}


def test_from_dict__optional_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: Optional[A]

    assert B.from_dict({
        'a': {
            'a': 'xxx'
        }
    }) == B(A('xxx'))


def test_to_dict__optional_list_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: Optional[List[A]]

    assert B([A('xxx'), A('yyy')]).to_dict() == {
        'a': [{
            'a': 'xxx',
        }, {
            'a': 'yyy',
        }]
    }
    assert B(None).to_dict() == {}


def test_from_dict__optional_list_nested():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: Optional[List[A]]

    assert B.from_dict({
        'a': [{
            'a': 'xxx',
        }, {
            'a': 'yyy',
        }]
    }) == B([A('xxx'), A('yyy')])


def test_from_dict__optional_list_nested_with_defaults():

    @dataclass
    class A:
        a: str

    @dataclass_json
    @dataclass
    class B:
        a: Optional[List[A]] = None

    assert B.from_dict({
        'a': [{
            'a': 'xxx',
        }, {
            'a': 'yyy',
        }]
    }) == B([A('xxx'), A('yyy')])


def test_from_dict__default():

    @dataclass_json
    @dataclass
    class Account:
        # Balance must contain at least one € to begin with
        bank_balance: int = 1

    assert Account.from_dict({}) == Account(bank_balance=1)


def test_from_dict__default_factory():

    @dataclass_json
    @dataclass
    class A:
        # Balance must contain at least one € to begin with
        xs: List[int] = field(default_factory=list)

    assert A.from_dict({}) == A(xs=[])


# These have to be defined at the module level since that's where string type
# hints are evaluated, they are for the string_type_name

@dataclass
class A:
    s: str


@dataclass_json
@dataclass
class B:
    A: Optional['A'] = None


def test_from_dict__string_type_name():

    assert B.from_dict({
        'A': {
            's': 'yes',
        }
    }) == B(A('yes'))


def test_to_dict__string_type_name():

    assert B(A('yes')).to_dict() == {
        'A': {
            's': 'yes',
        }
    }


@dataclass_json
@dataclass
class D:
    C: Optional['C'] = None


@dataclass
class C:
    s: str


def test_from_dict__string_type_name__reverse_definition_order():

    assert D.from_dict({
        'C': {
            's': 'yes',
        }
    }) == D(C('yes'))


def test_to_dict__string_type_name__reverse_definition_order():

    assert D(C('yes')).to_dict() == {
        'C': {
            's': 'yes',
        }
    }


def test_to_dict__enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: A

    assert B(A.X).to_dict() == {'a': 'ex'}
    assert B(A.Y).to_dict() == {'a': 'why'}


def test_from_dict__enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: A

    assert B.from_dict({'a': 'ex'}) == B(A.X)
    assert B.from_dict({'a': 'why'}) == B(A.Y)


def test_from_dict__enum_functional_syntax():
    from enum import Enum

    A = Enum('A', (('X', 'ex'), ('Y', 'why'),))

    @dataclass_json
    @dataclass
    class B:
        a: A

    assert B.from_dict({'a': 'ex'}) == B(A.X)
    assert B.from_dict({'a': 'why'}) == B(A.Y)


def test_to_dict__optional_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: Optional[A]

    assert B(A.X).to_dict() == {'a': 'ex'}
    assert B(A.Y).to_dict() == {'a': 'why'}
    assert B(None).to_dict() == {}


def test_from_dict__optional_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: Optional[A]

    assert B.from_dict({'a': 'ex'}) == B(A.X)
    assert B.from_dict({'a': 'why'}) == B(A.Y)
    assert B.from_dict({}) == B(None)


def test_to_dict__list_of_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: List[A]

    assert B([A.X]).to_dict() == {'a': ['ex']}
    assert B([A.Y]).to_dict() == {'a': ['why']}


def test_from_dict__list_of_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: List[A]

    assert B.from_dict({'a': ['ex']}) == B([A.X])
    assert B.from_dict({'a': ['why']}) == B([A.Y])


def test_to_dict__dict_of_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: Dict[str, A]

    assert B({'marky': A.X}).to_dict() == {'a': {'marky': 'ex'}}
    assert B({'marky': A.Y}).to_dict() == {'a': {'marky': 'why'}}


def test_from_dict__dict_of_enum():
    from enum import Enum

    class A(Enum):
        X = 'ex'
        Y = 'why'

    @dataclass_json
    @dataclass
    class B:
        a: Dict[str, A]

    assert B.from_dict({'a': {'marky': 'ex'}}) == B({'marky': A.X})
    assert B.from_dict({'a': {'marky': 'why'}}) == B({'marky': A.Y})


def test_to_dict__date():
    from datetime import date

    @dataclass_json
    @dataclass
    class A:
        x: date

    assert A(date(2021, 6, 17)).to_dict() == {'x': "2021-06-17"}


def test_from_dict__date():
    from datetime import date

    @dataclass_json
    @dataclass
    class A:
        x: date

    assert A.from_dict({'x': "2021-06-17"}) == A(date(2021, 6, 17))


def test_to_dict__datetime():
    from datetime import datetime, timezone

    @dataclass_json
    @dataclass
    class A:
        x: datetime

    assert A(datetime(2021, 6, 17)).to_dict() == \
        {'x': "2021-06-17T00:00:00"}

    assert A(datetime(2021, 6, 17, 10, 0, 0,)).to_dict() \
        == {'x': "2021-06-17T10:00:00"}

    assert A(datetime(2021, 6, 17, 10, 0, 0, tzinfo=timezone.utc)).to_dict() \
        == {'x': "2021-06-17T10:00:00+00:00"}

    assert A(datetime(2021, 9, 22, 7, 54, 13, 370000,
                      tzinfo=timezone.utc)).to_dict() \
        == {'x': "2021-09-22T07:54:13.370000+00:00"}


def test_from_dict__datetime():
    from datetime import datetime, timezone

    @dataclass_json
    @dataclass
    class A:
        x: datetime

    assert A.from_dict({'x': "2021-06-17"}) == A(datetime(2021, 6, 17))

    assert A.from_dict({'x': "2021-06-17T10:00:00"}) \
        == A(datetime(2021, 6, 17, 10, 0, 0,))

    assert A.from_dict({'x': "2021-06-17T10:00:00+00:00"}) \
        == A(datetime(2021, 6, 17, 10, 0, 0, tzinfo=timezone.utc))
    assert A.from_dict({'x': "2021-06-17T10:00:00Z"}) \
        == A(datetime(2021, 6, 17, 10, 0, 0, tzinfo=timezone.utc))


def test_datetimes_not_supported_by_standard_library():
    pytest.importorskip("dateutil")
    from datetime import datetime, timezone

    @dataclass_json
    @dataclass
    class A:
        x: datetime

    assert A.from_dict({'x': "2021-09-22T07:54:13.37Z"}) \
        == A(datetime(2021, 9, 22, 7, 54, 13, 370000, tzinfo=timezone.utc))


def test_to_dict__decimal():
    from decimal import Decimal

    @dataclass_json
    @dataclass
    class A:
        x: Decimal

    assert A(Decimal('9.99')).to_dict() == {'x': "9.99"}


def test_from_dict__decimal():
    from decimal import Decimal

    @dataclass_json
    @dataclass
    class A:
        x: Decimal

    assert A.from_dict({'x': "9.99"}) == A(Decimal('9.99'))

    # Want to not surprise people if non-string is sent
    # Decimal(1.23) == \
    # Decimal('1.229999999999999982236431605997495353221893310546875')
    assert A.from_dict({'x': 1.23}) == A(Decimal('1.23'))


def test_to_dict__uuid():
    from uuid import UUID

    @dataclass_json
    @dataclass
    class A:
        x: UUID

    assert A(UUID('8199d02b-e2fb-4d95-9bdc-d5db0dd0c66d')).to_dict() \
        == {'x': '8199d02b-e2fb-4d95-9bdc-d5db0dd0c66d'}


def test_from_dict__uuid():
    from uuid import UUID

    @dataclass_json
    @dataclass
    class A:
        x: UUID

    assert A.from_dict({'x': '8199d02b-e2fb-4d95-9bdc-d5db0dd0c66d'}) == \
        A(UUID('8199d02b-e2fb-4d95-9bdc-d5db0dd0c66d'))


def test_to_dict__custom_encoder():

    @dataclass
    class Point:
        x: float
        y: float

    @dataclass_json
    @dataclass
    class A:
        x: List[Point] = field(metadata={
            "fastclasses_json": {
                "encoder": lambda ps: [[p.x, p.y] for p in ps]
            }
        })

    # The default to_json would give a list of dictionaries
    # but maybe we want a more compact output, say two-element arrays
    a = A([
        Point(0.1, 0.2),
        Point(0.3, 0.4),
    ])
    assert a.to_dict() == {"x": [[0.1, 0.2], [0.3, 0.4]]}


def test_to_dict__custom_encoder2():
    from datetime import date

    @dataclass_json
    @dataclass
    class C:
        x: date = field(metadata={
            "fastclasses_json": {
                "encoder": lambda d: d.year * 10000 + d.month * 100 + d.day
            }
        })

    assert C(date(1999, 1, 23)).to_dict() == {'x': 19990123}


def test_from_dict__custom_decoder():

    @dataclass
    class Point:
        x: float
        y: float

    @dataclass_json
    @dataclass
    class A:
        x: List[Point] = field(metadata={
            "fastclasses_json": {
                "decoder": lambda ps: [Point(p[0], p[1]) for p in ps]
            }
        })

    # The default to_json would give a list of dictionaries
    # but maybe we want a mroe compact output, say two-element arrays
    a = A([
        Point(0.1, 0.2),
        Point(0.3, 0.4),
    ])
    assert A.from_dict({"x": [[0.1, 0.2], [0.3, 0.4]]}) == a


def test__custom_field_name():

    @dataclass
    class Coach:
        from_: str = field(metadata={
            "fastclasses_json": {"field_name": "from"}
        })
        to_: str = field(metadata={
            "fastclasses_json": {"field_name": "to"}
        })

    @dataclass_json
    @dataclass
    class Itinerary:
        journeys: List[Coach]

    a = Itinerary([
        Coach("Land's End", "John O' Groats"),
        Coach("London Victoria", "Amsterdam Sloterdijk"),
    ])

    expected_dict = {"journeys": [
        {"from": "Land's End", "to": "John O' Groats"},
        {"from": "London Victoria", "to": "Amsterdam Sloterdijk"},
    ]}

    assert a.to_dict() == expected_dict

    assert Itinerary.from_dict(expected_dict) == a


def test__custom_field_name__errors():

    @dataclass_json
    @dataclass
    class A:
        x: int = field(metadata={
            "fastclasses_json": {"field_name": 99}
        })

    a = A(1)

    # These would actually work ok. but the to_json and from_json start
    # getting weird and its probably not what people expect...

    with pytest.raises(TypeError):
        a.to_dict()

    with pytest.raises(TypeError):
        a.from_dict({99: 1})


def test__missing_type_params():

    @dataclass_json
    @dataclass
    class B:
        a: List
        b: Dict

    assert B(['x', 'y'], {}).to_dict() == {'a': ['x', 'y'], 'b': {}}
    assert B.from_dict({'a': ['x', 'y'], 'b': {}}) == B(['x', 'y'], {})


@pytest.mark.xfail(reason="Not sure of the use cases")
def test_from_dict__non_init_params():

    @dataclass_json
    @dataclass
    class A:
        a: str
        b: str = field(init=False)

    a = A.from_dict({'a': 'here', 'b': 'here'})
    assert a.a == 'here'

    #
    assert hasattr(a, 'b') is False
    assert a.b == 'here'
    # Should the b be included or not
    a.to_dict()
