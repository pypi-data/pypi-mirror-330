"""
Functions to parse margin data compiled by
Prof. Aswath Damodaran, Stern School of Business, NYU.

Provides :func:`margin_data_resampler` for generating margin data
from an estimated Gaussian KDE from the source (margin) data.

Data are downloaded or reused from a local copy, on demand.

For terms of use of Prof. Damodaran's data, please see:
https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html

NOTES
-----

Prof. Damodaran notes that the data construction may not be
consistent from iteration to iteration. He also notes that,
"the best use for my data is in real time corporate financial analysis
and valuation." Here, gross margin data compiled by Prof. Damodaran are
optionally used to model the distribution of price-cost margin
across firms that antitrust enforcement agencies are likely to review in
merger enforcement investigations over a multi-year span. The
implicit assumption is that refinements in source-data construction from
iteration to iteration do not result in inconsistent estimates of
the empirical distribution of margins estimated using
a Gaussian kernel density estimator (KDE).

Second, other procedures included in this package allow the researcher to
generate margins for a single firm and impute margins of other firms in
a model relevant antitrust market based on FOCs for profit maximization by
firms facing MNL demand. In that exercise, the distribution of
inferred margins does not follow the empirical distribution estimated
from the source data, due to restrictions resulting from the distribution of
generated market shares across firms and the feasibility condition that
price-cost margins fall in the interval :math:`[0, 1]`.

"""

import shutil
import zipfile
from collections.abc import Mapping
from importlib import resources
from pathlib import Path
from types import MappingProxyType

import numpy as np
import urllib3
from numpy.random import PCG64DXSM, Generator, SeedSequence
from scipy import stats  # type: ignore
from xlrd import open_workbook  # type: ignore

from .. import _PKG_NAME, DATA_DIR, VERSION, ArrayDouble, this_yaml  # noqa: TID252
from . import _mappingproxy_from_mapping

__version__ = VERSION

MGNDATA_ARCHIVE_PATH = DATA_DIR / "damodaran_margin_data_serialized.zip"


u3pm = urllib3.PoolManager()


def margin_data_getter(  # noqa: PLR0912
    _table_name: str = "margin",
    *,
    data_archive_path: Path | None = None,
    data_download_flag: bool = False,
) -> MappingProxyType[str, MappingProxyType[str, float | int]]:
    if _table_name != "margin":  # Not validated for other tables
        raise ValueError(
            "This code is designed for parsing Prof. Damodaran's margin tables."
        )

    data_archive_path_ = data_archive_path or MGNDATA_ARCHIVE_PATH
    workbook_path_ = data_archive_path_.parent / f"damodaran_{_table_name}_data.xls"
    if data_archive_path_.is_file() and not data_download_flag:
        # with data_archive_path_.open("r") as _yfh:
        #     margin_data_dict: dict[str, dict[str, float | int]] = this_yaml.load(_yfh)
        with (
            zipfile.ZipFile(data_archive_path_) as _yzip,
            _yzip.open(f"{data_archive_path_.stem}.yaml") as _yfh,
        ):
            margin_data_dict: dict[str, dict[str, float | int]] = this_yaml.load(_yfh)
        return _mappingproxy_from_mapping(margin_data_dict)
    elif workbook_path_.is_file():
        workbook_path_.unlink()
        if data_archive_path_.is_file():
            data_archive_path_.unlink()

    margin_urlstr = (
        f"https://pages.stern.nyu.edu/~adamodar/pc/datasets/{_table_name}.xls"
    )
    try:
        chunk_size_ = 1024 * 1024
        with (
            u3pm.request(
                "GET", margin_urlstr, preload_content=False
            ) as _urlopen_handle,
            workbook_path_.open("wb") as margin_file,
        ):
            while True:
                data_ = _urlopen_handle.read(chunk_size_)
                if not data_:
                    break
                margin_file.write(data_)

        print(f"Downloaded {margin_urlstr} to {workbook_path_}.")

    except urllib3.exceptions.MaxRetryError as error_:
        if isinstance(error_.__cause__, urllib3.exceptions.SSLError):
            # Works fine with other sites secured with certificates
            # from the Internet2 CA, such as,
            # https://snap.stanford.edu/data/web-Stanford.txt.gz
            print(
                f"WARNING: Could not establish secure connection to, {margin_urlstr}."
                "Using bundled copy."
            )
            if not workbook_path_.is_file():
                with resources.as_file(
                    resources.files(f"{_PKG_NAME}.data").joinpath(
                        "empirical_margin_distribution.xls"
                    )
                ) as margin_data_archive_path:
                    shutil.copy2(margin_data_archive_path, workbook_path_)
        else:
            raise error_

    xl_book_ = open_workbook(workbook_path_, ragged_rows=True, on_demand=True)
    xl_sheet_ = xl_book_.sheet_by_name("Industry Averages")

    margin_dict: dict[str, dict[str, float | int]] = {}
    row_keys_: list[str] = []
    read_row_flag = False
    for _ridx in range(xl_sheet_.nrows):
        xl_row = xl_sheet_.row_values(_ridx)
        if xl_row[0] == "Industry Name":
            read_row_flag = True
            row_keys_ = xl_row
            continue

        if not xl_row[0] or not read_row_flag:
            continue

        xl_row[1] = int(xl_row[1])
        margin_dict[xl_row[0]] = dict(zip(row_keys_[1:], xl_row[1:], strict=True))

    with (
        zipfile.ZipFile(data_archive_path_, "w") as _yzip,
        _yzip.open(f"{data_archive_path_.stem}.yaml", "w") as _yfh,
    ):
        this_yaml.dump(margin_dict, _yfh)

    return _mappingproxy_from_mapping(margin_dict)


