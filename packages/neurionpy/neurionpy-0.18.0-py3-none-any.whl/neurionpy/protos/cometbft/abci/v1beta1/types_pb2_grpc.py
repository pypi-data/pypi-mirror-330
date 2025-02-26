# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from cometbft.abci.v1beta1 import types_pb2 as cometbft_dot_abci_dot_v1beta1_dot_types__pb2

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
        + f' but the generated code in cometbft/abci/v1beta1/types_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ABCIApplicationStub(object):
    """----------------------------------------
    Service Definition

    ABCIApplication is a service for an ABCI application.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Echo = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/Echo',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEcho.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEcho.FromString,
                _registered_method=True)
        self.Flush = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/Flush',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestFlush.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseFlush.FromString,
                _registered_method=True)
        self.Info = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/Info',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInfo.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInfo.FromString,
                _registered_method=True)
        self.SetOption = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/SetOption',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestSetOption.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseSetOption.FromString,
                _registered_method=True)
        self.DeliverTx = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/DeliverTx',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestDeliverTx.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseDeliverTx.FromString,
                _registered_method=True)
        self.CheckTx = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/CheckTx',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCheckTx.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCheckTx.FromString,
                _registered_method=True)
        self.Query = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/Query',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestQuery.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseQuery.FromString,
                _registered_method=True)
        self.Commit = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/Commit',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCommit.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCommit.FromString,
                _registered_method=True)
        self.InitChain = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/InitChain',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInitChain.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInitChain.FromString,
                _registered_method=True)
        self.BeginBlock = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/BeginBlock',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestBeginBlock.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseBeginBlock.FromString,
                _registered_method=True)
        self.EndBlock = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/EndBlock',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEndBlock.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEndBlock.FromString,
                _registered_method=True)
        self.ListSnapshots = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/ListSnapshots',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestListSnapshots.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseListSnapshots.FromString,
                _registered_method=True)
        self.OfferSnapshot = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/OfferSnapshot',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestOfferSnapshot.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseOfferSnapshot.FromString,
                _registered_method=True)
        self.LoadSnapshotChunk = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/LoadSnapshotChunk',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestLoadSnapshotChunk.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseLoadSnapshotChunk.FromString,
                _registered_method=True)
        self.ApplySnapshotChunk = channel.unary_unary(
                '/cometbft.abci.v1beta1.ABCIApplication/ApplySnapshotChunk',
                request_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestApplySnapshotChunk.SerializeToString,
                response_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseApplySnapshotChunk.FromString,
                _registered_method=True)


class ABCIApplicationServicer(object):
    """----------------------------------------
    Service Definition

    ABCIApplication is a service for an ABCI application.
    """

    def Echo(self, request, context):
        """Echo returns back the same message it is sent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Flush(self, request, context):
        """Flush flushes the write buffer.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Info(self, request, context):
        """Info returns information about the application state.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOption(self, request, context):
        """SetOption sets a parameter in the application.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeliverTx(self, request, context):
        """DeliverTx applies a transaction.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckTx(self, request, context):
        """CheckTx validates a transaction.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Query(self, request, context):
        """Query queries the application state.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Commit(self, request, context):
        """Commit commits a block of transactions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitChain(self, request, context):
        """InitChain initializes the blockchain.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BeginBlock(self, request, context):
        """BeginBlock signals the beginning of a block.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndBlock(self, request, context):
        """EndBlock signals the end of a block, returns changes to the validator set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListSnapshots(self, request, context):
        """ListSnapshots lists all the available snapshots.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OfferSnapshot(self, request, context):
        """OfferSnapshot sends a snapshot offer.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadSnapshotChunk(self, request, context):
        """LoadSnapshotChunk returns a chunk of snapshot.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplySnapshotChunk(self, request, context):
        """ApplySnapshotChunk applies a chunk of snapshot.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ABCIApplicationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Echo': grpc.unary_unary_rpc_method_handler(
                    servicer.Echo,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEcho.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEcho.SerializeToString,
            ),
            'Flush': grpc.unary_unary_rpc_method_handler(
                    servicer.Flush,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestFlush.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseFlush.SerializeToString,
            ),
            'Info': grpc.unary_unary_rpc_method_handler(
                    servicer.Info,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInfo.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInfo.SerializeToString,
            ),
            'SetOption': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOption,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestSetOption.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseSetOption.SerializeToString,
            ),
            'DeliverTx': grpc.unary_unary_rpc_method_handler(
                    servicer.DeliverTx,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestDeliverTx.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseDeliverTx.SerializeToString,
            ),
            'CheckTx': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckTx,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCheckTx.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCheckTx.SerializeToString,
            ),
            'Query': grpc.unary_unary_rpc_method_handler(
                    servicer.Query,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestQuery.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseQuery.SerializeToString,
            ),
            'Commit': grpc.unary_unary_rpc_method_handler(
                    servicer.Commit,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCommit.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCommit.SerializeToString,
            ),
            'InitChain': grpc.unary_unary_rpc_method_handler(
                    servicer.InitChain,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInitChain.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInitChain.SerializeToString,
            ),
            'BeginBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.BeginBlock,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestBeginBlock.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseBeginBlock.SerializeToString,
            ),
            'EndBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.EndBlock,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEndBlock.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEndBlock.SerializeToString,
            ),
            'ListSnapshots': grpc.unary_unary_rpc_method_handler(
                    servicer.ListSnapshots,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestListSnapshots.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseListSnapshots.SerializeToString,
            ),
            'OfferSnapshot': grpc.unary_unary_rpc_method_handler(
                    servicer.OfferSnapshot,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestOfferSnapshot.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseOfferSnapshot.SerializeToString,
            ),
            'LoadSnapshotChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadSnapshotChunk,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestLoadSnapshotChunk.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseLoadSnapshotChunk.SerializeToString,
            ),
            'ApplySnapshotChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplySnapshotChunk,
                    request_deserializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestApplySnapshotChunk.FromString,
                    response_serializer=cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseApplySnapshotChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cometbft.abci.v1beta1.ABCIApplication', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('cometbft.abci.v1beta1.ABCIApplication', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ABCIApplication(object):
    """----------------------------------------
    Service Definition

    ABCIApplication is a service for an ABCI application.
    """

    @staticmethod
    def Echo(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/Echo',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEcho.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEcho.FromString,
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
    def Flush(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/Flush',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestFlush.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseFlush.FromString,
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
    def Info(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/Info',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInfo.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInfo.FromString,
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
    def SetOption(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/SetOption',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestSetOption.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseSetOption.FromString,
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
    def DeliverTx(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/DeliverTx',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestDeliverTx.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseDeliverTx.FromString,
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
    def CheckTx(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/CheckTx',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCheckTx.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCheckTx.FromString,
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
    def Query(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/Query',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestQuery.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseQuery.FromString,
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
    def Commit(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/Commit',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestCommit.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseCommit.FromString,
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
    def InitChain(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/InitChain',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestInitChain.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseInitChain.FromString,
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
    def BeginBlock(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/BeginBlock',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestBeginBlock.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseBeginBlock.FromString,
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
    def EndBlock(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/EndBlock',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestEndBlock.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseEndBlock.FromString,
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
    def ListSnapshots(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/ListSnapshots',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestListSnapshots.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseListSnapshots.FromString,
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
    def OfferSnapshot(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/OfferSnapshot',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestOfferSnapshot.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseOfferSnapshot.FromString,
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
    def LoadSnapshotChunk(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/LoadSnapshotChunk',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestLoadSnapshotChunk.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseLoadSnapshotChunk.FromString,
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
    def ApplySnapshotChunk(request,
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
            '/cometbft.abci.v1beta1.ABCIApplication/ApplySnapshotChunk',
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.RequestApplySnapshotChunk.SerializeToString,
            cometbft_dot_abci_dot_v1beta1_dot_types__pb2.ResponseApplySnapshotChunk.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
