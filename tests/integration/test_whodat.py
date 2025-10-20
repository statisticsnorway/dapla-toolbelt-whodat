from pathlib import Path

import pandas as pd
import polars as pl
import pytest

from dapla_whodat import Whodat
from tests.integration.utils import integration_test


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_default() -> None:
    df = pl.read_json(
        "tests/data/data.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    )

    r = (
        Whodat.from_polars(df)
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
def test_whodat_some_missing() -> None:
    df = pl.read_json(
        "tests/data/data.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    )

    r = (
        Whodat.from_polars(df)
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
def test_whodat_with_indices_polars() -> None:
    df = pl.read_json(
        "tests/data/data.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    ).with_row_index()

    r = (
        Whodat.from_polars(df)
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
def test_whodat_with_indices_pandas() -> None:
    df = pd.read_json(
        path_or_buf=Path("tests/data/data.json"),
        dtype={
            "navn": str,
            "foedselsdato": str,
            "bostedsadresse": str,
            "kjoenn": str,
        },
    )

    r = (
        Whodat.from_pandas(df)
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
def test_whodat_original_indices() -> None:
    df = pl.read_json(
        "tests/data/data.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    ).with_row_index()
    r = (
        Whodat.from_polars(df)
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
def test_whodat_some_nulls() -> None:
    df = pl.read_json(
        "tests/data/data_some_nulls.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    )

    r = (
        Whodat.from_polars(df)
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
            "number_of_found_ids": 10000,
            "unique_response_step_number": None,
        },
    ]


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat_freg_api_error() -> None:
    df = pl.read_json(
        "tests/data/data_invalid.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    )

    with pytest.raises(ValueError, match="FREG API returned an error"):
        (
            Whodat.from_polars(df)
            .search_fnr()
            .with_search_strategy(variables=["navn", "kjoenn"])
            .run()
        )
