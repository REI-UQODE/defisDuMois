#!/usr/bin/env python3
"""Soumission pour le defi Traitre.exe."""

from __future__ import annotations

import argparse
import json
import random
import sys
import unicodedata
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Mapping, MutableMapping, Sequence


COLLABORATE = "collaborer"
BETRAY = "trahir"
OUR_NAME = "Traitre.exe"


ACTION_ALIASES = {
    "c": COLLABORATE,
    "cooperate": COLLABORATE,
    "cooperer": COLLABORATE,
    "coop?rer": COLLABORATE,
    "collaborer": COLLABORATE,
    "collabore": COLLABORATE,
    "confiance": COLLABORATE,
    "faire confiance": COLLABORATE,
    "d": BETRAY,
    "defect": BETRAY,
    "betray": BETRAY,
    "trahir": BETRAY,
    "trahit": BETRAY,
    "traitre": BETRAY,
    "tra?tre": BETRAY,
}

PAYOFFS = {
    (COLLABORATE, COLLABORATE): 2,
    (COLLABORATE, BETRAY): 0,
    (BETRAY, COLLABORATE): 3,
    (BETRAY, BETRAY): 1,
}


def normalize_action(value: object) -> str:
    """Convertit une action recue en valeur canonique."""
    key = strip_accents(str(value).strip().lower())
    if key not in ACTION_ALIASES:
        raise ValueError(f"action inconnue: {value!r}")
    return ACTION_ALIASES[key]


def strip_accents(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value)
    return "".join(character for character in decomposed if unicodedata.category(character) != "Mn")


@dataclass(frozen=True)
class Round:
    """Tour deja joue."""

    actions: Mapping[str, str]

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "Round":
        actions = value.get("actions", value)
        if not isinstance(actions, Mapping):
            raise ValueError("un tour doit contenir un objet 'actions'")
        return cls({str(player): normalize_action(action) for player, action in actions.items()})


@dataclass
class GameState:
    """Etat public de la partie."""

    players: List[str]
    self_name: str = OUR_NAME
    total_rounds: int = 250
    history: List[Round] = field(default_factory=list)

    @property
    def round_number(self) -> int:
        return len(self.history) + 1

    @property
    def opponents(self) -> List[str]:
        return [player for player in self.players if player != self.self_name]

    @classmethod
    def from_json(cls, data: Mapping[str, object]) -> "GameState":
        players = data.get("players")
        if not isinstance(players, list) or not players:
            raise ValueError("le JSON doit contenir une liste 'players'")

        self_name = str(data.get("self", data.get("self_name", OUR_NAME)))
        total_rounds = int(data.get("total_rounds", data.get("rounds", 250)))
        raw_history = data.get("history", [])
        if not isinstance(raw_history, list):
            raise ValueError("'history' doit etre une liste")

        return cls(
            players=[str(player) for player in players],
            self_name=self_name,
            total_rounds=total_rounds,
            history=[Round.from_mapping(round_data) for round_data in raw_history],
        )


def decide(state: GameState) -> str:
    """Choisit la prochaine action."""

    round_number = state.round_number
    opponents = state.opponents
    if len(opponents) != 2:
        raise ValueError("ce defi attend exactement trois joueurs")

    if round_number > max(1, state.total_rounds - 8):
        return BETRAY

    if not state.history:
        return COLLABORATE

    recent = state.history[-4:]
    last_round = state.history[-1].actions
    opponent_stats = {opponent: _stats_for(opponent, state.history) for opponent in opponents}
    recent_betrayals = sum(
        1
        for turn in recent
        for opponent in opponents
        if turn.actions.get(opponent) == BETRAY
    )
    last_betrayers = [opponent for opponent in opponents if last_round.get(opponent) == BETRAY]

    if all(stats["betray_rate"] >= 0.55 and stats["rounds"] >= 8 for stats in opponent_stats.values()):
        return BETRAY

    if last_betrayers:
        if len(last_betrayers) == 1:
            culprit = last_betrayers[0]
            stats = opponent_stats[culprit]
            if stats["betray_rate"] <= 0.18 and recent_betrayals == 1:
                return COLLABORATE
        return BETRAY

    if round_number in {37, 89, 151, 211} and recent_betrayals == 0:
        return BETRAY

    if recent_betrayals == 0:
        return COLLABORATE

    if len(state.history) >= 2:
        previous_two = state.history[-2:]
        if all(
            turn.actions.get(opponent) == COLLABORATE
            for turn in previous_two
            for opponent in opponents
        ):
            return COLLABORATE

    return BETRAY


def _stats_for(player: str, history: Sequence[Round]) -> Dict[str, float]:
    actions = [turn.actions.get(player) for turn in history if player in turn.actions]
    betrayals = sum(1 for action in actions if action == BETRAY)
    rounds = len(actions)
    return {
        "rounds": float(rounds),
        "betrayals": float(betrayals),
        "betray_rate": betrayals / rounds if rounds else 0.0,
    }


