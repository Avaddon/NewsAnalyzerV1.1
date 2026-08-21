from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy
from ..AnalyzerModels import Token
from program.NewsAnalyzer.Proccessing.Tokenizer import TokenType
from program.NewsAnalyzer.patterns import Patterns


@dataclass
class TokenBuilder:

    building:Token = field(default_factory=Token)

    def __init__(self):
        self.state: str = 'START'
        self.transitions = self.create_transitions()
        self.wspaces = {x:' ' for x in self.transitions['START']}
        self.wspaces.update({TokenType.SYMBOL:'', TokenType.COMMA:'', TokenType.UNQUOTE:''})

    def create_transitions(self) -> dict:
        return {
            'START':{
                TokenType.DETERMINER:'PREPOSITIONAL_PHRASE',
                TokenType.SYMBOL:'PREPOSITIONAL_PHRASE',
                TokenType.QUOTE:'CITATION',
                TokenType.UNQUOTE:'CITATION',
                TokenType.COMMA:'PREPOSITIONAL_PHRASE',
                TokenType.DASH:'PREPOSITIONAL_PHRASE',
                TokenType.PERCENT:'PREPOSITIONAL_PHRASE',
                TokenType.NEGATION:'VERB',
                TokenType.PREPOSITION:'PREPOSITIONAL_PHRASE',
                TokenType.CONJUNCTION:'CONJUNCTION',
                TokenType.WORD:'WORD',
                TokenType.VERB:'VERB',
                TokenType.NUMBER: 'NUM_BUILDER',
                TokenType.LOCATION:'LOCATION_BUILDER',
                TokenType.LOCATION_WORD: 'LOCATION_PHRASE_BUILDER',
                TokenType.DATE:'DATE_BUILDER',
                TokenType.INITIATOR:'INITIATOR_BUILDER'
                },
            'PREPOSITIONAL_PHRASE':{
                'base':          {'include':['word','dash','location_word','comma','symbol'],  'type':TokenType.PREPOSITION},
                'transitional':  ['num','determiner','location','initiator','date'],
                'trigger':       ['word'],
                'change_state':  'AFTER_WORD_PREPOSITION',
            },
            'AFTER_WORD_PREPOSITION':{
                'base':          {'include':['word','dash','location','location_word','comma','symbol'], 'type':TokenType.PREPOSITION},
                'transitional':  ['num','determiner','location','initiator','date'],
            },
            'NUM_BUILDER':{
                'base':          {'include':['num','word','symbol','comma'],  'type':TokenType.NUMBER},
                'transitional':  ['date'],
                'trigger':       ['location'],
                'change_state':  'AFTER_REGION_NUM'
            },
            'AFTER_REGION_NUM':  {'base': {'include':['num','word','symbol','comma','location'],  'type':TokenType.LOCATION}},
            'VERB':              {'base': {'include':['verb','negation','comma','symbol'],'type':TokenType.VERB}},
            'WORD':              {'base': {'include':['word','location_word','dash','symbol','comma','location'],  'type':TokenType.WORD}},
            'LOCATION_BUILDER':  {'base': {'include':['location','location_word','symbol','comma'],  'type':TokenType.LOCATION}},
            'LOCATION_PHRASE_BUILDER':  {'base': {'include':['location','location_word','symbol','comma','word'],  'type':TokenType.LOCATION}},
            'INITIATOR_BUILDER': {'base': {'include':['initiator','word','location','conjunction','symbol'],  'type':TokenType.INITIATOR}},
            'CONJUNCTION':       {'base': {'include':['conjunction'],  'type':TokenType.CONJUNCTION}},
            'DATE_BUILDER':      {'base': {'include':['date','num','conjunction','word'], 'type':TokenType.DATE}},
            'CITATION':{
                'base':         {'include':[*Patterns.keys()],'type':TokenType.QUOTE},
                'trigger':      ['unquote'],
                'change_state':  'AFTER_UNQUOTE_CITATION'
            },
            'AFTER_UNQUOTE_CITATION': {'include':['symbol','comma','unquote','dash'],'type':TokenType.QUOTE}
        }


    def end(self, token:Token, state = None, data_type:Optional[TokenType] = None):

        result = self.building
        if data_type:
            result.type = data_type

        self.building = token

        if state == None:
            self.state = self.transitions['START'][token.type]
        else:
            self.state = state
        return result


    def write(self, params, token:Token):

        wspace = self.wspaces[token.type]

        if token.type.value in params['base']['include']:
            self.building = Token(type=params['base']['type'], value=self.building.value + wspace + token.value, start=self.building.start, end=token.end)

        elif token.type.value in params['transitional']:
            self.building = Token(type=token.type, value=self.building.value + wspace + token.value, start=self.building.start, end=token.end)
            self.state = self.transitions['START'][token.type]

        if token.type.value in ['comma','symbol','determiner']:
            return self.end(token, 'START')


    def build(self, token:Token):
    
        if self.state == 'START':
            if token.type in self.transitions['START']:
                self.building = Token(
                        token.type, 
                        token.value, 
                        token.start, 
                        token.end
                )
                self.state = self.transitions['START'][token.type]

        else:
            building_params = deepcopy(self.transitions[self.state])

            if token.type.value in building_params.get('trigger', []):
                self.state = building_params['change_state']
                building_params = deepcopy(self.transitions[self.state])

            if (
                token.type.value in building_params['base']['include'] 
                or token.type.value in building_params.get('transitional', [])
            ):
                result = self.write(token=token, params=building_params)
                if result:
                    return result
            else:
                return self.end(token)