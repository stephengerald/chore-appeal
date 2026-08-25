from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently review a household chore completion claim"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"verdict": "COMPLETE"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_chore_appeal_flow():
    owner, assignee, challenger = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "chore_appeal.py")
    args = ["Three housemates share a kitchen and use this ledger only for ordinary chores and friendly points.", "COMPLETE requires every material requirement, PARTIAL requires real progress with work remaining, and NOT_DONE lacks substantive evidence."]
    deployed = factory.deploy_contract_tx(args=args, account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    household = factory.build_contract(address, account=owner)
    worker = factory.build_contract(address, account=assignee)
    peer = factory.build_contract(address, account=challenger)
    ok(household.add_member(args=["sam", assignee.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(household.add_member(args=["lee", challenger.address]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(household.create_chore(args=["kitchen", "sam", "Clean the shared kitchen after the weekend meal.", "Wash dishes, wipe counters and stove, sweep the floor, and remove the full trash bag.", 20]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(worker.claim_completion(args=["kitchen", "Loaded and ran the dishwasher, washed pans, wiped counters and stove, swept the floor, and removed the full trash bag."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(peer.challenge_claim(args=["kitchen", "The floor initially looked unswept, but the assignee documents a final sweep after that observation."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(peer.review_chore(args=["kitchen"]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(household.finalize_chore(args=["kitchen"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert household.get_member(args=["sam"]).call()["score"] == 20
