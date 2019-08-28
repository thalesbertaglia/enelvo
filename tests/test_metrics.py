from enelvo import metrics


def test_edit_distance():
    assert metrics.edit_distance("casa", "caza") == 1
    assert metrics.edit_distance("qq eh isso", "o que é isso") == 5
    assert metrics.edit_distance("abc def zzz", "abc def zzz") == 0


def test_lcs():
    assert metrics.eval_lcs("casa", "caza") == 3
    assert metrics.eval_lcs("qq eh isso", "o que é isso") == 7
    assert metrics.eval_lcs("abc def zzz", "abc def zzz") == 11
    assert metrics.eval_lcs("abc def zzz", "yyy") == 0


def test_lcs_ratio():
    assert metrics.lcs_ratio("casa", "caza") == 0.75
    assert metrics.lcs_ratio("qq eh isso", "o que é isso") == 7 / 12
    assert metrics.lcs_ratio("abc def zzz", "abc def zzz") == 1.0
    assert metrics.lcs_ratio("abc def zzz", "yyy") == 0.0


def test_complement_lcs():
    assert metrics.c_lcs("casa", "caza") == 1
    assert metrics.c_lcs("qq eh isso", "o que é isso") == 3
    assert metrics.c_lcs("abc def zzz", "abc def zzz") == 0
    assert metrics.c_lcs("abc def zzz", "yyy") == 11


def test_complement_lcs_ratio():
    assert metrics.c_lcs_ratio("casa", "caza") == 0.25
    assert metrics.c_lcs_ratio("qq eh isso", "o que é isso") == 1 - (7 / 12)
    assert metrics.c_lcs_ratio("abc def zzz", "abc def zzz") == 0.0
    assert metrics.c_lcs_ratio("abc def zzz", "yyy") == 1.0


def test_diacritic_sym():
    assert metrics.diacritic_sym("maca", "maçã") == 2
    assert metrics.diacritic_sym("ímã", "íma") == 1
    assert metrics.diacritic_sym("vose", "você") == 1
    assert metrics.diacritic_sym("maca maçã ãôíá", "abc") == 0
