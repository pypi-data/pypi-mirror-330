# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from collections.abc import Callable
from dataclasses import dataclass, field
from logging import getLogger
from os import PathLike
from typing import Optional, TypeVar, cast
from pprint import pformat

import luminarycloud.params.enum._enum_wrappers as enum

from luminarycloud._helpers.warnings import experimental
from luminarycloud._helpers.cond import params_to_str
from luminarycloud._helpers.simulation_params_from_json import (
    simulation_params_from_json_path,
)
from luminarycloud._proto.client import simulation_pb2 as clientpb
from luminarycloud._proto.output import output_pb2 as outputpb
from luminarycloud._proto.quantity import quantity_options_pb2 as quantityoptspb
from luminarycloud._proto.client.entity_pb2 import EntityIdentifier
from luminarycloud.params.convergence_criteria import ConvergenceCriteria
from luminarycloud.params.geometry import Volume
from luminarycloud.params.param_wrappers.simulation_param_ import (
    SimulationParam as _SimulationParam,
)
from luminarycloud.params.param_wrappers.simulation_param.volume_entity_ import VolumeEntity
from luminarycloud.params.param_wrappers.simulation_param.material_entity_ import MaterialEntity
from luminarycloud.params.param_wrappers.simulation_param.entity_relationships.volume_material_relationship_ import (
    VolumeMaterialRelationship,
)
from luminarycloud.params.param_wrappers.simulation_param.physics_ import Physics
from luminarycloud.params.param_wrappers.simulation_param.entity_relationships.volume_physics_relationship_ import (
    VolumePhysicsRelationship,
)
from luminarycloud.enum import QuantityType, AveragingType
from luminarycloud.reference_values import ReferenceValues, ReferenceValuesType
from luminarycloud.types import Vector3Like
from luminarycloud.types.vector3 import _to_vector3_ad_proto

logger = getLogger(__name__)


