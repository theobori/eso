"""The esolang metadata module."""

from pydantic import BaseModel, Field


class EsolangMetadata(BaseModel):
    """This model represents an esoteric language."""

    name: str = Field(
        title="The Name",
        description="This is the value of the esoteric language name",
    )
    description: str = Field(
        title="The Description",
        description="This is the value of the esoteric language description",
    )
    year: int = Field(
        title="The Creation Year",
        description="This is the value of the esoteric language creation",
        gt=1899,
    )
    author: str = Field(
        title="The Author Name",
        description="This is the value of the esoteric language author name",
    )
