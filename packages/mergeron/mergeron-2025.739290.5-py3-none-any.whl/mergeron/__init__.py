from __future__ import annotations

import enum
from collections.abc import Mapping
from multiprocessing import cpu_count
from pathlib import Path
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
from ruamel import yaml

_PKG_NAME: str = Path(__file__).parent.stem

VERSION = "2025.739290.5"

__version__ = VERSION

DATA_DIR: Path = Path.home() / _PKG_NAME
"""
Defines a subdirectory named for this package in the user's home path.

If the subdirectory doesn't exist, it is created on package invocation.
"""
if not DATA_DIR.is_dir():
    DATA_DIR.mkdir(parents=False)

DEFAULT_REC_RATIO = 0.85

EMPTY_ARRAYDOUBLE = np.array([], float)
EMPTY_ARRAYINT = np.array([], int)

NTHREADS = 2 * cpu_count()

PKG_ATTRS_MAP: dict[str, object] = {}

np.set_printoptions(precision=24, floatmode="fixed")

type HMGPubYear = Literal[1982, 1984, 1992, 2010, 2023]

type ArrayBoolean = NDArray[np.bool_]
type ArrayFloat = NDArray[np.floating]
type ArrayINT = NDArray[np.unsignedinteger]

type ArrayDouble = NDArray[np.float64]
type ArrayBIGINT = NDArray[np.uint64]


this_yaml = yaml.YAML(typ="rt")
this_yaml.indent(mapping=2, sequence=4, offset=2)

# Add yaml representer, constructor for NoneType
(_, _) = (
    this_yaml.representer.add_representer(
        type(None), lambda _r, _d: _r.represent_scalar("!None", "none")
    ),
    this_yaml.constructor.add_constructor("!None", lambda _c, _n, /: None),
)


# Add yaml representer, constructor for ndarray
(_, _) = (
    this_yaml.representer.add_representer(
        np.ndarray,
        lambda _r, _d: _r.represent_sequence("!ndarray", (_d.tolist(), _d.dtype.str)),
    ),
    this_yaml.constructor.add_constructor(
        "!ndarray", lambda _c, _n, /: np.array(*_c.construct_sequence(_n, deep=True))
    ),
)


def yaml_rt_mapper(
    _c: yaml.constructor.RoundTripConstructor, _n: yaml.MappingNode
) -> Mapping[str, Any]:
    """
    Constructs a mapping from a mapping node with the RoundTripConstructor

    """
    data_: Mapping[str, Any] = yaml.constructor.CommentedMap()
    _c.construct_mapping(_n, maptyp=data_, deep=True)
    return data_


def yamelize_attrs(
    _typ: object, /, *, attr_map: Mapping[str, object] = PKG_ATTRS_MAP
) -> None:
    """Add yaml representer, constructor for attrs-defined class.

    Applying this function, attributes with property, `init=False` are
    not serialized to YAML.
    """

    attr_map |= {_typ.__name__: _typ}

    _ = this_yaml.representer.add_representer(
        _typ,
        lambda _r, _d: _r.represent_mapping(
            f"!{_d.__class__.__name__}",
            # construct mapping, rather than calling attrs.asdict(),
            # to use yaml representers defined in this package for
            # "upstream" objects
            {_a.name: getattr(_d, _a.name) for _a in _d.__attrs_attrs__ if _a.init},
        ),
    )
    _ = this_yaml.constructor.add_constructor(
        f"!{_typ.__name__}",
        lambda _c, _n: attr_map[_n.tag.lstrip("!")](**yaml_rt_mapper(_c, _n)),
    )


@this_yaml.register_class
class Enameled(enum.Enum):
    """Add YAML representer, constructor for enum.Enum"""

    @classmethod
    def to_yaml(
        cls, _r: yaml.representer.RoundTripRepresenter, _d: object[enum.EnumType]
    ) -> yaml.ScalarNode:
        return _r.represent_scalar(
            f"!{super().__getattribute__(cls, '__name__')}", f"{_d.name}"
        )

    @classmethod
    def from_yaml(
        cls, _c: yaml.constructor.RoundTripConstructor, _n: yaml.ScalarNode
    ) -> object[enum.EnumType]:
        return super().__getattribute__(cls, _n.value)


@this_yaml.register_class
@enum.unique
class RECForm(str, Enameled):
    """For derivation of recapture ratio from market shares."""

    INOUT = "inside-out"
    R"""
    Given, :math:`\overline{r}, s_i {\ } \forall {\ } i \in \set{1, 2, \ldots, m}`, with
    :math:`s_{min} = \min(s_1, s_2)`,

    .. math::

        REC_i = \frac{(1 - s_i) \overline{r}}{(1 - s_{min}) - (s_i - s_{min}) \overline{r}}

    """

    OUTIN = "outside-in"
    R"""
    Given, :math:`\pi_i {\ } \forall {\ } i \in N`,

    .. math::

        REC_i = \frac{\sum_{i \in M} \pi_i}{\sum_{j \in N} \pi_j}

    """

    FIXED = "proportional"
    R"""Given, :math:`\overline{r}`,

    .. math::

        REC_i = \overline{r} {\ } \forall {\ } i \in M

    """


@this_yaml.register_class
@enum.unique
class UPPAggrSelector(str, Enameled):
    """
    Aggregator for GUPPI and diversion ratio estimates.

    """

    AVG = "average"
    CPA = "cross-product-share weighted average"
    CPD = "cross-product-share weighted distance"
    CPG = "cross-product-share weighted geometric mean"
    DIS = "symmetrically-weighted distance"
    GMN = "geometric mean"
    MAX = "max"
    MIN = "min"
    OSA = "own-share weighted average"
    OSD = "own-share weighted distance"
    OSG = "own-share weighted geometric mean"
