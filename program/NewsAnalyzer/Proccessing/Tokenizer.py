from dataclasses import dataclass
from typing import Optional
from enum import Enum
import re

class TokenType(Enum):

    WORD = 'word'
    VERB = 'verb'
    NUMBER = 'num'
    DATE = 'date'
    LOCATION = 'location'
    LOCATION_WORD = 'location_word'
    OBJECT = 'object'
    INITIATOR = 'initiator'
    DETERMINER = 'determiner'
    PREPOSITION = 'preposition'
    PLACE_PREPOSITION = 'place_preposition'
    CONJUNCTION = 'conjunction'
    NEGATION = 'negation'
    SYMBOL = 'symbol'
    COMMA = 'comma'
    PERCENT = 'percent'
    DASH = 'dash'
    QUOTE = 'quote'
    UNQUOTE = 'unquote'


@dataclass
class Token:
    type: Optional[TokenType] = None
    value: Optional[str]|Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None

class TextTokenizer:

    def __init__(self, patterns:dict):
        self.word_pattern = re.compile(r'\w+([-,.:]\w+)?([%])?')
        self.symbol_pattern = re.compile(r'([,.])')
        self.quote_pattern = re.compile(r'[«»“”—]')
        self.patterns = patterns

    def tokenize(self, text:str) -> list[Token]:

        tokens = []

        text_with_end_mark = text + ' ^'

        for match in self.word_pattern.finditer(text_with_end_mark.casefold()):
            tokens.append(Token(
                type=TokenType.WORD,
                value=match.group(),
                start=match.start(),
                end=match.end()
            ))

        for match in self.symbol_pattern.finditer(text_with_end_mark.casefold()):
            tokens.append(Token(
                type=TokenType.SYMBOL,
                value=match.group(1),
                start=match.start(),
                end=match.end()
            ))

        for match in self.quote_pattern.finditer(text_with_end_mark.casefold()):
            tokens.append(Token(
                type=TokenType.QUOTE,
                value=match.group(),
                start=match.start(),
                end=match.end()
            ))

        tokens.sort(key=lambda t:t.start)

        return tokens


    def classify_tokens(self, tokens: list[Token]) -> list[Token]:

        for token in tokens:

            if re.fullmatch(r'\d+([.,-]\d+)?', token.value):
                token.type = TokenType.NUMBER
            elif re.fullmatch(r'\d+[:]+\d+', token.value):
                token.type = TokenType.DATE
            else:
                for token_type, aliases in self.patterns.items():

                    if token.value in aliases:
                        token.type = TokenType(token_type)
                        break
        return tokens