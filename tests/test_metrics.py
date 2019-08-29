from enelvo import metrics


def test_edit_distance():
    assert metrics.edit_distance("casa", "caza") == 1
    assert metrics.edit_distance("qq eh isso", "o que é isso") == 5
    assert metrics.edit_distance("abc def zzz", "abc def zzz") == 0


def test_lcs():
    assert metrics.eval_lcs("casa", "caza", cython=False) == 3
    assert metrics.eval_lcs("qq eh isso", "o que é isso", cython=False) == 7
    assert metrics.eval_lcs("abc def zzz", "abc def zzz", cython=False) == 11
    assert metrics.eval_lcs("abc def zzz", "yyy", cython=False) == 0


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


def test_lcs_ratio_sym():
    assert metrics.lcs_ratio_sym("maca", "maçã") == 1.0
    assert metrics.lcs_ratio_sym("íimmãoaea", "iimmãó") == 6 / 9
    assert metrics.lcs_ratio_sym("íimmãoaea", "zwwqsdd") == 0.0


def test_hassan_similarity():
    assert metrics.hassan_similarity("casa", "caza") == 0.75
    assert metrics.hassan_similarity("qq eh isso", "o que é isso") == (7 / 12) / 5
    assert metrics.hassan_similarity("abc def zzz", "abc def zzz") == 1.0


def test_c_hassan_similarity():
    assert metrics.c_hassan_similarity("casa", "caza") == 0.25
    assert metrics.c_hassan_similarity("qq eh isso", "o que é isso") == 1 - (
        (7 / 12) / 5
    )
    assert metrics.c_hassan_similarity("abc def zzz", "abc def zzz") == 0.0


def test_word_frequency():
    lex = {"a": 5, "b": 15, "c": 2}
    assert metrics.word_frequency(lex, "a") == 5
    assert metrics.word_frequency(lex, "b") == 15
    assert metrics.word_frequency(lex, "c") == 2
    assert metrics.word_frequency(lex, "d") == 0
