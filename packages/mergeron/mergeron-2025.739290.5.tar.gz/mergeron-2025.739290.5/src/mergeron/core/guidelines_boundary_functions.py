import decimal
from typing import Any, Literal, TypedDict

import matplotlib as mpl
import matplotlib.axes as mpa
import matplotlib.patches as mpp
import matplotlib.pyplot as plt
import matplotlib.ticker as mpt
import numpy as np
from attrs import frozen
from mpmath import mp, mpf  # type: ignore

from .. import DEFAULT_REC_RATIO, VERSION, ArrayBIGINT, ArrayDouble  # noqa: TID252
from . import MPFloat

__version__ = VERSION

mp.dps = 32
mp.trap_complex = True


class ShareRatioBoundaryKeywords(TypedDict, total=False):
    """Keyword arguments for functions generating share ratio boundaries."""

    recapture_form: Literal["inside-out", "proportional"]
    dps: int
    agg_method: Literal["arithmetic mean", "geometric mean", "distance"]
    weighting: Literal["own-share", "cross-product-share", None]


@frozen
class GuidelinesBoundary:
    """Output of a Guidelines boundary function."""

    coordinates: ArrayDouble
    """Market-share pairs as Cartesian coordinates of points on the boundary."""

    area: float
    """Area under the boundary."""


def dh_area(_delta_bound: float | MPFloat = 0.01, /, *, dps: int = 9) -> float:
    R"""
    Area under the ΔHHI boundary.

    When the given ΔHHI bound matches a Guidelines standard,
    the area under the boundary is half the intrinsic clearance rate
    for the ΔHHI safeharbor.

    Notes
    -----
    To derive the knots, :math:`(s^0_1, s^1_1), (s^1_1, s^0_1)`
    of the ΔHHI boundary, i.e., the points where it intersects
    the merger-to-monopoly boundary, solve

    .. math::

        2 s1 s_2 &= ΔHHI\\
        _s_1 + s_2 &= 1

    Parameters
    ----------
    _delta_bound
        Change in concentration.
    dps
        Specified precision in decimal places.

    Returns
    -------
        Area under ΔHHI boundary.

    """

    _delta_bound = mpf(f"{_delta_bound}")
    _s_naught = (1 - mp.sqrt(1 - 2 * _delta_bound)) / 2

    return round(
        float(
            _s_naught + (_delta_bound / 2) * (mp.ln(1 - _s_naught) - mp.ln(_s_naught))
        ),
        dps,
    )


def hhi_delta_boundary(
    _delta_bound: float | decimal.Decimal | MPFloat = 0.01, /, *, dps: int = 5
) -> GuidelinesBoundary:
    """
    Generate the list of share combination on the ΔHHI boundary.

    Parameters
    ----------
    _delta_bound:
        Merging-firms' ΔHHI bound.
    dps
        Number of decimal places for rounding reported shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """

    _delta_bound = mpf(f"{_delta_bound}")
    _s_naught = 1 / 2 * (1 - mp.sqrt(1 - 2 * _delta_bound))
    _s_mid = mp.sqrt(_delta_bound / 2)

    _step_size = mp.power(10, -6)
    _s_1 = np.array(mp.arange(_s_mid, _s_naught - mp.eps, -_step_size))

    # Boundary points
    half_bdry = np.vstack((
        np.column_stack((_s_1, _delta_bound / (2 * _s_1))).astype(float),
        np.array([(mpf("0.0"), mpf("1.0"))], float),
    ))
    bdry = np.vstack((half_bdry[::-1], half_bdry[1:, ::-1]))

    return GuidelinesBoundary(bdry, dh_area(_delta_bound, dps=dps))


