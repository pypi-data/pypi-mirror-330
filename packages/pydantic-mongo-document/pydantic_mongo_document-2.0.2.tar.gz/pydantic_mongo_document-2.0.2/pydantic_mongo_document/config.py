from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ClientOptions(BaseModel):
    """Mongodb client options model."""

    model_config = ConfigDict(populate_by_name=True)

    replica_set: Optional[str] = Field(None, description="Replica set name.", alias="replicaSet")
    read_preference: Optional[
        Literal[
            "primary",
            "primaryPreferred",
            "secondary",
            "secondaryPreferred",
            "nearest",
        ]
    ] = Field(
        None,
        description="Read preference.",
        alias="readPreference",
    )
    write_concern: Optional[Literal["majority", "local"]] = Field(
        None,
        description="Write concern.",
        alias="w",
    )
    read_concern: Optional[Literal["majority", "local"]] = Field(
        None,
        description="Read concern.",
        alias="readConcernLevel",
    )


class ReplicaConfig(BaseModel):
    """Mongodb replica config model."""

    model_config = ConfigDict(populate_by_name=True)

    uri: Annotated[
        str,
        Field(..., description="Mongodb connection URI."),
    ]
    client_options: ClientOptions = Field(
        default_factory=ClientOptions,
        description="Mongodb client options.",
    )
