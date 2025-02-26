from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.ibc.core.connection.interface import IBCCoreConnection  # type: ignore
from neurionpy.protos.ibc.core.connection.v1.query_pb2 import (
    QueryClientConnectionsRequest,
    QueryClientConnectionsResponse,
    QueryConnectionClientStateRequest,
    QueryConnectionClientStateResponse,
    QueryConnectionConsensusStateRequest,
    QueryConnectionConsensusStateResponse,
    QueryConnectionRequest,
    QueryConnectionResponse,
    QueryConnectionsRequest,
    QueryConnectionsResponse,
)


class IBCCoreConnectionRestClient(IBCCoreConnection):
    """IBC Core Connection REST client."""

    API_URL = "/ibc/core/connection/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Connection(self, request: QueryConnectionRequest) -> QueryConnectionResponse:
        """
        Connection queries an IBC connection end.

        :param request: QueryConnectionRequest
        :return: QueryConnectionResponse
        """  # noqa: D401
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}"
        )
        return Parse(json_response, QueryConnectionResponse())

    def Connections(self, request: QueryConnectionsRequest) -> QueryConnectionsResponse:
        """
        Connections queries all the IBC connections of a chain.

        :param request: QueryConnectionsRequest
        :return: QueryConnectionsResponse
        """  # noqa: D401
        json_response = self._rest_api.get(f"{self.API_URL}/connections", request)
        return Parse(json_response, QueryConnectionsResponse())

    def ClientConnections(
        self, request: QueryClientConnectionsRequest
    ) -> QueryClientConnectionsResponse:
        """
        ClientConnections queries the connection paths associated with a client state.

        :param request: QueryClientConnectionsRequest
        :return: QueryClientConnectionsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/client_connections/{request.client_id}"
        )
        return Parse(json_response, QueryClientConnectionsResponse())

    def ConnectionClientState(
        self, request: QueryConnectionClientStateRequest
    ) -> QueryConnectionClientStateResponse:
        """
        ConnectionClientState queries the client state associated with the connection.

        :param request: QueryConnectionClientStateRequest
        :return: QueryConnectionClientStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}/client_state"
        )
        return Parse(json_response, QueryConnectionClientStateResponse())

    def ConnectionConsensusState(
        self, request: QueryConnectionConsensusStateRequest
    ) -> QueryConnectionConsensusStateResponse:
        """
        ConnectionConsensusState queries the consensus state associated with the connection.

        :param request: QueryConnectionConsensusStateRequest
        :return: QueryConnectionConsensusStateResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/connections/{request.connection_id}/consensus_state/revision/{request.revision_number}/height/{request.revision_height}"
        )
        return Parse(json_response, QueryConnectionConsensusStateResponse())
