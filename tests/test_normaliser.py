from enelvo import normaliser

def test_raw():
    norm = normaliser.Normaliser()
    assert norm.normalise('Que dia lindo') == 'que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'hoje eu vou dar uma voltinha 😀'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'vou dar uma passada na casa do eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'domingo é dia de paredão no bbb'
    assert norm.normalise('#python > #javascript') == 'hashtag > hashtag'

def test_sanitize():
    norm = normaliser.Normaliser(sanitize=True)
    assert norm.normalise('Que dia lindo') == 'que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'hoje eu vou dar uma voltinha'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'vou dar uma passada na casa do eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'domingo é dia de paredão no bbb'
    assert norm.normalise('#python > #javascript') == 'hashtag hashtag'

def test_capitalize_pns():
    norm = normaliser.Normaliser(capitalize_pns=True)
    assert norm.normalise('Que dia lindo') == 'que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'hoje eu vou dar uma voltinha 😀'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'vou dar uma passada na casa do Eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'domingo é dia de paredão no bbb'
    assert norm.normalise('#python > #javascript') == 'Hashtag > Hashtag'

def test_capitalize_inis():
    norm = normaliser.Normaliser(capitalize_inis=True)
    assert norm.normalise('Que dia lindo') == 'Que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'Hoje eu vou dar uma voltinha 😀'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'Vou dar uma passada na casa do eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'Domingo é dia de paredão no bbb'
    assert norm.normalise('#python > #javascript') == 'Hashtag > hashtag'

def test_capitalize_acs():
    norm = normaliser.Normaliser(capitalize_acs=True)
    assert norm.normalise('Que dia lindo') == 'que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'hoje eu vou dar uma voltinha 😀'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'vou dar uma passada na casa do eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'domingo é dia de paredão no BBB'
    assert norm.normalise('#python > #javascript') == 'hashtag > hashtag'

def test_readable_tokenizer():
    norm = normaliser.Normaliser(tokenizer='readable')
    assert norm.normalise('Que dia lindo') == 'que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'hoje eu vou dar uma voltinha 😀'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'vou dar uma passada na casa do eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'domingo é dia de paredão no bbb'
    assert norm.normalise('#python > #javascript') == '#python > #javascript'

def test_all():
    norm = normaliser.Normaliser(sanitize=True, capitalize_pns=True, capitalize_inis=True, capitalize_acs=True, tokenizer='readable')
    assert norm.normalise('Que dia lindo') == 'Que dia lindo'
    assert norm.normalise('Hoje eu vou dar uma voltinha 😀') == 'Hoje eu vou dar uma voltinha'
    assert norm.normalise('Vou dar uma passada na casa do Eduardo') == 'Vou dar uma passada na casa do Eduardo'
    assert norm.normalise('Domingo é dia de paredão no BBB') == 'Domingo é dia de paredão no BBB'
    assert norm.normalise('#python > #javascript') == 'python javascript'
    