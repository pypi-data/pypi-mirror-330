# Copyright DB InfraGO AG and contributors
# SPDX-License-Identifier: Apache-2.0

import pytest

from raillabel_providerkit.validation.validate_ontology._ontology_classes._scope import _Scope
from raillabel_providerkit.validation.validate_ontology._ontology_classes._attributes._multi_select_attribute import (
    _MultiSelectAttribute,
)
from raillabel_providerkit.validation import IssueIdentifiers, IssueType


def test_supports__empty_dict():
    assert not _MultiSelectAttribute.supports({})


def test_supports__correct(example_multi_select_attribute_dict):
    assert _MultiSelectAttribute.supports(example_multi_select_attribute_dict)


def test_supports__invalid_type_string(example_string_attribute_dict):
    assert not _MultiSelectAttribute.supports(example_string_attribute_dict)


def test_supports__invalid_type_dict(example_single_select_attribute_dict):
    assert not _MultiSelectAttribute.supports(example_single_select_attribute_dict)


def test_fromdict__empty():
    with pytest.raises(ValueError):
        _MultiSelectAttribute.fromdict({})


def test_fromdict__optional(example_multi_select_attribute_dict):
    for val in [False, True]:
        example_multi_select_attribute_dict["optional"] = val
        assert _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict).optional == val


def test_fromdict__scope_invalid(example_multi_select_attribute_dict):
    with pytest.raises(ValueError):
        example_multi_select_attribute_dict["scope"] = "some random string"
        _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict)


def test_fromdict__scope_empty(example_multi_select_attribute_dict):
    del example_multi_select_attribute_dict["scope"]
    assert (
        _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict).scope
        == _Scope.ANNOTATION
    )


def test_fromdict__scope_annotation(example_multi_select_attribute_dict):
    example_multi_select_attribute_dict["scope"] = "annotation"
    assert (
        _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict).scope
        == _Scope.ANNOTATION
    )


def test_fromdict__scope_frame(example_multi_select_attribute_dict):
    example_multi_select_attribute_dict["scope"] = "frame"
    assert _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict).scope == _Scope.FRAME


def test_fromdict__scope_object(example_multi_select_attribute_dict):
    example_multi_select_attribute_dict["scope"] = "object"
    assert _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict).scope == _Scope.OBJECT


def test_check_type_and_value__wrong_type(example_multi_select_attribute_dict):
    attr = _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict)
    errors = attr.check_type_and_value("example_name", 42, IssueIdentifiers())
    assert len(errors) == 1
    assert errors[0].type == IssueType.ATTRIBUTE_TYPE


def test_check_type_and_value__wrong_value(example_multi_select_attribute_dict):
    attr = _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict)
    errors = attr.check_type_and_value("example_name", ["some invalid string"], IssueIdentifiers())
    assert len(errors) == 1
    assert errors[0].type == IssueType.ATTRIBUTE_VALUE


def test_check_type_and_value__correct(example_multi_select_attribute_dict):
    attr = _MultiSelectAttribute.fromdict(example_multi_select_attribute_dict)
    assert attr.check_type_and_value("example_name", ["foo"], IssueIdentifiers()) == []
