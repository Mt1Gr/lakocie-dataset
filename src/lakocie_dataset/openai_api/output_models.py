from pydantic import BaseModel, Field
from enum import Enum


class AnalyticalComponentType(str, Enum):
    CALCIUM = "Wapń"
    PHOSPHORUS = "Fosfor"
    PROTEIN = "Białko"
    FAT = "Tłuszcz"
    CRUDE_FIBER = "Włókno surowe"
    CRUDE_ASH = "Popiół surowy"
    MOISTURE = "Wilgotność"
    OTHER = "Inny"


class AnalyticalComponent(BaseModel):
    value: float = Field(..., description="Odczytana wartość składnika [%]")
    type: AnalyticalComponentType = Field(..., description="Typ składnika")
    name: str = Field(..., description="Odczytana nazwa składnika analitycznego")


class AnalyticalComponents(BaseModel):
    components: list[AnalyticalComponent]


class DietaryComponent(BaseModel):
    value: float | None = Field(
        default=None, description="Odczytana wartość, jeśli podana"
    )
    unit: str | None = Field(default=None, description="Jednostka, jeśli podana")
    name: str = Field(..., description="Odczytana nazwa dodatku dietetycznego")
    chemical_form: str | None = Field(
        default=None, description="Forma chemiczna np.: Jednowodny siarczan manganu(II)"
    )


class DietaryComponents(BaseModel):
    components: list[DietaryComponent]
