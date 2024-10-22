from common.utils.validate import name_bras


def test_validate_name_bras():
    assert (
        name_bras("ANZ-BRAS-00_HUAWEI_00") == True
        and name_bras("ANZ") == False
        and name_bras("PER-BRAS-00_HUAWEI_00-00") == False
    )
