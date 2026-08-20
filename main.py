# from program.parser.to_csv import save_csv, save_excel
# from gsu_parser import get_gsu_news_data
# from kommersant_parser import get_kommersant_news_data
# from database import save_articles, select_articles
# from program.analysis.find_region import store_analyzed_text
# from models_copy import Token
from program.NewsAnalyzer.Proccessing import Tokenizer, TokenBuilder, TokenMerger, RelationBuilder, EventBuilder
from program.NewsAnalyzer.patterns import Patterns


def test(dataset:list):
    for item in dataset:
        print(item)

test_text ='Средства ПВО России с 20:00 до 8:00 мск уничтожили 822 беспилотника ВСУ над 17 российскими регионами, а также акваториями Азовского и Черного морей. Об этом заявили в пресс-службе Минобороны России.'
test_text += ' ^'

tokenizer = Tokenizer.TextTokenizer(patterns=Patterns)
primary_tokens = tokenizer.tokenize(test_text.casefold())
classifieed_tokens = tokenizer.classify_tokens(primary_tokens)
#test(classifieed_tokens)

builder = TokenBuilder.TokenBuilder()
builded_list = []
for token in classifieed_tokens:
    builded_token = builder.build(token)
    if builded_token:
        builded_list.append(builded_token)
#test(builded_list)

merger = TokenMerger.TokenMerger()
merged_list = merger.merge_related_tokens(builded_list)
#test(merged_list)

relation_builder = RelationBuilder.RelationBuilder()
actions = relation_builder.make_relation(merged_list)
test(actions)

event_builder = EventBuilder.EventBuilder()
events = event_builder.build_event(actions)

for event in events:
    print(event)

#gsu_article = get_gsu_news_data()
# komm_article =get_kommersant_news_data()

# for item in komm_article:
#     print(item,'\n')

# save_articles(gsu_article)
#save_articles(komm_article)
#select_articles(params='id, title')
