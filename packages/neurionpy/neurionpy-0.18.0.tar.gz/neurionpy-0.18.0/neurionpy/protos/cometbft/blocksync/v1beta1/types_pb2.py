# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cometbft/blocksync/v1beta1/types.proto
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
    'cometbft/blocksync/v1beta1/types.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cometbft.types.v1beta1 import block_pb2 as cometbft_dot_types_dot_v1beta1_dot_block__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&cometbft/blocksync/v1beta1/types.proto\x12\x1a\x63ometbft.blocksync.v1beta1\x1a\"cometbft/types/v1beta1/block.proto\"\x1e\n\x0c\x42lockRequest\x12\x0e\n\x06height\x18\x01 \x01(\x03\"!\n\x0fNoBlockResponse\x12\x0e\n\x06height\x18\x01 \x01(\x03\"=\n\rBlockResponse\x12,\n\x05\x62lock\x18\x01 \x01(\x0b\x32\x1d.cometbft.types.v1beta1.Block\"\x0f\n\rStatusRequest\".\n\x0eStatusResponse\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12\x0c\n\x04\x62\x61se\x18\x02 \x01(\x03\"\xee\x02\n\x07Message\x12\x41\n\rblock_request\x18\x01 \x01(\x0b\x32(.cometbft.blocksync.v1beta1.BlockRequestH\x00\x12H\n\x11no_block_response\x18\x02 \x01(\x0b\x32+.cometbft.blocksync.v1beta1.NoBlockResponseH\x00\x12\x43\n\x0e\x62lock_response\x18\x03 \x01(\x0b\x32).cometbft.blocksync.v1beta1.BlockResponseH\x00\x12\x43\n\x0estatus_request\x18\x04 \x01(\x0b\x32).cometbft.blocksync.v1beta1.StatusRequestH\x00\x12\x45\n\x0fstatus_response\x18\x05 \x01(\x0b\x32*.cometbft.blocksync.v1beta1.StatusResponseH\x00\x42\x05\n\x03sumB=Z;github.com/cometbft/cometbft/api/cometbft/blocksync/v1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cometbft.blocksync.v1beta1.types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/cometbft/cometbft/api/cometbft/blocksync/v1beta1'
  _globals['_BLOCKREQUEST']._serialized_start=106
  _globals['_BLOCKREQUEST']._serialized_end=136
  _globals['_NOBLOCKRESPONSE']._serialized_start=138
  _globals['_NOBLOCKRESPONSE']._serialized_end=171
  _globals['_BLOCKRESPONSE']._serialized_start=173
  _globals['_BLOCKRESPONSE']._serialized_end=234
  _globals['_STATUSREQUEST']._serialized_start=236
  _globals['_STATUSREQUEST']._serialized_end=251
  _globals['_STATUSRESPONSE']._serialized_start=253
  _globals['_STATUSRESPONSE']._serialized_end=299
  _globals['_MESSAGE']._serialized_start=302
  _globals['_MESSAGE']._serialized_end=668
# @@protoc_insertion_point(module_scope)
