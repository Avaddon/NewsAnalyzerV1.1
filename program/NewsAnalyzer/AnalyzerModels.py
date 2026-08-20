from dataclasses import dataclass, fields
from program.NewsAnalyzer.Proccessing.Tokenizer import Token
from typing import Optional

@dataclass
class Primary_Token:
    
    data_type:str
    value:str
    start:int
    end:int


@dataclass
class Action:

    before_verb: Optional[Token] = None
    verb: Optional[Token] = None
    after_verb: Optional[Token] = None


@dataclass
class Relation:

    source: Optional[str] = None
    verb: Optional[str] = None
    target: Optional[str] = None


@dataclass
class Event:

    initiator: Optional[Token] = None
    object: Optional[Token] = None
    verb: Optional[Token] = None
    date: Optional[Token] = None
    location: Optional[Token] = None         

    def get_sorted_tokens(self) -> list[Token]:

        tokens = [t for t in [self.initiator, self.object, self.verb, 
                              self.date, self.location] if t]
        return sorted(tokens, key=lambda x:x.end)

    def build_sentence(self) -> str:
        return ' '.join(token.value for token in self.get_sorted_tokens())