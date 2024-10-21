def bits_a_gbps(bits: float) -> float:
    """Converts bits to gigabytes."""
    gigabits = bits / 1000000000
    return round(gigabits, 2)


def transform_states(state: str) -> str:
    """Transforms states to match database syntax."""
    if "-" in state:
        state = state.replace("-", " ")
    return state.upper()
