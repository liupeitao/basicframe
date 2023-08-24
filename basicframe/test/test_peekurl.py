from basicframe.utils.peekurl import judge_full_type, judge_psp_type


def test_judge_psp_type():
    assert judge_psp_type('https://wetter.faz.net/')
def test_judge_full_type():
    assert judge_full_type('https://wetter.faz.net/')
