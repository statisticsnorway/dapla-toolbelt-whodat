
import polars as pl

from whodat.whodat import Whodat


def test_whodat(
) -> None:
    df = (pl.read_json("tests/data/data.json", schema={"navn": pl.String,
        "foedselsdato": pl.String, "bostedsadresse": pl.String, "kjoenn": pl.String}))
    
    result = (
        Whodat.from_polars(df)
        .search_fnr()
        .with_search_strategy(
            variables=["navn", "foedselsdato"],
            inkluder_oppholdsadresse=True,
            soek_fonetisk=False,
            inkluder_doede=True,
        )
        .run()
    )
    
    assert False