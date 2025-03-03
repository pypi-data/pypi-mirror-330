"""
Non-public functions called in data_generation.py
"""

from __future__ import annotations

from typing import Literal

import numpy as np
from attrs import evolve
from numpy.random import SeedSequence

from .. import (  # noqa: TID252
    DEFAULT_REC_RATIO,
    NTHREADS,
    VERSION,
    ArrayDouble,
    ArrayFloat,
    RECForm,
)
from ..core.empirical_margin_distribution import margin_data_resampler  # noqa: TID252
from ..core.pseudorandom_numbers import (  # noqa: TID252
    DEFAULT_BETA_DIST_PARMS,
    DEFAULT_DIST_PARMS,
    MultithreadedRNG,
    prng,
)
from . import (
    DEFAULT_BETA_BND_DIST_PARMS,
    DEFAULT_FCOUNT_WTS,
    FM2Constraint,
    MarginDataSample,
    PCMDistribution,
    PCMSpec,
    PriceDataSample,
    PriceSpec,
    ShareDataSample,
    ShareSpec,
    SHRDistribution,
    SSZConstant,
)

__version__ = VERSION


def gen_share_data(
    _sample_size: int,
    _share_spec: ShareSpec,
    _fcount_rng_seed_seq: SeedSequence | None,
    _mktshr_rng_seed_seq: SeedSequence,
    _nthreads: int,
    /,
) -> ShareDataSample:
    """Helper function for generating share data.

    Parameters
    ----------
    _share_spec
        Class specifying parameters for generating market share data
    _fcount_rng_seed_seq
        Seed sequence for assuring independent and, optionally, redundant streams
    _mktshr_rng_seed_seq
        Seed sequence for assuring independent and, optionally, redundant streams
    _nthreads
        Must be specified for generating repeatable random streams

    Returns
    -------
        Arrays representing shares, diversion ratios, etc. structured as a :ShareDataSample:

    """

    dist_type_mktshr, firm_count_prob_wts, dist_parms_mktshr, recapture_form = (
        getattr(_share_spec, _f)
        for _f in ("dist_type", "firm_counts_weights", "dist_parms", "recapture_form")
    )

    if dist_type_mktshr == SHRDistribution.UNI:
        mkt_share_sample = gen_market_shares_uniform(
            _sample_size, dist_parms_mktshr, _mktshr_rng_seed_seq, _nthreads
        )

    elif dist_type_mktshr.name.startswith("DIR_"):
        mkt_share_sample = _gen_market_shares_dirichlet_multimarket(
            _sample_size,
            recapture_form,
            dist_type_mktshr,
            dist_parms_mktshr,
            firm_count_prob_wts,
            _fcount_rng_seed_seq,
            _mktshr_rng_seed_seq,
            _nthreads,
        )

    else:
        raise ValueError(
            f'Unexpected type, "{dist_type_mktshr}" for share distribution.'
        )

    # If recapture_form == "inside-out", recalculate _aggregate_purchase_prob
    frmshr_array = mkt_share_sample.mktshr_array[:, :2]
    r_bar_ = _share_spec.recapture_ratio or DEFAULT_REC_RATIO
    if recapture_form == RECForm.INOUT:
        mkt_share_sample = ShareDataSample(
            mkt_share_sample.mktshr_array,
            mkt_share_sample.fcounts,
            mkt_share_sample.nth_firm_share,
            r_bar_ / (1 - (1 - r_bar_) * frmshr_array.min(axis=1, keepdims=True)),
        )

    return mkt_share_sample


