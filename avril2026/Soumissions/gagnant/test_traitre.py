import unittest

import traitre


class TraitreStrategyTests(unittest.TestCase):
    def test_first_round_collaborates(self):
        state = traitre.GameState(players=[traitre.OUR_NAME, "Alice", "Bob"])
        self.assertEqual(traitre.decide(state), traitre.COLLABORATE)

    def test_retaliates_after_recent_betrayal(self):
        state = traitre.GameState(
            players=[traitre.OUR_NAME, "Alice", "Bob"],
            history=[
                traitre.Round(
                    {
                        traitre.OUR_NAME: traitre.COLLABORATE,
                        "Alice": traitre.BETRAY,
                        "Bob": traitre.COLLABORATE,
                    }
                )
            ],
        )
        self.assertEqual(traitre.decide(state), traitre.BETRAY)

    def test_forgives_after_two_peaceful_rounds(self):
        state = traitre.GameState(
            players=[traitre.OUR_NAME, "Alice", "Bob"],
            history=[
                traitre.Round(
                    {
                        traitre.OUR_NAME: traitre.COLLABORATE,
                        "Alice": traitre.BETRAY,
                        "Bob": traitre.COLLABORATE,
                    }
                ),
                traitre.Round(
                    {
                        traitre.OUR_NAME: traitre.BETRAY,
                        "Alice": traitre.COLLABORATE,
                        "Bob": traitre.COLLABORATE,
                    }
                ),
                traitre.Round(
                    {
                        traitre.OUR_NAME: traitre.COLLABORATE,
                        "Alice": traitre.COLLABORATE,
                        "Bob": traitre.COLLABORATE,
                    }
                ),
            ],
        )
        self.assertEqual(traitre.decide(state), traitre.COLLABORATE)

    def test_betrays_near_end(self):
        state = traitre.GameState(
            players=[traitre.OUR_NAME, "Alice", "Bob"],
            total_rounds=250,
            history=[
                traitre.Round(
                    {
                        traitre.OUR_NAME: traitre.COLLABORATE,
                        "Alice": traitre.COLLABORATE,
                        "Bob": traitre.COLLABORATE,
                    }
                )
                for _ in range(242)
            ],
        )
        self.assertEqual(traitre.decide(state), traitre.BETRAY)

    def test_score_round_uses_challenge_payoffs(self):
        scores = traitre.score_round(
            {
                "Joueur1": traitre.BETRAY,
                "Joueur2": traitre.COLLABORATE,
                "Joueur3": traitre.BETRAY,
            }
        )
        self.assertEqual(scores, {"Joueur1": 4, "Joueur2": 0, "Joueur3": 4})


if __name__ == "__main__":
    unittest.main()
