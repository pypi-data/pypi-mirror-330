from enum import Enum
from typing import Annotated

from pydantic import Field


class EIP712Format(str, Enum):
    AMOUNT = "amount"
    RAW = "raw"
    DATETIME = "datetime"


class EIP712Version(Enum):
    V1 = 1
    V2 = 2


HexString = Annotated[str, Field(pattern=r"^[a-f0-9]+$")]

ContractAddress = Annotated[str, Field(pattern=r"^(0x)?[a-f0-9]{40}$")]
