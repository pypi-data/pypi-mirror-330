from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Any

import mpmath  # type: ignore
import numpy as np
from attrs import cmp_using, field, frozen

from .. import VERSION, ArrayBIGINT, this_yaml, yaml_rt_mapper  # noqa: TID252

__version__ = VERSION

type MPFloat = mpmath.ctx_mp_python.mpf
type MPMatrix = mpmath.matrix  # type: ignore


@frozen
class INVTableData:
    industry_group: str
    additional_evidence: str
    data_array: ArrayBIGINT = field(eq=cmp_using(eq=np.array_equal))


type INVData = MappingProxyType[
    str, MappingProxyType[str, MappingProxyType[str, INVTableData]]
]
type INVData_in_ = Mapping[str, Mapping[str, Mapping[str, INVTableData]]]


(_, _) = (
    this_yaml.representer.add_representer(
        Decimal, lambda _r, _d: _r.represent_scalar("!Decimal", f"{_d}")
    ),
    this_yaml.constructor.add_constructor(
        "!Decimal", lambda _c, _n, /: Decimal(_c.construct_scalar(_n))
    ),
)


(_, _) = (
    this_yaml.representer.add_representer(
        mpmath.mpf, lambda _r, _d: _r.represent_scalar("!MPFloat", f"{_d}")
    ),
    this_yaml.constructor.add_constructor(
        "!MPFloat", lambda _c, _n, /: mpmath.mpf(_c.construct_scalar(_n))
    ),
)

(_, _) = (
    this_yaml.representer.add_representer(
        mpmath.matrix, lambda _r, _d: _r.represent_sequence("!MPMatrix", _d.tolist())
    ),
    this_yaml.constructor.add_constructor(
        "!MPMatrix",
        lambda _c, _n, /: mpmath.matrix(_c.construct_sequence(_n, deep=True)),
    ),
)


def _dict_from_mapping(_p: Mapping[Any, Any], /) -> dict[Any, Any]:
    retval = {}
    for _k, _v in _p.items():  # for subit in it:
        retval |= {_k: _dict_from_mapping(_v)} if isinstance(_v, Mapping) else {_k: _v}
    return retval


def _mappingproxy_from_mapping(_p: Mapping[Any, Any], /) -> MappingProxyType[Any, Any]:
    retval = {}
    for _k, _v in _p.items():  # for subit in it:
        retval |= (
            {_k: _mappingproxy_from_mapping(_v)}
            if isinstance(_v, Mapping)
            else {_k: _v}
        )
    return MappingProxyType(retval)


_, _ = (
    this_yaml.representer.add_representer(
        MappingProxyType,
        lambda _r, _d: _r.represent_mapping("!mappingproxy", dict(_d.items())),
    ),
    this_yaml.constructor.add_constructor(
        "!mappingproxy", lambda _c, _n: MappingProxyType(yaml_rt_mapper(_c, _n))
    ),
)


for _typ in (INVTableData,):
    _, _ = (
        this_yaml.representer.add_representer(
            _typ,
            lambda _r, _d: _r.represent_mapping(
                f"!{_d.__class__.__name__}",
                {
                    _a.name: getattr(_d, _a.name)
                    for _a in _d.__attrs_attrs__
                    if _a.name not in {"coordinates", "area"}
                },
            ),
        ),
        this_yaml.constructor.add_constructor(
            f"!{_typ.__name__}",
            lambda _c, _n: globals()[_n.tag.lstrip("!")](**yaml_rt_mapper(_c, _n)),
        ),
    )
