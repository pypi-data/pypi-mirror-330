"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ..api import files_pb2 as api_dot_files__pb2
from ..api import logging_pb2 as api_dot_logging__pb2
from ..api import query_pb2 as api_dot_query__pb2
from ..api import status_pb2 as api_dot_status__pb2
from ..api import synapse_pb2 as api_dot_synapse__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class SynapseDeviceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Info = channel.unary_unary('/synapse.SynapseDevice/Info', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=api_dot_synapse__pb2.DeviceInfo.FromString)
        self.Configure = channel.unary_unary('/synapse.SynapseDevice/Configure', request_serializer=api_dot_synapse__pb2.DeviceConfiguration.SerializeToString, response_deserializer=api_dot_status__pb2.Status.FromString)
        self.Start = channel.unary_unary('/synapse.SynapseDevice/Start', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=api_dot_status__pb2.Status.FromString)
        self.Stop = channel.unary_unary('/synapse.SynapseDevice/Stop', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=api_dot_status__pb2.Status.FromString)
        self.Query = channel.unary_unary('/synapse.SynapseDevice/Query', request_serializer=api_dot_query__pb2.QueryRequest.SerializeToString, response_deserializer=api_dot_query__pb2.QueryResponse.FromString)
        self.ListFiles = channel.unary_unary('/synapse.SynapseDevice/ListFiles', request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, response_deserializer=api_dot_files__pb2.ListFilesResponse.FromString)
        self.WriteFile = channel.unary_unary('/synapse.SynapseDevice/WriteFile', request_serializer=api_dot_files__pb2.WriteFileRequest.SerializeToString, response_deserializer=api_dot_files__pb2.WriteFileResponse.FromString)
        self.ReadFile = channel.unary_stream('/synapse.SynapseDevice/ReadFile', request_serializer=api_dot_files__pb2.ReadFileRequest.SerializeToString, response_deserializer=api_dot_files__pb2.ReadFileResponse.FromString)
        self.DeleteFile = channel.unary_unary('/synapse.SynapseDevice/DeleteFile', request_serializer=api_dot_files__pb2.DeleteFileRequest.SerializeToString, response_deserializer=api_dot_files__pb2.DeleteFileResponse.FromString)
        self.GetLogs = channel.unary_unary('/synapse.SynapseDevice/GetLogs', request_serializer=api_dot_logging__pb2.LogQueryRequest.SerializeToString, response_deserializer=api_dot_logging__pb2.LogQueryResponse.FromString)
        self.TailLogs = channel.unary_stream('/synapse.SynapseDevice/TailLogs', request_serializer=api_dot_logging__pb2.TailLogsRequest.SerializeToString, response_deserializer=api_dot_logging__pb2.LogEntry.FromString)

class SynapseDeviceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Configure(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Start(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Query(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WriteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLogs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TailLogs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_SynapseDeviceServicer_to_server(servicer, server):
    rpc_method_handlers = {'Info': grpc.unary_unary_rpc_method_handler(servicer.Info, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=api_dot_synapse__pb2.DeviceInfo.SerializeToString), 'Configure': grpc.unary_unary_rpc_method_handler(servicer.Configure, request_deserializer=api_dot_synapse__pb2.DeviceConfiguration.FromString, response_serializer=api_dot_status__pb2.Status.SerializeToString), 'Start': grpc.unary_unary_rpc_method_handler(servicer.Start, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=api_dot_status__pb2.Status.SerializeToString), 'Stop': grpc.unary_unary_rpc_method_handler(servicer.Stop, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=api_dot_status__pb2.Status.SerializeToString), 'Query': grpc.unary_unary_rpc_method_handler(servicer.Query, request_deserializer=api_dot_query__pb2.QueryRequest.FromString, response_serializer=api_dot_query__pb2.QueryResponse.SerializeToString), 'ListFiles': grpc.unary_unary_rpc_method_handler(servicer.ListFiles, request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, response_serializer=api_dot_files__pb2.ListFilesResponse.SerializeToString), 'WriteFile': grpc.unary_unary_rpc_method_handler(servicer.WriteFile, request_deserializer=api_dot_files__pb2.WriteFileRequest.FromString, response_serializer=api_dot_files__pb2.WriteFileResponse.SerializeToString), 'ReadFile': grpc.unary_stream_rpc_method_handler(servicer.ReadFile, request_deserializer=api_dot_files__pb2.ReadFileRequest.FromString, response_serializer=api_dot_files__pb2.ReadFileResponse.SerializeToString), 'DeleteFile': grpc.unary_unary_rpc_method_handler(servicer.DeleteFile, request_deserializer=api_dot_files__pb2.DeleteFileRequest.FromString, response_serializer=api_dot_files__pb2.DeleteFileResponse.SerializeToString), 'GetLogs': grpc.unary_unary_rpc_method_handler(servicer.GetLogs, request_deserializer=api_dot_logging__pb2.LogQueryRequest.FromString, response_serializer=api_dot_logging__pb2.LogQueryResponse.SerializeToString), 'TailLogs': grpc.unary_stream_rpc_method_handler(servicer.TailLogs, request_deserializer=api_dot_logging__pb2.TailLogsRequest.FromString, response_serializer=api_dot_logging__pb2.LogEntry.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('synapse.SynapseDevice', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class SynapseDevice(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Info(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/Info', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, api_dot_synapse__pb2.DeviceInfo.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Configure(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/Configure', api_dot_synapse__pb2.DeviceConfiguration.SerializeToString, api_dot_status__pb2.Status.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Start(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/Start', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, api_dot_status__pb2.Status.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stop(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/Stop', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, api_dot_status__pb2.Status.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Query(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/Query', api_dot_query__pb2.QueryRequest.SerializeToString, api_dot_query__pb2.QueryResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFiles(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/ListFiles', google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString, api_dot_files__pb2.ListFilesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WriteFile(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/WriteFile', api_dot_files__pb2.WriteFileRequest.SerializeToString, api_dot_files__pb2.WriteFileResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadFile(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/synapse.SynapseDevice/ReadFile', api_dot_files__pb2.ReadFileRequest.SerializeToString, api_dot_files__pb2.ReadFileResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFile(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/DeleteFile', api_dot_files__pb2.DeleteFileRequest.SerializeToString, api_dot_files__pb2.DeleteFileResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLogs(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/synapse.SynapseDevice/GetLogs', api_dot_logging__pb2.LogQueryRequest.SerializeToString, api_dot_logging__pb2.LogQueryResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TailLogs(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_stream(request, target, '/synapse.SynapseDevice/TailLogs', api_dot_logging__pb2.TailLogsRequest.SerializeToString, api_dot_logging__pb2.LogEntry.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)