from tracdap.rt._impl.grpc.tracdap.metadata import object_id_pb2 as _object_id_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import object_pb2 as _object_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESOURCE_TYPE_NOT_SET: _ClassVar[ResourceType]
    MODEL_REPOSITORY: _ClassVar[ResourceType]
    INTERNAL_STORAGE: _ClassVar[ResourceType]
RESOURCE_TYPE_NOT_SET: ResourceType
MODEL_REPOSITORY: ResourceType
INTERNAL_STORAGE: ResourceType
