"""
Methods to compute intrinsic clearance rates and intrinsic enforcement rates
from generated market data.

"""

from collections.abc import Sequence
from typing import TypedDict

import numpy as np
from numpy.random import SeedSequence

from .. import (  # noqa
    VERSION,
    ArrayBIGINT,
    ArrayBoolean,
    ArrayDouble,
    ArrayFloat,
    ArrayINT,
    HMGPubYear,
    UPPAggrSelector,
)
from ..core import guidelines_boundaries as gbl  # noqa: TID252
from . import (
    INVResolution,
    MarketSampleData,
    UPPTestRegime,
    UPPTestsCounts,
    UPPTestsRaw,
)
from . import enforcement_stats as esl

__version__ = VERSION


class INVRESCntsArgs(TypedDict, total=False):
    "Keyword arguments of function, :code:`sim_enf_cnts`"

    sample_size: int
    seed_seq_list: Sequence[SeedSequence] | None
    nthreads: int


def compute_upp_test_counts(
    _market_data_sample: MarketSampleData,
    _upp_test_parms: gbl.HMGThresholds,
    _upp_test_regime: UPPTestRegime,
    /,
) -> UPPTestsCounts:
    """Estimate enforcement and clearance counts from market data sample

    Parameters
    ----------
    _market_data_sample
        Market data sample

    _upp_test_parms
        Threshold values for various Guidelines criteria

    _upp_test_regime
        Specifies whether to analyze enforcement, clearance, or both
        and the GUPPI and diversion ratio aggregators employed, with
        default being to analyze enforcement based on the maximum
        merging-firm GUPPI and maximum diversion ratio between the
        merging firms

    Returns
    -------
    UPPTestsCounts
        Enforced and cleared counts

    """

    upp_test_arrays = compute_upp_test_arrays(
        _market_data_sample, _upp_test_parms, _upp_test_regime
    )

    fcounts, hhi_delta, hhi_post = (
        getattr(_market_data_sample, _g) for _g in ("fcounts", "hhi_delta", "hhi_post")
    )

    stats_rowlen = 6
    # Clearance/enforcement counts --- by firm count
    enf_cnts_sim_byfirmcount_array: ArrayBIGINT = np.zeros(stats_rowlen, int)
    firmcounts_list = np.unique(fcounts)
    if firmcounts_list.any():
        for _fc in firmcounts_list:
            fc_test = fcounts == _fc

            enf_cnts_sim_byfirmcount_array = np.vstack((
                enf_cnts_sim_byfirmcount_array,
                np.array([
                    _fc,
                    np.einsum("ij->", 1 * fc_test),
                    *[
                        np.einsum(
                            "ij->", 1 * (fc_test & getattr(upp_test_arrays, _a.name))
                        )
                        for _a in upp_test_arrays.__attrs_attrs__
                    ],
                ]),
            ))

        enf_cnts_sim_byfirmcount_array = enf_cnts_sim_byfirmcount_array[1:]
    else:
        enf_cnts_sim_byfirmcount_array = np.array([], int)

    # Clearance/enforcement counts --- by delta
    enf_cnts_sim_bydelta_array: ArrayBIGINT = np.zeros(stats_rowlen, int)
    hhi_deltaranged = esl.hhi_delta_ranger(hhi_delta)
    for hhi_deltalim in esl.HHI_DELTA_KNOTS[:-1]:
        hhi_deltatest = hhi_deltaranged == hhi_deltalim

        enf_cnts_sim_bydelta_array = np.vstack((
            enf_cnts_sim_bydelta_array,
            np.array([
                hhi_deltalim,
                np.einsum("ij->", 1 * hhi_deltatest),
                *[
                    np.einsum(
                        "ij->", 1 * (hhi_deltatest & getattr(upp_test_arrays, _a.name))
                    )
                    for _a in upp_test_arrays.__attrs_attrs__
                ],
            ]),
        ))

    enf_cnts_sim_bydelta_array = enf_cnts_sim_bydelta_array[1:]

    # Clearance/enforcement counts --- by zone
    if np.isnan(hhi_post).all():
        stats_byconczone_sim = np.array([], int)
    else:
        try:
            hhi_zone_post_ranged = esl.hhi_zone_post_ranger(hhi_post)
        except ValueError as _err:
            print(hhi_post)
            raise _err

        stats_byconczone_sim = np.zeros(stats_rowlen + 1, int)
        for hhi_zone_post_knot in esl.HHI_POST_ZONE_KNOTS[:-1]:
            level_test = hhi_zone_post_ranged == hhi_zone_post_knot

            for hhi_zone_delta_knot in [0, 100, 200]:
                delta_test = (
                    hhi_deltaranged > 100
                    if hhi_zone_delta_knot == 200
                    else hhi_deltaranged == hhi_zone_delta_knot
                )

                conc_test = level_test & delta_test

                stats_byconczone_sim = np.vstack((
                    stats_byconczone_sim,
                    np.array([
                        hhi_zone_post_knot,
                        hhi_zone_delta_knot,
                        np.einsum("ij->", 1 * conc_test),
                        *[
                            np.einsum(
                                "ij->",
                                1 * (conc_test & getattr(upp_test_arrays, _a.name)),
                            )
                            for _a in upp_test_arrays.__attrs_attrs__
                        ],
                    ]),
                ))

    enf_cnts_sim_byconczone_array = esl.enf_cnts_byconczone(stats_byconczone_sim[1:])

    del stats_byconczone_sim
    del hhi_delta, hhi_post, fcounts

    return UPPTestsCounts(
        enf_cnts_sim_byfirmcount_array,
        enf_cnts_sim_bydelta_array,
        enf_cnts_sim_byconczone_array,
    )


