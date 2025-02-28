from luminarycloud.types import Vector3
from luminarycloud.vis.visualization import DisplayAttributes
from .._proto.api.v0.luminarycloud.vis import vis_pb2
from abc import ABC, abstractmethod
from typing import List, cast
import string, random


def generate_id(prefix: str) -> str:
    return prefix + "".join(random.choices(string.ascii_lowercase, k=24))


def is_list_vec3(obj: list) -> bool:
    if isinstance(obj, list) and len(obj) == 3:
        return all(isinstance(item, (int, float)) for item in obj)
    return False


def convertToVec3(value: list | Vector3) -> Vector3:
    if isinstance(value, Vector3):
        return value
    elif is_list_vec3(value):
        return Vector3(x=value[0], y=value[1], z=value[2])
    else:
        raise TypeError(f"Invalid type for vec3: '{value}'")


def set_filter_display_attrs(filter: vis_pb2.Filter, attrs: DisplayAttributes) -> None:
    filter.display_attrs.visible = attrs.visible
    filter.display_attrs.representation = attrs.representation
    filter.display_attrs.field.component = attrs.field.component
    filter.display_attrs.field.quantity_typ = attrs.field.quantity


class Plane:
    """
    This class defines a plane.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    origin : Vector3
        A point defined on the plane. Default: [0,0,0].
    normal : Vector3
        The vector orthogonal to the  plane. Default: [0,1,0]
    """

    def __init__(self) -> None:
        self._origin: Vector3 = Vector3(x=0, y=0, z=0)
        self._normal: Vector3 = Vector3(x=1, y=0, z=0)

    @property
    def origin(self) -> Vector3:
        return self._origin

    @origin.setter
    def origin(self, new_origin: Vector3 | List[float]) -> None:
        self._origin = cast(Vector3, convertToVec3(new_origin))

    @property
    def normal(self) -> Vector3:
        return self._normal

    @normal.setter
    def normal(self, new_normal: Vector3 | List[float]) -> None:
        self._normal = cast(Vector3, convertToVec3(new_normal))


class Filter(ABC):
    """
    This is the base class for all filters. Each derived filter class
    is responsible for providing a _to_proto method to convert to a filter
    protobuf.
    .. warning:: This feature is experimental and may change or be removed in the future.
    """

    def __init__(self) -> None:
        self.display_attrs = DisplayAttributes()

    @abstractmethod
    def _to_proto(self) -> vis_pb2.Filter:
        pass


class Slice(Filter):
    """
    The slice filter is used to extract a cross-section of a 3D dataset by
    slicing it with a plane.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    plane : Plane
        The slice plane.
    name : str
        A user provided name for the filter.
    display_attrs : DisplayAttributes
        Specifies this filter's appearance.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._plane = Plane()
        self._project_vectors: bool = False
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id = generate_id("slice-")
        self.name = name

    @property
    def plane(self) -> Plane:
        return self._plane

    @plane.setter
    def plane(self, new_plane: Plane) -> None:
        if not isinstance(new_plane, Plane):
            raise TypeError(f"Expected 'Plane', got {type(new_plane).__name__}")
        self._plane = new_plane

    @property
    def project_vectors(self) -> bool:
        return self._project_vectors

    @project_vectors.setter
    def project_vectors(self, new_project_vectors: bool) -> None:
        if not isinstance(new_project_vectors, bool):
            raise TypeError(f"Expected 'bool', got {type(new_project_vectors).__name__}")
        self._project_vectors = new_project_vectors

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.slice.plane.origin.CopyFrom(self.plane.origin._to_proto())
        vis_filter.slice.plane.normal.CopyFrom(self.plane.normal._to_proto())
        vis_filter.slice.project_vectors = self.project_vectors
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter


class Clip(Filter):
    """
    Clip the dataset using a plane.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    origin : Vector3
        A point defined on the plane. Default: [0,0,0].
    normal : Vector3
        The vector orthogonal to the clip plane.  Default: [0,1,0]
    name : str
        A user provided name for the filter.
    display_attrs (DisplayAttributes)
        Specifies how this filter's appearance.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._plane: Plane = Plane()
        # TODO(matt): We could make this a prop to that is unsettable. Or we could
        # not use ids and force that the filter names are unique.
        self.id = generate_id("clip-")
        self.name = name

    @property
    def plane(self) -> Plane:
        return self._plane

    @plane.setter
    def plane(self, new_plane: Plane) -> None:
        if not isinstance(new_plane, Plane):
            raise TypeError(f"Expected 'Plane', got {type(new_plane).__name__}")
        self._plane = new_plane

    def _to_proto(self) -> vis_pb2.Filter:
        vis_filter = vis_pb2.Filter()
        vis_filter.id = self.id
        vis_filter.name = self.name
        vis_filter.clip.plane.origin.CopyFrom(self.plane.origin._to_proto())
        vis_filter.clip.plane.normal.CopyFrom(self.plane.normal._to_proto())
        set_filter_display_attrs(vis_filter, self.display_attrs)
        return vis_filter
