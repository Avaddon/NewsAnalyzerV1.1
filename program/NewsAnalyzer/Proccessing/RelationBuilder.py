from dataclasses import dataclass, fields
from program.NewsAnalyzer.AnalyzerModels import Action, Relation
from program.NewsAnalyzer.Proccessing.Tokenizer import Token, TokenType


@dataclass
class RelationBuilder:

    patterns = {
        TokenType.INITIATOR: [ ['word','verb'],   ['initiator','verb'],  ['preposition','verb'] ],
        TokenType.OBJECT:    [ ['verb','word'],   ['verb','num'], ['verb','preposition'], ['determiner','verb'] ]
        }

    actors = ['word','initiator','preposition','num','determiner']

    def make_action(self, token_list:list) -> list[Action]:

        i = 0

        action = Action()

        action_list = []

        while i < len(token_list):

            j = i+1

            if token_list[i].type.value in self.actors and not token_list[i].value.endswith('.'):
                
                action.before_verb = token_list[i]

                while j < len(token_list):

                    if token_list[j].type.value == 'verb':
                        action.verb = token_list[j]
                        
                    elif token_list[j].type.value in self.actors:
                        action.after_verb = token_list[j]
                    j+=1

                    if all(action.__getattribute__(field.name) for field in fields(action)):
                        action_list.append(action)
                        action = Action()
                        break
            i = j

        return action_list
        
    def make_relation(self, token_list:list):

        action_list = self.make_action(token_list)

        relation_list = []

        for action in action_list:

            for token_type, pattern in self.patterns.items():

                if [action.before_verb.type.value, action.verb.type.value] in pattern:
                    action.before_verb.type = token_type

                    if token_type == TokenType.INITIATOR:
                        action.after_verb.type = TokenType.OBJECT
                    else:
                        action.after_verb.type = TokenType.INITIATOR
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