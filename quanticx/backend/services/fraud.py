from __future__ import annotations

from typing import Dict


def score_transaction(features: Dict) -> float:
    # Simple heuristic placeholder
    amount = float(features.get('amount', 0))
    country = str(features.get('country', 'UA'))
    risky = {'RU', 'BY', 'IR', 'KP'}
    base = amount / 1000.0
    if country in risky:
        base += 0.3
    return min(1.0, round(base, 2))