def gen_market_shares_uniform(
    _s_size: int,
    _dist_parms_mktshr: ArrayDouble,
    _mktshr_rng_seed_seq: SeedSequence,
    _nthreads: int,
    /,
) -> ShareDataSample:
    """Generate merging-firm shares from Uniform distribution on the 3-D simplex.

    Parameters
    ----------
    _s_size
        size of sample to be drawn

    _mktshr_rng_seed_seq
        seed for rng, so results can be made replicable

    _nthreads
        number of threads for random number generation

    Returns
    -------
        market shares and other market statistics for each draw (market)

    """

    frmshr_array: ArrayDouble = np.empty((_s_size, 2), float)

    MultithreadedRNG(
        frmshr_array,
        dist_type="Uniform",
        dist_parms=_dist_parms_mktshr,
        seed_sequence=_mktshr_rng_seed_seq,
        nthreads=_nthreads,
    ).fill()

    # Convert draws on U[0, 1] to Uniformly-distributed draws on simplex, s_1 + s_2 <= 1
    frmshr_array = np.hstack((
        frmshr_array.min(axis=1, keepdims=True),
        np.abs(np.diff(frmshr_array, axis=1)),
    ))

    # Keep only share combinations representing feasible mergers
    # This is a no-op for 64-bit floats, but is necessary for smaller floats
    frmshr_array = frmshr_array[frmshr_array.min(axis=1) > 0]

    # Let a third column have values of "np.nan", so HHI calculations return "np.nan"
    mktshr_array_ = np.pad(
        frmshr_array, ((0, 0), (0, 1)), "constant", constant_values=np.nan
    )

    fcounts_, nth_firm_share_, aggregate_purchase_prob_ = (
        np.empty((_s_size, 1), type_) for type_ in (np.uint8, np.float64, np.float64)
    )

    fcounts_.fill(0)
    nth_firm_share_.fill(np.nan)
    aggregate_purchase_prob_.fill(np.nan)

    return ShareDataSample(
        mktshr_array_, fcounts_, nth_firm_share_, aggregate_purchase_prob_
    )


def _gen_market_shares_dirichlet_multimarket(
    _s_size: int,
    _recapture_form: RECForm,
    _dist_type_dir: SHRDistribution,
    _dist_parms_dir: ArrayDouble,
    _firm_count_wts: ArrayDouble,
    _fcount_rng_seed_seq: SeedSequence | None,
    _mktshr_rng_seed_seq: SeedSequence,
    _nthreads: int = NTHREADS,
    /,
) -> ShareDataSample:
    """Dirichlet-distributed shares with multiple firm-counts.

    Firm-counts may be specified as having Uniform distribution over the range
    of firm counts, or a set of probability weights may be specified. In the
    latter case the proportion of draws for each firm-count matches the
    specified probability weight.

    Parameters
    ----------
    _s_size
        sample size to be drawn

    _firm_count_wts
        firm count weights array for sample to be drawn

    _dist_type_dir
        Whether Dirichlet is Flat or Asymmetric

    _recapture_form
        r_1 = r_2 if "proportional", otherwise MNL-consistent

    _fcount_rng_seed_seq
        seed firm count rng, for replicable results

    _mktshr_rng_seed_seq
        seed market share rng, for replicable results

    _nthreads
        number of threads for parallelized random number generation

    Returns
    -------
        array of market shares and other market statistics

    """

    _firm_count_wts = (
        DEFAULT_FCOUNT_WTS
        if _firm_count_wts is None or not len(_firm_count_wts)
        else _firm_count_wts
    )

    min_choice_wt = 0.03 if _dist_type_dir == SHRDistribution.DIR_FLAT_CONSTR else 0.00
    fcount_keys, choice_wts = zip(
        *(
            f_
            for f_ in zip(
                2 + np.arange(len(_firm_count_wts), dtype=np.uint8),
                _firm_count_wts / _firm_count_wts.sum(),
                strict=True,
            )
            if f_[1] > min_choice_wt
        )
    )
    choice_wts /= sum(choice_wts)

    fc_max = fcount_keys[-1]
    dir_alphas_full = (
        _dist_parms_dir[:fc_max] if len(_dist_parms_dir) else [1.0] * fc_max
    )
    if _dist_type_dir == SHRDistribution.DIR_ASYM:
        dir_alphas_full = [2.0] * 6 + [1.5] * 5 + [1.25] * min(7, fc_max)

    if _dist_type_dir == SHRDistribution.DIR_COND:

        def _gen_dir_alphas(_fcv: int) -> ArrayDouble:
            dat_ = [2.5] * 2
            if _fcv > len(dat_):
                dat_ += [1.0 / (_fcv - 2)] * (_fcv - 2)
            return np.array(dat_, float)

    else:

        def _gen_dir_alphas(_fcv: int) -> ArrayDouble:
            return np.array(dir_alphas_full[:_fcv], float)

    fcounts_ = prng(_fcount_rng_seed_seq).choice(
        fcount_keys, size=(_s_size, 1), p=choice_wts
    )

    mktshr_seed_seq_ch = _mktshr_rng_seed_seq.spawn(len(fcount_keys))

    aggregate_purchase_prob_, nth_firm_share_ = (
        np.empty((_s_size, 1)) for _ in range(2)
    )
    mktshr_array_ = np.empty((_s_size, fc_max), float)
    for f_val, f_sseq in zip(fcount_keys, mktshr_seed_seq_ch, strict=True):
        fcounts_match_rows = np.where(fcounts_ == f_val)[0]
        dir_alphas_test = _gen_dir_alphas(f_val)

        try:
            mktshr_sample_f = gen_market_shares_dirichlet(
                dir_alphas_test,
                len(fcounts_match_rows),
                _recapture_form,
                f_sseq,
                _nthreads,
            )
        except ValueError as err_:
            print(f_val, len(fcounts_match_rows))
            raise err_

        # Push data for present sample to parent
        mktshr_array_[fcounts_match_rows] = np.pad(
            mktshr_sample_f.mktshr_array,
            ((0, 0), (0, fc_max - mktshr_sample_f.mktshr_array.shape[1])),
            "constant",
        )
        aggregate_purchase_prob_[fcounts_match_rows] = (
            mktshr_sample_f.aggregate_purchase_prob
        )
        nth_firm_share_[fcounts_match_rows] = mktshr_sample_f.nth_firm_share

    if (iss_ := np.round(np.einsum("ij->", mktshr_array_))) != _s_size or iss_ != len(
        mktshr_array_
    ):
        raise ValueError(
            "DATA GENERATION ERROR: {} {} {}".format(
                "Generation of sample shares is inconsistent:",
                "array of drawn shares must some to the number of draws",
                "i.e., the sample size, which condition is not met.",
            )
        )

    return ShareDataSample(
        mktshr_array_, fcounts_, nth_firm_share_, aggregate_purchase_prob_
    )


