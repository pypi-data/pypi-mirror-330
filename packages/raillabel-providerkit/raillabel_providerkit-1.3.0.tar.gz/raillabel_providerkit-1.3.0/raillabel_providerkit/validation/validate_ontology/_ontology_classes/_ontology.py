# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

import raillabel

from raillabel_providerkit.validation import Issue, IssueIdentifiers, IssueType
from raillabel_providerkit.validation.validate_ontology._ontology_classes._sensor_type import (
    _SensorType,
)

from ._object_classes import _ObjectClass


@dataclass
class _Ontology:
    classes: dict[str, _ObjectClass]
    errors: list[Issue]

    @classmethod
    def fromdict(cls, data: dict) -> _Ontology:
        return _Ontology(
            {class_id: _ObjectClass.fromdict(class_) for class_id, class_ in data.items()}, []
        )

    def check(self, scene: raillabel.Scene) -> list[Issue]:
        self.errors = []

        self._check_class_validity(scene)
        annotations = _Ontology._compile_annotations(scene)
        for annotation_uid, annotation, sensor_type, frame_id in annotations:
            annotation_class = scene.objects.get(annotation.object_id).type
            if annotation_class not in self.classes:
                continue

            object_type = scene.objects[annotation.object_id].type

            self.errors.extend(
                self.classes[annotation_class].check(
                    annotation_uid, annotation, sensor_type, frame_id, object_type
                )
            )

        return self.errors

    def _check_class_validity(self, scene: raillabel.Scene) -> None:
        for obj_uid, obj in scene.objects.items():
            object_class = obj.type
            if object_class not in self.classes:
                self.errors.append(
                    Issue(
                        type=IssueType.OBJECT_TYPE_UNDEFINED,
                        identifiers=IssueIdentifiers(object=obj_uid, object_type=object_class),
                    )
                )

    @classmethod
    def _compile_annotations(
        cls, scene: raillabel.Scene
    ) -> list[
        tuple[
            UUID,
            raillabel.format.Bbox
            | raillabel.format.Cuboid
            | raillabel.format.Poly2d
            | raillabel.format.Poly3d
            | raillabel.format.Seg3d,
            _SensorType,
            int,
        ]
    ]:
        annotations = []
        for frame_id, frame in scene.frames.items():
            for annotation_uid, annotation in frame.annotations.items():
                sensor_type_str = scene.sensors.get(annotation.sensor_id).TYPE

                sensor_type = None
                try:
                    sensor_type = _SensorType(sensor_type_str)
                except ValueError:
                    # NOTE: This would be detected by validate_schema
                    continue

                annotations.append(
                    (
                        annotation_uid,
                        annotation,
                        sensor_type,
                        frame_id,
                    )
                )

        return annotations
