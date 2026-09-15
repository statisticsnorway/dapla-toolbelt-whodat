import pandas as pd
import polars as pl
import pytest

from dapla_whodat import Whodat
from tests.integration.utils import integration_test


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_default(df_personer_pl: pl.DataFrame) -> None:

    r = (
        Whodat.from_polars(df_personer_pl)
        .search_fnr()
        .with_search_strategy(variables=["navn"])
        .with_search_strategy(
            variables=["navn", "foedselsdato"],
            inkluder_oppholdsadresse=True,
            soek_fonetisk=False,
            inkluder_doede=True,
        )
        .run()
    )

    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": None,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": None,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": None,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
    ]
    assert r.to_list() == ["23859574084", "29890798770", "02846497938"]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_some_missing(df_personer_pl: pl.DataFrame) -> None:

    r = (
        Whodat.from_polars(df_personer_pl)
        .search_fnr()
        .with_search_strategy(variables=["navn"])
        .with_search_strategy(variables=["navn", "kjoenn"])
        .run()
    )
    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": None,
            "number_of_found_ids": 0,
            "unique_response_step_number": None,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": None,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": None,
            "number_of_found_ids": 3,
            "unique_response_step_number": None,
        },
    ]
    assert r.to_list() == [None, "29890798770", None]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_with_indices_polars(df_personer_pl: pl.DataFrame) -> None:

    r = (
        Whodat.from_polars(df_personer_pl.with_row_index())
        .search_fnr()
        .with_search_strategy(variables=["navn"])
        .with_search_strategy(variables=["navn", "kjoenn"])
        .run()
    )
    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": 0,
            "number_of_found_ids": 0,
            "unique_response_step_number": None,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": 1,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": 2,
            "number_of_found_ids": 3,
            "unique_response_step_number": None,
        },
    ]
    assert r.to_list() == [None, "29890798770", None]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_with_indices_pandas(df_personer_pd: pd.DataFrame) -> None:

    r = (
        Whodat.from_pandas(df_personer_pd)
        .search_fnr()
        .with_search_strategy(variables=["navn"])
        .with_search_strategy(variables=["navn", "kjoenn"])
        .run()
    )
    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": 0,
            "number_of_found_ids": 0,
            "unique_response_step_number": None,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": 1,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": 2,
            "number_of_found_ids": 3,
            "unique_response_step_number": None,
        },
    ]
    assert r.to_list() == [None, "29890798770", None]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_original_indices(df_personer_pl: pl.DataFrame) -> None:

    r = (
        Whodat.from_polars(df_personer_pl.with_row_index())
        .search_fnr()
        .with_search_strategy(variables=["navn"])
        .with_search_strategy(variables=["navn", "kjoenn"])
        .run()
    )
    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": 0,
            "number_of_found_ids": 0,
            "unique_response_step_number": None,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": 1,
            "number_of_found_ids": 1,
            "unique_response_step_number": 2,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": 2,
            "number_of_found_ids": 3,
            "unique_response_step_number": None,
        },
    ]
    assert r.to_dict_from_original_indices() == {
        1: "29890798770",
    }


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_some_nulls(df_personer_some_nulls: pl.DataFrame) -> None:

    r = (
        Whodat.from_polars(df_personer_some_nulls)
        .search_fnr()
        .with_search_strategy(variables=["navn", "kjoenn"])
        .run()
    )
    assert r.details == [
        {
            "index_fnr_search_df": 0,
            "index_original_df": None,
            "number_of_found_ids": 0,
            "unique_response_step_number": None,
        },
        {
            "index_fnr_search_df": 1,
            "index_original_df": None,
            "number_of_found_ids": 1,
            "unique_response_step_number": 1,
        },
        {
            "index_fnr_search_df": 2,
            "index_original_df": None,
            "number_of_found_ids": 3,
            "unique_response_step_number": None,
        },
    ]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_freg_api_error(df_personer_invalid: pl.DataFrame) -> None:

    with pytest.raises(ValueError, match="FREG API returned an error"):
        (
            Whodat.from_polars(df_personer_invalid)
            .search_fnr()
            .with_search_strategy(variables=["navn", "kjoenn"])
            .run()
        )
