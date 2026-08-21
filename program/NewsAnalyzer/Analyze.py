from program.NewsAnalyzer.Proccessing import Tokenizer, TokenBuilder, TokenMerger, RelationBuilder, EventBuilder
from program.NewsAnalyzer.patterns import Patterns
from program.NewsAnalyzer.AnalyzerModels import Event

def AnalyzeText(text:str) -> list[Event]:
    
    tokenizer = Tokenizer.TextTokenizer(patterns=Patterns)
    primary_tokens = tokenizer.tokenize(text.casefold())
    classifieed_tokens = tokenizer.classify_tokens(primary_tokens)

    builder = TokenBuilder.TokenBuilder()
    builded_list = []

    for token in classifieed_tokens:
        builded_token = builder.build(token)
        if builded_token:
            builded_list.append(builded_token)


    merger = TokenMerger.TokenMerger()
    merged_list = merger.merge_related_tokens(builded_list)

    relation_builder = RelationBuilder.RelationBuilder()
    actions = relation_builder.make_relation(merged_list)

    event_builder = EventBuilder.EventBuilder()
    events = event_builder.build_event(actions)

    return events