def gen_market_shares_dirichlet(
    _dir_alphas: ArrayDouble,
    _s_size: int,
    _recapture_form: RECForm,
    _mktshr_rng_seed_seq: SeedSequence,
    _nthreads: int,
    /,
) -> ShareDataSample:
    """Dirichlet-distributed shares with fixed firm-count.

    Parameters
    ----------
    _dir_alphas
        Shape parameters for Dirichlet distribution

    _s_size
        sample size to be drawn

    _recapture_form
        r_1 = r_2 if RECForm.FIXED, otherwise MNL-consistent. If
        RECForm.OUTIN; the number of columns in the output share array
        is len(_dir_alphas) - 1.

    _mktshr_rng_seed_seq
        seed market share rng, for replicable results

    _nthreads
        number of threads for parallelized random number generation

    Returns
    -------
        array of market shares and other market statistics

    """

    if not isinstance(_dir_alphas, np.ndarray):
        _dir_alphas = np.array(_dir_alphas)

    if _recapture_form == RECForm.OUTIN:
        _dir_alphas = np.concatenate((_dir_alphas, _dir_alphas[-1:]))

    mktshr_array = np.empty((_s_size, len(_dir_alphas)), float)
    MultithreadedRNG(
        mktshr_array,
        dist_type="Dirichlet",
        dist_parms=_dir_alphas,
        seed_sequence=_mktshr_rng_seed_seq,
        nthreads=_nthreads,
    ).fill()
    # mrng_ = MultithreadedRNG(
    #     mktshr_array,
    #     dist_type="Dirichlet",
    #     dist_parms=_dir_alphas,
    #     seed_sequence=_mktshr_rng_seed_seq,
    #     nthreads=_nthreads,
    # )
    # mrng_.fill()
    # del mrng_

    if (iss_ := np.round(np.einsum("ij->", mktshr_array))) != _s_size or iss_ != len(
        mktshr_array
    ):
        print(_dir_alphas, iss_, repr(_s_size), len(mktshr_array))
        print(repr(mktshr_array[-10:, :]))
        raise ValueError(
            "DATA GENERATION ERROR: {} {} {}".format(
                "Generation of sample shares is inconsistent:",
                "array of drawn shares must sum to the number of draws",
                "i.e., the sample size, which condition is not met.",
            )
        )

    # If recapture_form == 'inside_out', further calculations downstream
    aggregate_purchase_prob_ = np.empty((_s_size, 1), float)
    aggregate_purchase_prob_.fill(np.nan)
    if _recapture_form == RECForm.OUTIN:
        aggregate_purchase_prob_ = 1 - mktshr_array[:, [-1]]  # type: ignore
        mktshr_array = mktshr_array[:, :-1] / aggregate_purchase_prob_

    return ShareDataSample(
        mktshr_array,
        (mktshr_array.shape[-1] * np.ones((_s_size, 1))).astype(np.int64),
        mktshr_array[:, [-1]],
        aggregate_purchase_prob_,
    )


