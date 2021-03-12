# -*- coding: utf-8 -*-

__all__ = (
    "StakeCommand",
    "SetStakeCommand",
    "PRepCommand",
    "PRepsCommand",
    "MainPRepsCommand",
    "SubPRepsCommand",
    "DelegationCommand",
    "IScoreCommand",
    "ClaimIScoreCommand",
)

import functools
from typing import Dict, Any

import icon
from icon.data import (
    Address,
    str_to_object_by_type,
)
from icon.data.unit import loop_to_str
from icon.wallet import KeyWallet

from .command import Command
from .. import result_type
from ..score.system import SystemScore
from ..utils import (
    confirm_transaction,
    get_address_from_args,
    print_result,
    print_request,
    print_response,
    resolve_nid,
    resolve_url,
    resolve_wallet,
)


class StakeCommand(Command):
    def __init__(self):
        super().__init__(name="stake", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getStake command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument("address", type=str, nargs="?", help="address")
        parser.add_argument(
            "--keystore", "-k", type=str, required=False, help="keystore file path"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        address: Address = get_address_from_args(args)

        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_stake(address, hooks=self._hooks)
        self._print_result(result)

        return 0

    @classmethod
    def _print_result(cls, result: Dict[str, str]):
        result: Dict[str, Any] = str_to_object_by_type(
            result_type.GET_STAKE, result
        )

        result["stake"] = loop_to_str(result["stake"])

        print_result(result)


class SetStakeCommand(Command):
    def __init__(self):
        super().__init__(name="setStake", readonly=False)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "setStake command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument("stake", type=int, help="stake")
        parser.set_defaults(func=self._run)

    def _run(self, args) -> bytes:
        score = _create_system_score(args, invoke=True)
        return score.set_stake(args.stake, hooks=self._hooks)


class PRepCommand(Command):
    def __init__(self):
        super().__init__(name="prep", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getPRep command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument("address", type=str, nargs="?", help="address")
        parser.add_argument(
            "--keystore", "-k", type=str, required=False, help="keystore file path"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        address: Address = get_address_from_args(args)

        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_prep(address, hooks=self._hooks)

        result: Dict[str, Any] = str_to_object_by_type(result_type.GET_PREP, result)
        print_result(result)

        return 0


class PRepsCommand(Command):
    def __init__(self):
        super().__init__(name="preps", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getPReps command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument(
            "--start", type=int, nargs="?", default=0, help="start ranking"
        )
        parser.add_argument(
            "--end", type=int, nargs="?", default=0, help="end ranking"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        start: int = args.start
        end: int = args.end

        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_preps(start, end, hooks=self._hooks)

        result: Dict[str, Any] = str_to_object_by_type(result_type.GET_PREPS, result)
        print_result(result)

        return 0


class MainPRepsCommand(Command):
    def __init__(self):
        super().__init__(name="mainpreps", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getMainPReps command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_main_preps(hooks=self._hooks)
        print_result(result)

        return 0


class SubPRepsCommand(Command):
    def __init__(self):
        super().__init__(name="subpreps", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getSubPReps command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_sub_preps(hooks=self._hooks)
        print_result(result)

        return 0


class PRepStatsCommand(Command):
    def __init__(self):
        super().__init__(name="preps", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getPRepStats command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_prep_stats(hooks=self._hooks)

        result: Dict[str, Any] = str_to_object_by_type(result_type.GET_PREPS, result)
        print_result(result)

        return 0


class DelegationCommand(Command):
    def __init__(self):
        super().__init__(name="delegation", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "getDelegation command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument("address", type=str, nargs="?", help="address")
        parser.add_argument(
            "--keystore", "-k", type=str, required=False, help="keystore file path"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        address: Address = get_address_from_args(args)

        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.get_delegation(address, hooks=self._hooks)

        result: Dict[str, Any] = str_to_object_by_type(
            result_type.GET_DELEGATION, result
        )
        loop: int = result["totalDelegated"]
        result["totalDelegated"] = loop_to_str(loop)

        print_result(result)

        return 0


class IScoreCommand(Command):
    def __init__(self):
        super().__init__(name="iscore", readonly=True)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "queryIScore command of system score"

        parser = sub_parser.add_parser(
            self.name, parents=[common_parent_parser], help=desc
        )

        parser.add_argument("address", type=str, nargs="?", help="address")
        parser.add_argument(
            "--keystore", "-k", type=str, required=False, help="keystore file path"
        )
        parser.set_defaults(func=self._run)

    def _run(self, args) -> int:
        address: Address = get_address_from_args(args)

        score = _create_system_score(args, invoke=False)
        result: Dict[str, str] = score.query_iscore(address, hooks=self._hooks)
        self._print_result(result)

        return 0

    @classmethod
    def _print_result(cls, result: Dict[str, str]):
        result: Dict[str, Any] = str_to_object_by_type(
            result_type.QUERY_ISCORE, result
        )

        key = "estimatedICX"
        result[key] = loop_to_str(result[key])

        print_result(result)


class ClaimIScoreCommand(Command):
    def __init__(self):
        super().__init__(name="claimIScore", readonly=False)
        self._hooks = {"request": print_request, "response": print_response}

    def init(self, sub_parser, common_parent_parser, invoke_parent_parser):
        desc = "claimIScore command of system score"

        parser = sub_parser.add_parser(
            self.name,
            parents=[common_parent_parser, invoke_parent_parser],
            help=desc
        )

        parser.set_defaults(func=self._run)

    @classmethod
    def _run(cls, args) -> bytes:
        yes: bool = args.yes

        hooks = {
            "request": [
                functools.partial(confirm_transaction, yes=yes),
                print_request,
            ],
            "response": print_response,
        }
        score = _create_system_score(args, invoke=True)
        return score.claim_iscore(hooks=hooks)


def _create_system_score(args, invoke: bool) -> SystemScore:
    url: str = resolve_url(args.url)
    nid: int = resolve_nid(args.nid, args.url)

    client: icon.Client = icon.create_client(url)

    if invoke:
        step_limit: int = args.step_limit
        estimate: bool = args.estimate
        wallet: KeyWallet = resolve_wallet(args)

        return SystemScore(
            client=client,
            owner=wallet,
            nid=nid,
            step_limit=step_limit,
            estimate=estimate
        )
    else:
        return SystemScore(client)
