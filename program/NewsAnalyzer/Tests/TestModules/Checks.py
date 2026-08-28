from typing import Literal
import re


def call_checker(checker_name:Literal['check_token','check_complex_token'], 
                 item_type:Literal['Token','Action_Candidate','Action','Event'], 
                 attributes:list[Literal['VALUE','TYPE','SUBJECT','PREDICATE','OBJECT']], 
                 benchmark:list[str], item) -> bool:

    if checker_name == 'check_token':

        if check_start(item=item, item_type=item_type, benchmark=benchmark):
            return True
        return check_token(item=item, item_type=item_type, benchmark=benchmark, attributes=attributes)
    elif checker_name == 'check_complex_token':
        return check_complex_token(item=item, item_type=item_type, benchmark=benchmark)

def print_error_message(errors:list[str]):
    error_message = 'Incorrect'
    for error in errors:
        error_message += ' ' + error
    print(error_message,'\n')


def format_attrs(item, item_type:Literal['Token','Action_Candidate','Action','Event']):

    try:
        if item_type == 'Token':
            return [{
            'START':f"start={item.start},",
            'VALUE':f"'{item.value}',",
            'TYPE':f"{item.type}:"
            }]
        elif item_type == 'Action_Candidate':
            return [{
            'START':f"start={item.token.start},",
            'VALUE':f"'{item.token.value}',",
            'TYPE':f"{item.token.type}:"
            }]
    except AttributeError:
        print(f"Output: {item}")
        return
    
def check_start(item, item_type:Literal['Token','Action_Candidate','Action','Event'],
                 benchmark:list[str]) -> bool:
    object_config = format_attrs(item=item, item_type=item_type)
    if not object_config:
        return True

    for object_part_attrs in object_config:
        if not any(re.search(object_part_attrs['START'], b_token) for b_token in benchmark):
            print('check_start:')
            print(f'Output:     {item}')
            print(f'Benchmark:  {None}\n')
            return True
    return False


def check_token(item, item_type:Literal['Token','Action_Candidate','Action','Event'],
                benchmark:list[str], attributes:list[Literal['VALUE','TYPE','SUBJECT','PREDICATE','OBJECT']]) -> bool:
    object_config = format_attrs(item=item, item_type=item_type)
    if not object_config:
        return True

    for b_token in benchmark:
        mistake_types = []

        for object_part_attrs in object_config:
            for attribute in attributes:

                if re.search(object_part_attrs['START'], b_token):
                    if str(object_part_attrs[attribute]) not in b_token:
                        mistake_types.append(attribute)
            if mistake_types:
                print(f'Output:     {item}')
                print(f'Benchmark:  {b_token}')
                print_error_message(mistake_types)
                return True
    return False


def check_complex_token(item, item_type:Literal['Action','Event'], benchmark:list[str]) -> bool:

    mistake_types = []

    object_config = {
        'Action':{
            'subject':['value'],
            'predicate':['value'],
            'object':['value']
        },
        'Event':{
            'initiator':['value','type'],
            'verb':['value','type'],
            'object':['value','type'],
            'location':['value','type'],
            'time':['value','type'],
            'source':['value','type']
        }
    }
    for b_token in benchmark:
        for attribute in object_config[item_type]:

            if getattr(item, attribute) is None:
                if not f"{str(attribute)}=None" in b_token:
                    #print(f'Missing Token in {item_type}:{str(attribute)}')
                    pass
            else:
                if str(f"start={getattr(getattr(item, attribute), 'start')}") in b_token:
                    if str(f"{attribute}={getattr(item, attribute)}") not in b_token:
                        mistake_types.append(attribute)
        if mistake_types:
            print(f'Output:     {item}')
            print(f'Benchmark:  {b_token}')
            print_error_message(mistake_types)
            return True
    return False
