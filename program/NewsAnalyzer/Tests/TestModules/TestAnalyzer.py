from program.NewsAnalyzer.Proccessing import Tokenizer, TokenBuilder, TokenMerger, RelationBuilder, EventBuilder
from program.NewsAnalyzer.Tests.TestModules.DataLoad import TestDataDownloader, FunctionCaller
from program.NewsAnalyzer.Tests.TestModules.Checks import check_start, check_token, call_checker
from program.NewsAnalyzer.Analyze import AnalyzeText
from program.NewsAnalyzer.patterns import Patterns
from dataclasses import fields
import json, os, re

data_downloader = TestDataDownloader()


class AnalysisTester:

    def __init__(self):
        
        self.checklist = {
            'Tokenizer':{
                'tokenize':['VALUE'],
                'classify_tokens':['TYPE']},
            'TokenBuilder':{
                'build':['VALUE','TYPE']},
            'TokenMerger':{
                'merge_related_tokens':['VALUE','TYPE']},
            'RelationBuilder':{
                "identify_relevant_tokens":['TYPE'],
                "make_action":['TYPE','VALUE','SUBJECT','PREDICATE','OBJECT'],
                "make_relation":['TYPE','VALUE']},
            'EventBuilder':{
                'build_event':['TYPE']}}
        self.types = {
            'tokenize':'Token',
            'classify_tokens':'Token',
            'build':'Token',
            'merge_related_tokens':'Token',
            'identify_relevant_tokens':'Action_Candidate',
            'make_action':'Action',
            'make_relation':'Token',
            'build_event':'Event'
        }
        self.checker = {
            'tokenize':'check_token',
            'classify_tokens':'check_token',
            'build':'check_token',
            'merge_related_tokens':'check_token',
            'identify_relevant_tokens':'check_token',
            'make_action':'check_complex_token',
            'make_relation':'check_token',
            'build_event':'check_complex_token',
        }

    def test_pipeline(self, stop_after_mistake:bool = True):

        tests_data = data_downloader.get_test_data()

        for test in tests_data:

            print('_____________________________________________________________________')
            print(test.text)
            print('_____________________________________________________________________\n')
            function_caller = FunctionCaller()
            got_error = False

            for module, functions in self.checklist.items():
                for func in functions:

                    print(f'-------- [{str(func).capitalize()}] --------')

                    output_data = function_caller.call_module_func(func_name=func, text=test.text)
                    
                    for token in output_data:
                        
                            if call_checker(item=token, checker_name=self.checker[func], item_type=self.types[func], 
                                            attributes=self.checklist[module][func], benchmark=test.benchmark_data[module][func]):
                                got_error = True
                    if not got_error:
                        print(f'✅ {func} work done correctly\n')
                    else:
                        if stop_after_mistake:
                            print(f"Mistake(s) occured in {module}: {str(func).lower()}")
                            return