def hhi_pre_contrib_boundary(
    _hhi_bound: float | decimal.Decimal | MPFloat = 0.03125, /, *, dps: int = 5
) -> GuidelinesBoundary:
    """
    Share combinations on the premerger HHI contribution boundary.

    Parameters
    ----------
    _hhi_bound:
        Merging-firms' pre-merger HHI contribution bound.
    dps
        Number of decimal places for rounding reported shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """
    _hhi_bound = mpf(f"{_hhi_bound}")
    _s_mid = mp.sqrt(_hhi_bound / 2)

    step_size = mp.power(10, -dps)
    # Range-limit is 0 less a step, which is -1 * step-size
    _s_1 = np.array(mp.arange(_s_mid, -step_size, -step_size))
    s_2 = np.sqrt(_hhi_bound - _s_1**2)
    half_bdry = np.column_stack((_s_1, s_2)).astype(float)

    return GuidelinesBoundary(
        np.vstack((half_bdry[::-1], half_bdry[1:, ::-1])),
        round(float(mp.pi * _hhi_bound / 4), dps),
    )


def combined_share_boundary(
    _s_intcpt: float | decimal.Decimal | MPFloat = 0.0625, /, *, dps: int = 10
) -> GuidelinesBoundary:
    """
    Share combinations on the merging-firms' combined share boundary.

    Assumes symmetric merging-firm margins. The combined-share is
    congruent to the post-merger HHI contribution boundary, as the
    post-merger HHI bound is the square of the combined-share bound.

    Parameters
    ----------
    _s_intcpt:
        Merging-firms' combined share.
    dps
        Number of decimal places for rounding reported shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """
    _s_intcpt = mpf(f"{_s_intcpt}")
    _s_mid = _s_intcpt / 2

    _s1 = np.array([0, _s_mid, _s_intcpt], float)
    return GuidelinesBoundary(
        np.column_stack((_s1, _s1[::-1])), round(float(_s_intcpt * _s_mid), dps)
    )


def hhi_post_contrib_boundary(
    _hhi_bound: float | decimal.Decimal | MPFloat = 0.800, /, *, dps: int = 10
) -> GuidelinesBoundary:
    """
    Share combinations on the postmerger HHI contribution boundary.

    The post-merger HHI contribution boundary is identical to the
    combined-share boundary.

    Parameters
    ----------
    _hhi_bound:
        Merging-firms' pre-merger HHI contribution bound.
    dps
        Number of decimal places for rounding reported shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """
    return combined_share_boundary(
        _hhi_bound.sqrt()
        if isinstance(_hhi_bound, decimal.Decimal | mpf)
        else np.sqrt(_hhi_bound),
        dps=dps,
    )


