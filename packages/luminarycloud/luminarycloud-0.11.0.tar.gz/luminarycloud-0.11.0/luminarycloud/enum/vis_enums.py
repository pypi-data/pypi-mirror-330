from .._proto.api.v0.luminarycloud.vis import vis_pb2
from enum import IntEnum


class VisQuantity(IntEnum):
    """
    The visualization quantity. This is a subset of all quantities.
    .. warning:: This feature is experimental and may change or be removed in the future.
    """

    NONE = vis_pb2.FIELD_NONE
    ABSOLUTE_PRESSURE = vis_pb2.FIELD_ABSOLUTE_PRESSURE
    PRESSURE = vis_pb2.FIELD_PRESSURE
    PRESSURE_COEFFICIENT = vis_pb2.FIELD_PRESSURE_COEFFICIENT
    TOTAL_PRESSURE = vis_pb2.FIELD_TOTAL_PRESSURE
    TOTAL_PRESSURE_COEFFICIENT = vis_pb2.FIELD_TOTAL_PRESSURE_COEFFICIENT
    DENSITY = vis_pb2.FIELD_DENSITY
    HEAT_FLUX = vis_pb2.FIELD_HEAT_FLUX
    TEMPERATURE = vis_pb2.FIELD_TEMPERATURE
    TOTAL_TEMPREATURE = vis_pb2.FIELD_TOTAL_TEMPERATURE
    MACH = vis_pb2.FIELD_MACH
    Q_CRITERION = vis_pb2.FIELD_Q_CRITERION
    VELOCITY = vis_pb2.FIELD_VELOCITY
    FRICTION_COEFFICIENT = vis_pb2.FIELD_SKIN_FRICTION_COEFFICIENT
    WALL_SHEAR_STRESS = vis_pb2.FIELD_WALL_SHEAR_STRESS


class Representation(IntEnum):
    """
    The representation defines how objects will appear in the scene.

    Attributes:
    -----------
    SURFACE
        Show the surface of the object.
    SURFACE_WITH_EDGES
        Show the surface of the object with mesh lines.
    WIREFRAME
        Show only the object's mesh lines.
    POINTS
        Show only the objects points.
    """

    SURFACE = vis_pb2.SURFACE
    SURFACE_WITH_EDGES = vis_pb2.SURFACE_WITH_EDGES
    # TODO(matt): need to hook these up in the image renderer
    WIREFRAME = vis_pb2.WIREFRAME
    POINTS = vis_pb2.POINTS


class FieldComponent(IntEnum):
    """
    Specifies which component of a field is used for visualization.
    When using scalars, the X component is the only valid component.

    Attributes:
    -----------
    X
        Use the 'x' component.
    Y
        Use the 'y' component.
    Z
        Use the 'z' component.
    MAGNITUDE
        Use the magnitude of the vector.
    """

    X = vis_pb2.Field.COMPONENT_X
    Y = vis_pb2.Field.COMPONENT_Y
    Z = vis_pb2.Field.COMPONENT_Z
    MAGNITUDE = vis_pb2.Field.COMPONENT_MAGNITUDE


class ColorMapPreset(IntEnum):
    """Predefined color map presets."""

    VIRIDIS = vis_pb2.ColorMapName.COLOR_MAP_NAME_VIRIDIS
    TURBO = vis_pb2.ColorMapName.COLOR_MAP_NAME_TURBO
    JET = vis_pb2.ColorMapName.COLOR_MAP_NAME_JET
    WAVE = vis_pb2.ColorMapName.COLOR_MAP_NAME_WAVE
    COOL_TO_WARM = vis_pb2.ColorMapName.COLOR_MAP_NAME_COOL_TO_WARM
    XRAY = vis_pb2.ColorMapName.COLOR_MAP_NAME_XRAY


class CameraProjection(IntEnum):
    """
    The type of projection used in the camera.

    Attributes
    ----------
    ORTHOGRAPHIC
        A orthographic (i.e., parallel) projection.
    PERSPECTIVE
        A perspective projection.
    """

    ORTHOGRAPHIC = vis_pb2.ORTHOGRAPHIC
    PERSPECTIVE = vis_pb2.PERSPECTIVE


class CameraDirection(IntEnum):
    """
    Directional camera options

    Attributes
    ----------
    X_POSITIVE
        Look down the positive x-axis
    Y_POSITIVE
        Look down the positive y-axis
    Z_POSITIVE
        Look down the positive z-axis
    X_NEGATIVE
        Look down the negative x-axis
    Y_NEGATIVE
        Look down the negative y-axis
    Z_NEGATIVE
        Look down the negative z-axis
    """

    X_POSITIVE = vis_pb2.X_POSITIVE
    Y_POSITIVE = vis_pb2.Y_POSITIVE
    Z_POSITIVE = vis_pb2.Z_POSITIVE
    X_NEGATIVE = vis_pb2.X_NEGATIVE
    Y_NEGATIVE = vis_pb2.Y_NEGATIVE
    Z_NEGATIVE = vis_pb2.Z_NEGATIVE


class ImageStatusType(IntEnum):
    """
    Represents the status of an image request.

    Attributes
    ----------
    ACTIVE
        The request is currently active and being processed.
    COMPLETED
        The request is complete.
    FAILED
        The request has failed.
    INVALID
        The request is invalid.

    .. warning:: This feature is experimental and may change or be removed in the future.
    """

    ACTIVE = vis_pb2.Active
    COMPLTETED = vis_pb2.Completed
    FAILED = vis_pb2.Failed
    INVALID = vis_pb2.Invalid


class EntityType(IntEnum):
    """
    An enum for specifying the source of an image. When listing extracts,
    the user must specify what type of extract they are interested in. This
    enum is only used by the visualization code.

    Attributes
    ----------
    SIMULATION
        Specifies a similuation entity (i.e., a result).
    MESH
        Specifies a mesh entity.
    GEOMETRY
        Specifies a geometry entity.
    """

    SIMULATION = 0
    MESH = 1
    GEOMETRY = 2
