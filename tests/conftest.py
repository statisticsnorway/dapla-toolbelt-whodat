import pandas as pd
import polars as pl
import pytest_cases


@pytest_cases.fixture()
def df_personer_pl() -> pl.DataFrame:
    JSON_FILE = "tests/data/data.json"
    return pl.read_json(
        JSON_FILE,
        schema={
            "fnr": pl.String,
            "navn": pl.String,
            "kjoenn": pl.String,
            "foedselsdato": pl.String,
        },
    )


@pytest_cases.fixture()
def df_personer_pd() -> pd.DataFrame:
    JSON_FILE = "tests/data/data.json"
    return pd.read_json(
        JSON_FILE,
        dtype={
            "fnr": str,
            "navn": str,
            "kjoenn": str,
            "foedselsdato": str,
        },
    )


@pytest_cases.fixture()
def df_personer_some_nulls() -> pl.DataFrame:
    JSON_FILE = "tests/data/data_some_nulls.json"
    return pl.read_json(
        JSON_FILE,
        schema={
            "fnr": pl.String,
            "navn": pl.String,
            "kjoenn": pl.String,
            "foedselsdato": pl.String,
        },
    )


@pytest_cases.fixture()
def df_personer_invalid() -> pl.DataFrame:
    JSON_FILE = "tests/data/data_invalid.json"
    return pl.read_json(
        JSON_FILE,
        schema={
            "fnr": pl.String,
            "navn": pl.String,
            "kjoenn": pl.String,
            "foedselsdato": pl.String,
        },
    )