def compute_upp_test_arrays(
    _market_data_sample: MarketSampleData,
    _upp_test_parms: gbl.HMGThresholds,
    _sim_test_regime: UPPTestRegime,
    /,
) -> UPPTestsRaw:
    """
    Generate UPP tests arrays for given configuration and market sample

    Given a standards vector, market

    Parameters
    ----------
    _market_data_sample
        market data sample
    _upp_test_parms
        guidelines thresholds for testing UPP and related statistics
    _sim_test_regime
        configuration to use for generating UPP tests

    """
    g_bar_, divr_bar_, cmcr_bar_, ipr_bar_ = (
        getattr(_upp_test_parms, _f) for _f in ("guppi", "divr", "cmcr", "ipr")
    )

    guppi_array, ipr_array, cmcr_array = (
        np.empty_like(_market_data_sample.price_array) for _ in range(3)
    )

    np.einsum(
        "ij,ij,ij->ij",
        _market_data_sample.divr_array,
        _market_data_sample.pcm_array[:, ::-1],
        _market_data_sample.price_array[:, ::-1] / _market_data_sample.price_array,
        out=guppi_array,
    )

    np.divide(
        np.einsum(
            "ij,ij->ij", _market_data_sample.pcm_array, _market_data_sample.divr_array
        ),
        1 - _market_data_sample.divr_array,
        out=ipr_array,
    )

    np.divide(ipr_array, 1 - _market_data_sample.pcm_array, out=cmcr_array)

    (divr_test_vector,) = _compute_test_array_seq(
        (_market_data_sample.divr_array,),
        _market_data_sample.frmshr_array,
        _sim_test_regime.divr_aggregator,
    )

    (guppi_test_vector, cmcr_test_vector, ipr_test_vector) = _compute_test_array_seq(
        (guppi_array, cmcr_array, ipr_array),
        _market_data_sample.frmshr_array,
        _sim_test_regime.guppi_aggregator,
    )
    del cmcr_array, ipr_array, guppi_array

    if _sim_test_regime.resolution == INVResolution.ENFT:
        upp_test_arrays = UPPTestsRaw(
            guppi_test_vector >= g_bar_,
            (guppi_test_vector >= g_bar_) | (divr_test_vector >= divr_bar_),
            cmcr_test_vector >= cmcr_bar_,
            ipr_test_vector >= ipr_bar_,
        )
    else:
        upp_test_arrays = UPPTestsRaw(
            guppi_test_vector < g_bar_,
            (guppi_test_vector < g_bar_) & (divr_test_vector < divr_bar_),
            cmcr_test_vector < cmcr_bar_,
            ipr_test_vector < ipr_bar_,
        )

    return upp_test_arrays


def _compute_test_array_seq(
    _test_measure_seq: tuple[ArrayDouble, ...],
    _wt_array: ArrayDouble,
    _aggregator: UPPAggrSelector,
) -> tuple[ArrayDouble, ...]:
    _wt_array = (
        _wt_array / np.einsum("ij->i", _wt_array)[:, None]
        if _aggregator
        in {
            UPPAggrSelector.CPA,
            UPPAggrSelector.CPD,
            UPPAggrSelector.OSA,
            UPPAggrSelector.OSD,
        }
        else np.array([0.5, 0.5], float)
    )

    match _aggregator:
        case UPPAggrSelector.AVG:
            test_array_seq = (
                1 / 2 * np.einsum("ij->i", _g)[:, None] for _g in _test_measure_seq
            )
        case UPPAggrSelector.CPA:
            test_array_seq = (
                np.einsum("ij,ij->i", _wt_array[:, ::-1], _g)[:, None]
                for _g in _test_measure_seq
            )
        case UPPAggrSelector.CPD:
            test_array_seq = (
                np.sqrt(np.einsum("ij,ij,ij->i", _wt_array[:, ::-1], _g, _g))[:, None]
                for _g in _test_measure_seq
            )
        case UPPAggrSelector.DIS:
            test_array_seq = (
                np.sqrt(1 / 2 * np.einsum("ij,ij->i", _g, _g))[:, None]
                for _g in _test_measure_seq
            )
        case UPPAggrSelector.MAX:
            test_array_seq = (_g.max(axis=1, keepdims=True) for _g in _test_measure_seq)
        case UPPAggrSelector.MIN:
            test_array_seq = (_g.min(axis=1, keepdims=True) for _g in _test_measure_seq)
        case UPPAggrSelector.OSA:
            test_array_seq = (
                np.einsum("ij,ij->i", _wt_array, _g)[:, None]
                for _g in _test_measure_seq
            )
        case UPPAggrSelector.OSD:
            test_array_seq = (
                np.sqrt(np.einsum("ij,ij,ij->i", _wt_array, _g, _g))[:, None]
                for _g in _test_measure_seq
            )
        case _:
            raise ValueError("GUPPI/diversion ratio aggregation method is invalid.")
    return tuple(test_array_seq)


if __name__ == "__main__":
    print(
        "This module defines classes with methods for generating UPP test arrays and UPP test-counts arrays on given data."
    )