def shrratio_boundary_wtd_avg(  # noqa: PLR0914
    _delta_star: float = 0.075,
    _r_val: float = DEFAULT_REC_RATIO,
    /,
    *,
    agg_method: Literal[
        "arithmetic mean", "geometric mean", "distance"
    ] = "arithmetic mean",
    weighting: Literal["own-share", "cross-product-share", None] = "own-share",
    recapture_form: Literal["inside-out", "proportional"] = "inside-out",
    dps: int = 5,
) -> GuidelinesBoundary:
    """
    Share combinations on the share-weighted average diversion ratio boundary.

    Parameters
    ----------
    _delta_star
        Share ratio (:math:`\\overline{d} / \\overline{r}`)
    _r_val
        recapture ratio
    agg_method
        Whether "arithmetic mean", "geometric mean", or "distance".
    weighting
        Whether "own-share" or "cross-product-share"  (or None for simple, unweighted average).
    recapture_form
        Whether recapture-ratio is MNL-consistent ("inside-out") or has fixed
        value for both merging firms ("proportional").
    dps
        Number of decimal places for rounding returned shares and area.

    Returns
    -------
        Array of share-pairs, area under boundary.

    Notes
    -----
    An analytical expression for the share-weighted arithmetic mean boundary
    is derived and plotted from y-intercept to the ray of symmetry as follows::

        from sympy import plot as symplot, solve, symbols
        _s_1, s_2 = symbols("_s_1 s_2", positive=True)

        g_val, r_val, m_val = 0.06, 0.80, 0.30
        delta_star = g_val / (r_val * m_val)

        # recapture_form == "inside-out"
        oswag = solve(
            _s_1 * s_2 / (1 - _s_1)
            + s_2 * _s_1 / (1 - (r_val * s_2 + (1 - r_val) * _s_1))
            - (_s_1 + s_2) * delta_star,
            s_2
        )[0]
        symplot(
            oswag,
            (_s_1, 0., d_hat / (1 + d_hat)),
            ylabel=s_2
        )

        cpswag = solve(
            s_2 * s_2 / (1 - _s_1)
            + _s_1 * _s_1 / (1 - (r_val * s_2 + (1 - r_val) * _s_1))
            - (_s_1 + s_2) * delta_star,
            s_2
        )[1]
        symplot(
            cpwag,
            (_s_1, 0., d_hat / (1 + d_hat)),
            ylabel=s_2
        )

        # recapture_form == "proportional"
        oswag = solve(
            _s_1 * s_2 / (1 - _s_1)
            + s_2 * _s_1 / (1 - s_2)
            - (_s_1 + s_2) * delta_star,
             s_2
        )[0]
        symplot(
            oswag,
            (_s_1, 0., d_hat / (1 + d_hat)),
            ylabel=s_2
        )

        cpswag = solve(
            s_2 * s_2 / (1 - _s_1)
            + _s_1 * _s_1 / (1 - s_2)
            - (_s_1 + s_2) * delta_star,
             s_2
        )[1]
        symplot(
            cpswag,
            (_s_1, 0.0, d_hat / (1 + d_hat)),
            ylabel=s_2
        )


    """

    _delta_star, _r_val = (mpf(f"{_v}") for _v in (_delta_star, _r_val))
    _s_mid = mp.fdiv(_delta_star, 1 + _delta_star)

    # initial conditions
    bdry = [(_s_mid, _s_mid)]
    s_1_pre, s_2_pre = _s_mid, _s_mid
    s_2_oddval, s_2_oddsum, s_2_evnsum = True, 0.0, 0.0

    # parameters for iteration
    _step_size = mp.power(10, -dps)
    theta_ = _step_size * (10 if weighting == "cross-product-share" else 1)
    for _s_1 in mp.arange(_s_mid - _step_size, 0, -_step_size):
        # The wtd. avg. GUPPI is not always convex to the origin, so we
        #   increment s_2 after each iteration in which our algorithm
        #   finds (s1, s2) on the boundary
        s_2 = s_2_pre * (1 + theta_)

        if (_s_1 + s_2) > mpf("0.99875"):
            # Loss of accuracy at 3-9s and up
            break

        while True:
            de_1 = s_2 / (1 - _s_1)
            de_2 = (
                _s_1 / (1 - lerp(_s_1, s_2, _r_val))
                if recapture_form == "inside-out"
                else _s_1 / (1 - s_2)
            )

            r_ = (
                mp.fdiv(_s_1 if weighting == "cross-product-share" else s_2, _s_1 + s_2)
                if weighting
                else 0.5
            )

            match agg_method:
                case "geometric mean":
                    delta_test = mp.expm1(lerp(mp.log1p(de_1), mp.log1p(de_2), r_))
                case "distance":
                    delta_test = mp.sqrt(lerp(de_1**2, de_2**2, r_))
                case _:
                    delta_test = lerp(de_1, de_2, r_)

            test_flag, incr_decr = (
                (delta_test > _delta_star, -1)
                if weighting == "cross-product-share"
                else (delta_test < _delta_star, 1)
            )

            if test_flag:
                s_2 += incr_decr * _step_size
            else:
                break

        # Build-up boundary points
        bdry.append((_s_1, s_2))

        # Build up area terms
        s_2_oddsum += s_2 if s_2_oddval else 0
        s_2_evnsum += s_2 if not s_2_oddval else 0
        s_2_oddval = not s_2_oddval

        # Hold share points
        s_2_pre = s_2
        s_1_pre = _s_1

    if s_2_oddval:
        s_2_evnsum -= s_2_pre
    else:
        s_2_oddsum -= s_1_pre

    _s_intcpt = _shrratio_boundary_intcpt(
        s_2_pre,
        _delta_star,
        _r_val,
        recapture_form=recapture_form,
        agg_method=agg_method,
        weighting=weighting,
    )

    if weighting == "own-share":
        gbd_prtlarea = (
            _step_size * (4 * s_2_oddsum + 2 * s_2_evnsum + _s_mid + s_2_pre) / 3
        )
        # Area under boundary
        bdry_area_total = float(
            2 * (s_1_pre + gbd_prtlarea)
            - (mp.power(_s_mid, "2") + mp.power(s_1_pre, "2"))
        )

    else:
        gbd_prtlarea = (
            _step_size * (4 * s_2_oddsum + 2 * s_2_evnsum + _s_mid + _s_intcpt) / 3
        )
        # Area under boundary
        bdry_area_total = float(2 * gbd_prtlarea - mp.power(_s_mid, "2"))

    bdry.append((mpf("0.0"), _s_intcpt))
    bdry_array = np.array(bdry, float)

    # Points defining boundary to point-of-symmetry
    return GuidelinesBoundary(
        np.vstack((bdry_array[::-1], bdry_array[1:, ::-1])),
        round(float(bdry_area_total), dps),
    )


