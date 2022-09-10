from enchant.checker import SpellChecker

MAX_ERROR_COUNT = 4
MIN_TEXT_LENGTH = 3

"""
Detect that string is english or not.
"""
def is_en(txt):
    d = SpellChecker("en_US")
    d.set_text(txt)
    errors = [err.word for err in d]
    return False if ((len(errors) > MAX_ERROR_COUNT) or len(txt.split()) < MIN_TEXT_LENGTH) else True

