"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aapi/nodes/stream_out.proto\x12\x07synapse"9\n\x0fStreamOutConfig\x12\r\n\x05label\x18\x01 \x01(\t\x12\x17\n\x0fmulticast_group\x18\x02 \x01(\t"*\n\x0fStreamOutStatus\x12\x17\n\x0fthroughput_mbps\x18\x01 \x01(\x02b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.stream_out_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_STREAMOUTCONFIG']._serialized_start = 39
    _globals['_STREAMOUTCONFIG']._serialized_end = 96
    _globals['_STREAMOUTSTATUS']._serialized_start = 98
    _globals['_STREAMOUTSTATUS']._serialized_end = 140