def shrratio_boundary_xact_avg(  # noqa: PLR0914
    _delta_star: float = 0.075,
    _r_val: float = DEFAULT_REC_RATIO,
    /,
    *,
    recapture_form: Literal["inside-out", "proportional"] = "inside-out",
    dps: int = 5,
) -> GuidelinesBoundary:
    """
    Share combinations for the simple average GUPPI boundary with symmetric
    merging-firm margins.

    Notes
    -----
    An analytical expression for the exact average boundary is derived
    and plotted from the y-intercept to the ray of symmetry as follows::

        from sympy import latex, plot as symplot, solve, symbols

        _s_1, s_2 = symbols("_s_1 s_2")

        g_val, r_val, m_val = 0.06, 0.80, 0.30
        d_hat = g_val / (r_val * m_val)

        # recapture_form = "inside-out"
        sag = solve(
            (s_2 / (1 - _s_1))
            + (_s_1 / (1 - (r_val * s_2 + (1 - r_val) * _s_1)))
            - 2 * d_hat,
            s_2
        )[0]
        symplot(
            sag,
            (_s_1, 0., d_hat / (1 + d_hat)),
            ylabel=s_2
        )

        # recapture_form = "proportional"
        sag = solve((s_2/(1 - _s_1)) + (_s_1/(1 - s_2)) - 2 * d_hat, s_2)[0]
        symplot(
            sag,
            (_s_1, 0., d_hat / (1 + d_hat)),
            ylabel=s_2
        )

    Parameters
    ----------
    _delta_star
        Share ratio (:math:`\\overline{d} / \\overline{r}`).
    _r_val
        Recapture ratio
    recapture_form
        Whether recapture-ratio is MNL-consistent ("inside-out") or has fixed
        value for both merging firms ("proportional").
    dps
        Number of decimal places for rounding returned shares.

    Returns
    -------
        Array of share-pairs, area under boundary, area under boundary.

    """

    _delta_star, _r_val = (mpf(f"{_v}") for _v in (_delta_star, _r_val))
    _s_mid = _delta_star / (1 + _delta_star)
    _step_size = mp.power(10, -dps)

    _bdry_start = np.array([(_s_mid, _s_mid)])
    _s_1 = np.array(mp.arange(_s_mid - _step_size, 0, -_step_size))
    if recapture_form == "inside-out":
        _s_intcpt = mp.fdiv(
            mp.fsub(
                2 * _delta_star * _r_val + 1, mp.fabs(2 * _delta_star * _r_val - 1)
            ),
            2 * mpf(f"{_r_val}"),
        )
        nr_t1 = 1 + 2 * _delta_star * _r_val * (1 - _s_1) - _s_1 * (1 - _r_val)

        nr_sqrt_mdr = 4 * _delta_star * _r_val
        nr_sqrt_mdr2 = nr_sqrt_mdr * _r_val
        nr_sqrt_md2r2 = nr_sqrt_mdr2 * _delta_star

        nr_sqrt_t1 = nr_sqrt_md2r2 * (_s_1**2 - 2 * _s_1 + 1)
        nr_sqrt_t2 = nr_sqrt_mdr2 * _s_1 * (_s_1 - 1)
        nr_sqrt_t3 = nr_sqrt_mdr * (2 * _s_1 - _s_1**2 - 1)
        nr_sqrt_t4 = (_s_1**2) * (_r_val**2 - 6 * _r_val + 1)
        nr_sqrt_t5 = _s_1 * (6 * _r_val - 2) + 1

        nr_t2_mdr = nr_sqrt_t1 + nr_sqrt_t2 + nr_sqrt_t3 + nr_sqrt_t4 + nr_sqrt_t5

        # Alternative grouping of terms in np.sqrt
        nr_sqrt_s1sq = (_s_1**2) * (
            nr_sqrt_md2r2 + nr_sqrt_mdr2 - nr_sqrt_mdr + _r_val**2 - 6 * _r_val + 1
        )
        nr_sqrt_s1 = _s_1 * (
            -2 * nr_sqrt_md2r2 - nr_sqrt_mdr2 + 2 * nr_sqrt_mdr + 6 * _r_val - 2
        )
        nr_sqrt_nos1 = nr_sqrt_md2r2 - nr_sqrt_mdr + 1

        nr_t2_s1 = nr_sqrt_s1sq + nr_sqrt_s1 + nr_sqrt_nos1

        if not np.isclose(
            np.einsum("i->", nr_t2_mdr.astype(float)),
            np.einsum("i->", nr_t2_s1.astype(float)),
            rtol=0,
            atol=0.5 * dps,
        ):
            raise RuntimeError(
                "Calculation of sq. root term in exact average GUPPI"
                f"with recapture spec, {f'"{recapture_form}"'} is incorrect."
            )

        s_2 = (nr_t1 - np.sqrt(nr_t2_s1)) / (2 * _r_val)

    else:
        _s_intcpt = mp.fsub(_delta_star + 1 / 2, mp.fabs(_delta_star - 1 / 2))
        s_2 = (
            (1 / 2)
            + _delta_star
            - _delta_star * _s_1
            - np.sqrt(
                ((_delta_star**2) - 1) * (_s_1**2)
                + (-2 * (_delta_star**2) + _delta_star + 1) * _s_1
                + (_delta_star**2)
                - _delta_star
                + (1 / 4)
            )
        )

    bdry_inner = np.column_stack((_s_1, s_2))
    bdry_end = np.array([(mpf("0.0"), _s_intcpt)], float)

    bdry = np.vstack((
        bdry_end,
        bdry_inner[::-1],
        _bdry_start,
        bdry_inner[:, ::-1],
        bdry_end[:, ::-1],
    )).astype(float)
    s_2 = np.concatenate((np.array([_s_mid], float), s_2))

    bdry_ends = [0, -1]
    bdry_odds = np.array(range(1, len(s_2), 2), int)
    bdry_evns = np.array(range(2, len(s_2), 2), int)

    # Double the are under the curve, and subtract the double counted bit.
    bdry_area_simpson = 2 * _step_size * (
        (4 / 3) * np.sum(s_2.take(bdry_odds))
        + (2 / 3) * np.sum(s_2.take(bdry_evns))
        + (1 / 3) * np.sum(s_2.take(bdry_ends))
    ) - np.power(_s_mid, 2)

    return GuidelinesBoundary(bdry, round(float(bdry_area_simpson), dps))


