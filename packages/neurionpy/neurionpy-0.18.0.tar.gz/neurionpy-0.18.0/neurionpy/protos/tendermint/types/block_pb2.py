# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tendermint/types/block.proto
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
    'tendermint/types/block.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from tendermint.types import types_pb2 as tendermint_dot_types_dot_types__pb2
from tendermint.types import evidence_pb2 as tendermint_dot_types_dot_evidence__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ctendermint/types/block.proto\x12\x10tendermint.types\x1a\x14gogoproto/gogo.proto\x1a\x1ctendermint/types/types.proto\x1a\x1ftendermint/types/evidence.proto\"\xca\x01\n\x05\x42lock\x12.\n\x06header\x18\x01 \x01(\x0b\x32\x18.tendermint.types.HeaderB\x04\xc8\xde\x1f\x00\x12*\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x16.tendermint.types.DataB\x04\xc8\xde\x1f\x00\x12\x36\n\x08\x65vidence\x18\x03 \x01(\x0b\x32\x1e.tendermint.types.EvidenceListB\x04\xc8\xde\x1f\x00\x12-\n\x0blast_commit\x18\x04 \x01(\x0b\x32\x18.tendermint.types.CommitB9Z7github.com/tendermint/tendermint/proto/tendermint/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tendermint.types.block_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/tendermint/tendermint/proto/tendermint/types'
  _globals['_BLOCK'].fields_by_name['header']._loaded_options = None
  _globals['_BLOCK'].fields_by_name['header']._serialized_options = b'\310\336\037\000'
  _globals['_BLOCK'].fields_by_name['data']._loaded_options = None
  _globals['_BLOCK'].fields_by_name['data']._serialized_options = b'\310\336\037\000'
  _globals['_BLOCK'].fields_by_name['evidence']._loaded_options = None
  _globals['_BLOCK'].fields_by_name['evidence']._serialized_options = b'\310\336\037\000'
  _globals['_BLOCK']._serialized_start=136
  _globals['_BLOCK']._serialized_end=338
# @@protoc_insertion_point(module_scope)
