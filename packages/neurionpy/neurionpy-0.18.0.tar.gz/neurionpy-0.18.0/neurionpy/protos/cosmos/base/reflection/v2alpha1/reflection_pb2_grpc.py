# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from cosmos.base.reflection.v2alpha1 import reflection_pb2 as cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2

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
        + f' but the generated code in cosmos/base/reflection/v2alpha1/reflection_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ReflectionServiceStub(object):
    """ReflectionService defines a service for application reflection.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAuthnDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetAuthnDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorResponse.FromString,
                _registered_method=True)
        self.GetChainDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetChainDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorResponse.FromString,
                _registered_method=True)
        self.GetCodecDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetCodecDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorResponse.FromString,
                _registered_method=True)
        self.GetConfigurationDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetConfigurationDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorResponse.FromString,
                _registered_method=True)
        self.GetQueryServicesDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetQueryServicesDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorResponse.FromString,
                _registered_method=True)
        self.GetTxDescriptor = channel.unary_unary(
                '/cosmos.base.reflection.v2alpha1.ReflectionService/GetTxDescriptor',
                request_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorRequest.SerializeToString,
                response_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorResponse.FromString,
                _registered_method=True)


class ReflectionServiceServicer(object):
    """ReflectionService defines a service for application reflection.
    """

    def GetAuthnDescriptor(self, request, context):
        """GetAuthnDescriptor returns information on how to authenticate transactions in the application
        NOTE: this RPC is still experimental and might be subject to breaking changes or removal in
        future releases of the cosmos-sdk.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChainDescriptor(self, request, context):
        """GetChainDescriptor returns the description of the chain
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCodecDescriptor(self, request, context):
        """GetCodecDescriptor returns the descriptor of the codec of the application
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetConfigurationDescriptor(self, request, context):
        """GetConfigurationDescriptor returns the descriptor for the sdk.Config of the application
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetQueryServicesDescriptor(self, request, context):
        """GetQueryServicesDescriptor returns the available gRPC queryable services of the application
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTxDescriptor(self, request, context):
        """GetTxDescriptor returns information on the used transaction object and available msgs that can be used
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReflectionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAuthnDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAuthnDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorResponse.SerializeToString,
            ),
            'GetChainDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChainDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorResponse.SerializeToString,
            ),
            'GetCodecDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCodecDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorResponse.SerializeToString,
            ),
            'GetConfigurationDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetConfigurationDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorResponse.SerializeToString,
            ),
            'GetQueryServicesDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetQueryServicesDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorResponse.SerializeToString,
            ),
            'GetTxDescriptor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTxDescriptor,
                    request_deserializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorRequest.FromString,
                    response_serializer=cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.base.reflection.v2alpha1.ReflectionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cosmos.base.reflection.v2alpha1.ReflectionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ReflectionService(object):
    """ReflectionService defines a service for application reflection.
    """

    @staticmethod
    def GetAuthnDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetAuthnDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetAuthnDescriptorResponse.FromString,
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
    def GetChainDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetChainDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetChainDescriptorResponse.FromString,
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
    def GetCodecDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetCodecDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetCodecDescriptorResponse.FromString,
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
    def GetConfigurationDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetConfigurationDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetConfigurationDescriptorResponse.FromString,
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
    def GetQueryServicesDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetQueryServicesDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetQueryServicesDescriptorResponse.FromString,
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
    def GetTxDescriptor(request,
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
            '/cosmos.base.reflection.v2alpha1.ReflectionService/GetTxDescriptor',
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorRequest.SerializeToString,
            cosmos_dot_base_dot_reflection_dot_v2alpha1_dot_reflection__pb2.GetTxDescriptorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
