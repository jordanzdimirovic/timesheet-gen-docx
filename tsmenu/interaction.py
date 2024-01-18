from copy import deepcopy
from typing import Iterable

# Padded print
def pprint(value: object):
    print(value)
    print()


def hprint(line: str):
    print("=" * (len(line) + 4))
    print(f"| {line.title()} |")
    print("=" * (len(line) + 4))
    

def generic_get(prompt: str, default: object = None, typecast: callable = None, do_strip: bool = False) -> object:
    value = input(f"{prompt} >>> ")
    if do_strip: value = value.strip()
    if not value:
        if not default:
            pprint("Invalid input (empty with no default). Try again...")
            return generic_get(prompt, default, typecast, do_strip)
            
        # Nothing provided - use default
        value = deepcopy(default)
    
    return typecast(value) if typecast else value



def generic_select(prompt: str, options: Iterable[tuple[object, str]], transform: callable = lambda v: v.upper()):
    option_type = type(options[0][0])
    assert all(type(option[0]) is option_type for option in options), "Options must all be of the same type"
    
    pprint(prompt)
    pprint("[Select from the following options:]")
    
    for option in options:
        pprint(f"[{option[0]}] | {option[1]}")
        
    try:
        result = option_type(transform(input("[SELECT] >>> ")))
        if not any(result == option[0] for option in options):
            pprint("Invalid response (not in given list). Try again...")
            return generic_select(prompt, options, transform)
        
        return result
        
    except ValueError:
        pprint("Invalid response (wrong type). Try again...")
        return generic_select(prompt, options, transform)
    
    