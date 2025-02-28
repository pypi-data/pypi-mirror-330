"""Root of the mastapy package."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private._0 import APIBase
    from mastapy._private._1 import Initialiser
    from mastapy._private._2 import LegacyV2RuntimeActivationPolicyAttributeSetter
    from mastapy._private._3 import PythonUtility
    from mastapy._private._4 import UtilityMethods
    from mastapy._private._5 import Versioning
    from mastapy._private._7711 import ConsoleProgress
    from mastapy._private._7712 import MarshalByRefObjectPermanent
    from mastapy._private._7713 import MarshalByRefObjects
    from mastapy._private._7714 import EnvironmentVariableUtility
    from mastapy._private._7715 import Remoting
    from mastapy._private._7716 import ScriptedPropertyNameAttribute
    from mastapy._private._7717 import SimpleTaskProgress
    from mastapy._private._7718 import TaskProgress
    from mastapy._private._internal import (
        AssemblyLoadError,
        CastException,
        Examples,
        ListWithSelectedItem,
        MastaInitException,
        MastaPropertyException,
        MastaPropertyTypeException,
        MastapyImportException,
        MeasurementType,
        TupleWithName,
        TypeCheckException,
        UnavailableMethodError,
        __api_version__,
        __version__,
        init,
        masta_after,
        masta_before,
        masta_licences,
        masta_property,
        overridable,
    )
    from mastapy._private._math import (
        Color,
        Long,
        Matrix2x2,
        Matrix3x3,
        Matrix4x4,
        MatrixException,
        Vector2D,
        Vector3D,
        Vector4D,
        VectorException,
        approximately_equal,
        clamp,
        fract,
        sign,
        smoothstep,
        step,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private._internal": [
            "MastaInitException",
            "MastaPropertyException",
            "MastaPropertyTypeException",
            "masta_property",
            "masta_before",
            "masta_after",
            "init",
            "__version__",
            "__api_version__",
            "TupleWithName",
            "CastException",
            "MastapyImportException",
            "overridable",
            "MeasurementType",
            "TypeCheckException",
            "masta_licences",
            "AssemblyLoadError",
            "UnavailableMethodError",
            "Examples",
            "ListWithSelectedItem",
        ],
        "_private._math": [
            "clamp",
            "sign",
            "fract",
            "step",
            "smoothstep",
            "approximately_equal",
            "Long",
            "Vector2D",
            "Vector3D",
            "Vector4D",
            "Color",
            "VectorException",
            "Matrix2x2",
            "Matrix3x3",
            "Matrix4x4",
            "MatrixException",
        ],
        "_private._0": ["APIBase"],
        "_private._1": ["Initialiser"],
        "_private._2": ["LegacyV2RuntimeActivationPolicyAttributeSetter"],
        "_private._3": ["PythonUtility"],
        "_private._4": ["UtilityMethods"],
        "_private._5": ["Versioning"],
        "_private._7711": ["ConsoleProgress"],
        "_private._7712": ["MarshalByRefObjectPermanent"],
        "_private._7713": ["MarshalByRefObjects"],
        "_private._7714": ["EnvironmentVariableUtility"],
        "_private._7715": ["Remoting"],
        "_private._7716": ["ScriptedPropertyNameAttribute"],
        "_private._7717": ["SimpleTaskProgress"],
        "_private._7718": ["TaskProgress"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

    from mastapy._private._internal import mastafile_hook as __mh

    __mh()


__all__ = (
    "MastaInitException",
    "MastaPropertyException",
    "MastaPropertyTypeException",
    "masta_property",
    "masta_before",
    "masta_after",
    "init",
    "__version__",
    "__api_version__",
    "TupleWithName",
    "CastException",
    "MastapyImportException",
    "overridable",
    "MeasurementType",
    "TypeCheckException",
    "masta_licences",
    "AssemblyLoadError",
    "UnavailableMethodError",
    "Examples",
    "ListWithSelectedItem",
    "clamp",
    "sign",
    "fract",
    "step",
    "smoothstep",
    "approximately_equal",
    "Long",
    "Vector2D",
    "Vector3D",
    "Vector4D",
    "Color",
    "VectorException",
    "Matrix2x2",
    "Matrix3x3",
    "Matrix4x4",
    "MatrixException",
    "APIBase",
    "Initialiser",
    "LegacyV2RuntimeActivationPolicyAttributeSetter",
    "PythonUtility",
    "UtilityMethods",
    "Versioning",
    "ConsoleProgress",
    "MarshalByRefObjectPermanent",
    "MarshalByRefObjects",
    "EnvironmentVariableUtility",
    "Remoting",
    "ScriptedPropertyNameAttribute",
    "SimpleTaskProgress",
    "TaskProgress",
)
