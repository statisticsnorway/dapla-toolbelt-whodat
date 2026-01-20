import polars as pl
import pytest

from dapla_whodat import Whodat


def test_should_fail_empty_var_list(df_personer_pl: pl.DataFrame) -> None:
    with pytest.raises(ValueError):
        Whodat.from_polars(df_personer_pl).search_fnr().with_search_strategy(
            variables=[]
        )
