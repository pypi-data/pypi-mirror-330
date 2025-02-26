# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: neurion/crucible/plagiarism_report.proto
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
    'neurion/crucible/plagiarism_report.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(neurion/crucible/plagiarism_report.proto\x12\x10neurion.crucible\"\xe3\x02\n\x10PlagiarismReport\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x0f\n\x07task_id\x18\x02 \x01(\x04\x12\x1c\n\x14\x63opied_submission_id\x18\x03 \x01(\x04\x12\x1f\n\x17suspected_submission_id\x18\x04 \x01(\x04\x12\x12\n\narbitrator\x18\x05 \x01(\t\x12\x38\n\x06result\x18\x06 \x01(\x0e\x32(.neurion.crucible.PlagiarismReportResult\x12\x19\n\x11\x63reated_timestamp\x18\x07 \x01(\x04\x12\x1a\n\x12\x64\x65\x63ision_timestamp\x18\x08 \x01(\x04\x12\x1b\n\x13proof_of_plagiarism\x18\t \x01(\t\x12\x1c\n\x14reason_for_rejection\x18\n \x01(\t\x12\x0f\n\x07\x64\x65posit\x18\x0c \x01(\x04\x12\x10\n\x08reporter\x18\r \x01(\t\x12\x10\n\x08reportee\x18\x0e \x01(\t*\x92\x01\n\x16PlagiarismReportResult\x12*\n&PLAGIARISM_REPORT_RESULT_NOT_AVAILABLE\x10\x00\x12%\n!PLAGIARISM_REPORT_RESULT_ACCEPTED\x10\x01\x12%\n!PLAGIARISM_REPORT_RESULT_REJECTED\x10\x02\x42\x1aZ\x18neurion/x/crucible/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'neurion.crucible.plagiarism_report_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\030neurion/x/crucible/types'
  _globals['_PLAGIARISMREPORTRESULT']._serialized_start=421
  _globals['_PLAGIARISMREPORTRESULT']._serialized_end=567
  _globals['_PLAGIARISMREPORT']._serialized_start=63
  _globals['_PLAGIARISMREPORT']._serialized_end=418
# @@protoc_insertion_point(module_scope)
