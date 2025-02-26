# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from neurion.ganglion import tx_pb2 as neurion_dot_ganglion_dot_tx__pb2

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
        + f' but the generated code in neurion/ganglion/tx_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class MsgStub(object):
    """Msg defines the Msg service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UpdateParams = channel.unary_unary(
                '/neurion.ganglion.Msg/UpdateParams',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParams.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
                _registered_method=True)
        self.RegisterIon = channel.unary_unary(
                '/neurion.ganglion.Msg/RegisterIon',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIon.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIonResponse.FromString,
                _registered_method=True)
        self.ReportUnavailableIon = channel.unary_unary(
                '/neurion.ganglion.Msg/ReportUnavailableIon',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIon.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIonResponse.FromString,
                _registered_method=True)
        self.UnreportUnavailableIon = channel.unary_unary(
                '/neurion.ganglion.Msg/UnreportUnavailableIon',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIon.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIonResponse.FromString,
                _registered_method=True)
        self.AddValidator = channel.unary_unary(
                '/neurion.ganglion.Msg/AddValidator',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgAddValidator.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgAddValidatorResponse.FromString,
                _registered_method=True)
        self.RemoveValidator = channel.unary_unary(
                '/neurion.ganglion.Msg/RemoveValidator',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidator.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidatorResponse.FromString,
                _registered_method=True)
        self.ValidateAvailability = channel.unary_unary(
                '/neurion.ganglion.Msg/ValidateAvailability',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailability.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailabilityResponse.FromString,
                _registered_method=True)
        self.RegisterPathway = channel.unary_unary(
                '/neurion.ganglion.Msg/RegisterPathway',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathway.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathwayResponse.FromString,
                _registered_method=True)
        self.StakePathway = channel.unary_unary(
                '/neurion.ganglion.Msg/StakePathway',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakePathway.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakePathwayResponse.FromString,
                _registered_method=True)
        self.RefundPathwayStake = channel.unary_unary(
                '/neurion.ganglion.Msg/RefundPathwayStake',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStake.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStakeResponse.FromString,
                _registered_method=True)
        self.InitUnstakePathway = channel.unary_unary(
                '/neurion.ganglion.Msg/InitUnstakePathway',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathway.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathwayResponse.FromString,
                _registered_method=True)
        self.ClaimProtocolFee = channel.unary_unary(
                '/neurion.ganglion.Msg/ClaimProtocolFee',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFee.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFeeResponse.FromString,
                _registered_method=True)
        self.SettlePathwayStake = channel.unary_unary(
                '/neurion.ganglion.Msg/SettlePathwayStake',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStake.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStakeResponse.FromString,
                _registered_method=True)
        self.StakeToGanglion = channel.unary_unary(
                '/neurion.ganglion.Msg/StakeToGanglion',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglion.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglionResponse.FromString,
                _registered_method=True)
        self.ClaimReward = channel.unary_unary(
                '/neurion.ganglion.Msg/ClaimReward',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimReward.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimRewardResponse.FromString,
                _registered_method=True)
        self.UnstakeFromGanglion = channel.unary_unary(
                '/neurion.ganglion.Msg/UnstakeFromGanglion',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglion.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglionResponse.FromString,
                _registered_method=True)
        self.UpdatePathway = channel.unary_unary(
                '/neurion.ganglion.Msg/UpdatePathway',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathway.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathwayResponse.FromString,
                _registered_method=True)
        self.RemoveIon = channel.unary_unary(
                '/neurion.ganglion.Msg/RemoveIon',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIon.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIonResponse.FromString,
                _registered_method=True)
        self.RemovePathway = channel.unary_unary(
                '/neurion.ganglion.Msg/RemovePathway',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathway.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathwayResponse.FromString,
                _registered_method=True)
        self.SetAllowedIps = channel.unary_unary(
                '/neurion.ganglion.Msg/SetAllowedIps',
                request_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIps.SerializeToString,
                response_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIpsResponse.FromString,
                _registered_method=True)


class MsgServicer(object):
    """Msg defines the Msg service.
    """

    def UpdateParams(self, request, context):
        """UpdateParams defines a (governance) operation for updating the module
        parameters. The authority defaults to the x/gov module account.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterIon(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReportUnavailableIon(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnreportUnavailableIon(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddValidator(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveValidator(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateAvailability(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterPathway(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StakePathway(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RefundPathwayStake(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitUnstakePathway(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimProtocolFee(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SettlePathwayStake(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StakeToGanglion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimReward(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnstakeFromGanglion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePathway(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveIon(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemovePathway(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetAllowedIps(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UpdateParams': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateParams,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParams.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParamsResponse.SerializeToString,
            ),
            'RegisterIon': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterIon,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIon.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIonResponse.SerializeToString,
            ),
            'ReportUnavailableIon': grpc.unary_unary_rpc_method_handler(
                    servicer.ReportUnavailableIon,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIon.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIonResponse.SerializeToString,
            ),
            'UnreportUnavailableIon': grpc.unary_unary_rpc_method_handler(
                    servicer.UnreportUnavailableIon,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIon.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIonResponse.SerializeToString,
            ),
            'AddValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.AddValidator,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgAddValidator.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgAddValidatorResponse.SerializeToString,
            ),
            'RemoveValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveValidator,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidator.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidatorResponse.SerializeToString,
            ),
            'ValidateAvailability': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateAvailability,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailability.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailabilityResponse.SerializeToString,
            ),
            'RegisterPathway': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterPathway,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathway.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathwayResponse.SerializeToString,
            ),
            'StakePathway': grpc.unary_unary_rpc_method_handler(
                    servicer.StakePathway,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakePathway.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakePathwayResponse.SerializeToString,
            ),
            'RefundPathwayStake': grpc.unary_unary_rpc_method_handler(
                    servicer.RefundPathwayStake,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStake.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStakeResponse.SerializeToString,
            ),
            'InitUnstakePathway': grpc.unary_unary_rpc_method_handler(
                    servicer.InitUnstakePathway,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathway.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathwayResponse.SerializeToString,
            ),
            'ClaimProtocolFee': grpc.unary_unary_rpc_method_handler(
                    servicer.ClaimProtocolFee,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFee.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFeeResponse.SerializeToString,
            ),
            'SettlePathwayStake': grpc.unary_unary_rpc_method_handler(
                    servicer.SettlePathwayStake,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStake.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStakeResponse.SerializeToString,
            ),
            'StakeToGanglion': grpc.unary_unary_rpc_method_handler(
                    servicer.StakeToGanglion,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglion.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglionResponse.SerializeToString,
            ),
            'ClaimReward': grpc.unary_unary_rpc_method_handler(
                    servicer.ClaimReward,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimReward.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgClaimRewardResponse.SerializeToString,
            ),
            'UnstakeFromGanglion': grpc.unary_unary_rpc_method_handler(
                    servicer.UnstakeFromGanglion,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglion.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglionResponse.SerializeToString,
            ),
            'UpdatePathway': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePathway,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathway.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathwayResponse.SerializeToString,
            ),
            'RemoveIon': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveIon,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIon.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIonResponse.SerializeToString,
            ),
            'RemovePathway': grpc.unary_unary_rpc_method_handler(
                    servicer.RemovePathway,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathway.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathwayResponse.SerializeToString,
            ),
            'SetAllowedIps': grpc.unary_unary_rpc_method_handler(
                    servicer.SetAllowedIps,
                    request_deserializer=neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIps.FromString,
                    response_serializer=neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIpsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'neurion.ganglion.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('neurion.ganglion.Msg', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Msg defines the Msg service.
    """

    @staticmethod
    def UpdateParams(request,
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
            '/neurion.ganglion.Msg/UpdateParams',
            neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParams.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
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
    def RegisterIon(request,
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
            '/neurion.ganglion.Msg/RegisterIon',
            neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIon.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRegisterIonResponse.FromString,
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
    def ReportUnavailableIon(request,
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
            '/neurion.ganglion.Msg/ReportUnavailableIon',
            neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIon.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgReportUnavailableIonResponse.FromString,
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
    def UnreportUnavailableIon(request,
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
            '/neurion.ganglion.Msg/UnreportUnavailableIon',
            neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIon.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgUnreportUnavailableIonResponse.FromString,
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
    def AddValidator(request,
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
            '/neurion.ganglion.Msg/AddValidator',
            neurion_dot_ganglion_dot_tx__pb2.MsgAddValidator.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgAddValidatorResponse.FromString,
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
    def RemoveValidator(request,
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
            '/neurion.ganglion.Msg/RemoveValidator',
            neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidator.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRemoveValidatorResponse.FromString,
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
    def ValidateAvailability(request,
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
            '/neurion.ganglion.Msg/ValidateAvailability',
            neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailability.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgValidateAvailabilityResponse.FromString,
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
    def RegisterPathway(request,
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
            '/neurion.ganglion.Msg/RegisterPathway',
            neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathway.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRegisterPathwayResponse.FromString,
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
    def StakePathway(request,
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
            '/neurion.ganglion.Msg/StakePathway',
            neurion_dot_ganglion_dot_tx__pb2.MsgStakePathway.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgStakePathwayResponse.FromString,
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
    def RefundPathwayStake(request,
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
            '/neurion.ganglion.Msg/RefundPathwayStake',
            neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStake.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRefundPathwayStakeResponse.FromString,
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
    def InitUnstakePathway(request,
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
            '/neurion.ganglion.Msg/InitUnstakePathway',
            neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathway.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgInitUnstakePathwayResponse.FromString,
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
    def ClaimProtocolFee(request,
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
            '/neurion.ganglion.Msg/ClaimProtocolFee',
            neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFee.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgClaimProtocolFeeResponse.FromString,
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
    def SettlePathwayStake(request,
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
            '/neurion.ganglion.Msg/SettlePathwayStake',
            neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStake.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgSettlePathwayStakeResponse.FromString,
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
    def StakeToGanglion(request,
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
            '/neurion.ganglion.Msg/StakeToGanglion',
            neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglion.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgStakeToGanglionResponse.FromString,
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
    def ClaimReward(request,
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
            '/neurion.ganglion.Msg/ClaimReward',
            neurion_dot_ganglion_dot_tx__pb2.MsgClaimReward.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgClaimRewardResponse.FromString,
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
    def UnstakeFromGanglion(request,
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
            '/neurion.ganglion.Msg/UnstakeFromGanglion',
            neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglion.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgUnstakeFromGanglionResponse.FromString,
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
    def UpdatePathway(request,
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
            '/neurion.ganglion.Msg/UpdatePathway',
            neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathway.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgUpdatePathwayResponse.FromString,
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
    def RemoveIon(request,
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
            '/neurion.ganglion.Msg/RemoveIon',
            neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIon.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRemoveIonResponse.FromString,
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
    def RemovePathway(request,
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
            '/neurion.ganglion.Msg/RemovePathway',
            neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathway.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgRemovePathwayResponse.FromString,
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
    def SetAllowedIps(request,
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
            '/neurion.ganglion.Msg/SetAllowedIps',
            neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIps.SerializeToString,
            neurion_dot_ganglion_dot_tx__pb2.MsgSetAllowedIpsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
