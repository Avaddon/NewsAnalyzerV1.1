from program.NewsAnalyzer.Proccessing import Tokenizer, TokenBuilder, TokenMerger, RelationBuilder, EventBuilder
from program.NewsAnalyzer.patterns import Patterns
from dataclasses import dataclass, field
from typing import Optional, Literal
import json, os


@dataclass
class FilesPair:
    text_filename:str
    benchmark_filename:str

@dataclass
class DataPair:

    text:str
    benchmark_data:dict


@dataclass
class PipelineBenchmark:

    tokenizer_benchmark:list
    classifier_benchmark:list
    builder_benchmark:list
    merger_benchmark:list


class TestDataDownloader:

    def group_text_benchmark_filenames(self, directory:str) -> list[FilesPair]:
        t_b_pairs = []

        for entry in os.scandir(path=directory):
            if entry.name.endswith('.txt'):
                t_b_pairs.append(FilesPair(text_filename=entry.name, benchmark_filename=entry.name.replace('.txt', '.json')))
        return t_b_pairs


    def get_test_data(self, directory:str = 'F:/parsing/program/NewsAnalyzer/Tests/TestTexts') -> list[DataPair]:
        text_benchmark_pairs = self.group_text_benchmark_filenames(directory)

        tests_data = []

        for t_b_pair in text_benchmark_pairs:
            with open(f'F:/parsing/program/NewsAnalyzer/Tests/TestTexts/{t_b_pair.text_filename}', 'r', encoding='utf-8') as f:
                text = f.readline()
            with open(f'F:/parsing/program/NewsAnalyzer/Tests/TestTexts/{t_b_pair.benchmark_filename}', 'r', encoding='utf-8') as f:
                benchmark_data = json.load(f)

            tests_data.append(DataPair(text=text, benchmark_data=benchmark_data))
        return tests_data



class FunctionCaller:

    def __init__(self):
        
        self.tokenizer = Tokenizer.TextTokenizer(patterns=Patterns)
        self.token_builder = TokenBuilder.TokenBuilder()
        self.token_merger = TokenMerger.TokenMerger()
        self.relation = RelationBuilder.RelationBuilder()
        self.event_builder = EventBuilder.EventBuilder()

        self.primary_tokens = list()
        self.clsssified_tokens = list()
        self.builded_tokens = list()
        self.merged_tokens = list()
        self.relation_relevant = list()
        self.actions = list()
        self.relations = list()
        self.events = list()

    def call_module_func(self, text:str, func_name:Literal['tokenize','classify_tokens','build','merge_related_tokens',
                                    'identify_relevant_tokens','make_action','make_relation','build_event']):

        if func_name == 'tokenize':
            primary_tokens = self.tokenizer.tokenize(text)
            return primary_tokens
        
        elif func_name == 'classify_tokens':
            if not self.primary_tokens:
                    self.primary_tokens = self.tokenizer.tokenize(text)
            self.classified_tokens = self.tokenizer.classify_tokens(self.primary_tokens)
            return self.classified_tokens
        
        elif func_name == 'build':
            if not self.classified_tokens:
                    self.classified_tokens = self.call_module_func('classify_tokens', text)
            for token in self.classified_tokens:
                result = self.token_builder.build(token=token)
                if result:
                    self.builded_tokens.append(result)
            return self.builded_tokens
        elif func_name == 'merge_related_tokens':
            if not self.builded_tokens:
                    self.builded_tokens = self.call_module_func('build', text)
            self.merged_tokens = self.token_merger.merge_related_tokens(self.builded_tokens)
            return self.merged_tokens
        elif func_name == 'identify_relevant_tokens':
            if not self.merged_tokens:
                    self.merged_tokens = self.call_module_func('merge_related_tokens', text)
            self.relation_relevant = self.relation.identify_relevant_tokens(self.merged_tokens)
            return self.relation_relevant
        elif func_name == 'make_action':
            if not self.relation_relevant:
                    self.relation_relevant = self.call_module_func('identify_relevant_tokens', text)
            self.actions = self.relation.make_action(self.relation_relevant)
            return self.actions
        elif func_name == 'make_relation':
            if not self.actions:
                 self.actions = self.call_module_func('make_action', text)
            self.relations = self.relation.make_relation(self.actions, self.merged_tokens)
            return self.relations
        elif func_name == 'build_event':
            if not self.relations:
                    self.relations = self.call_module_func('make_relation', text)
            self.events = self.event_builder.build_event(self.relations)
            return self.events