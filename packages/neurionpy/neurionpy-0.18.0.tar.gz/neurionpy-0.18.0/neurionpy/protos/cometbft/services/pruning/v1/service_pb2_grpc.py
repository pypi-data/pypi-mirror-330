# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from cometbft.services.pruning.v1 import pruning_pb2 as cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in cometbft/services/pruning/v1/service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PruningServiceStub(object):
    """PruningService provides privileged access to specialized pruning
    functionality on the CometBFT node to help control node storage.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetBlockRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/SetBlockRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightResponse.FromString,
                _registered_method=True)
        self.GetBlockRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/GetBlockRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightResponse.FromString,
                _registered_method=True)
        self.SetBlockResultsRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/SetBlockResultsRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightResponse.FromString,
                _registered_method=True)
        self.GetBlockResultsRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/GetBlockResultsRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightResponse.FromString,
                _registered_method=True)
        self.SetTxIndexerRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/SetTxIndexerRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightResponse.FromString,
                _registered_method=True)
        self.GetTxIndexerRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/GetTxIndexerRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightResponse.FromString,
                _registered_method=True)
        self.SetBlockIndexerRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/SetBlockIndexerRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightResponse.FromString,
                _registered_method=True)
        self.GetBlockIndexerRetainHeight = channel.unary_unary(
                '/cometbft.services.pruning.v1.PruningService/GetBlockIndexerRetainHeight',
                request_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightRequest.SerializeToString,
                response_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightResponse.FromString,
                _registered_method=True)


class PruningServiceServicer(object):
    """PruningService provides privileged access to specialized pruning
    functionality on the CometBFT node to help control node storage.
    """

    def SetBlockRetainHeight(self, request, context):
        """SetBlockRetainHeightRequest indicates to the node that it can safely
        prune all block data up to the specified retain height.

        The lower of this retain height and that set by the application in its
        Commit response will be used by the node to determine which heights' data
        can be pruned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockRetainHeight(self, request, context):
        """GetBlockRetainHeight returns information about the retain height
        parameters used by the node to influence block retention/pruning.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetBlockResultsRetainHeight(self, request, context):
        """SetBlockResultsRetainHeightRequest indicates to the node that it can
        safely prune all block results data up to the specified height.

        The node will always store the block results for the latest height to
        help facilitate crash recovery.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockResultsRetainHeight(self, request, context):
        """GetBlockResultsRetainHeight returns information about the retain height
        parameters used by the node to influence block results retention/pruning.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTxIndexerRetainHeight(self, request, context):
        """SetTxIndexerRetainHeightRequest indicates to the node that it can safely
        prune all tx indices up to the specified retain height.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTxIndexerRetainHeight(self, request, context):
        """GetTxIndexerRetainHeight returns information about the retain height
        parameters used by the node to influence TxIndexer pruning
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetBlockIndexerRetainHeight(self, request, context):
        """SetBlockIndexerRetainHeightRequest indicates to the node that it can safely
        prune all block indices up to the specified retain height.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockIndexerRetainHeight(self, request, context):
        """GetBlockIndexerRetainHeight returns information about the retain height
        parameters used by the node to influence BlockIndexer pruning
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PruningServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetBlockRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.SetBlockRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightResponse.SerializeToString,
            ),
            'GetBlockRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlockRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightResponse.SerializeToString,
            ),
            'SetBlockResultsRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.SetBlockResultsRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightResponse.SerializeToString,
            ),
            'GetBlockResultsRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlockResultsRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightResponse.SerializeToString,
            ),
            'SetTxIndexerRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTxIndexerRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightResponse.SerializeToString,
            ),
            'GetTxIndexerRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTxIndexerRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightResponse.SerializeToString,
            ),
            'SetBlockIndexerRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.SetBlockIndexerRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightResponse.SerializeToString,
            ),
            'GetBlockIndexerRetainHeight': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlockIndexerRetainHeight,
                    request_deserializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightRequest.FromString,
                    response_serializer=cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cometbft.services.pruning.v1.PruningService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cometbft.services.pruning.v1.PruningService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class PruningService(object):
    """PruningService provides privileged access to specialized pruning
    functionality on the CometBFT node to help control node storage.
    """

    @staticmethod
    def SetBlockRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/SetBlockRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetBlockRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/GetBlockRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetBlockResultsRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/SetBlockResultsRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockResultsRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetBlockResultsRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/GetBlockResultsRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockResultsRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetTxIndexerRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/SetTxIndexerRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetTxIndexerRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTxIndexerRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/GetTxIndexerRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetTxIndexerRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetBlockIndexerRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/SetBlockIndexerRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.SetBlockIndexerRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetBlockIndexerRetainHeight(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/cometbft.services.pruning.v1.PruningService/GetBlockIndexerRetainHeight',
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightRequest.SerializeToString,
            cometbft_dot_services_dot_pruning_dot_v1_dot_pruning__pb2.GetBlockIndexerRetainHeightResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