Strategy = Callable[[GameState], str]


def strategy_traitre(state: GameState) -> str:
    return decide(state)


def strategy_always_cooperate(state: GameState) -> str:
    return COLLABORATE


def strategy_always_betray(state: GameState) -> str:
    return BETRAY


def strategy_tit_for_tat(state: GameState) -> str:
    if not state.history:
        return COLLABORATE
    opponents = state.opponents
    return BETRAY if any(state.history[-1].actions.get(player) == BETRAY for player in opponents) else COLLABORATE


def strategy_grudger(state: GameState) -> str:
    opponents = state.opponents
    for turn in state.history:
        if any(turn.actions.get(player) == BETRAY for player in opponents):
            return BETRAY
    return COLLABORATE


def strategy_random_factory(seed: int) -> Strategy:
    rng = random.Random(seed)

    def strategy_random(state: GameState) -> str:
        return BETRAY if rng.random() < 0.5 else COLLABORATE

    return strategy_random


BUILTIN_STRATEGIES: Dict[str, Strategy] = {
    "traitre": strategy_traitre,
    "cooperateur": strategy_always_cooperate,
    "mefiant": strategy_always_betray,
    "donnant-donnant": strategy_tit_for_tat,
    "rancunier": strategy_grudger,
}


def score_round(actions: Mapping[str, str]) -> Dict[str, int]:
    scores = {player: 0 for player in actions}
    players = list(actions)
    for i, player in enumerate(players):
        for opponent in players[i + 1 :]:
            player_action = actions[player]
            opponent_action = actions[opponent]
            scores[player] += PAYOFFS[(player_action, opponent_action)]
            scores[opponent] += PAYOFFS[(opponent_action, player_action)]
    return scores


def simulate(strategies: Mapping[str, Strategy], rounds: int) -> Dict[str, int]:
    players = list(strategies)
    totals = {player: 0 for player in players}
    history: List[Round] = []

    for _ in range(rounds):
        actions: MutableMapping[str, str] = {}
        for player, strategy in strategies.items():
            state = GameState(players=players, self_name=player, total_rounds=rounds, history=history)
            actions[player] = normalize_action(strategy(state))

        round_scores = score_round(actions)
        for player, points in round_scores.items():
            totals[player] += points
        history.append(Round(actions=dict(actions)))

    return totals


def parse_state_from_stdin() -> GameState:
    content = sys.stdin.read().strip()
    if not content:
        raise ValueError("aucun JSON recu sur stdin")
    return GameState.from_json(json.loads(content))


def command_action(args: argparse.Namespace) -> int:
    if args.state:
        with open(args.state, "r", encoding="utf-8") as handle:
            state = GameState.from_json(json.load(handle))
    else:
        state = parse_state_from_stdin()
    print(decide(state))
    return 0


def command_simulate(args: argparse.Namespace) -> int:
    selected: Dict[str, Strategy] = {}
    for index, name in enumerate(args.players):
        if name == "aleatoire":
            selected[f"aleatoire-{index + 1}"] = strategy_random_factory(args.seed + index)
            continue
        if name not in BUILTIN_STRATEGIES:
            choices = ", ".join(sorted([*BUILTIN_STRATEGIES, "aleatoire"]))
            raise ValueError(f"strategie inconnue {name!r}; choix: {choices}")
        player_name = OUR_NAME if name == "traitre" else name
        suffix = 2
        unique_name = player_name
        while unique_name in selected:
            unique_name = f"{player_name}-{suffix}"
            suffix += 1
        selected[unique_name] = BUILTIN_STRATEGIES[name]

    if len(selected) != 3:
        raise ValueError("la simulation attend exactement trois strategies")

    totals = simulate(selected, args.rounds)
    width = max(len(player) for player in totals)
    for player, score in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"{player:<{width}}  {score:4d} $")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Agent et simulateur pour le defi Traitre.exe.",
    )
    subparsers = parser.add_subparsers(dest="command")

    action_parser = subparsers.add_parser("action", help="calcule la prochaine action depuis un etat JSON")
    action_parser.add_argument("--state", help="chemin vers un fichier JSON d'etat; stdin par defaut")
    action_parser.set_defaults(func=command_action)

    simulate_parser = subparsers.add_parser("simulate", help="lance une simulation locale")
    simulate_parser.add_argument("--rounds", type=int, default=250, help="nombre de tours")
    simulate_parser.add_argument("--seed", type=int, default=2026, help="graine des strategies aleatoires")
    simulate_parser.add_argument(
        "--players",
        nargs=3,
        default=["traitre", "donnant-donnant", "rancunier"],
        metavar=("P1", "P2", "P3"),
        help="strategies: traitre, cooperateur, mefiant, donnant-donnant, rancunier, aleatoire",
    )
    simulate_parser.set_defaults(func=command_simulate)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"erreur: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
