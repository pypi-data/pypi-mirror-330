# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cosmos/bank/v1beta1/tx.proto
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
    'cosmos/bank/v1beta1/tx.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from cosmos.bank.v1beta1 import bank_pb2 as cosmos_dot_bank_dot_v1beta1_dot_bank__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1c\x63osmos/bank/v1beta1/tx.proto\x12\x13\x63osmos.bank.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x1e\x63osmos/bank/v1beta1/bank.proto\"\xca\x01\n\x07MsgSend\x12-\n\x0c\x66rom_address\x18\x01 \x01(\tB\x17\xf2\xde\x1f\x13yaml:\"from_address\"\x12)\n\nto_address\x18\x02 \x01(\tB\x15\xf2\xde\x1f\x11yaml:\"to_address\"\x12[\n\x06\x61mount\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\x08\x88\xa0\x1f\x00\xe8\xa0\x1f\x00\"\x11\n\x0fMsgSendResponse\"z\n\x0cMsgMultiSend\x12\x30\n\x06inputs\x18\x01 \x03(\x0b\x32\x1a.cosmos.bank.v1beta1.InputB\x04\xc8\xde\x1f\x00\x12\x32\n\x07outputs\x18\x02 \x03(\x0b\x32\x1b.cosmos.bank.v1beta1.OutputB\x04\xc8\xde\x1f\x00:\x04\xe8\xa0\x1f\x00\"\x16\n\x14MsgMultiSendResponse2\xac\x01\n\x03Msg\x12J\n\x04Send\x12\x1c.cosmos.bank.v1beta1.MsgSend\x1a$.cosmos.bank.v1beta1.MsgSendResponse\x12Y\n\tMultiSend\x12!.cosmos.bank.v1beta1.MsgMultiSend\x1a).cosmos.bank.v1beta1.MsgMultiSendResponseB+Z)github.com/cosmos/cosmos-sdk/x/bank/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.bank.v1beta1.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/bank/types'
  _globals['_MSGSEND'].fields_by_name['from_address']._loaded_options = None
  _globals['_MSGSEND'].fields_by_name['from_address']._serialized_options = b'\362\336\037\023yaml:\"from_address\"'
  _globals['_MSGSEND'].fields_by_name['to_address']._loaded_options = None
  _globals['_MSGSEND'].fields_by_name['to_address']._serialized_options = b'\362\336\037\021yaml:\"to_address\"'
  _globals['_MSGSEND'].fields_by_name['amount']._loaded_options = None
  _globals['_MSGSEND'].fields_by_name['amount']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _globals['_MSGSEND']._loaded_options = None
  _globals['_MSGSEND']._serialized_options = b'\210\240\037\000\350\240\037\000'
  _globals['_MSGMULTISEND'].fields_by_name['inputs']._loaded_options = None
  _globals['_MSGMULTISEND'].fields_by_name['inputs']._serialized_options = b'\310\336\037\000'
  _globals['_MSGMULTISEND'].fields_by_name['outputs']._loaded_options = None
  _globals['_MSGMULTISEND'].fields_by_name['outputs']._serialized_options = b'\310\336\037\000'
  _globals['_MSGMULTISEND']._loaded_options = None
  _globals['_MSGMULTISEND']._serialized_options = b'\350\240\037\000'
  _globals['_MSGSEND']._serialized_start=140
  _globals['_MSGSEND']._serialized_end=342
  _globals['_MSGSENDRESPONSE']._serialized_start=344
  _globals['_MSGSENDRESPONSE']._serialized_end=361
  _globals['_MSGMULTISEND']._serialized_start=363
  _globals['_MSGMULTISEND']._serialized_end=485
  _globals['_MSGMULTISENDRESPONSE']._serialized_start=487
  _globals['_MSGMULTISENDRESPONSE']._serialized_end=509
  _globals['_MSG']._serialized_start=512
  _globals['_MSG']._serialized_end=684
# @@protoc_insertion_point(module_scope)
