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
        default="Unknown",
    )


def get_metadata_sentence(metadata: EsolangMetadata) -> str:
    """Returns a sentence from the esolang metadata.

    Args:
        metadata (EsolangMetadata): The esolang metadata.

    Returns:
        str: The sentence.
    """

    return (
        f"The '{metadata.name}' esoteric programming language."
        + f" {metadata.description}"
        + f" It has been created in {metadata.year} by {metadata.author}."
    )
