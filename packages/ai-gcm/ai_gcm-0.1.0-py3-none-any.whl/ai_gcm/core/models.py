"""Models for AI Commit."""

from pydantic import BaseModel, Field

class CommitMessage(BaseModel):
    """Pydantic model for commit message response.
    
    Attributes:
        message (str): The commit message that follows conventional commit format.
            Must be between 1 and 72 characters long and start with a type
            (e.g., feat, fix, etc.).
    """
    message: str = Field(
        ...,  # ... means required
        description="A conventional commit message starting with type (feat, fix, etc.) followed by a description",
        min_length=1,
        max_length=72
    ) 