def shrratio_boundary_min(
    _delta_star: float = 0.075,
    _r_val: float = DEFAULT_REC_RATIO,
    /,
    *,
    recapture_form: str = "inside-out",
    dps: int = 10,
) -> GuidelinesBoundary:
    """
    Share combinations on the minimum GUPPI boundary, with symmetric
    merging-firm margins.

    Notes
    -----
    With symmetric merging-firm margins, the maximum GUPPI boundary is
    defined by the diversion ratio from the smaller merging-firm to the
    larger one, and is hence unaffected by the method of estimating the
    diversion ratio for the larger firm.

    Parameters
    ----------
    _delta_star
        Share ratio (:math:`\\overline{d} / \\overline{r}`).
    _r_val
        Recapture ratio.
    recapture_form
        Whether recapture-ratio is MNL-consistent ("inside-out") or has fixed
        value for both merging firms ("proportional").
    dps
        Number of decimal places for rounding returned shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """

    _delta_star, _r_val = (mpf(f"{_v}") for _v in (_delta_star, _r_val))
    _s_intcpt = mpf("1.00")
    _s_mid = _delta_star / (1 + _delta_star)

    if recapture_form == "inside-out":
        # ## Plot envelope of GUPPI boundaries with rk_ = r_bar if sk_ = min(_s_1, s_2)
        # ## See (si_, sj_) in equation~(44), or thereabouts, in paper
        smin_nr = _delta_star * (1 - _r_val)
        smax_nr = 1 - _delta_star * _r_val
        dr = smin_nr + smax_nr
        s_1 = np.array((0, smin_nr / dr, _s_mid, smax_nr / dr, _s_intcpt), float)

        bdry_area = _s_mid + s_1[1] * (1 - 2 * _s_mid)
    else:
        s_1, bdry_area = np.array((0, _s_mid, _s_intcpt), float), _s_mid

    return GuidelinesBoundary(
        np.column_stack((s_1, s_1[::-1])), round(float(bdry_area), dps)
    )


