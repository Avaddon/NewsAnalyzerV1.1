from dataclasses import dataclass
from program.NewsAnalyzer.AnalyzerModels import Primary_Token, Token
from copy import deepcopy


@dataclass
class TokenMerger:

    def __init__(self):
        self.patterns = self.create_patterns()

    def create_patterns(self):
        return {       
           'word':['word','preposition','conjunction','num'],
           'verb':['verb'],
           'num':['num','NUM_PHRASE'],
           'preposition':['preposition','conjunction'],
           'location':['location','conjunction','word'],   
           'determiner':[],  'quote':[],'unquote':[],
           'date':['date'],  'conjunction':[],   'dash':[], 'region_word':[],
           'comma':[],   'initiator':[]}

    def merge_related_tokens(self, token_list:list[Token]) -> list[Token]:

        i = 0

        result = []

        while i < len(token_list):

            current_token = deepcopy(token_list[i])

            j = i+1

            while j < len(token_list) and token_list[j].type.value in self.patterns.get(current_token.type.value, []):
                current_token.value += ' ' + token_list[j].value
                current_token.end = token_list[j].end

                j+=1

                if token_list[j-1].value.endswith('.'):
                    break

            result.append(current_token)

            i = j

        return result