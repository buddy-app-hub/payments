# Standard library imports
from datetime import datetime

from pydantic import Field, model_validator, ConfigDict

NOW_FACTORY = datetime.now


class CreatedUpdatedAt:
    """Created and updated at mixin that automatically updates updated_at field."""

    created_at: datetime = Field(default_factory=NOW_FACTORY)
    updated_at: datetime = Field(default_factory=NOW_FACTORY)

    model_config = ConfigDict(
        validate_assignment=True,
    )

    @model_validator(mode="after")
    @classmethod
    def update_updated_at(cls, obj: "CreatedUpdatedAt") -> "CreatedUpdatedAt":
        """Update updated_at field."""
        # must disable validation to avoid infinite loop
        obj.model_config["validate_assignment"] = False

        obj.updated_at = NOW_FACTORY()

        # enable validation again
        obj.model_config["validate_assignment"] = True
        return obj