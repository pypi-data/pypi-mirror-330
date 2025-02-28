import dataclasses as dc
from dataclasses import dataclass
from ..enum.vis_enums import *


@dataclass
class Field:
    """
    The field controls the field displayed on the object. If the field doesn't
    exist, we show a solid color.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attribues:
    ----------
    quantity : VisQuantity
        The quantity to color by.
    component : FieldComponent
        The component of the field to use, applicable to vector fields. If the field is a
        scalar, use the default X component.
    """

    quantity: VisQuantity = VisQuantity.ABSOLUTE_PRESSURE
    component: FieldComponent = FieldComponent.X


@dataclass
class DisplayAttributes:
    """
    Display attributes specify how objects such as meshes, geometries, and
    filters appear in the scene.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    ----------
    visible : bool
        If the object is visible or not. Default: True
    opacity : float
        How opaque the object is. This is a normalized number between
        0 (i.e., fully transparent) and 1 (i.e., fully opaque). Default: 1
    field : Field
        What field quantity/component to color by, if applicable.
    representation : Representation
        how the object is represented in the scene (e.g., surface, surface with
        edges, wireframe or points). Default: surface.
    """

    visible: bool = True
    # TODO(matt): opacity not hooked up yet.
    opacity: float = 1.0
    field: Field = dc.field(default_factory=Field)
    representation: Representation = Representation.SURFACE


@dataclass
class DataRange:
    """
    The data range represents a range of values. Ranges are only valid if the
    max value is greater than the or equal to the min_value. The default is
    invalid.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes:
    -----------
    min_value : float
        The minimum value of the range.
    max_value : float
        The maximum value of the range.
    """

    min_value: float = float("inf")
    max_value: float = float("-inf")

    def is_valid(self) -> bool:
        return self.max_value >= self.min_value


@dataclass
class ColorMap:
    """
    The color map allows user control over how field values are mapped to
    colors.  Color maps are assigned to fields (e.g., the quantity
    and component) and not individual display attributes. This means that there
    can only ever be one color map per field/component combination (e.g.,
    velocity-magnitude or velocity-x). Any display attribute in the scene
    (i.e., filter display attributes or global display attributes) that maps to
    this color map will be color in the same manner.
    .. warning:: This feature is experimental and may change or be removed in the future.

    Attributes
    ----------
    field : Field
        The field and component this color map applies to.
    preset : ColorMapPreset
        The color map preset to use. This defines the colors used in the color
        map. Default is 'JET'.
    data_range : DataRange
        An optional data range to use for the color map. The user must explicity
        set the data ranges. If not set explicitly, the fields global data range
        is used. For comparing multiple results, either with different solutions
        in the same simulation or with different simulations, its highly
        recommended that a range is provided so the color scales are the same
        between the resulting images. Default: is an invalid data range.
    discretize : bool
        Use discrete color bins instead of a continuous range. When True,
        'n_colors' indicates how many discrete bins to use. Default: False.
    n_colors : int
        How many discrete bins to use when discretize is True. Valid n_colors
        values are [1, 256]. Default: 8.
    """

    field: Field = dc.field(default_factory=Field)
    preset: ColorMapPreset = ColorMapPreset.JET
    data_range: DataRange = dc.field(default_factory=DataRange)
    discretize: bool = False
    n_colors: int = 8

    def _to_proto(self) -> vis_pb2.ColorMap:
        res: vis_pb2.ColorMap = vis_pb2.ColorMap()
        res.field.component = self.field.component.value
        res.field.quantity_typ = self.field.quantity.value
        res.name = self.preset.value
        res.discretize.value = self.discretize
        res.n_colors.value = self.n_colors
        if self.data_range.is_valid():
            res.range.max = self.data_range.max_value
            res.range.min = self.data_range.min_value
        return res
