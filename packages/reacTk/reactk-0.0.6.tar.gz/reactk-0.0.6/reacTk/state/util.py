import tkinter as tk

from widget_state import BoolState, NumberState, StringState


def to_tk_var(state: BoolState | NumberState | StringState) -> tk.Variable:
    if isinstance(state, BoolState):
        variable = tk.BooleanVar(value=state.value)
    elif isinstance(state, NumberState):
        if isinstance(state.value, int):
            variable = tk.IntVar(value=state.value)
        else:
            variable = tk.DoubleVar(value=state.value)
    elif isinstance(state, StringState):
        variable = tk.StringVar(value=state.value)
    else:
        raise TypeError("Cannot map {styte.__class__.__name__} to a tk.Variable")

    state.on_change(lambda _: variable.set(state.value))
    variable.trace_add("write", lambda *_: state.set(variable.get()))

    return variable
