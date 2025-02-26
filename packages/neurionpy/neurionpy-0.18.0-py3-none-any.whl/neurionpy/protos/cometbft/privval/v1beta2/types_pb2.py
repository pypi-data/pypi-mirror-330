# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: cometbft/privval/v1beta2/types.proto
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
    'cometbft/privval/v1beta2/types.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cometbft.crypto.v1 import keys_pb2 as cometbft_dot_crypto_dot_v1_dot_keys__pb2
from cometbft.types.v1 import types_pb2 as cometbft_dot_types_dot_v1_dot_types__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$cometbft/privval/v1beta2/types.proto\x12\x18\x63ometbft.privval.v1beta2\x1a\x1d\x63ometbft/crypto/v1/keys.proto\x1a\x1d\x63ometbft/types/v1/types.proto\x1a\x14gogoproto/gogo.proto\"6\n\x11RemoteSignerError\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\"!\n\rPubKeyRequest\x12\x10\n\x08\x63hain_id\x18\x01 \x01(\t\"\x82\x01\n\x0ePubKeyResponse\x12\x34\n\x07pub_key\x18\x01 \x01(\x0b\x32\x1d.cometbft.crypto.v1.PublicKeyB\x04\xc8\xde\x1f\x00\x12:\n\x05\x65rror\x18\x02 \x01(\x0b\x32+.cometbft.privval.v1beta2.RemoteSignerError\"J\n\x0fSignVoteRequest\x12%\n\x04vote\x18\x01 \x01(\x0b\x32\x17.cometbft.types.v1.Vote\x12\x10\n\x08\x63hain_id\x18\x02 \x01(\t\"}\n\x12SignedVoteResponse\x12+\n\x04vote\x18\x01 \x01(\x0b\x32\x17.cometbft.types.v1.VoteB\x04\xc8\xde\x1f\x00\x12:\n\x05\x65rror\x18\x02 \x01(\x0b\x32+.cometbft.privval.v1beta2.RemoteSignerError\"V\n\x13SignProposalRequest\x12-\n\x08proposal\x18\x01 \x01(\x0b\x32\x1b.cometbft.types.v1.Proposal\x12\x10\n\x08\x63hain_id\x18\x02 \x01(\t\"\x89\x01\n\x16SignedProposalResponse\x12\x33\n\x08proposal\x18\x01 \x01(\x0b\x32\x1b.cometbft.types.v1.ProposalB\x04\xc8\xde\x1f\x00\x12:\n\x05\x65rror\x18\x02 \x01(\x0b\x32+.cometbft.privval.v1beta2.RemoteSignerError\"\r\n\x0bPingRequest\"\x0e\n\x0cPingResponse\"\xd6\x04\n\x07Message\x12\x42\n\x0fpub_key_request\x18\x01 \x01(\x0b\x32\'.cometbft.privval.v1beta2.PubKeyRequestH\x00\x12\x44\n\x10pub_key_response\x18\x02 \x01(\x0b\x32(.cometbft.privval.v1beta2.PubKeyResponseH\x00\x12\x46\n\x11sign_vote_request\x18\x03 \x01(\x0b\x32).cometbft.privval.v1beta2.SignVoteRequestH\x00\x12L\n\x14signed_vote_response\x18\x04 \x01(\x0b\x32,.cometbft.privval.v1beta2.SignedVoteResponseH\x00\x12N\n\x15sign_proposal_request\x18\x05 \x01(\x0b\x32-.cometbft.privval.v1beta2.SignProposalRequestH\x00\x12T\n\x18signed_proposal_response\x18\x06 \x01(\x0b\x32\x30.cometbft.privval.v1beta2.SignedProposalResponseH\x00\x12=\n\x0cping_request\x18\x07 \x01(\x0b\x32%.cometbft.privval.v1beta2.PingRequestH\x00\x12?\n\rping_response\x18\x08 \x01(\x0b\x32&.cometbft.privval.v1beta2.PingResponseH\x00\x42\x05\n\x03sum*\xa8\x01\n\x06\x45rrors\x12\x12\n\x0e\x45RRORS_UNKNOWN\x10\x00\x12\x1e\n\x1a\x45RRORS_UNEXPECTED_RESPONSE\x10\x01\x12\x18\n\x14\x45RRORS_NO_CONNECTION\x10\x02\x12\x1d\n\x19\x45RRORS_CONNECTION_TIMEOUT\x10\x03\x12\x17\n\x13\x45RRORS_READ_TIMEOUT\x10\x04\x12\x18\n\x14\x45RRORS_WRITE_TIMEOUT\x10\x05\x42;Z9github.com/cometbft/cometbft/api/cometbft/privval/v1beta2b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cometbft.privval.v1beta2.types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z9github.com/cometbft/cometbft/api/cometbft/privval/v1beta2'
  _globals['_PUBKEYRESPONSE'].fields_by_name['pub_key']._loaded_options = None
  _globals['_PUBKEYRESPONSE'].fields_by_name['pub_key']._serialized_options = b'\310\336\037\000'
  _globals['_SIGNEDVOTERESPONSE'].fields_by_name['vote']._loaded_options = None
  _globals['_SIGNEDVOTERESPONSE'].fields_by_name['vote']._serialized_options = b'\310\336\037\000'
  _globals['_SIGNEDPROPOSALRESPONSE'].fields_by_name['proposal']._loaded_options = None
  _globals['_SIGNEDPROPOSALRESPONSE'].fields_by_name['proposal']._serialized_options = b'\310\336\037\000'
  _globals['_ERRORS']._serialized_start=1438
  _globals['_ERRORS']._serialized_end=1606
  _globals['_REMOTESIGNERERROR']._serialized_start=150
  _globals['_REMOTESIGNERERROR']._serialized_end=204
  _globals['_PUBKEYREQUEST']._serialized_start=206
  _globals['_PUBKEYREQUEST']._serialized_end=239
  _globals['_PUBKEYRESPONSE']._serialized_start=242
  _globals['_PUBKEYRESPONSE']._serialized_end=372
  _globals['_SIGNVOTEREQUEST']._serialized_start=374
  _globals['_SIGNVOTEREQUEST']._serialized_end=448
  _globals['_SIGNEDVOTERESPONSE']._serialized_start=450
  _globals['_SIGNEDVOTERESPONSE']._serialized_end=575
  _globals['_SIGNPROPOSALREQUEST']._serialized_start=577
  _globals['_SIGNPROPOSALREQUEST']._serialized_end=663
  _globals['_SIGNEDPROPOSALRESPONSE']._serialized_start=666
  _globals['_SIGNEDPROPOSALRESPONSE']._serialized_end=803
  _globals['_PINGREQUEST']._serialized_start=805
  _globals['_PINGREQUEST']._serialized_end=818
  _globals['_PINGRESPONSE']._serialized_start=820
  _globals['_PINGRESPONSE']._serialized_end=834
  _globals['_MESSAGE']._serialized_start=837
  _globals['_MESSAGE']._serialized_end=1435
# @@protoc_insertion_point(module_scope)
