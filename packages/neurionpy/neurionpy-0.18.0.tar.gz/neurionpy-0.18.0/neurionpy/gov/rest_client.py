from google.protobuf.json_format import Parse

from neurionpy.common.rest_client import RestClient
from neurionpy.gov.interface import Gov
from neurionpy.protos.cosmos.gov.v1beta1.query_pb2 import (
    QueryDepositRequest,
    QueryDepositResponse,
    QueryDepositsRequest,
    QueryDepositsResponse,
    QueryParamsRequest,
    QueryParamsResponse,
    QueryProposalRequest,
    QueryProposalResponse,
    QueryProposalsRequest,
    QueryProposalsResponse,
    QueryTallyResultRequest,
    QueryTallyResultResponse,
    QueryVoteRequest,
    QueryVoteResponse,
    QueryVotesRequest,
    QueryVotesResponse,
)


class GovRestClient(Gov):
    """Gov REST client."""

    API_URL = "/cosmos/gov/v1beta1"

    def __init__(self, rest_api: RestClient) -> None:
        """
        Initialize.

        :param rest_api: RestClient api
        """
        self._rest_api = rest_api

    def Proposal(self, request: QueryProposalRequest) -> QueryProposalResponse:
        """
        Proposal queries proposal details based on ProposalID.

        :param request: QueryProposalRequest with proposal id

        :return: QueryProposalResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}",
        )
        return Parse(json_response, QueryProposalResponse())

    def Proposals(self, request: QueryProposalsRequest) -> QueryProposalsResponse:
        """
        Proposals queries all proposals based on given status.

        :param request: QueryProposalsRequest

        :return: QueryProposalsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/",
            request,
        )
        return Parse(json_response, QueryProposalsResponse())

    def Vote(self, request: QueryVoteRequest) -> QueryVoteResponse:
        """
        Vote queries voted information based on proposalID, voterAddr.

        :param request: QueryVoteRequest with voter and proposal id

        :return: QueryVoteResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}/votes/{request.voter}"
        )
        return Parse(json_response, QueryVoteResponse())

    def Votes(self, request: QueryVotesRequest) -> QueryVotesResponse:
        """
        Votes queries votes of a given proposal.

        :param request: QueryVotesResponse with proposal id

        :return: QueryVotesResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}/votes/",
            request,
            ["proposalID"],
        )
        return Parse(json_response, QueryVotesResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        """
        Params queries all parameters of the gov module.

        :param request: QueryParamsRequest with params_type

        :return: QueryParamsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/params/{request.params_type}"
        )
        return Parse(json_response, QueryParamsResponse())

    def Deposit(self, request: QueryDepositRequest) -> QueryDepositResponse:
        """
        Deposit queries single deposit information based proposalID, depositAddr.

        :param request: QueryDepositRequest with depositor and proposal_id

        :return: QueryDepositResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}/deposits/{request.depositor}"
        )
        return Parse(json_response, QueryDepositResponse())

    def Deposits(self, request: QueryDepositsRequest) -> QueryDepositsResponse:
        """Deposits queries all deposits of a single proposal.

        :param request: QueryDepositsRequest with proposal_id

        :return: QueryDepositsResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}/deposits/",
            request,
            ["proposalID"],
        )
        return Parse(json_response, QueryDepositsResponse())

    def TallyResult(self, request: QueryTallyResultRequest) -> QueryTallyResultResponse:
        """
        Tally Result queries the tally of a proposal vote.

        :param request: QueryTallyResultRequest with proposal_id

        :return: QueryTallyResultResponse
        """
        json_response = self._rest_api.get(
            f"{self.API_URL}/proposals/{request.proposal_id}/tally"
        )
        return Parse(json_response, QueryTallyResultResponse())