def shrratio_boundary_max(
    _delta_star: float = 0.075, _: float = DEFAULT_REC_RATIO, /, *, dps: int = 10
) -> GuidelinesBoundary:
    """
    Share combinations on the minimum GUPPI boundary with symmetric
    merging-firm margins.

    Parameters
    ----------
    _delta_star
        Share ratio (:math:`\\overline{d} / \\overline{r}`).
    _
        Placeholder for recapture ratio included for consistency with other
        share-ratio boundary functions.
    dps
        Number of decimal places for rounding returned shares.

    Returns
    -------
        Array of share-pairs, area under boundary.

    """

    _delta_star = mpf(f"{_delta_star}")
    _s_intcpt = _delta_star
    _s_mid = _delta_star / (1 + _delta_star)
    _s1_pts = (0, _s_mid, _s_intcpt)

    return GuidelinesBoundary(
        np.column_stack((np.array(_s1_pts, float), np.array(_s1_pts[::-1], float))),
        round(float(_s_intcpt * _s_mid), dps),  # simplified calculation
    )


def _shrratio_boundary_intcpt(
    s_2_pre: float,
    _delta_star: MPFloat,
    _r_val: MPFloat,
    /,
    *,
    recapture_form: Literal["inside-out", "proportional"],
    agg_method: Literal["arithmetic mean", "geometric mean", "distance"],
    weighting: Literal["cross-product-share", "own-share", None],
) -> float:
    match weighting:
        case "cross-product-share":
            _s_intcpt: float = _delta_star
        case "own-share":
            _s_intcpt = mpf("1.0")
        case None if agg_method == "distance":
            _s_intcpt = _delta_star * mp.sqrt("2")
        case None if agg_method == "arithmetic mean" and recapture_form == "inside-out":
            _s_intcpt = mp.fdiv(
                mp.fsub(
                    2 * _delta_star * _r_val + 1, mp.fabs(2 * _delta_star * _r_val - 1)
                ),
                2 * mpf(f"{_r_val}"),
            )
        case None if (
            agg_method == "arithmetic mean" and recapture_form == "proportional"
        ):
            _s_intcpt = mp.fsub(_delta_star + 1 / 2, mp.fabs(_delta_star - 1 / 2))
        case _:
            _s_intcpt = s_2_pre

    return _s_intcpt