def margin_data_builder(
    _src_data_dict: Mapping[str, Mapping[str, float | int]] | None = None, /
) -> tuple[ArrayDouble, ArrayDouble, ArrayDouble]:
    if _src_data_dict is None:
        _src_data_dict = margin_data_getter()

    margin_data_wts, margin_data_obs = (
        _f.flatten()
        for _f in np.hsplit(
            np.array([
                tuple(
                    _src_data_dict[_g][_h] for _h in ["Number of firms", "Gross Margin"]
                )
                for _g in _src_data_dict
                if not _g.startswith("Total Market")
                and _g
                not in {
                    "Bank (Money Center)",
                    "Banks (Regional)",
                    "Brokerage & Investment Banking",
                    "Financial Svcs. (Non-bank & Insurance)",
                    "Insurance (General)",
                    "Insurance (Life)",
                    "Insurance (Prop/Cas.)",
                    "Investments & Asset Management",
                    "R.E.I.T.",
                    "Retail (REITs)",
                    "Reinsurance",
                }
            ]),
            2,
        )
    )

    margin_wtd_avg = np.average(margin_data_obs, weights=margin_data_wts)
    # https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weighvar.pdf
    margin_wtd_stderr = np.sqrt(
        np.average((margin_data_obs - margin_wtd_avg) ** 2, weights=margin_data_wts)
        * (len(margin_data_wts) / (len(margin_data_wts) - 1))
    )

    return (
        margin_data_obs,
        margin_data_wts,
        np.round(
            (
                margin_wtd_avg,
                margin_wtd_stderr,
                margin_data_obs.min(),
                margin_data_obs.max(),
            ),
            8,
        ),
    )


def margin_data_resampler(
    _sample_size: int | tuple[int, ...] = (10**6, 2),
    /,
    *,
    seed_sequence: SeedSequence | None = None,
) -> ArrayDouble:
    """
    Generate draws from the empirical distribution bassed on Prof. Damodaran's margin data.

    The empirical distribution is estimated using a Gaussian KDE; the bandwidth
    selected using Silverman's rule is narrowed to reflect that the margin data
    are multimodal. Margins for firms in finance, investment, insurance, reinsurance, and
    REITs are excluded from the sample used to estimate the empirical distribution.

    Parameters
    ----------
    _sample_size
        Number of draws; if tuple, (number of draws, number of columns)

    seed_sequence
        SeedSequence for seeding random-number generator when results
        are to be repeatable

    Returns
    -------
        Array of margin values

    """

    seed_sequence_ = seed_sequence or SeedSequence(pool_size=8)

    x_, w_, _ = margin_data_builder(margin_data_getter())

    margin_kde = stats.gaussian_kde(x_, weights=w_, bw_method="silverman")
    margin_kde.set_bandwidth(bw_method=margin_kde.factor / 3.0)

    if isinstance(_sample_size, int):
        return np.array(
            margin_kde.resample(
                _sample_size, seed=Generator(PCG64DXSM(seed_sequence_))
            )[0]
        )
    elif isinstance(_sample_size, tuple) and len(_sample_size) == 2:
        ssz, num_cols = _sample_size
        ret_array = np.empty(_sample_size, np.float64)
        for idx, seed_seq in enumerate(seed_sequence_.spawn(num_cols)):
            ret_array[:, idx] = margin_kde.resample(
                ssz, seed=Generator(PCG64DXSM(seed_seq))
            )[0]
        return ret_array
    else:
        raise ValueError(f"Invalid sample size: {_sample_size!r}")
