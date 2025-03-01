from typing import List

from videodb._constants import ApiPath

from videodb.image import Frame


class Scene:
    def __init__(
        self,
        video_id: str,
        start: float,
        end: float,
        description: str,
        id: str = None,
        frames: List[Frame] = [],
        metadata: dict = {},
        connection=None,
    ):
        self.id = id
        self.video_id = video_id
        self.start = start
        self.end = end
        self.frames: List[Frame] = frames
        self.description = description
        self.metadata = metadata
        self._connection = connection

    def __repr__(self) -> str:
        return (
            f"Scene("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"start={self.start}, "
            f"end={self.end}, "
            f"frames={self.frames}, "
            f"description={self.description}), "
            f"metadata={self.metadata})"
        )

    def to_json(self):
        return {
            "id": self.id,
            "video_id": self.video_id,
            "start": self.start,
            "end": self.end,
            "frames": [frame.to_json() for frame in self.frames],
            "description": self.description,
            "metadata": self.metadata,
        }

    def describe(self, prompt: str = None, model_name=None) -> None:
        if self._connection is None:
            raise ValueError("Connection is required to describe a scene")
        description_data = self._connection.post(
            path=f"{ApiPath.video}/{self.video_id}/{ApiPath.scene}/{self.id}/{ApiPath.describe}",
            data={"prompt": prompt, "model_name": model_name},
        )
        self.description = description_data.get("description", None)
        return self.description


class SceneCollection:
    def __init__(
        self,
        _connection,
        id: str,
        video_id: str,
        config: dict,
        scenes: List[Scene],
    ) -> None:
        self._connection = _connection
        self.id = id
        self.video_id = video_id
        self.config: dict = config
        self.scenes: List[Scene] = scenes

    def __repr__(self) -> str:
        return (
            f"SceneCollection("
            f"id={self.id}, "
            f"video_id={self.video_id}, "
            f"config={self.config}, "
            f"scenes={self.scenes})"
        )

    def delete(self) -> None:
        self._connection.delete(
            path=f"{ApiPath.video}/{self.video_id}/{ApiPath.scenes}/{self.id}"
        )