def lerp[LerpT: (float, MPFloat, ArrayDouble, ArrayBIGINT)](
    _x1: LerpT, _x2: LerpT, _r: float | MPFloat = 0.25, /
) -> LerpT:
    """
    From the function of the same name in the C++ standard [2]_

    Constructs the weighted average, :math:`w_1 x_1 + w_2 x_2`, where
    :math:`w_1 = 1 - r` and :math:`w_2 = r`.

    Parameters
    ----------
    _x1, _x2
        bounds :math:`x_1, x_2` to interpolate between.
    _r
        interpolation weight :math:`r` assigned to :math:`x_2`

    Returns
    -------
        The linear interpolation, or weighted average,
        :math:`x_1 + r \\cdot (x_1 - x_2) \\equiv (1 - r) \\cdot x_1 + r \\cdot x_2`.

    Raises
    ------
    ValueError
        If the interpolation weight is not in the interval, :math:`[0, 1]`.

    References
    ----------

    .. [2] C++ Reference, https://en.cppreference.com/w/cpp/numeric/lerp

    """

    if not 0 <= _r <= 1:
        raise ValueError("Specified interpolation weight must lie in [0, 1].")
    elif _r == 0:
        return _x1
    elif _r == 1:
        return _x2
    else:
        return _r * _x2 + (1 - _r) * _x1


def round_cust(
    _num: float | decimal.Decimal | MPFloat = 0.060215,
    /,
    *,
    frac: float = 0.005,
    rounding_mode: str = "ROUND_HALF_UP",
) -> float:
    """
    Custom rounding, to the nearest 0.5% by default.

    Parameters
    ----------
    _num
        Number to be rounded.
    frac
        Fraction to be rounded to.
    rounding_mode
        Rounding mode, as defined in the :code:`decimal` package.

    Returns
    -------
        The given number, rounded as specified.

    Raises
    ------
    ValueError
        If rounding mode is not defined in the :code:`decimal` package.

    Notes
    -----
    Integer-round the quotient, :code:`(_num / frac)` using the specified
    rounding mode. Return the product of the rounded quotient times
    the specified precision, :code:`frac`.

    """

    if rounding_mode not in {
        decimal.ROUND_05UP,
        decimal.ROUND_CEILING,
        decimal.ROUND_DOWN,
        decimal.ROUND_FLOOR,
        decimal.ROUND_HALF_DOWN,
        decimal.ROUND_HALF_EVEN,
        decimal.ROUND_HALF_UP,
        decimal.ROUND_UP,
    }:
        raise ValueError(
            f"Value, {f'"{rounding_mode}"'} is invalid for rounding_mode."
            'Documentation for the, "decimal" built-in lists valid rounding modes.'
        )

    n_, f_, e_ = (decimal.Decimal(f"{g_}") for g_ in [_num, frac, 1])

    return float(f_ * (n_ / f_).quantize(e_, rounding=rounding_mode))


