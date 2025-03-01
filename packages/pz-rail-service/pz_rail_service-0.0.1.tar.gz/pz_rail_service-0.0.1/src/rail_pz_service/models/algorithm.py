"""Pydantic model for the Algorithm"""

from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class AlgorithmBase(BaseModel):
    """Algorithm parameters that are in DB tables and also used to create new rows"""

    # Name for this Algorithm, unique
    name: str

    # Name for the python class implementing the algorithm
    class_name: str


class AlgorithmCreate(AlgorithmBase):
    """Algorithm Parameters that are used to create new rows but not in DB tables"""


class Algorithm(AlgorithmBase):
    """Algorithm Parameters that are in DB tables and not used to create new rows"""

    model_config = ConfigDict(from_attributes=True)

    col_names_for_table: ClassVar[list[str]] = ["id", "name", "class_name"]

    # primary key
    id: int