def gen_divr_array(
    _recapture_form: RECForm,
    _recapture_ratio: float | None,
    _frmshr_array: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble,
    /,
) -> ArrayDouble:
    """
    Given merging-firm shares and related parameters, return diverion ratios.

    If recapture is specified as :attr:`mergeron.RECForm.OUTIN`, then the
    choice-probability for the outside good must be supplied.

    Parameters
    ----------
    _recapture_form
        Enum specifying Fixed (proportional), Inside-out, or Outside-in

    _recapture_ratio
        If recapture is proportional or inside-out, the recapture ratio
        for the firm with the smaller share.

    _frmshr_array
        Merging-firm shares.

    _aggregate_purchase_prob
        1 minus probability that the outside good is chosen; converts
        market shares to choice probabilities by multiplication.

    Raises
    ------
    ValueError
        If the firm with the smaller share does not have the larger
        diversion ratio between the merging firms.

    Returns
    -------
        Merging-firm diversion ratios for mergers in the sample.

    """

    divr_array: ArrayDouble
    if _recapture_form == RECForm.FIXED:
        divr_array = _recapture_ratio * _frmshr_array[:, ::-1] / (1 - _frmshr_array)  # type: ignore

    else:
        purchprob_array = _aggregate_purchase_prob * _frmshr_array
        divr_array = purchprob_array[:, ::-1] / (1 - purchprob_array)

    divr_assert_test = (
        (np.round(np.einsum("ij->i", _frmshr_array), 15) == 1)
        | (np.argmin(_frmshr_array, axis=1) == np.argmax(divr_array, axis=1))
    )[:, None]
    if not all(divr_assert_test):
        raise ValueError(
            "{} {} {} {}".format(
                "Data construction fails tests:",
                "the index of min(s_1, s_2) must equal",
                "the index of max(d_12, d_21), for all draws.",
                "unless frmshr_array sums to 1.00.",
            )
        )

    return divr_array


