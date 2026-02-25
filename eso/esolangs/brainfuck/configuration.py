"""The brainfuck configuration module."""

from pydantic import BaseModel, Field


class BrainfuckConfiguration(BaseModel):
    """This model represents a configuration for the Brainfuck esoteric language.
    It mainly configures parameters used at brainfuck execution."""

    enable_memory_wrapping: bool = Field(
        title="Enable Memory Wrapping",
        description="This is the value for controlling the memory wrapping",
        default=False,
    )
    enable_memory_wrapping_protection: bool = Field(
        title="Enable Memory Wrapping protection",
        description="This is the value for controlling the memory wrapping protection",
        default=False,
    )
    memory_size: int = Field(
        title="The Memory Size",
        description="This is the value of the memory size",
        lt=1_000_000 + 1,
        gt=0xFF - 1,
        default=30_000,
    )
