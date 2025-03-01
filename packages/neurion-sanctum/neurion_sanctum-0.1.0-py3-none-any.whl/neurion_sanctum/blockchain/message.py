from neurionpy.protos.neurion.sanctum.tx_pb2 import (
    MsgSubmitDatasetApplication, MsgApproveApplication,
    MsgRejectApplication, MsgDisclaimDataset, MsgRequestToUseDataset,
    MsgCancelDatasetUsageRequest, MsgRejectDatasetUsageRequest,
    MsgApproveDatasetUsageRequest, MsgAddProcessor, MsgRemoveProcessor,
    MsgProcessDatasetUsageRequest, MsgFinishDatasetUsageRequest,
    MsgDisputeDatasetUsageRequest, MsgApproveDispute, MsgRejectDispute,
    MsgStakeToSanctum, MsgUnstakeFromSanctum, MsgClaimReward
)
from .client import get_message_client
from .wallet import get_wallet


def _prepare_message(message) -> None:
    """Automatically assigns `creator` to the wallet's address if not set."""
    wallet = get_wallet()
    if hasattr(message, "creator") and not message.creator:
        message.creator = str(wallet.address())


def submit_dataset_application(encrypted_data_link: str, explanation_link: str, contact: str,
                               stake: int, proof_of_authenticity: str, dataset_usage_fee: int) -> None:
    """Submit a dataset application."""
    message_client = get_message_client()
    message = MsgSubmitDatasetApplication(
        encrypted_data_link=encrypted_data_link,
        explanation_link=explanation_link,
        contact=contact,
        stake=stake,
        proof_of_authenticity=proof_of_authenticity,
        dataset_usage_fee=dataset_usage_fee
    )
    _prepare_message(message)
    tx = message_client.SubmitDatasetApplication(message)
    tx.wait_to_complete()


def approve_application(application_id: int, reason: str) -> None:
    """Approve a dataset application."""
    message_client = get_message_client()
    message = MsgApproveApplication(application_id=application_id, reason=reason)
    _prepare_message(message)
    tx = message_client.ApproveApplication(message)
    tx.wait_to_complete()


def reject_application(application_id: int, reason: str) -> None:
    """Reject a dataset application."""
    message_client = get_message_client()
    message = MsgRejectApplication(application_id=application_id, reason=reason)
    _prepare_message(message)
    tx = message_client.RejectApplication(message)
    tx.wait_to_complete()


def disclaim_dataset(application_id: int, reason: str) -> None:
    """Disclaim a dataset."""
    message_client = get_message_client()
    message = MsgDisclaimDataset(application_id=application_id, reason=reason)
    _prepare_message(message)
    tx = message_client.DisclaimDataset(message)
    tx.wait_to_complete()


def request_to_use_dataset(dataset_id: int, intent: str, training_repository: str, contact: str) -> None:
    """Request to use a dataset."""
    message_client = get_message_client()
    message = MsgRequestToUseDataset(
        dataset_id=dataset_id, intent=intent, training_repository=training_repository, contact=contact
    )
    _prepare_message(message)
    tx = message_client.RequestToUseDataset(message)
    tx.wait_to_complete()


def cancel_dataset_usage_request(request_id: int, reason: str) -> None:
    """Cancel a dataset usage request."""
    message_client = get_message_client()
    message = MsgCancelDatasetUsageRequest(request_id=request_id, reason=reason)
    _prepare_message(message)
    tx = message_client.CancelDatasetUsageRequest(message)
    tx.wait_to_complete()


def reject_dataset_usage_request(request_id: int, reason: str) -> None:
    """Reject a dataset usage request."""
    message_client = get_message_client()
    message = MsgRejectDatasetUsageRequest(request_id=request_id, reason=reason)
    _prepare_message(message)
    tx = message_client.RejectDatasetUsageRequest(message)
    tx.wait_to_complete()


def approve_dataset_usage_request(request_id: int, reason: str) -> None:
    """Approve a dataset usage request."""
    message_client = get_message_client()
    message = MsgApproveDatasetUsageRequest(request_id=request_id, reason=reason)
    _prepare_message(message)
    tx = message_client.ApproveDatasetUsageRequest(message)
    tx.wait_to_complete()


def add_processor(processor: str) -> None:
    """Add a processor."""
    message_client = get_message_client()
    message = MsgAddProcessor(processor=processor)
    _prepare_message(message)
    tx = message_client.AddProcessor(message)
    tx.wait_to_complete()


def remove_processor(processor: str) -> None:
    """Remove a processor."""
    message_client = get_message_client()
    message = MsgRemoveProcessor(processor=processor)
    _prepare_message(message)
    tx = message_client.RemoveProcessor(message)
    tx.wait_to_complete()


def process_dataset_usage_request(request_id: int) -> None:
    """Process a dataset usage request."""
    message_client = get_message_client()
    message = MsgProcessDatasetUsageRequest(request_id=request_id)
    _prepare_message(message)
    tx = message_client.ProcessDatasetUsageRequest(message)
    tx.wait_to_complete()


def finish_dataset_usage_request(request_id: int, feedback: str) -> None:
    """Finish a dataset usage request."""
    message_client = get_message_client()
    message = MsgFinishDatasetUsageRequest(request_id=request_id, feedback=feedback)
    _prepare_message(message)
    tx = message_client.FinishDatasetUsageRequest(message)
    tx.wait_to_complete()


def dispute_dataset_usage_request(request_id: int, model: str, reason: str) -> None:
    """Dispute a dataset usage request."""
    message_client = get_message_client()
    message = MsgDisputeDatasetUsageRequest(request_id=request_id, model=model, reason=reason)
    _prepare_message(message)
    tx = message_client.DisputeDatasetUsageRequest(message)
    tx.wait_to_complete()


def approve_dispute(request_id: int, reason: str) -> None:
    """Approve a dispute."""
    message_client = get_message_client()
    message = MsgApproveDispute(request_id=request_id, reason=reason)
    _prepare_message(message)
    tx = message_client.ApproveDispute(message)
    tx.wait_to_complete()


def reject_dispute(request_id: int, reason: str) -> None:
    """Reject a dispute."""
    message_client = get_message_client()
    message = MsgRejectDispute(request_id=request_id, reason=reason)
    _prepare_message(message)
    tx = message_client.RejectDispute(message)
    tx.wait_to_complete()


def stake_to_sanctum(amount: int) -> None:
    """Stake tokens to Sanctum."""
    message_client = get_message_client()
    message = MsgStakeToSanctum(amount=amount)
    _prepare_message(message)
    tx = message_client.StakeToSanctum(message)
    tx.wait_to_complete()


def unstake_from_sanctum(amount: int) -> None:
    """Unstake tokens from Sanctum."""
    message_client = get_message_client()
    message = MsgUnstakeFromSanctum(amount=amount)
    _prepare_message(message)
    tx = message_client.UnstakeFromSanctum(message)
    tx.wait_to_complete()


def claim_reward() -> None:
    """Claim rewards."""
    message_client = get_message_client()
    message = MsgClaimReward()
    _prepare_message(message)
    tx = message_client.ClaimReward(message)
    tx.wait_to_complete()