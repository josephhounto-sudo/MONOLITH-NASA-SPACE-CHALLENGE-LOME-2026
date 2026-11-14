from csync.language import banned_hits
def test_banned_words_caught_even_negated():
    assert banned_hits("This report contains no diagnosis.") == ["diagnosis"]
def test_clean_text_passes():
    assert banned_hits("Several signals deviate together from the personal baseline for two days.") == []
def test_because_is_not_cause():
    assert banned_hits("shown because the link returned") == []
