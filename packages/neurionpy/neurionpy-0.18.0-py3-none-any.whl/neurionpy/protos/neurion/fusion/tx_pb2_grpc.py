# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from neurion.fusion import tx_pb2 as neurion_dot_fusion_dot_tx__pb2

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
        + f' but the generated code in neurion/fusion/tx_pb2_grpc.py depends on'
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
                '/neurion.fusion.Msg/UpdateParams',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgUpdateParams.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
                _registered_method=True)
        self.ApplyCreator = channel.unary_unary(
                '/neurion.fusion.Msg/ApplyCreator',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgApplyCreator.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgApplyCreatorResponse.FromString,
                _registered_method=True)
        self.ApproveApplication = channel.unary_unary(
                '/neurion.fusion.Msg/ApproveApplication',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgApproveApplication.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgApproveApplicationResponse.FromString,
                _registered_method=True)
        self.RejectApplication = channel.unary_unary(
                '/neurion.fusion.Msg/RejectApplication',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRejectApplication.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRejectApplicationResponse.FromString,
                _registered_method=True)
        self.CreateTask = channel.unary_unary(
                '/neurion.fusion.Msg/CreateTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgCreateTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgCreateTaskResponse.FromString,
                _registered_method=True)
        self.StartTask = channel.unary_unary(
                '/neurion.fusion.Msg/StartTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTaskResponse.FromString,
                _registered_method=True)
        self.ProposeModel = channel.unary_unary(
                '/neurion.fusion.Msg/ProposeModel',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgProposeModel.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgProposeModelResponse.FromString,
                _registered_method=True)
        self.RegisterProposer = channel.unary_unary(
                '/neurion.fusion.Msg/RegisterProposer',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposer.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposerResponse.FromString,
                _registered_method=True)
        self.RegisterValidator = channel.unary_unary(
                '/neurion.fusion.Msg/RegisterValidator',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidator.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidatorResponse.FromString,
                _registered_method=True)
        self.StartTesting = channel.unary_unary(
                '/neurion.fusion.Msg/StartTesting',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTesting.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTestingResponse.FromString,
                _registered_method=True)
        self.RequestValidationTask = channel.unary_unary(
                '/neurion.fusion.Msg/RequestValidationTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTaskResponse.FromString,
                _registered_method=True)
        self.SubmitScore = channel.unary_unary(
                '/neurion.fusion.Msg/SubmitScore',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgSubmitScore.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgSubmitScoreResponse.FromString,
                _registered_method=True)
        self.DisputeModelScore = channel.unary_unary(
                '/neurion.fusion.Msg/DisputeModelScore',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScore.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScoreResponse.FromString,
                _registered_method=True)
        self.StartNewRound = channel.unary_unary(
                '/neurion.fusion.Msg/StartNewRound',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartNewRound.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartNewRoundResponse.FromString,
                _registered_method=True)
        self.TerminateTask = channel.unary_unary(
                '/neurion.fusion.Msg/TerminateTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgTerminateTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgTerminateTaskResponse.FromString,
                _registered_method=True)
        self.StakeToTask = channel.unary_unary(
                '/neurion.fusion.Msg/StakeToTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStakeToTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStakeToTaskResponse.FromString,
                _registered_method=True)
        self.ClaimTaskReward = channel.unary_unary(
                '/neurion.fusion.Msg/ClaimTaskReward',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskReward.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskRewardResponse.FromString,
                _registered_method=True)
        self.UnstakeFromTask = channel.unary_unary(
                '/neurion.fusion.Msg/UnstakeFromTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTaskResponse.FromString,
                _registered_method=True)
        self.DisclaimCreatorStatus = channel.unary_unary(
                '/neurion.fusion.Msg/DisclaimCreatorStatus',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatus.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatusResponse.FromString,
                _registered_method=True)
        self.AbortTask = channel.unary_unary(
                '/neurion.fusion.Msg/AbortTask',
                request_serializer=neurion_dot_fusion_dot_tx__pb2.MsgAbortTask.SerializeToString,
                response_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgAbortTaskResponse.FromString,
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

    def ApplyCreator(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApproveApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RejectApplication(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProposeModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterProposer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterValidator(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartTesting(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RequestValidationTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitScore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisputeModelScore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartNewRound(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TerminateTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StakeToTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimTaskReward(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnstakeFromTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisclaimCreatorStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AbortTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UpdateParams': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateParams,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgUpdateParams.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgUpdateParamsResponse.SerializeToString,
            ),
            'ApplyCreator': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyCreator,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgApplyCreator.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgApplyCreatorResponse.SerializeToString,
            ),
            'ApproveApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.ApproveApplication,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgApproveApplication.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgApproveApplicationResponse.SerializeToString,
            ),
            'RejectApplication': grpc.unary_unary_rpc_method_handler(
                    servicer.RejectApplication,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRejectApplication.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRejectApplicationResponse.SerializeToString,
            ),
            'CreateTask': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgCreateTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgCreateTaskResponse.SerializeToString,
            ),
            'StartTask': grpc.unary_unary_rpc_method_handler(
                    servicer.StartTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTaskResponse.SerializeToString,
            ),
            'ProposeModel': grpc.unary_unary_rpc_method_handler(
                    servicer.ProposeModel,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgProposeModel.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgProposeModelResponse.SerializeToString,
            ),
            'RegisterProposer': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterProposer,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposer.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposerResponse.SerializeToString,
            ),
            'RegisterValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterValidator,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidator.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidatorResponse.SerializeToString,
            ),
            'StartTesting': grpc.unary_unary_rpc_method_handler(
                    servicer.StartTesting,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTesting.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartTestingResponse.SerializeToString,
            ),
            'RequestValidationTask': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestValidationTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTaskResponse.SerializeToString,
            ),
            'SubmitScore': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitScore,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgSubmitScore.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgSubmitScoreResponse.SerializeToString,
            ),
            'DisputeModelScore': grpc.unary_unary_rpc_method_handler(
                    servicer.DisputeModelScore,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScore.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScoreResponse.SerializeToString,
            ),
            'StartNewRound': grpc.unary_unary_rpc_method_handler(
                    servicer.StartNewRound,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStartNewRound.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStartNewRoundResponse.SerializeToString,
            ),
            'TerminateTask': grpc.unary_unary_rpc_method_handler(
                    servicer.TerminateTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgTerminateTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgTerminateTaskResponse.SerializeToString,
            ),
            'StakeToTask': grpc.unary_unary_rpc_method_handler(
                    servicer.StakeToTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgStakeToTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgStakeToTaskResponse.SerializeToString,
            ),
            'ClaimTaskReward': grpc.unary_unary_rpc_method_handler(
                    servicer.ClaimTaskReward,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskReward.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskRewardResponse.SerializeToString,
            ),
            'UnstakeFromTask': grpc.unary_unary_rpc_method_handler(
                    servicer.UnstakeFromTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTaskResponse.SerializeToString,
            ),
            'DisclaimCreatorStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.DisclaimCreatorStatus,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatus.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatusResponse.SerializeToString,
            ),
            'AbortTask': grpc.unary_unary_rpc_method_handler(
                    servicer.AbortTask,
                    request_deserializer=neurion_dot_fusion_dot_tx__pb2.MsgAbortTask.FromString,
                    response_serializer=neurion_dot_fusion_dot_tx__pb2.MsgAbortTaskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'neurion.fusion.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('neurion.fusion.Msg', rpc_method_handlers)


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
            '/neurion.fusion.Msg/UpdateParams',
            neurion_dot_fusion_dot_tx__pb2.MsgUpdateParams.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
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
    def ApplyCreator(request,
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
            '/neurion.fusion.Msg/ApplyCreator',
            neurion_dot_fusion_dot_tx__pb2.MsgApplyCreator.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgApplyCreatorResponse.FromString,
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
    def ApproveApplication(request,
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
            '/neurion.fusion.Msg/ApproveApplication',
            neurion_dot_fusion_dot_tx__pb2.MsgApproveApplication.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgApproveApplicationResponse.FromString,
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
    def RejectApplication(request,
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
            '/neurion.fusion.Msg/RejectApplication',
            neurion_dot_fusion_dot_tx__pb2.MsgRejectApplication.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgRejectApplicationResponse.FromString,
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
    def CreateTask(request,
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
            '/neurion.fusion.Msg/CreateTask',
            neurion_dot_fusion_dot_tx__pb2.MsgCreateTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgCreateTaskResponse.FromString,
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
    def StartTask(request,
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
            '/neurion.fusion.Msg/StartTask',
            neurion_dot_fusion_dot_tx__pb2.MsgStartTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgStartTaskResponse.FromString,
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
    def ProposeModel(request,
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
            '/neurion.fusion.Msg/ProposeModel',
            neurion_dot_fusion_dot_tx__pb2.MsgProposeModel.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgProposeModelResponse.FromString,
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
    def RegisterProposer(request,
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
            '/neurion.fusion.Msg/RegisterProposer',
            neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposer.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgRegisterProposerResponse.FromString,
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
    def RegisterValidator(request,
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
            '/neurion.fusion.Msg/RegisterValidator',
            neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidator.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgRegisterValidatorResponse.FromString,
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
    def StartTesting(request,
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
            '/neurion.fusion.Msg/StartTesting',
            neurion_dot_fusion_dot_tx__pb2.MsgStartTesting.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgStartTestingResponse.FromString,
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
    def RequestValidationTask(request,
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
            '/neurion.fusion.Msg/RequestValidationTask',
            neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgRequestValidationTaskResponse.FromString,
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
    def SubmitScore(request,
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
            '/neurion.fusion.Msg/SubmitScore',
            neurion_dot_fusion_dot_tx__pb2.MsgSubmitScore.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgSubmitScoreResponse.FromString,
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
    def DisputeModelScore(request,
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
            '/neurion.fusion.Msg/DisputeModelScore',
            neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScore.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgDisputeModelScoreResponse.FromString,
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
    def StartNewRound(request,
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
            '/neurion.fusion.Msg/StartNewRound',
            neurion_dot_fusion_dot_tx__pb2.MsgStartNewRound.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgStartNewRoundResponse.FromString,
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
    def TerminateTask(request,
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
            '/neurion.fusion.Msg/TerminateTask',
            neurion_dot_fusion_dot_tx__pb2.MsgTerminateTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgTerminateTaskResponse.FromString,
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
    def StakeToTask(request,
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
            '/neurion.fusion.Msg/StakeToTask',
            neurion_dot_fusion_dot_tx__pb2.MsgStakeToTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgStakeToTaskResponse.FromString,
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
    def ClaimTaskReward(request,
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
            '/neurion.fusion.Msg/ClaimTaskReward',
            neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskReward.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgClaimTaskRewardResponse.FromString,
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
    def UnstakeFromTask(request,
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
            '/neurion.fusion.Msg/UnstakeFromTask',
            neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgUnstakeFromTaskResponse.FromString,
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
    def DisclaimCreatorStatus(request,
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
            '/neurion.fusion.Msg/DisclaimCreatorStatus',
            neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatus.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgDisclaimCreatorStatusResponse.FromString,
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
    def AbortTask(request,
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
            '/neurion.fusion.Msg/AbortTask',
            neurion_dot_fusion_dot_tx__pb2.MsgAbortTask.SerializeToString,
            neurion_dot_fusion_dot_tx__pb2.MsgAbortTaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
