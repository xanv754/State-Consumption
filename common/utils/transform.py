def bits_a_gbps(bits: float) -> float:
    """Converts bits to gigabytes."""
    gigabits = bits / 1000000000
    return round(gigabits, 2)