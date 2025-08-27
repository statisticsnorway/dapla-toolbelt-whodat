from typing import Any

import pandas as pd
import polars as pl

from whodat.model import WhodatModifiers
from whodat.model import WhodatRequest
from whodat.model import WhodatVariables


class Whodat:
    @staticmethod
    def from_pandas(dataframe: pd.DataFrame) -> "Whodat._MethodSelector":
        return Whodat._MethodSelector().search_fnr(pl.from_pandas(dataframe))

    @staticmethod
    def from_polars(dataframe: pl.DataFrame) -> "Whodat._MethodSelector":
        return Whodat._MethodSelector().search_fnr(dataframe)

    class _MethodSelector:
        def __init__(self) -> None:
            pass

        def search_fnr(dataframe: pl.DataFrame, personal_id_col_name: str) -> None:
            pass

    class _VariableSelector:
        def __init__(
            self, personal_id_col_name: str, dataframe: pl.DataFrame,
        ) -> None:
            self.personal_id_col_name: str = personal_id_col_name
            self.dataframe: pl.DataFrame = dataframe
            self.all_variables: list[list[str]] = []
            self.all_modifiers: list[WhodatModifiers] = []

        def with_search_strategy(
            self,
            variables: list[str],
            inkluder_oppholdsadresse: bool | None = None,
            soek_fonetisk: bool | None = None,
            inkluder_doede: bool | None = None,
            opplysningsgrunnlag: str | None = None,
        ) -> "Whodat._VariableSelector":
            self.all_variables.append(variables)
            self.all_modifiers.append(WhodatModifiers(
                inkluder_oppholdsadresse=inkluder_oppholdsadresse,
                soek_fonetisk=soek_fonetisk,
                inkluder_doede=inkluder_doede,
                opplysningsgrunnlag=opplysningsgrunnlag))
            
            return self

        def run(self) -> None:
            def index_column_to_dict(variables: list[str], row: dict[str, Any]) -> dict[str, Any]:
                if not all(var in row for var in variables):
                    raise ValueError(f"Not all variables {variables} are were found in the dataframe columns {row.keys()}")
                
                return {var: self.dataframe.select(var) for var in variables}
            
            for row in self.dataframe.iter_rows(named=True):
                for variables, modifiers in zip(self.all_variables, self.all_modifiers, strict=True):
                    request = WhodatRequest(
                        data=row[self.personal_id_col_name],
                        variables=WhodatVariables(index_column_to_dict(variables, row)),
                        modifiers=modifiers
                    )
                    print(request.json(indent=2, exclude_none=True))