def boundary_plot(*, mktshares_plot_flag: bool = True) -> tuple[Any, ...]:
    """Setup basic figure and axes for plots of safe harbor boundaries.

    See, https://matplotlib.org/stable/tutorials/text/pgf.html
    """

    mpl.use("pgf")

    plt.rcParams.update({
        "pgf.rcfonts": False,
        "pgf.texsystem": "lualatex",
        "pgf.preamble": "\n".join([
            R"\pdfvariable minorversion=7",
            R"\usepackage{fontspec}",
            R"\usepackage{luacode}",
            R"\begin{luacode}",
            R"local function embedfull(tfmdata)",
            R'    tfmdata.embedding = "full"',
            R"end",
            R"",
            R"luatexbase.add_to_callback("
            R'  "luaotfload.patch_font", embedfull, "embedfull"'
            R")",
            R"\end{luacode}",
            R"\usepackage{mathtools}",
            R"\usepackage{unicode-math}",
            R"\setmathfont[math-style=ISO]{STIX Two Math}",
            R"\setmainfont{STIX Two Text}",
            r"\setsansfont{Fira Sans Light}",
            R"\setmonofont[Scale=MatchLowercase,]{Fira Mono}",
            R"\defaultfontfeatures[\rmfamily]{",
            R"  Ligatures={TeX, Common},",
            R"  Numbers={Proportional, Lining},",
            R"  }",
            R"\defaultfontfeatures[\sffamily]{",
            R"  Ligatures={TeX, Common},",
            R"  Numbers={Monospaced, Lining},",
            R"  LetterSpace=0.50,",
            R"  }",
            R"\usepackage[",
            R"  activate={true, nocompatibility},",
            R"  tracking=true,",
            R"  ]{microtype}",
        ]),
    })

    # Initialize a canvas with a single figure (set of axes)
    fig_ = plt.figure(figsize=(5, 5), dpi=600)
    ax_out = fig_.add_subplot()

    def _set_axis_def(
        ax1_: mpa.Axes,
        /,
        *,
        mktshares_plot_flag: bool = False,
        mktshares_axlbls_flag: bool = False,
    ) -> mpa.Axes:
        # Set the width of axis grid lines, and tick marks:
        # both axes, both major and minor ticks
        # Frame, grid, and face color
        for _spos0 in "left", "bottom":
            ax1_.spines[_spos0].set_linewidth(0.5)
            ax1_.spines[_spos0].set_zorder(5)
        for _spos1 in "top", "right":
            ax1_.spines[_spos1].set_linewidth(0.0)
            ax1_.spines[_spos1].set_zorder(0)
            ax1_.spines[_spos1].set_visible(False)
        ax1_.set_facecolor("#E6E6E6")

        ax1_.grid(linewidth=0.5, linestyle=":", color="grey", zorder=1)
        ax1_.tick_params(axis="x", which="both", width=0.5)
        ax1_.tick_params(axis="y", which="both", width=0.5)

        # Tick marks skip, size, and rotation
        # x-axis
        plt.setp(
            ax1_.xaxis.get_majorticklabels(),
            horizontalalignment="right",
            fontsize=6,
            rotation=45,
        )
        # y-axis
        plt.setp(
            ax1_.yaxis.get_majorticklabels(), horizontalalignment="right", fontsize=6
        )

        if mktshares_plot_flag:
            # Axis labels
            if mktshares_axlbls_flag:
                # x-axis
                ax1_.set_xlabel("Firm 1 Market Share, $_s_1$", fontsize=10)
                ax1_.xaxis.set_label_coords(0.75, -0.1)
                # y-axis
                ax1_.set_ylabel("Firm 2 Market Share, $s_2$", fontsize=10)
                ax1_.yaxis.set_label_coords(-0.1, 0.75)

            # Plot the ray of symmetry
            ax1_.plot(
                [0, 1], [0, 1], linewidth=0.5, linestyle=":", color="grey", zorder=1
            )

            # Axis scale
            ax1_.set_xlim(0, 1)
            ax1_.set_ylim(0, 1)
            ax1_.set_aspect(1.0)

            # Truncate the axis frame to a triangle:
            ax1_.add_patch(
                mpp.Rectangle(
                    xy=(1.0025, 0.00),
                    width=1.1 * mp.sqrt(2),
                    height=1.1 * mp.sqrt(2),
                    angle=45,
                    color="white",
                    edgecolor=None,
                    fill=True,
                    clip_on=True,
                    zorder=5,
                )
            )
            # Feasible space is bounded by the other diagonal:
            ax1_.plot(
                [0, 1], [1, 0], linestyle="-", linewidth=0.5, color="black", zorder=1
            )

            # Axis Tick-mark locations
            # One can supply an argument to mpt.AutoMinorLocator to
            # specify a fixed number of minor intervals per major interval, e.g.:
            # minorLocator = mpt.AutoMinorLocator(2)
            # would lead to a single minor tick between major ticks.
            minor_locator = mpt.AutoMinorLocator(5)
            major_locator = mpt.MultipleLocator(0.05)
            for axs_ in ax1_.xaxis, ax1_.yaxis:
                if axs_ == ax1_.xaxis:
                    _majorticklabels_rot = 45
                elif axs_ == ax1_.yaxis:
                    _majorticklabels_rot = 0
                # x-axis
                axs_.set_major_locator(major_locator)
                axs_.set_minor_locator(minor_locator)
                # It"s always x when specifying the format
                axs_.set_major_formatter(mpt.StrMethodFormatter("{x:>3.0%}"))

            # Hide every other tick-label
            for axl_ in ax1_.get_xticklabels(), ax1_.get_yticklabels():
                plt.setp(axl_[::2], visible=False)

        return ax1_

    ax_out = _set_axis_def(ax_out, mktshares_plot_flag=mktshares_plot_flag)

    return plt, fig_, ax_out, _set_axis_def
