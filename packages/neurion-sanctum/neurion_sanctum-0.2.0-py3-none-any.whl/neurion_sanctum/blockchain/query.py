from neurionpy.protos.neurion.sanctum.query_pb2 import (
    QueryParamsRequest, QueryParamsResponse,
    QueryGetAvailableDatasetsRequest, QueryGetAvailableDatasetsResponse,
    QueryGetApprovedUsageRequestsRequest, QueryGetApprovedUsageRequestsResponse,
    QueryGetRewardRequest, QueryGetRewardResponse,
    QueryGetStakeRequest, QueryGetStakeResponse,
    QueryGetPendingDatasetsRequest, QueryGetPendingDatasetsResponse,
    QueryGetPendingUsageRequestsRequest, QueryGetPendingUsageRequestsResponse,
    QueryGetDatasetRequest, QueryGetDatasetResponse,
    QueryGetUsageRequestRequest, QueryGetUsageRequestResponse,
    QueryGetUsageRequestsForDatasetRequest, QueryGetUsageRequestsForDatasetResponse,
    QueryGetUsageRequestsForUserRequest, QueryGetUsageRequestsForUserResponse,
    QueryGetDatasetsForUserRequest, QueryGetDatasetsForUserResponse
)
from .client import get_query_client
from .wallet import get_wallet


def params() -> QueryParamsResponse:
    """Query Sanctum module parameters."""
    query_client = get_query_client()
    return query_client.Params(QueryParamsRequest())


def get_available_datasets(offset: int, limit: int) -> QueryGetAvailableDatasetsResponse:
    """Query available datasets with pagination."""
    query_client = get_query_client()
    return query_client.GetAvailableDatasets(QueryGetAvailableDatasetsRequest(offset=offset, limit=limit))


def get_approved_usage_requests() -> QueryGetApprovedUsageRequestsResponse:
    """Query all approved dataset usage requests."""
    query_client = get_query_client()
    return query_client.GetApprovedUsageRequests(QueryGetApprovedUsageRequestsRequest())


def get_reward() -> QueryGetRewardResponse:
    """Query the user’s rewards."""
    query_client = get_query_client()
    wallet = get_wallet()
    return query_client.GetReward(QueryGetRewardRequest(user=str(wallet.address())))


def get_stake() -> QueryGetStakeResponse:
    """Query the user’s staked amount in Sanctum."""
    query_client = get_query_client()
    wallet = get_wallet()
    return query_client.GetStake(QueryGetStakeRequest(user=str(wallet.address())))


def get_pending_datasets() -> QueryGetPendingDatasetsResponse:
    """Query all pending dataset applications."""
    query_client = get_query_client()
    return query_client.GetPendingDatasets(QueryGetPendingDatasetsRequest())


def get_pending_usage_requests() -> QueryGetPendingUsageRequestsResponse:
    """Query all pending dataset usage requests for the user."""
    query_client = get_query_client()
    wallet = get_wallet()
    return query_client.GetPendingUsageRequests(QueryGetPendingUsageRequestsRequest(user=str(wallet.address())))


def get_dataset(dataset_id: int) -> QueryGetDatasetResponse:
    """Query a dataset by its ID."""
    query_client = get_query_client()
    return query_client.GetDataset(QueryGetDatasetRequest(id=dataset_id))


def get_usage_request(request_id: int) -> QueryGetUsageRequestResponse:
    """Query a specific dataset usage request by its ID."""
    query_client = get_query_client()
    return query_client.GetUsageRequest(QueryGetUsageRequestRequest(id=request_id))


def get_usage_requests_for_dataset(dataset_id: int, offset: int, limit: int) -> QueryGetUsageRequestsForDatasetResponse:
    """Query dataset usage requests for a specific dataset."""
    query_client = get_query_client()
    return query_client.GetUsageRequestsForDataset(
        QueryGetUsageRequestsForDatasetRequest(dataset_id=dataset_id, offset=offset, limit=limit)
    )


def get_usage_requests_for_user(offset: int, limit: int) -> QueryGetUsageRequestsForUserResponse:
    """Query dataset usage requests made by the user."""
    query_client = get_query_client()
    wallet = get_wallet()
    return query_client.GetUsageRequestsForUser(
        QueryGetUsageRequestsForUserRequest(user=str(wallet.address()), offset=offset, limit=limit)
    )


def get_datasets_for_user(offset: int, limit: int) -> QueryGetDatasetsForUserResponse:
    """Query datasets submitted by the user."""
    query_client = get_query_client()
    wallet = get_wallet()
    return query_client.GetDatasetsForUser(
        QueryGetDatasetsForUserRequest(user=str(wallet.address()), offset=offset, limit=limit)
    )