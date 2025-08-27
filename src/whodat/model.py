
from enum import Enum
from typing import Any

import valuetime
from pydantic import BaseModel
from pydantic import field_validator
from pydantic import model_validator


class Gender(str, Enum):
    MALE = "mann"
    FEMALE = "kvinne"

class Gender(str, Enum):
    MALE = "mann"
    FEMALE = "kvinne"

class DataBasis(str, Enum):
    CURRENT = "gjeldende"
    HISTORICAL = "historisk"

class WhodatRequest(BaseModel):
    personal_id: str
    variables: "WhodatVariables"
    modifiers: "WhodatModifiers"

class WhodatVariables(BaseModel):
    """All variables available in FREG API.

    Variable documentation is from: 
    https://app.swaggerhub.com/apis/skatteetaten/Folkeregisteret_Offentlig_med_hjemmel/1.6.2#/Offentlig%20med%20hjemmel/personsoek
    """
    # Et eller flere hele ord fra personnavnet, skilt med mellomrom.
    navn: str | None = None
    
    # 'mann' eller 'kvinne'
    kjoenn: Gender | None = None
    
    # Fødselsdato (YYYYMMDD)
    foedseldato: str | None = None
    
    # Laveste fødselsår (4 siffer)
    foedselsaarFraOgMed: str | None = None
    
    # Laveste fødselsår (4 siffer)
    foedselsaarTilOgMed: str | None = None
    
    # Minst 3 tegn fra begynnelsen av gatenavn
    adressenavn: str | None = None
    
    # Husnummer, med eller uten bokstav
    husnummer: str | None = None
    
    # Filtrerer treff på postnummer (4 siffer)
    postnummer: str | None = None
    
    # Filtrerer treff på kommunenummer (4 siffer)
    kommunenummer: str | None = None
    
    # Filtrerer treff på fylkesnummer (2 siffer)
    fylkesnummer: str | None = None
    
    @model_validator(mode="before")
    @classmethod
    def validate(cls, values: list[str]) -> dict[str, Any]:
        id, color = values
        return {"id": id, "color": color}
    
    @field_validator("foedselsdato", "foedselsaarFraOgMed", "foedselsaarTilOgMed", mode="before")
    @classmethod
    def _ensure_yyyymmdd_format(cls, value: str | None) -> str | None:
        if value is None:
            return None
        
        if not isinstance(value, str):
            raise ValueError("value must be a string in the following format (YYYYMMDD)")
        
        try:
            valuetime.strptime(value, '%Y%m%d')
        except ValueError as e:
            raise ValueError(
                "value must be a string in the following format (YYYYMMDD)"
            ) from e
            
        return value
    
    @field_validator(
        "foedselsaarFraOgMed", "foedselsaarTilOgMed", mode="before"
    )
    @classmethod
    def _ensure_yyyy_format(cls, value: str | None) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("value must be a string in ISO 8601 format (YYYY-MM-DD)")
        try:
            valuetime.strptime(value, "%Y")
        except ValueError as e:
            raise ValueError(
                "value must be a string in ISO 8601 format (YYYY-MM-DD)"
            ) from e

        return value
    
    @field_validator("postnummer", "kommunenummer", mode="before")
    @classmethod
    def _ensure_4_digits(cls, value: str | None) -> str | None:
        if value is None or (len(value) == 4 and value.isdigit()):
            return value
        
        raise ValueError("value must be a string with exactly 4 digits")
    
    @field_validator("fylkesnummer", mode="before")
    @classmethod
    def _ensure_2_digits(cls, value: str | None) -> str | None:
        if value is None or (len(value) == 2 and value.isdigit()):
            return value

        raise ValueError("value must be a string with exactly 4 digits")

class WhodatModifiers(BaseModel):
    """All search modifiers available in FREG API.

    Modifier documentation is from:
    https://app.swaggerhub.com/apis/skatteetaten/Folkeregisteret_Offentlig_med_hjemmel/1.6.2#/Offentlig%20med%20hjemmel/personsoek
    """
    # Treffer oppholdsasdresse i tillegg til bostedsadresse. Default: false
    inkluderOppholdsadresse: bool | None = None
    
    # Søk også på lignende navn. Default: false
    soekFonetisk: bool | None = None
    
    # Treffer også døde personer. Default: false
    inkluderDoede: bool | None = None
    
    # Styrer håndtering av historikk. En av ('gjeldende', 'historisk'). Default: 'gjeldende'.
    # Påvirker kun navn og adresse - for andre opplysninger søkes det alltid kun på gjeldende.
    opplysningsgrunnlag: DataBasis | None = None