import polars as pl
import pytest

from dapla_whodat import Whodat
from tests.integration.utils import integration_test


@pytest.mark.usefixtures("setup")
@integration_test()
def test_whodat() -> None:
    df = pl.read_json(
        "tests/data/data.json",
        schema={
            "navn": pl.String,
            "foedselsdato": pl.String,
            "bostedsadresse": pl.String,
            "kjoenn": pl.String,
        },
    )

    _ = (
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
