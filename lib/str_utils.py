import six
from six import text_type, binary_type
from typing import Union

def force_text(s, encoding='utf-8'):
    # type: (Union[text_type, binary_type], str) -> text_type
    """converts a string to a text string"""
    if isinstance(s, text_type):
        return s
    elif isinstance(s, binary_type):
        return s.decode(encoding)
    else:
        raise ValueError("force_text expects a string type")

def force_bytes(s, encoding='utf-8'):
    # type: (Union[text_type, binary_type], str) -> binary_type
    """converts a string to binary string"""
    if isinstance(s, binary_type):
        return s
    elif isinstance(s, text_type):
        return s.encode(encoding)
    else:
        raise ValueError("force_bytes expects a string type")

def force_str(s, encoding='utf-8'):
    # type: (Union[text_type, binary_type], str) -> str
    """converts a string to a native string"""
    if isinstance(s, str):
        return s
    elif isinstance(s, text_type):
        return s.encode(encoding)
    elif isinstance(s, binary_type):
        return s.decode(encoding)
    else:
        raise ValueError("force_str expects a string type")
