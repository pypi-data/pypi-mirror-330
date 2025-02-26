# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cosmos/vesting/v1beta1/vesting.proto
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
    'cosmos/vesting/v1beta1/vesting.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from cosmos.auth.v1beta1 import auth_pb2 as cosmos_dot_auth_dot_v1beta1_dot_auth__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$cosmos/vesting/v1beta1/vesting.proto\x12\x16\x63osmos.vesting.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x1e\x63osmos/auth/v1beta1/auth.proto\"\x89\x04\n\x12\x42\x61seVestingAccount\x12<\n\x0c\x62\x61se_account\x18\x01 \x01(\x0b\x32 .cosmos.auth.v1beta1.BaseAccountB\x04\xd0\xde\x1f\x01\x12\x80\x01\n\x10original_vesting\x18\x02 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBK\xc8\xde\x1f\x00\xf2\xde\x1f\x17yaml:\"original_vesting\"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12|\n\x0e\x64\x65legated_free\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBI\xc8\xde\x1f\x00\xf2\xde\x1f\x15yaml:\"delegated_free\"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\x82\x01\n\x11\x64\x65legated_vesting\x18\x04 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBL\xc8\xde\x1f\x00\xf2\xde\x1f\x18yaml:\"delegated_vesting\"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12%\n\x08\x65nd_time\x18\x05 \x01(\x03\x42\x13\xf2\xde\x1f\x0fyaml:\"end_time\":\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00\"\x9f\x01\n\x18\x43ontinuousVestingAccount\x12N\n\x14\x62\x61se_vesting_account\x18\x01 \x01(\x0b\x32*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01\x12)\n\nstart_time\x18\x02 \x01(\x03\x42\x15\xf2\xde\x1f\x11yaml:\"start_time\":\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00\"q\n\x15\x44\x65layedVestingAccount\x12N\n\x14\x62\x61se_vesting_account\x18\x01 \x01(\x0b\x32*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01:\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00\"{\n\x06Period\x12\x0e\n\x06length\x18\x01 \x01(\x03\x12[\n\x06\x61mount\x18\x02 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:\x04\x98\xa0\x1f\x00\"\xf6\x01\n\x16PeriodicVestingAccount\x12N\n\x14\x62\x61se_vesting_account\x18\x01 \x01(\x0b\x32*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01\x12)\n\nstart_time\x18\x02 \x01(\x03\x42\x15\xf2\xde\x1f\x11yaml:\"start_time\"\x12W\n\x0fvesting_periods\x18\x03 \x03(\x0b\x32\x1e.cosmos.vesting.v1beta1.PeriodB\x1e\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:\"vesting_periods\":\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00\"r\n\x16PermanentLockedAccount\x12N\n\x14\x62\x61se_vesting_account\x18\x01 \x01(\x0b\x32*.cosmos.vesting.v1beta1.BaseVestingAccountB\x04\xd0\xde\x1f\x01:\x08\x88\xa0\x1f\x00\x98\xa0\x1f\x00\x42\x33Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.vesting.v1beta1.vesting_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z1github.com/cosmos/cosmos-sdk/x/auth/vesting/types'
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['base_account']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['base_account']._serialized_options = b'\320\336\037\001'
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['original_vesting']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['original_vesting']._serialized_options = b'\310\336\037\000\362\336\037\027yaml:\"original_vesting\"\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['delegated_free']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['delegated_free']._serialized_options = b'\310\336\037\000\362\336\037\025yaml:\"delegated_free\"\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['delegated_vesting']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['delegated_vesting']._serialized_options = b'\310\336\037\000\362\336\037\030yaml:\"delegated_vesting\"\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['end_time']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT'].fields_by_name['end_time']._serialized_options = b'\362\336\037\017yaml:\"end_time\"'
  _globals['_BASEVESTINGACCOUNT']._loaded_options = None
  _globals['_BASEVESTINGACCOUNT']._serialized_options = b'\210\240\037\000\230\240\037\000'
  _globals['_CONTINUOUSVESTINGACCOUNT'].fields_by_name['base_vesting_account']._loaded_options = None
  _globals['_CONTINUOUSVESTINGACCOUNT'].fields_by_name['base_vesting_account']._serialized_options = b'\320\336\037\001'
  _globals['_CONTINUOUSVESTINGACCOUNT'].fields_by_name['start_time']._loaded_options = None
  _globals['_CONTINUOUSVESTINGACCOUNT'].fields_by_name['start_time']._serialized_options = b'\362\336\037\021yaml:\"start_time\"'
  _globals['_CONTINUOUSVESTINGACCOUNT']._loaded_options = None
  _globals['_CONTINUOUSVESTINGACCOUNT']._serialized_options = b'\210\240\037\000\230\240\037\000'
  _globals['_DELAYEDVESTINGACCOUNT'].fields_by_name['base_vesting_account']._loaded_options = None
  _globals['_DELAYEDVESTINGACCOUNT'].fields_by_name['base_vesting_account']._serialized_options = b'\320\336\037\001'
  _globals['_DELAYEDVESTINGACCOUNT']._loaded_options = None
  _globals['_DELAYEDVESTINGACCOUNT']._serialized_options = b'\210\240\037\000\230\240\037\000'
  _globals['_PERIOD'].fields_by_name['amount']._loaded_options = None
  _globals['_PERIOD'].fields_by_name['amount']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _globals['_PERIOD']._loaded_options = None
  _globals['_PERIOD']._serialized_options = b'\230\240\037\000'
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['base_vesting_account']._loaded_options = None
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['base_vesting_account']._serialized_options = b'\320\336\037\001'
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['start_time']._loaded_options = None
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['start_time']._serialized_options = b'\362\336\037\021yaml:\"start_time\"'
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['vesting_periods']._loaded_options = None
  _globals['_PERIODICVESTINGACCOUNT'].fields_by_name['vesting_periods']._serialized_options = b'\310\336\037\000\362\336\037\026yaml:\"vesting_periods\"'
  _globals['_PERIODICVESTINGACCOUNT']._loaded_options = None
  _globals['_PERIODICVESTINGACCOUNT']._serialized_options = b'\210\240\037\000\230\240\037\000'
  _globals['_PERMANENTLOCKEDACCOUNT'].fields_by_name['base_vesting_account']._loaded_options = None
  _globals['_PERMANENTLOCKEDACCOUNT'].fields_by_name['base_vesting_account']._serialized_options = b'\320\336\037\001'
  _globals['_PERMANENTLOCKEDACCOUNT']._loaded_options = None
  _globals['_PERMANENTLOCKEDACCOUNT']._serialized_options = b'\210\240\037\000\230\240\037\000'
  _globals['_BASEVESTINGACCOUNT']._serialized_start=151
  _globals['_BASEVESTINGACCOUNT']._serialized_end=672
  _globals['_CONTINUOUSVESTINGACCOUNT']._serialized_start=675
  _globals['_CONTINUOUSVESTINGACCOUNT']._serialized_end=834
  _globals['_DELAYEDVESTINGACCOUNT']._serialized_start=836
  _globals['_DELAYEDVESTINGACCOUNT']._serialized_end=949
  _globals['_PERIOD']._serialized_start=951
  _globals['_PERIOD']._serialized_end=1074
  _globals['_PERIODICVESTINGACCOUNT']._serialized_start=1077
  _globals['_PERIODICVESTINGACCOUNT']._serialized_end=1323
  _globals['_PERMANENTLOCKEDACCOUNT']._serialized_start=1325
  _globals['_PERMANENTLOCKEDACCOUNT']._serialized_end=1439
# @@protoc_insertion_point(module_scope)