def gen_margin_price_data(  # noqa: PLR0914
    _frmshr_array: ArrayDouble,
    _nth_firm_share: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble,
    _pcm_spec: PCMSpec,
    _price_spec: PriceSpec,
    _hsr_filing_test_type: SSZConstant,
    _pcm_rng_seed_seq: SeedSequence,
    _pr_rng_seed_seq: SeedSequence | None,
    _nthreads: int,
    /,
) -> tuple[MarginDataSample, PriceDataSample]:
    """Generate margin and price data for mergers in the sample.

    Parameters
    ----------
    _frmshr_array
        Merging-firm shares; see :class:`mergeron.gen.ShareSpec`.

    _nth_firm_share
        Share of the nth firm in the sample.

    _aggregate_purchase_prob
        1 minus probability that the outside good is chosen; converts
        market shares to choice probabilities by multiplication.

    _pcm_spec
        Enum specifying whether to use asymmetric or flat margins. see
        :class:`mergeron.gen.PCMSpec`.

    _price_spec
        Enum specifying whether to use symmetric, positive, or negative
        margins; see :class:`mergeron.gen.PriceSpec`.

    _hsr_filing_test_type
        Enum specifying restriction, if any, to impose on market data sample
        to model HSR filing requirements; see :class:`mergeron.gen.SSZConstant`.

    _pcm_rng_seed_seq
        Seed sequence for generating margin data.

    _pr_rng_seed_seq
        Seed sequence for generating price data.

    _nthreads
        Number of threads to use in generating price data.

    Returns
    -------
        Simulated margin- and price-data arrays for mergers in the sample.
    """

    margin_data = MarginDataSample(
        np.empty_like(_frmshr_array), np.ones(len(_frmshr_array)) == 0
    )

    nth_firm_price: ArrayDouble
    price_array: ArrayDouble = np.ones_like(_frmshr_array, np.float64)

    pr_max_ratio = 5.0
    match _price_spec:
        case PriceSpec.SYM:
            nth_firm_price = np.ones((len(_frmshr_array), 1), np.float64)
        case PriceSpec.POS:
            price_array, nth_firm_price = (
                np.ceil(_p * pr_max_ratio) for _p in (_frmshr_array, _nth_firm_share)
            )
        case PriceSpec.NEG:
            price_array, nth_firm_price = (
                np.ceil((1 - _p) * pr_max_ratio)
                for _p in (_frmshr_array, _nth_firm_share)
            )
        case PriceSpec.RNG:
            price_array_gen = prng(_pr_rng_seed_seq).choice(
                1 + np.arange(pr_max_ratio), size=(len(_frmshr_array), 3)
            )
            price_array = price_array_gen[:, :2]
            nth_firm_price = price_array_gen[:, [2]]
            # del _price_array_gen
        case PriceSpec.CSY:
            # TODO:
            # evolve FM2Constraint (save running MNL test twice); evolve copy of _mkt_sample_spec=1q
            # generate the margin data
            # generate price and margin data
            frmshr_array_plus = np.hstack((_frmshr_array, _nth_firm_share))
            pcm_spec_here = evolve(_pcm_spec, firm2_pcm_constraint=FM2Constraint.IID)
            margin_data = _gen_margin_data(
                frmshr_array_plus,
                np.ones_like(frmshr_array_plus, np.float64),
                _aggregate_purchase_prob,
                pcm_spec_here,
                _pcm_rng_seed_seq,
                _nthreads,
            )

            pcm_array, mnl_test_array = (
                getattr(margin_data, _f) for _f in ("pcm_array", "mnl_test_array")
            )

            price_array_here = 1 / (1 - pcm_array)
            price_array = price_array_here[:, :2]
            nth_firm_price = price_array_here[:, [-1]]
            if _pcm_spec.firm2_pcm_constraint == FM2Constraint.MNL:
                # Generate i.i.d. PCMs then take PCM0 and construct PCM1
                # Regenerate MNL test
                purchase_prob_array = _aggregate_purchase_prob * _frmshr_array
                pcm_array[:, 1] = np.divide(
                    (
                        m1_nr := np.divide(
                            np.einsum(
                                "ij,ij,ij->ij",
                                price_array[:, [0]],
                                pcm_array[:, [0]],
                                1 - purchase_prob_array[:, [0]],
                            ),
                            1 - purchase_prob_array[:, [1]],
                        )
                    ),
                    1 + m1_nr,
                )
                mnl_test_array = (pcm_array[:, [1]] >= 0) & (pcm_array[:, [1]] <= 1)

            margin_data = MarginDataSample(pcm_array[:, :2], mnl_test_array)
            del price_array_here
        case _:
            raise ValueError(
                f'Specification of price distribution, "{_price_spec.value}" is invalid.'
            )
    if _price_spec != PriceSpec.CSY:
        margin_data = _gen_margin_data(
            _frmshr_array,
            price_array,
            _aggregate_purchase_prob,
            _pcm_spec,
            _pcm_rng_seed_seq,
            _nthreads,
        )

    # _price_array = _price_array.astype(np.float64)
    rev_array = price_array * _frmshr_array
    nth_firm_rev = nth_firm_price * _nth_firm_share

    # Although `_test_rev_ratio_inv` is not fixed at 10%,
    # the ratio has not changed since inception of the HSR filing test,
    # so we treat it as a constant of merger enforcement policy.
    test_rev_ratio, test_rev_ratio_inv = 10, 1 / 10

    match _hsr_filing_test_type:
        case SSZConstant.HSR_TEN:
            # See, https://www.ftc.gov/enforcement/premerger-notification-program/
            #   -> Procedures For Submitting Post-Consummation Filings
            #    -> Key Elements to Determine Whether a Post Consummation Filing is Required
            #           under heading, "Historical Thresholds"
            # Revenue ratio has been 10-to-1 since inception
            # Thus, a simple form of the HSR filing test would impose a 10-to-1
            # ratio restriction on the merging firms' revenues
            rev_ratio = (rev_array.min(axis=1) / rev_array.max(axis=1)).round(4)
            hsr_filing_test = rev_ratio >= test_rev_ratio_inv
            # del _rev_array, _rev_ratio
        case SSZConstant.HSR_NTH:
            # To get around the 10-to-1 ratio restriction, specify that the nth firm test:
            # if the smaller merging firm matches or exceeds the n-th firm in size, and
            # the larger merging firm has at least 10 times the size of the nth firm,
            # the size test is considered met.
            # Alternatively, if the smaller merging firm has 10% or greater share,
            # the value of transaction test is considered met.
            rev_ratio_to_nth = np.round(np.sort(rev_array, axis=1) / nth_firm_rev, 4)
            hsr_filing_test = (
                np.einsum(
                    "ij->i",
                    1 * (rev_ratio_to_nth > [1, test_rev_ratio]),
                    dtype=np.int64,
                )
                == rev_ratio_to_nth.shape[1]
            )

            # del _nth_firm_rev, _rev_ratio_to_nth
        case _:
            # Otherwise, all draws meet the filing test
            hsr_filing_test = np.ones(len(_frmshr_array), dtype=bool)

    # Assume that if minimum mergeing-firm share is 10%, merger filing required
    # under value-of-transactions test or merger triggers post-consummation review
    hsr_filing_test |= _frmshr_array.min(axis=1) >= test_rev_ratio_inv

    return margin_data, PriceDataSample(price_array, hsr_filing_test)


