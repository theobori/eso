"""The befunge configuration module."""

from eso.esolangs.befunge.const import PROGRAM_W, PROGRAM_H

from pydantic import BaseModel, Field


class BefungeConfiguration(BaseModel):
    """This model represents a configuration for the befunge esoteric language.
    It mainly configures parameters used at befunge execution."""

    grid_width: int = Field(
        title="The Grid Width",
        description="This is the value of the grid width",
        ge=PROGRAM_W,
        default=PROGRAM_W,
    )
    grid_height: int = Field(
        title="The Grid Height",
        description="This is the value of the grid height",
        ge=PROGRAM_H,
        default=PROGRAM_H,
    )
    stack_bytes_size: int = Field(
        title="The Stack Bytes Size",
        description="This is the value of the stack bytes size for the generated C code",
        ge=256,
        default=256 * 256 * 8,
    )
