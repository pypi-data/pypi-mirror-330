# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cometbft/types/v2/params.proto
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
    'cometbft/types/v2/params.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x63ometbft/types/v2/params.proto\x12\x11\x63ometbft.types.v2\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1egoogle/protobuf/wrappers.proto\"\xfa\x02\n\x0f\x43onsensusParams\x12-\n\x05\x62lock\x18\x01 \x01(\x0b\x32\x1e.cometbft.types.v2.BlockParams\x12\x33\n\x08\x65vidence\x18\x02 \x01(\x0b\x32!.cometbft.types.v2.EvidenceParams\x12\x35\n\tvalidator\x18\x03 \x01(\x0b\x32\".cometbft.types.v2.ValidatorParams\x12\x31\n\x07version\x18\x04 \x01(\x0b\x32 .cometbft.types.v2.VersionParams\x12/\n\x04\x61\x62\x63i\x18\x05 \x01(\x0b\x32\x1d.cometbft.types.v2.ABCIParamsB\x02\x18\x01\x12\x35\n\tsynchrony\x18\x06 \x01(\x0b\x32\".cometbft.types.v2.SynchronyParams\x12\x31\n\x07\x66\x65\x61ture\x18\x07 \x01(\x0b\x32 .cometbft.types.v2.FeatureParams\"7\n\x0b\x42lockParams\x12\x11\n\tmax_bytes\x18\x01 \x01(\x03\x12\x0f\n\x07max_gas\x18\x02 \x01(\x03J\x04\x08\x03\x10\x04\"~\n\x0e\x45videnceParams\x12\x1a\n\x12max_age_num_blocks\x18\x01 \x01(\x03\x12=\n\x10max_age_duration\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationB\x08\xc8\xde\x1f\x00\x98\xdf\x1f\x01\x12\x11\n\tmax_bytes\x18\x03 \x01(\x03\"2\n\x0fValidatorParams\x12\x15\n\rpub_key_types\x18\x01 \x03(\t:\x08\xb8\xa0\x1f\x01\xe8\xa0\x1f\x01\"&\n\rVersionParams\x12\x0b\n\x03\x61pp\x18\x01 \x01(\x04:\x08\xb8\xa0\x1f\x01\xe8\xa0\x1f\x01\">\n\x0cHashedParams\x12\x17\n\x0f\x62lock_max_bytes\x18\x01 \x01(\x03\x12\x15\n\rblock_max_gas\x18\x02 \x01(\x03\"}\n\x0fSynchronyParams\x12\x32\n\tprecision\x18\x01 \x01(\x0b\x32\x19.google.protobuf.DurationB\x04\x98\xdf\x1f\x01\x12\x36\n\rmessage_delay\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationB\x04\x98\xdf\x1f\x01\"\x98\x01\n\rFeatureParams\x12H\n\x1dvote_extensions_enable_height\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x04\xc8\xde\x1f\x01\x12=\n\x12pbts_enable_height\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x04\xc8\xde\x1f\x01\"7\n\nABCIParams\x12%\n\x1dvote_extensions_enable_height\x18\x01 \x01(\x03:\x02\x18\x01\x42\x38Z2github.com/cometbft/cometbft/api/cometbft/types/v2\xa8\xe2\x1e\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cometbft.types.v2.params_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z2github.com/cometbft/cometbft/api/cometbft/types/v2\250\342\036\001'
  _globals['_CONSENSUSPARAMS'].fields_by_name['abci']._loaded_options = None
  _globals['_CONSENSUSPARAMS'].fields_by_name['abci']._serialized_options = b'\030\001'
  _globals['_EVIDENCEPARAMS'].fields_by_name['max_age_duration']._loaded_options = None
  _globals['_EVIDENCEPARAMS'].fields_by_name['max_age_duration']._serialized_options = b'\310\336\037\000\230\337\037\001'
  _globals['_VALIDATORPARAMS']._loaded_options = None
  _globals['_VALIDATORPARAMS']._serialized_options = b'\270\240\037\001\350\240\037\001'
  _globals['_VERSIONPARAMS']._loaded_options = None
  _globals['_VERSIONPARAMS']._serialized_options = b'\270\240\037\001\350\240\037\001'
  _globals['_SYNCHRONYPARAMS'].fields_by_name['precision']._loaded_options = None
  _globals['_SYNCHRONYPARAMS'].fields_by_name['precision']._serialized_options = b'\230\337\037\001'
  _globals['_SYNCHRONYPARAMS'].fields_by_name['message_delay']._loaded_options = None
  _globals['_SYNCHRONYPARAMS'].fields_by_name['message_delay']._serialized_options = b'\230\337\037\001'
  _globals['_FEATUREPARAMS'].fields_by_name['vote_extensions_enable_height']._loaded_options = None
  _globals['_FEATUREPARAMS'].fields_by_name['vote_extensions_enable_height']._serialized_options = b'\310\336\037\001'
  _globals['_FEATUREPARAMS'].fields_by_name['pbts_enable_height']._loaded_options = None
  _globals['_FEATUREPARAMS'].fields_by_name['pbts_enable_height']._serialized_options = b'\310\336\037\001'
  _globals['_ABCIPARAMS']._loaded_options = None
  _globals['_ABCIPARAMS']._serialized_options = b'\030\001'
  _globals['_CONSENSUSPARAMS']._serialized_start=140
  _globals['_CONSENSUSPARAMS']._serialized_end=518
  _globals['_BLOCKPARAMS']._serialized_start=520
  _globals['_BLOCKPARAMS']._serialized_end=575
  _globals['_EVIDENCEPARAMS']._serialized_start=577
  _globals['_EVIDENCEPARAMS']._serialized_end=703
  _globals['_VALIDATORPARAMS']._serialized_start=705
  _globals['_VALIDATORPARAMS']._serialized_end=755
  _globals['_VERSIONPARAMS']._serialized_start=757
  _globals['_VERSIONPARAMS']._serialized_end=795
  _globals['_HASHEDPARAMS']._serialized_start=797
  _globals['_HASHEDPARAMS']._serialized_end=859
  _globals['_SYNCHRONYPARAMS']._serialized_start=861
  _globals['_SYNCHRONYPARAMS']._serialized_end=986
  _globals['_FEATUREPARAMS']._serialized_start=989
  _globals['_FEATUREPARAMS']._serialized_end=1141
  _globals['_ABCIPARAMS']._serialized_start=1143
  _globals['_ABCIPARAMS']._serialized_end=1198
# @@protoc_insertion_point(module_scope)
