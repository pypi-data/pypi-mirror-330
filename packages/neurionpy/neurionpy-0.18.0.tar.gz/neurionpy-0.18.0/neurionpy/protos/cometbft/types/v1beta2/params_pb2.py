# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cometbft/types/v1beta2/params.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'cometbft/types/v1beta2/params.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cometbft.types.v1beta1 import params_pb2 as cometbft_dot_types_dot_v1beta1_dot_params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#cometbft/types/v1beta2/params.proto\x12\x16\x63ometbft.types.v1beta2\x1a\x14gogoproto/gogo.proto\x1a#cometbft/types/v1beta1/params.proto\"\xf3\x01\n\x0f\x43onsensusParams\x12\x32\n\x05\x62lock\x18\x01 \x01(\x0b\x32#.cometbft.types.v1beta2.BlockParams\x12\x38\n\x08\x65vidence\x18\x02 \x01(\x0b\x32&.cometbft.types.v1beta1.EvidenceParams\x12:\n\tvalidator\x18\x03 \x01(\x0b\x32\'.cometbft.types.v1beta1.ValidatorParams\x12\x36\n\x07version\x18\x04 \x01(\x0b\x32%.cometbft.types.v1beta1.VersionParams\"7\n\x0b\x42lockParams\x12\x11\n\tmax_bytes\x18\x01 \x01(\x03\x12\x0f\n\x07max_gas\x18\x02 \x01(\x03J\x04\x08\x03\x10\x04\x42=Z7github.com/cometbft/cometbft/api/cometbft/types/v1beta2\xa8\xe2\x1e\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cometbft.types.v1beta2.params_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/cometbft/cometbft/api/cometbft/types/v1beta2\250\342\036\001'
  _globals['_CONSENSUSPARAMS']._serialized_start=123
  _globals['_CONSENSUSPARAMS']._serialized_end=366
  _globals['_BLOCKPARAMS']._serialized_start=368
  _globals['_BLOCKPARAMS']._serialized_end=423
# @@protoc_insertion_point(module_scope)
