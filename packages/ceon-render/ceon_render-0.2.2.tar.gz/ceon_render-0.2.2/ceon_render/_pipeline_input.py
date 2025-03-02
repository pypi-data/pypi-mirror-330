from __future__ import annotations
import logging
from enum import StrEnum, auto
from dataclasses import dataclass, field
from typing import ClassVar, Type

logger = logging.getLogger(__name__)


# Inherting from str makes the enum JSON serializable
class CeonPipelineInputType(StrEnum):
    AUDIO = auto()
    BOOL = auto()
    COLOR = auto()
    FLOAT = auto()
    IMG = auto()
    INT = auto()
    STRING = auto()


FILE_TYPES = [CeonPipelineInputType.AUDIO, CeonPipelineInputType.IMG]


@dataclass
class CeonPipelineInput:
    """Defines an expected input for a pipeline."""

    #  Make types easily accessible for user without needing to explicitly import CeonPipelineInputType
    types: ClassVar[Type[CeonPipelineInputType]] = CeonPipelineInputType

    input_name: str
    input_type: CeonPipelineInputType
    input_type_settings: dict = field(
        default_factory=dict
    )  # User-provided arguments that are unique for this type, e.g. "dropdown_options"
    description: str = ""
    num_entries_min: int = 1
    num_entries_max: int = 1

    def __str__(self):
        msg = f"<{self.__class__.__name__} '{self.input_name}' of type '{self.input_type}'>"
        return msg
