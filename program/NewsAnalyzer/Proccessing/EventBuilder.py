from program.NewsAnalyzer.AnalyzerModels import Relation, Action, Event
from program.NewsAnalyzer.Proccessing.Tokenizer import Token
from dataclasses import dataclass, fields, field


@dataclass
class EventBuilder:

    def build_event(self, token_list:list):

        event = Event()
        event_fields = {field for field in fields(event)}

        data = []

        event_list = []
        event_sentences = []

        for token in token_list:
            for field in event_fields:
                
                if token.type.value == field.name:

                    if event.__getattribute__(field.name) is None:
                        event.__setattr__(field.name, token)

                    else:
                        if token.type.value in ['verb','initiator','object']:

                            event_list.append(event)

                            event = Event()
                            event.__setattr__(field.name, token)

                        else:
                            data.append(token)
                    break

        if any(event.__getattribute__(field.name) for field in fields(event)):
            event_list.append(event)

        for event in event_list:
            sentence = event.build_sentence()
            event_sentences.append(sentence)

        return event_sentences