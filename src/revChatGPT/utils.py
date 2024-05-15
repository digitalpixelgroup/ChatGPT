import re
from typing import Set, List
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

bindings = KeyBindings()

def create_keybindings(key: str = "c-@") -> KeyBindings:
    """
    Create keybindings for prompt_toolkit. Default key is ctrl+space.
    For possible keybindings, see:
    https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/key_bindings.html#list-of-special-keys
    """
    @bindings.add(key)
    def _(event) -> None:
        event.app.exit(result=event.app.current_buffer.text)
    return bindings

def create_session() -> PromptSession:
    """
    Create a PromptSession with in-memory history.
    """
    return PromptSession(history=InMemoryHistory())

def create_completer(commands: List[str], pattern_str: str = "$") -> WordCompleter:
    """
    Create a WordCompleter with a custom pattern.
    """
    return WordCompleter(words=commands, pattern=re.compile(pattern_str))

def get_input(
    session: PromptSession = None,
    completer: WordCompleter = None,
    key_bindings: KeyBindings = None,
) -> str:
    """
    Multiline input function.
    """
    if session:
        return session.prompt(
            completer=completer,
            multiline=True,
            auto_suggest=AutoSuggestFromHistory(),
            key_bindings=key_bindings,
        )
    else:
        return prompt(multiline=True)

async def get_input_async(
    session: PromptSession = None,
    completer: WordCompleter = None,
) -> str:
    """
    Asynchronous multiline input function.
    """
    if session:
        return await session.prompt_async(
            completer=completer,
            multiline=True,
            auto_suggest=AutoSuggestFromHistory(),
        )
    else:
        return prompt(multiline=True)

def get_filtered_keys_from_object(obj: object, *keys: str) -> Set[str]:
    """
    Get filtered list of object variable names.
    :param keys: List of keys to include. If the first key is "not", the remaining keys will be removed from the class keys.
    :return: List of class keys.
    """
    class_keys = set(obj.__dict__.keys())
    if not keys:
        return class_keys

    if keys[0] == "not":
        return {key for key in class_keys if key not in keys[1:]}
    
    invalid_keys = set(keys) - class_keys
    if invalid_keys:
        raise ValueError(f"Invalid keys: {invalid_keys}")
    
    return {key for key in keys if key in class_keys}