@dataclass(kw_only=True, repr=False)
class SimulationParam(_SimulationParam):
    """Simulation configuration that supports multiple physics."""

    reference_values: ReferenceValues = field(default_factory=ReferenceValues)
    "Reference values for outputs and stopping conditions."

    convergence_criteria: ConvergenceCriteria = field(default_factory=ConvergenceCriteria)
    "Convergence criteria for the simulation."

    def _to_proto(self) -> clientpb.SimulationParam:
        _proto = super()._to_proto()
        transient = self.basic is not None and self.basic.time == enum.FlowBehavior.TRANSIENT
        _proto.convergence_criteria.CopyFrom(self.convergence_criteria.to_proto(transient))
        if self.reference_values.reference_value_type == ReferenceValuesType.FARFIELD_VALUES:
            raise ValueError(
                "ReferenceValuesType.FARFIELD_VALUES cannot be used in SimulationParam yet."
            )
        self.reference_values._to_proto_common(_proto.reference_values)
        return _proto

    @classmethod
    def from_proto(self, proto: clientpb.SimulationParam) -> "SimulationParam":
        _wrapper = cast(SimulationParam, super().from_proto(proto))
        transient = (
            _wrapper.basic is not None and _wrapper.basic.time == enum.FlowBehavior.TRANSIENT
        )
        _wrapper.convergence_criteria = ConvergenceCriteria.from_proto(
            proto.convergence_criteria, transient
        )
        _wrapper.reference_values._from_proto_common(proto.reference_values)
        return _wrapper

    @classmethod
    def from_json(cls, path: PathLike) -> "SimulationParam":
        return cls.from_proto(simulation_params_from_json_path(path))

    def assign_material(self, material: MaterialEntity, volume: Volume | str) -> None:
        """
        Assigns a material entity to a volume ID.
        """
        if isinstance(volume, str):
            volume_identifier = EntityIdentifier(id=volume)
        else:
            volume_identifier = EntityIdentifier(id=volume._lcn_id)

        volume_material_pairs = self.entity_relationships.volume_material_relationship
        _remove_from_list_with_warning(
            _list=volume_material_pairs,
            _accessor=lambda v: v.volume_identifier.id,
            _to_remove=volume_identifier.id,
            _warning_message=lambda v: f"Volume {_stringify_identifier(volume_identifier)} has already been assigned material {_stringify_identifier(v.material_identifier)}. Overwriting...",
        )

        if volume_identifier.id not in (v.volume_identifier.id for v in self.volume_entity):
            volume_entity = VolumeEntity(volume_identifier=volume_identifier)
            self.volume_entity.append(volume_entity)
        if material.material_identifier.id not in (
            m.material_identifier.id for m in self.materials
        ):
            self.materials.append(material)

        volume_material_pairs.append(
            VolumeMaterialRelationship(
                volume_identifier=volume_identifier,
                material_identifier=material.material_identifier,
            )
        )

    def assign_physics(self, physics: Physics, volume: Volume | str) -> None:
        """
        Assigns a physics entity to a volume ID.
        """
        if isinstance(volume, str):
            volume_identifier = EntityIdentifier(id=volume)
        else:
            volume_identifier = EntityIdentifier(id=volume._lcn_id)

        volume_physics_pairs = self.entity_relationships.volume_physics_relationship
        _remove_from_list_with_warning(
            _list=volume_physics_pairs,
            _accessor=lambda v: v.volume_identifier.id,
            _to_remove=volume_identifier.id,
            _warning_message=lambda v: f"Volume {_stringify_identifier(volume_identifier)} has already been assigned physics {_stringify_identifier(v.physics_identifier)}. Overwriting...",
        )
        _remove_from_list_with_warning(
            _list=volume_physics_pairs,
            _accessor=lambda v: v.physics_identifier.id,
            _to_remove=physics.physics_identifier.id,
            _warning_message=lambda v: f"Physics {_stringify_identifier(physics.physics_identifier)} has already been assigned to volume {_stringify_identifier(v.volume_identifier)}. Overwriting...",
        )

        if volume_identifier.id not in (v.volume_identifier.id for v in self.volume_entity):
            self.volume_entity.append(VolumeEntity(volume_identifier=volume_identifier))
        if physics.physics_identifier.id not in (p.id for p in self.physics):
            self.physics.append(physics)

        volume_physics_pairs.append(
            VolumePhysicsRelationship(
                volume_identifier=volume_identifier,
                physics_identifier=physics.physics_identifier,
            )
        )

    @experimental
    def configure_adjoint_surface_output(
        self,
        quantity_type: QuantityType,
        surface_ids: list[str],
        *,
        reference_values: ReferenceValues = None,
        frame_id: str = "",
        force_direction: Optional[Vector3Like] = None,
        moment_center: Optional[Vector3Like] = None,
        averaging_type: AveragingType = AveragingType.UNSPECIFIED,
    ) -> None:
        """
        Helper to configure the surface output differentiated by the adjoint solver.
        See Simulation.download_surface_output() for details on the input parameters.

        .. warning:: This feature is experimental and may change or be removed without notice.
        """
        if self.adjoint.output is not None:
            self.adjoint.output.Clear()
        else:
            self.adjoint.output = outputpb.Output()
        self.adjoint.output.quantity = quantity_type
        self.adjoint.output.in_surfaces.extend(surface_ids)
        self.adjoint.output.frame_id = frame_id
        if QuantityType._is_average(quantity_type):
            self.adjoint.output.surface_average_properties.averaging_type = averaging_type
        elif QuantityType._is_force(quantity_type):
            self.adjoint.output.force_properties.CopyFrom(
                outputpb.ForceProperties(
                    force_dir_type=(
                        outputpb.FORCE_DIRECTION_BODY_ORIENTATION_AND_FLOW_DIR
                        if quantity_type._has_tag(quantityoptspb.TAG_AUTO_DIRECTION)
                        else outputpb.FORCE_DIRECTION_CUSTOM
                    ),
                    force_direction=(
                        _to_vector3_ad_proto(force_direction) if force_direction else None
                    ),
                    moment_center=_to_vector3_ad_proto(moment_center) if moment_center else None,
                )
            )
        else:
            raise ValueError("Invalid QuantityType.")

        if reference_values is not None:
            self.reference_values = reference_values

    def __repr__(self) -> str:
        return pformat(vars(self), compact=True, sort_dicts=True)


T = TypeVar("T")
U = TypeVar("U")


def _remove_from_list_with_warning(
    _list: list[T],
    _accessor: Callable[[T], U],
    _to_remove: U,
    _warning_message: Callable[[T], str],
) -> None:
    for i, e in reversed(list(enumerate(_list))):
        if _accessor(e) == _to_remove:
            logger.warning(_warning_message(e))
            _list.pop(i)


def _stringify_identifier(identifier: EntityIdentifier) -> str:
    if identifier.name:
        return f'"{identifier.name}" ({identifier.id})'
    else:
        return f"({identifier.id})"
