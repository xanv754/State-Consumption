from common.utils.validate import validate_name_bras


def test_validate_name_bras():
    assert (
        validate_name_bras("ANZ-BRAS-00_HUAWEI_00") == True
        and validate_name_bras("ANZ") == False
        and validate_name_bras("PER-BRAS-00_HUAWEI_00-00") == False
    )
