from typing import Any

from polars import exclude
from pydantic import BaseModel

from whodat.model import WhodatResponse


class SingleRowInfo(BaseModel):
    """Information about the personal ID search for a single row.
    
    Attributes:
        index_original_df (int): The index of the row in the original dataframe.
        number_of_found_ids (int): The number of personal IDs found for the row. 1 if unique.
        unique_response_step_number (int): The 1-indexed search algorithm that gave a unique result. 
            None if no unique result was found.
    """
    index_original_df: int
    number_of_found_ids: int
    unique_response_step_number: int | None

class Result:
    def __init__(self, responses: list[tuple[WhodatResponse, int]]) -> None:
        self.responses = responses
        self._details: list[dict[str, Any]] = self.generate_details()
    
    def to_list(self, exclude_nones: bool = False) -> list[str | None]:
        result: list[str | None] = []
        for response in self.responses:
            found_ids = response[0].found_personal_ids
            
            if len(found_ids) == 1:
                result.append(found_ids[0])
            elif exclude_nones is False:
                result.append(None)
        
        return result


    def generate_details(self) -> list[dict[str, Any]]:
        details = []
        for i, response in enumerate(self.responses):
            found_ids = response[0].found_personal_ids
            number_of_found_ids = len(found_ids)
            unique_response_step_number = response[1] if number_of_found_ids == 1 else None
            details.append(SingleRowInfo(
                index_original_df=i,
                number_of_found_ids=number_of_found_ids,
                unique_response_step_number=unique_response_step_number
            ).model_dump())
        
        return details
    
    @property
    def details(self) -> list[dict[str, Any]]:
        return self._details