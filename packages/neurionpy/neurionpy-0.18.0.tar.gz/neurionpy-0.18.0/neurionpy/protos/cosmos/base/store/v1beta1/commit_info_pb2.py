# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cosmos/base/store/v1beta1/commit_info.proto
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
    'cosmos/base/store/v1beta1/commit_info.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+cosmos/base/store/v1beta1/commit_info.proto\x12\x19\x63osmos.base.store.v1beta1\x1a\x14gogoproto/gogo.proto\"^\n\nCommitInfo\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12?\n\x0bstore_infos\x18\x02 \x03(\x0b\x32$.cosmos.base.store.v1beta1.StoreInfoB\x04\xc8\xde\x1f\x00\"W\n\tStoreInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12<\n\tcommit_id\x18\x02 \x01(\x0b\x32#.cosmos.base.store.v1beta1.CommitIDB\x04\xc8\xde\x1f\x00\"/\n\x08\x43ommitID\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12\x0c\n\x04hash\x18\x02 \x01(\x0c:\x04\x98\xa0\x1f\x00\x42*Z(github.com/cosmos/cosmos-sdk/store/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.store.v1beta1.commit_info_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z(github.com/cosmos/cosmos-sdk/store/types'
  _globals['_COMMITINFO'].fields_by_name['store_infos']._loaded_options = None
  _globals['_COMMITINFO'].fields_by_name['store_infos']._serialized_options = b'\310\336\037\000'
  _globals['_STOREINFO'].fields_by_name['commit_id']._loaded_options = None
  _globals['_STOREINFO'].fields_by_name['commit_id']._serialized_options = b'\310\336\037\000'
  _globals['_COMMITID']._loaded_options = None
  _globals['_COMMITID']._serialized_options = b'\230\240\037\000'
  _globals['_COMMITINFO']._serialized_start=96
  _globals['_COMMITINFO']._serialized_end=190
  _globals['_STOREINFO']._serialized_start=192
  _globals['_STOREINFO']._serialized_end=279
  _globals['_COMMITID']._serialized_start=281
  _globals['_COMMITID']._serialized_end=328
# @@protoc_insertion_point(module_scope)
