import polars as pl
import pytest_cases


@pytest_cases.fixture()
def df_personer() -> pl.DataFrame:
    JSON_FILE = "tests/data/personer.json"
    return pl.read_json(
        JSON_FILE,
        schema={
            "fnr": pl.String,
            "fornavn": pl.String,
            "etternavn": pl.String,
            "kjonn": pl.String,
            "fodselsdato": pl.String,
        },
    )
