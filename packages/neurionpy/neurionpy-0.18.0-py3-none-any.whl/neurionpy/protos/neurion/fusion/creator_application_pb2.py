# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: neurion/fusion/creator_application.proto
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
    'neurion/fusion/creator_application.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(neurion/fusion/creator_application.proto\x12\x0eneurion.fusion\"\xf1\x01\n\x12\x43reatorApplication\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0f\n\x07\x63reator\x18\x02 \x01(\t\x12\x31\n\x06result\x18\x03 \x01(\x0e\x32!.neurion.fusion.ApplicationResult\x12\x1a\n\x12\x64\x65\x63ision_timestamp\x18\x04 \x01(\x04\x12\x16\n\x0e\x64\x65\x63ision_maker\x18\x05 \x01(\t\x12\x17\n\x0f\x64\x65\x63ision_reason\x18\x06 \x01(\t\x12\r\n\x05stake\x18\x07 \x01(\x04\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\x12\x1a\n\x12\x63reation_timestamp\x18\t \x01(\x04*\x9d\x01\n\x11\x41pplicationResult\x12$\n APPLICATION_RESULT_NOT_AVAILABLE\x10\x00\x12\x1f\n\x1b\x41PPLICATION_RESULT_ACCEPTED\x10\x01\x12\x1f\n\x1b\x41PPLICATION_RESULT_REJECTED\x10\x02\x12 \n\x1c\x41PPLICATION_RESULT_RECLAIMED\x10\x03\x42\x18Z\x16neurion/x/fusion/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'neurion.fusion.creator_application_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\026neurion/x/fusion/types'
  _globals['_APPLICATIONRESULT']._serialized_start=305
  _globals['_APPLICATIONRESULT']._serialized_end=462
  _globals['_CREATORAPPLICATION']._serialized_start=61
  _globals['_CREATORAPPLICATION']._serialized_end=302
# @@protoc_insertion_point(module_scope)
