from typing import Dict, List

_MEMORY: Dict[str, List[dict]] = {}

def get_history(conversation_id: str) -> List[dict]:
    return _MEMORY.get(conversation_id, [])

def append_message(conversation_id: str, role: str, content: str) -> None:
    _MEMORY.setdefault(conversation_id, []).append({"role": role, "content": content})

def set_history(conversation_id: str, history: List[dict]) -> None:
    _MEMORY[conversation_id] = history

def clear(conversation_id: str) -> None:
    _MEMORY.pop(conversation_id, None)
