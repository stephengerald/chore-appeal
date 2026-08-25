from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "chore_appeal.py"
SDK = "v0.2.16"
PROMPT = "Independently review a household chore completion claim"
ARGS = (
    "Three housemates share a kitchen and use this ledger only for ordinary recurring chores and friendly points.",
    "Judge only the stored chore standard, completion claim, and any peer challenge. COMPLETE requires every material requirement, PARTIAL requires real progress with a remaining requirement, and NOT_DONE lacks substantive evidence.",
)


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), *ARGS, sdk_version=SDK)


def prepare(contract, bob, charlie):
    contract.add_member("sam", "0x" + bob.hex())
    contract.add_member("lee", "0x" + charlie.hex())
    contract.create_chore("kitchen-1", "sam", "Clean the shared kitchen after the weekend meal.", "Wash or load all dishes, wipe counters and stove, sweep the floor, and remove the full trash bag.", 20)


def test_peer_challenge_review_and_points(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_bob, direct_charlie)
    direct_vm.sender = direct_bob
    contract.claim_completion("kitchen-1", "Loaded and ran the dishwasher, hand-washed pans, wiped counters and stove, swept the floor, and replaced the full trash bag.")
    direct_vm.sender = direct_charlie
    contract.challenge_claim("kitchen-1", "The floor initially looked unswept, but Sam says it was completed after the first photo and describes the final sweep.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "COMPLETE"}))
    contract.review_chore("kitchen-1")
    direct_vm.sender = direct_alice
    contract.finalize_chore("kitchen-1")
    assert contract.get_member("sam")["score"] == 20
    assert contract.get_chore("kitchen-1")["state"] == "FINALIZED"
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_partial_result_allows_exactly_one_revision(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_bob, direct_charlie)
    direct_vm.sender = direct_bob
    contract.claim_completion("kitchen-1", "The dishes were washed and counters wiped, but the floor and full trash bag were not handled yet.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "PARTIAL"}))
    contract.review_chore("kitchen-1")
    contract.request_one_revision("kitchen-1")
    contract.claim_completion("kitchen-1", "Finished the remaining work by sweeping the floor, removing the full trash bag, and checking the already cleaned dishes and counters.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "COMPLETE"}))
    contract.review_chore("kitchen-1")
    with direct_vm.expect_revert("revision_not_available"):
        contract.request_one_revision("kitchen-1")


def test_identity_and_bad_verdict_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    prepare(contract, direct_bob, direct_charlie)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_assignee"):
        contract.claim_completion("kitchen-1", "A different member must not claim completion on behalf of the assigned household member.")
    direct_vm.sender = direct_bob
    contract.claim_completion("kitchen-1", "Completed all dishes, counters, stove, floor sweeping, and trash removal required by the stored standard.")
    direct_vm.mock_llm(PROMPT, json.dumps({"verdict": "MOSTLY"}))
    with direct_vm.expect_revert("invalid_verdict"):
        contract.review_chore("kitchen-1")
    assert contract.get_chore("kitchen-1")["state"] == "CLAIMED"
