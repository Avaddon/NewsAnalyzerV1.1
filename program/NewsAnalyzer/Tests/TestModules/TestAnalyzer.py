from program.NewsAnalyzer.Analyze import AnalyzeText
from dataclasses import fields
import json
import os

def get_test_data_from_files(directory:str = 'F:/parsing/program/NewsAnalyzer/Tests/TestTexts') -> tuple[list[str], list[dict]]:
    
    texts = []
    correct_events = []

    for entry in os.scandir(directory):
        if entry.is_file():

            with open(f'F:/parsing/program/NewsAnalyzer/Tests/TestTexts/{entry.name}', 'r', encoding='utf-8') as f:

                if entry.name.endswith('.txt'):
                    texts.append(f.readline())

                elif entry.name.endswith('.json'):
                    correct_events.append(json.load(f))
    return texts, correct_events

class AnalysisTester:

    def evaluate_analyzer_output(self):

        texts, correct_events_data = get_test_data_from_files()

        i = 0
        while i < len(texts):

            events = AnalyzeText(texts[i])

            for event in events:
                for field in fields(event):
                    attribute = event.__getattribute__(field.name)
                    if attribute is not None:
                        print(attribute.type, attribute.value)
                print('\n')

                for column, value in correct_events_data[i].items():
                    print('correct', column, value)
                print('\n --------------------------------------------- \n')
            i+=1
