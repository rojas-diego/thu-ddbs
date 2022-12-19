from rich.prompt import Prompt

def prompt(text, choices):
    print(text)
    res = Prompt.ask(choices=choices)
    return res
