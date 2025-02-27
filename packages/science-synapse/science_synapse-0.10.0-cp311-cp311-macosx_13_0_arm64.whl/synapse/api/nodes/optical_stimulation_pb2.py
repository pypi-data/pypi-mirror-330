"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#api/nodes/optical_stimulation.proto\x12\x07synapse"z\n\x18OpticalStimulationConfig\x12\x15\n\rperipheral_id\x18\x01 \x01(\r\x12\x12\n\npixel_mask\x18\x02 \x03(\r\x12\x11\n\tbit_width\x18\x03 \x01(\r\x12\x12\n\nframe_rate\x18\x04 \x01(\r\x12\x0c\n\x04gain\x18\x05 \x01(\x02b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.optical_stimulation_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_OPTICALSTIMULATIONCONFIG']._serialized_start = 48
    _globals['_OPTICALSTIMULATIONCONFIG']._serialized_end = 170