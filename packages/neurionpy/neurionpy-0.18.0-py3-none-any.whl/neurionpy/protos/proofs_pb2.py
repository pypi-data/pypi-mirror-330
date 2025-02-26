# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proofs.proto
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
    'proofs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cproofs.proto\x12\x05ics23\"g\n\x0e\x45xistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x1b\n\x04leaf\x18\x03 \x01(\x0b\x32\r.ics23.LeafOp\x12\x1c\n\x04path\x18\x04 \x03(\x0b\x32\x0e.ics23.InnerOp\"k\n\x11NonExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12#\n\x04left\x18\x02 \x01(\x0b\x32\x15.ics23.ExistenceProof\x12$\n\x05right\x18\x03 \x01(\x0b\x32\x15.ics23.ExistenceProof\"\xc7\x01\n\x0f\x43ommitmentProof\x12&\n\x05\x65xist\x18\x01 \x01(\x0b\x32\x15.ics23.ExistenceProofH\x00\x12,\n\x08nonexist\x18\x02 \x01(\x0b\x32\x18.ics23.NonExistenceProofH\x00\x12\"\n\x05\x62\x61tch\x18\x03 \x01(\x0b\x32\x11.ics23.BatchProofH\x00\x12\x31\n\ncompressed\x18\x04 \x01(\x0b\x32\x1b.ics23.CompressedBatchProofH\x00\x42\x07\n\x05proof\"\xa0\x01\n\x06LeafOp\x12\x1b\n\x04hash\x18\x01 \x01(\x0e\x32\r.ics23.HashOp\x12\"\n\x0bprehash_key\x18\x02 \x01(\x0e\x32\r.ics23.HashOp\x12$\n\rprehash_value\x18\x03 \x01(\x0e\x32\r.ics23.HashOp\x12\x1f\n\x06length\x18\x04 \x01(\x0e\x32\x0f.ics23.LengthOp\x12\x0e\n\x06prefix\x18\x05 \x01(\x0c\"F\n\x07InnerOp\x12\x1b\n\x04hash\x18\x01 \x01(\x0e\x32\r.ics23.HashOp\x12\x0e\n\x06prefix\x18\x02 \x01(\x0c\x12\x0e\n\x06suffix\x18\x03 \x01(\x0c\"y\n\tProofSpec\x12 \n\tleaf_spec\x18\x01 \x01(\x0b\x32\r.ics23.LeafOp\x12$\n\ninner_spec\x18\x02 \x01(\x0b\x32\x10.ics23.InnerSpec\x12\x11\n\tmax_depth\x18\x03 \x01(\x05\x12\x11\n\tmin_depth\x18\x04 \x01(\x05\"\x9c\x01\n\tInnerSpec\x12\x13\n\x0b\x63hild_order\x18\x01 \x03(\x05\x12\x12\n\nchild_size\x18\x02 \x01(\x05\x12\x19\n\x11min_prefix_length\x18\x03 \x01(\x05\x12\x19\n\x11max_prefix_length\x18\x04 \x01(\x05\x12\x13\n\x0b\x65mpty_child\x18\x05 \x01(\x0c\x12\x1b\n\x04hash\x18\x06 \x01(\x0e\x32\r.ics23.HashOp\"0\n\nBatchProof\x12\"\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x11.ics23.BatchEntry\"k\n\nBatchEntry\x12&\n\x05\x65xist\x18\x01 \x01(\x0b\x32\x15.ics23.ExistenceProofH\x00\x12,\n\x08nonexist\x18\x02 \x01(\x0b\x32\x18.ics23.NonExistenceProofH\x00\x42\x07\n\x05proof\"k\n\x14\x43ompressedBatchProof\x12,\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x1b.ics23.CompressedBatchEntry\x12%\n\rlookup_inners\x18\x02 \x03(\x0b\x32\x0e.ics23.InnerOp\"\x89\x01\n\x14\x43ompressedBatchEntry\x12\x30\n\x05\x65xist\x18\x01 \x01(\x0b\x32\x1f.ics23.CompressedExistenceProofH\x00\x12\x36\n\x08nonexist\x18\x02 \x01(\x0b\x32\".ics23.CompressedNonExistenceProofH\x00\x42\x07\n\x05proof\"a\n\x18\x43ompressedExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x1b\n\x04leaf\x18\x03 \x01(\x0b\x32\r.ics23.LeafOp\x12\x0c\n\x04path\x18\x04 \x03(\x05\"\x89\x01\n\x1b\x43ompressedNonExistenceProof\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12-\n\x04left\x18\x02 \x01(\x0b\x32\x1f.ics23.CompressedExistenceProof\x12.\n\x05right\x18\x03 \x01(\x0b\x32\x1f.ics23.CompressedExistenceProof*U\n\x06HashOp\x12\x0b\n\x07NO_HASH\x10\x00\x12\n\n\x06SHA256\x10\x01\x12\n\n\x06SHA512\x10\x02\x12\n\n\x06KECCAK\x10\x03\x12\r\n\tRIPEMD160\x10\x04\x12\x0b\n\x07\x42ITCOIN\x10\x05*\xab\x01\n\x08LengthOp\x12\r\n\tNO_PREFIX\x10\x00\x12\r\n\tVAR_PROTO\x10\x01\x12\x0b\n\x07VAR_RLP\x10\x02\x12\x0f\n\x0b\x46IXED32_BIG\x10\x03\x12\x12\n\x0e\x46IXED32_LITTLE\x10\x04\x12\x0f\n\x0b\x46IXED64_BIG\x10\x05\x12\x12\n\x0e\x46IXED64_LITTLE\x10\x06\x12\x14\n\x10REQUIRE_32_BYTES\x10\x07\x12\x14\n\x10REQUIRE_64_BYTES\x10\x08\x42\x1cZ\x1agithub.com/confio/ics23/gob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proofs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\032github.com/confio/ics23/go'
  _globals['_HASHOP']._serialized_start=1603
  _globals['_HASHOP']._serialized_end=1688
  _globals['_LENGTHOP']._serialized_start=1691
  _globals['_LENGTHOP']._serialized_end=1862
  _globals['_EXISTENCEPROOF']._serialized_start=23
  _globals['_EXISTENCEPROOF']._serialized_end=126
  _globals['_NONEXISTENCEPROOF']._serialized_start=128
  _globals['_NONEXISTENCEPROOF']._serialized_end=235
  _globals['_COMMITMENTPROOF']._serialized_start=238
  _globals['_COMMITMENTPROOF']._serialized_end=437
  _globals['_LEAFOP']._serialized_start=440
  _globals['_LEAFOP']._serialized_end=600
  _globals['_INNEROP']._serialized_start=602
  _globals['_INNEROP']._serialized_end=672
  _globals['_PROOFSPEC']._serialized_start=674
  _globals['_PROOFSPEC']._serialized_end=795
  _globals['_INNERSPEC']._serialized_start=798
  _globals['_INNERSPEC']._serialized_end=954
  _globals['_BATCHPROOF']._serialized_start=956
  _globals['_BATCHPROOF']._serialized_end=1004
  _globals['_BATCHENTRY']._serialized_start=1006
  _globals['_BATCHENTRY']._serialized_end=1113
  _globals['_COMPRESSEDBATCHPROOF']._serialized_start=1115
  _globals['_COMPRESSEDBATCHPROOF']._serialized_end=1222
  _globals['_COMPRESSEDBATCHENTRY']._serialized_start=1225
  _globals['_COMPRESSEDBATCHENTRY']._serialized_end=1362
  _globals['_COMPRESSEDEXISTENCEPROOF']._serialized_start=1364
  _globals['_COMPRESSEDEXISTENCEPROOF']._serialized_end=1461
  _globals['_COMPRESSEDNONEXISTENCEPROOF']._serialized_start=1464
  _globals['_COMPRESSEDNONEXISTENCEPROOF']._serialized_end=1601
# @@protoc_insertion_point(module_scope)
