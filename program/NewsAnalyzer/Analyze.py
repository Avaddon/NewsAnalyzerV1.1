from program.NewsAnalyzer.Proccessing import Tokenizer, TokenBuilder, TokenMerger, RelationBuilder, EventBuilder
from program.NewsAnalyzer.patterns import Patterns
from program.NewsAnalyzer.AnalyzerModels import Event

def AnalyzeText(text:str) -> list[Event]:
    
    tokenizer = Tokenizer.TextTokenizer(patterns=Patterns)
    primary_tokens = tokenizer.tokenize(text.casefold())
    
    classified_tokens = tokenizer.classify_tokens(primary_tokens)
    
    builder = TokenBuilder.TokenBuilder()
    builded_list = []

    for token in classified_tokens:
        builded_token = builder.build(token)
        if builded_token:
            builded_list.append(builded_token)

    merger = TokenMerger.TokenMerger()
    merged_list = merger.merge_related_tokens(builded_list)
    

    relation_builder = RelationBuilder.RelationBuilder()
    relation_relevant = relation_builder.identify_relevant_tokens(merged_list)
    
    actions = relation_builder.make_action(relation_relevant)
    relations = relation_builder.make_relation(actions, merged_list)


    event_builder = EventBuilder.EventBuilder()
    events = event_builder.build_event(relations)
    for token in relations:
                                print(token)
    return events
