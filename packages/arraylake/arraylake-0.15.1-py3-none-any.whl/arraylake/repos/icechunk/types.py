import json
from datetime import datetime
from typing import NewType

from icechunk import SnapshotInfo
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from zarr import AsyncArray, AsyncGroup
from zarr.abc.metadata import Metadata
from zarr.core.metadata.v3 import V3JsonEncoder

from arraylake.types import datetime_to_isoformat

CommitId = NewType("CommitId", str)
TagName = NewType("TagName", str)
BranchName = NewType("BranchName", str)


class Commit(BaseModel):
    id: CommitId = Field(alias="_id")
    message: str
    commit_time: datetime
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @classmethod
    def from_snapshot(cls, snapshot: SnapshotInfo) -> "Commit":
        return cls(
            _id=CommitId(snapshot.id),
            message=snapshot.message,
            commit_time=snapshot.written_at,
        )

    @field_serializer("commit_time")
    def serialize_commit_time(self, commit_time: datetime) -> str:
        return datetime_to_isoformat(commit_time)


class Branch(BaseModel):
    id: BranchName = Field(alias="_id")
    commit_id: CommitId
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class Tag(BaseModel):
    id: TagName
    commit_id: CommitId


class Tree(BaseModel):
    path: str
    metadata: Metadata
    children: dict[str, "Tree"]
    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    async def from_node(cls, node: AsyncGroup | AsyncArray, prefix: str = "", depth: int = 10) -> "Tree":
        if depth == 0 or not isinstance(node, AsyncGroup):
            return Tree(path=node.path, metadata=node.metadata, children={})

        children = {}
        async for name, member in node.members():
            if len(prefix) > 0 and not (prefix.startswith(member.path) or member.path.startswith(prefix)):
                continue
            children[name] = await Tree.from_node(member, prefix=prefix, depth=depth - 1)

        return Tree(path=node.path, metadata=node.metadata, children=children)

    @field_serializer("metadata")
    def metadata_field_serializer(self, v: Metadata):
        return json.loads(json.dumps(v.to_dict(), cls=V3JsonEncoder))
