from dataclasses import dataclass, fields, field
from program.NewsAnalyzer.AnalyzerModels import Action, Relation
from program.NewsAnalyzer.Proccessing.Tokenizer import Token, TokenType
import copy
from typing import Optional

@dataclass
class ActionCandidate:

    token:Optional[Token] = field(default_factory=Token())
    hierarchy_score:Optional[int] = None

@dataclass
class RelationBuilder:

    hierarchy = {
        'word': 3,
        'initiator':5,
        'preposition':2,
        'num':4,
        'determiner':4,
        'location':0,
        'date':0,
        'verb':10
    }

    patterns = {
        TokenType.INITIATOR: [ ['word','verb'],   ['initiator','verb'],  ['preposition','verb'] ],
        TokenType.OBJECT:    [ ['verb','word'],   ['verb','num'], ['verb','preposition'], ['determiner','verb'] ]
        }

    actors = ['word','initiator','preposition','num','determiner','verb']

    def identify_relevant_tokens(self, token_list:list[Token]) -> list[ActionCandidate]:

        action_tokens = []

        for token in token_list:
            if token.type.value in self.actors:
                action_tokens.append(ActionCandidate(token=token, hierarchy_score=self.hierarchy[token.type.value]))
        return action_tokens

    def make_action(self, token_list:list[Token]) -> list[Action]:

        action_tokens = self.identify_relevant_tokens(token_list)
        action = Action()
        current_token_score = -1
        action_list = []
        i = 0

        for token in action_tokens:

            if not action.predicate:
                if token.token.type.value == 'verb':
                    current_token_score = -1
                    action.predicate = token.token
                elif not action.subject:
                    action.subject = token.token
                    current_token_score = token.hierarchy_score
                else:
                    if token.hierarchy_score > current_token_score:
                        current_token_score = token.hierarchy_score
                        action.subject = token.token
            else:
                if token.token.type.value == 'verb' or token.hierarchy_score == current_token_score:
                    action_list.append(action)
                    current_token_score = None
                    action = Action()
                else:
                    if not action.object:
                        current_token_score = token.hierarchy_score
                        action.object = token.token
                    elif token.hierarchy_score > current_token_score:
                        action.object = token.token
                    if token.token.value.endswith('.'):
                        action_list.append(action)
                        current_token_score = None
                        action = Action()
        return action_list
        
    def make_relation(self, token_list:list):

        action_list = self.make_action(token_list)

        relation_list = []

        for action in action_list:

            for token_type, pattern in self.patterns.items():

                if [action.subject.type.value, action.predicate.type.value] in pattern:
                    action.subject.type = token_type

                    if token_type == TokenType.INITIATOR:
                        action.object.type = TokenType.OBJECT
                    else:
                        action.object.type = TokenType.INITIATOR
                    relation_list.append(action)

        result = self.modify_token_list(token_list, action_list=action_list)

        return result

    def modify_token_list(self, token_list:list[Token], action_list:list[Action]):

        action_tokens = []

        for action in action_list:
            for field in fields(action):

                action_tokens.append(action.__getattribute__(field.name))
                token_list.remove(action.__getattribute__(field.name))

        for token in action_tokens:
            token_list.append(token)

        return sorted(token_list, key=lambda t:t.end)