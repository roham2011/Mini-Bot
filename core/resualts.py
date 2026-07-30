from dataclasses import dataclass

@dataclass(slots=True)
class step_resualts():
    message : str
    next_state : str
    finished : bool = True 