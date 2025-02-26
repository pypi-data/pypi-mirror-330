# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from cometbft.rpc.grpc.v1beta1 import types_pb2 as cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2

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
        + f' but the generated code in cometbft/rpc/grpc/v1beta1/types_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class BroadcastAPIStub(object):
    """BroadcastAPI is an API for broadcasting transactions.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
                '/cometbft.rpc.grpc.v1beta1.BroadcastAPI/Ping',
                request_serializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestPing.SerializeToString,
                response_deserializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponsePing.FromString,
                _registered_method=True)
        self.BroadcastTx = channel.unary_unary(
                '/cometbft.rpc.grpc.v1beta1.BroadcastAPI/BroadcastTx',
                request_serializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestBroadcastTx.SerializeToString,
                response_deserializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponseBroadcastTx.FromString,
                _registered_method=True)


class BroadcastAPIServicer(object):
    """BroadcastAPI is an API for broadcasting transactions.
    """

    def Ping(self, request, context):
        """Ping the connection.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BroadcastTx(self, request, context):
        """BroadcastTx broadcasts the transaction.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BroadcastAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Ping': grpc.unary_unary_rpc_method_handler(
                    servicer.Ping,
                    request_deserializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestPing.FromString,
                    response_serializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponsePing.SerializeToString,
            ),
            'BroadcastTx': grpc.unary_unary_rpc_method_handler(
                    servicer.BroadcastTx,
                    request_deserializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestBroadcastTx.FromString,
                    response_serializer=cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponseBroadcastTx.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cometbft.rpc.grpc.v1beta1.BroadcastAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cometbft.rpc.grpc.v1beta1.BroadcastAPI', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class BroadcastAPI(object):
    """BroadcastAPI is an API for broadcasting transactions.
    """

    @staticmethod
    def Ping(request,
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
            '/cometbft.rpc.grpc.v1beta1.BroadcastAPI/Ping',
            cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestPing.SerializeToString,
            cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponsePing.FromString,
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
    def BroadcastTx(request,
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
            '/cometbft.rpc.grpc.v1beta1.BroadcastAPI/BroadcastTx',
            cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.RequestBroadcastTx.SerializeToString,
            cometbft_dot_rpc_dot_grpc_dot_v1beta1_dot_types__pb2.ResponseBroadcastTx.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
