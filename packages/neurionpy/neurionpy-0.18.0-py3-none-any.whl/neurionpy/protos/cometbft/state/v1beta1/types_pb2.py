# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cometbft/state/v1beta1/types.proto
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
    'cometbft/state/v1beta1/types.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cometbft.abci.v1beta1 import types_pb2 as cometbft_dot_abci_dot_v1beta1_dot_types__pb2
from cometbft.types.v1beta1 import types_pb2 as cometbft_dot_types_dot_v1beta1_dot_types__pb2
from cometbft.types.v1beta1 import validator_pb2 as cometbft_dot_types_dot_v1beta1_dot_validator__pb2
from cometbft.types.v1beta1 import params_pb2 as cometbft_dot_types_dot_v1beta1_dot_params__pb2
from cometbft.version.v1 import types_pb2 as cometbft_dot_version_dot_v1_dot_types__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"cometbft/state/v1beta1/types.proto\x12\x16\x63ometbft.state.v1beta1\x1a\x14gogoproto/gogo.proto\x1a!cometbft/abci/v1beta1/types.proto\x1a\"cometbft/types/v1beta1/types.proto\x1a&cometbft/types/v1beta1/validator.proto\x1a#cometbft/types/v1beta1/params.proto\x1a\x1f\x63ometbft/version/v1/types.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xca\x01\n\rABCIResponses\x12=\n\x0b\x64\x65liver_txs\x18\x01 \x03(\x0b\x32(.cometbft.abci.v1beta1.ResponseDeliverTx\x12:\n\tend_block\x18\x02 \x01(\x0b\x32\'.cometbft.abci.v1beta1.ResponseEndBlock\x12>\n\x0b\x62\x65gin_block\x18\x03 \x01(\x0b\x32).cometbft.abci.v1beta1.ResponseBeginBlock\"j\n\x0eValidatorsInfo\x12;\n\rvalidator_set\x18\x01 \x01(\x0b\x32$.cometbft.types.v1beta1.ValidatorSet\x12\x1b\n\x13last_height_changed\x18\x02 \x01(\x03\"{\n\x13\x43onsensusParamsInfo\x12G\n\x10\x63onsensus_params\x18\x01 \x01(\x0b\x32\'.cometbft.types.v1beta1.ConsensusParamsB\x04\xc8\xde\x1f\x00\x12\x1b\n\x13last_height_changed\x18\x02 \x01(\x03\"b\n\x11\x41\x42\x43IResponsesInfo\x12=\n\x0e\x61\x62\x63i_responses\x18\x01 \x01(\x0b\x32%.cometbft.state.v1beta1.ABCIResponses\x12\x0e\n\x06height\x18\x02 \x01(\x03\"T\n\x07Version\x12\x37\n\tconsensus\x18\x01 \x01(\x0b\x32\x1e.cometbft.version.v1.ConsensusB\x04\xc8\xde\x1f\x00\x12\x10\n\x08software\x18\x02 \x01(\t\"\xa1\x05\n\x05State\x12\x36\n\x07version\x18\x01 \x01(\x0b\x32\x1f.cometbft.state.v1beta1.VersionB\x04\xc8\xde\x1f\x00\x12\x1d\n\x08\x63hain_id\x18\x02 \x01(\tB\x0b\xe2\xde\x1f\x07\x43hainID\x12\x16\n\x0einitial_height\x18\x0e \x01(\x03\x12\x19\n\x11last_block_height\x18\x03 \x01(\x03\x12K\n\rlast_block_id\x18\x04 \x01(\x0b\x32\x1f.cometbft.types.v1beta1.BlockIDB\x13\xc8\xde\x1f\x00\xe2\xde\x1f\x0bLastBlockID\x12=\n\x0flast_block_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12=\n\x0fnext_validators\x18\x06 \x01(\x0b\x32$.cometbft.types.v1beta1.ValidatorSet\x12\x38\n\nvalidators\x18\x07 \x01(\x0b\x32$.cometbft.types.v1beta1.ValidatorSet\x12=\n\x0flast_validators\x18\x08 \x01(\x0b\x32$.cometbft.types.v1beta1.ValidatorSet\x12&\n\x1elast_height_validators_changed\x18\t \x01(\x03\x12G\n\x10\x63onsensus_params\x18\n \x01(\x0b\x32\'.cometbft.types.v1beta1.ConsensusParamsB\x04\xc8\xde\x1f\x00\x12,\n$last_height_consensus_params_changed\x18\x0b \x01(\x03\x12\x19\n\x11last_results_hash\x18\x0c \x01(\x0c\x12\x10\n\x08\x61pp_hash\x18\r \x01(\x0c\x42\x39Z7github.com/cometbft/cometbft/api/cometbft/state/v1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cometbft.state.v1beta1.types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/cometbft/cometbft/api/cometbft/state/v1beta1'
  _globals['_CONSENSUSPARAMSINFO'].fields_by_name['consensus_params']._loaded_options = None
  _globals['_CONSENSUSPARAMSINFO'].fields_by_name['consensus_params']._serialized_options = b'\310\336\037\000'
  _globals['_VERSION'].fields_by_name['consensus']._loaded_options = None
  _globals['_VERSION'].fields_by_name['consensus']._serialized_options = b'\310\336\037\000'
  _globals['_STATE'].fields_by_name['version']._loaded_options = None
  _globals['_STATE'].fields_by_name['version']._serialized_options = b'\310\336\037\000'
  _globals['_STATE'].fields_by_name['chain_id']._loaded_options = None
  _globals['_STATE'].fields_by_name['chain_id']._serialized_options = b'\342\336\037\007ChainID'
  _globals['_STATE'].fields_by_name['last_block_id']._loaded_options = None
  _globals['_STATE'].fields_by_name['last_block_id']._serialized_options = b'\310\336\037\000\342\336\037\013LastBlockID'
  _globals['_STATE'].fields_by_name['last_block_time']._loaded_options = None
  _globals['_STATE'].fields_by_name['last_block_time']._serialized_options = b'\310\336\037\000\220\337\037\001'
  _globals['_STATE'].fields_by_name['consensus_params']._loaded_options = None
  _globals['_STATE'].fields_by_name['consensus_params']._serialized_options = b'\310\336\037\000'
  _globals['_ABCIRESPONSES']._serialized_start=299
  _globals['_ABCIRESPONSES']._serialized_end=501
  _globals['_VALIDATORSINFO']._serialized_start=503
  _globals['_VALIDATORSINFO']._serialized_end=609
  _globals['_CONSENSUSPARAMSINFO']._serialized_start=611
  _globals['_CONSENSUSPARAMSINFO']._serialized_end=734
  _globals['_ABCIRESPONSESINFO']._serialized_start=736
  _globals['_ABCIRESPONSESINFO']._serialized_end=834
  _globals['_VERSION']._serialized_start=836
  _globals['_VERSION']._serialized_end=920
  _globals['_STATE']._serialized_start=923
  _globals['_STATE']._serialized_end=1596
# @@protoc_insertion_point(module_scope)
