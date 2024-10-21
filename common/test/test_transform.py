from common.utils.transform import bits_a_gbps


def test_bits_a_gbps():
    assert bits_a_gbps(1000000000) == 1.0