def _gen_margin_data(
    _frmshr_array: ArrayDouble,
    _price_array: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble,
    _pcm_spec: PCMSpec,
    _pcm_rng_seed_seq: SeedSequence,
    _nthreads: int,
    /,
) -> MarginDataSample:
    dist_type_pcm, dist_parms_pcm, dist_firm2_pcm = (
        getattr(_pcm_spec, _f)
        for _f in ("dist_type", "dist_parms", "firm2_pcm_constraint")
    )

    pcm_array = (
        np.empty((len(_frmshr_array), 1), float)
        if _pcm_spec.firm2_pcm_constraint == FM2Constraint.SYM
        else np.empty_like(_frmshr_array, float)
    )

    dist_parms_: ArrayFloat
    beta_min, beta_max = [0.0] * 2  # placeholder
    if dist_type_pcm == PCMDistribution.EMPR:
        pcm_array = margin_data_resampler(
            pcm_array.shape, seed_sequence=_pcm_rng_seed_seq
        )
    else:
        dist_type_: Literal["Beta", "Uniform"]
        if dist_type_pcm in {PCMDistribution.BETA, PCMDistribution.BETA_BND}:
            dist_type_ = "Beta"
            if dist_type_pcm == PCMDistribution.BETA_BND:
                dist_parms_pcm = (
                    DEFAULT_BETA_BND_DIST_PARMS
                    if dist_parms_pcm is None  # Eliminated by converter
                    else dist_parms_pcm
                )
                dist_parms_ = beta_located_bound(dist_parms_pcm)
            else:
                dist_parms_ = (
                    DEFAULT_BETA_DIST_PARMS
                    if dist_parms_pcm is None
                    else dist_parms_pcm
                )

        else:
            dist_type_ = "Uniform"
            dist_parms_ = (
                DEFAULT_DIST_PARMS
                if dist_parms_pcm is None or not len(dist_parms_pcm)
                else dist_parms_pcm
            )

        MultithreadedRNG(
            pcm_array,
            dist_type=dist_type_,
            dist_parms=dist_parms_,
            seed_sequence=_pcm_rng_seed_seq,
            nthreads=_nthreads,
        ).fill()

    if dist_type_pcm == PCMDistribution.BETA_BND:
        beta_min, beta_max = dist_parms_pcm[2:]
        pcm_array = (beta_max - beta_min) * pcm_array + beta_min
        del beta_min, beta_max

    if dist_firm2_pcm == FM2Constraint.SYM:
        pcm_array = np.column_stack((pcm_array,) * _frmshr_array.shape[1])
    if dist_firm2_pcm == FM2Constraint.MNL:
        # Impose FOCs from profit-maximization with MNL demand
        if dist_type_pcm == PCMDistribution.EMPR:
            print(
                "NOTE: Estimated Firm 2 parameters will not be consistent with "
                "the empirical distribution of margins in the source data. For "
                "consistency, respecify pcm_spec.firm2_pcm_constraint = FM2Constraint.IID."
            )
        purchase_prob_array = _aggregate_purchase_prob * _frmshr_array

        pcm_array[:, [1]] = np.divide(
            np.einsum(
                "ij,ij,ij->ij",
                _price_array[:, [0]],
                pcm_array[:, [0]],
                1 - purchase_prob_array[:, [0]],
            ),
            np.einsum(
                "ij,ij->ij", _price_array[:, [1]], 1 - purchase_prob_array[:, [1]]
            ),
        )

        mnl_test_array = (pcm_array[:, 1] >= 0) & (pcm_array[:, 1] <= 1)
    else:
        mnl_test_array = np.ones(len(pcm_array), dtype=bool)

    return MarginDataSample(pcm_array, mnl_test_array)


