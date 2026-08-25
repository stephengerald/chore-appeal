import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_peer_challenge_review(default_account, secondary_account, tertiary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "chore_appeal.py")
    args = ["Three housemates share a kitchen and use this ledger only for ordinary chores and friendly points.", "COMPLETE requires every material requirement, PARTIAL requires real progress with work remaining, and NOT_DONE lacks substantive evidence."]
    deployed = _ok(factory.deploy_contract_tx(args=args, account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    household = factory.build_contract(address, account=default_account)
    worker = factory.build_contract(address, account=secondary_account)
    peer = factory.build_contract(address, account=tertiary_account)
    _ok(household.add_member(args=["sam", secondary_account.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(household.add_member(args=["lee", tertiary_account.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(household.create_chore(args=["kitchen", "sam", "Clean the shared kitchen after the weekend meal.", "Wash dishes, wipe counters and stove, sweep the floor, and remove the full trash bag.", 20]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(worker.claim_completion(args=["kitchen", "Loaded and ran the dishwasher, washed pans, wiped counters and stove, swept the floor, and removed the full trash bag."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(peer.challenge_claim(args=["kitchen", "The floor initially looked unswept, but the assignee documents a final sweep after that observation."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(peer.review_chore(args=["kitchen"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    verdict = household.get_chore(args=["kitchen"]).call()["verdict"]
    assert verdict in ("COMPLETE", "PARTIAL", "NOT_DONE")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": verdict}, sort_keys=True))