def _beta_located(
    _mu: float | ArrayDouble, _sigma: float | ArrayDouble, /
) -> ArrayDouble:
    """
    Given mean and stddev, return shape parameters for corresponding Beta distribution

    Solve the first two moments of the standard Beta to get the shape parameters.

    Parameters
    ----------
    _mu
        mean
    _sigma
        standardd deviation

    Returns
    -------
        shape parameters for Beta distribution

    """

    mul = -1 + _mu * (1 - _mu) / _sigma**2
    return np.array([_mu * mul, (1 - _mu) * mul], float)


def beta_located_bound(_dist_parms: ArrayDouble, /) -> ArrayDouble:
    R"""
    Return shape parameters for a non-standard beta, given the mean, stddev, range


    Recover the r.v.s as
    :math:`\min + (\max - \min) \cdot \symup{Β}(a, b)`,
    with `a` and `b` calculated from the specified mean (:math:`\mu`) and
    variance (:math:`\sigma`). [8]_

    Parameters
    ----------
    _dist_parms
        vector of :math:`\mu`, :math:`\sigma`, :math:`\mathtt{\min}`, and :math:`\mathtt{\max}` values

    Returns
    -------
        shape parameters for Beta distribution

    Notes
    -----
    For example, ``beta_located_bound(np.array([0.5, 0.2887, 0.0, 1.0]))``.

    References
    ----------
    .. [8] NIST, Beta Distribution. https://www.itl.nist.gov/div898/handbook/eda/section3/eda366h.htm
    """  # noqa: RUF002

    bmu, bsigma, bmin, bmax = _dist_parms
    return _beta_located((bmu - bmin) / (bmax - bmin), bsigma / (bmax - bmin))
