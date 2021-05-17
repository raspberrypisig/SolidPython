import inspect
import keyword

from types import ModuleType

def indent(s: str) -> str:
    return s.replace("\n", "\n\t")

def calling_module(stack_depth: int = 2) -> ModuleType:
    """
    Returns the module *2* back in the frame stack.  That means:
    code in module A calls code in module B, which asks calling_module()
    for module A.

    This means that we have to know exactly how far back in the stack
    our desired module is; if code in module B calls another function in 
    module B, we have to increase the stack_depth argument to account for
    this.

    Got that?
    """
    frm = inspect.stack()[stack_depth]
    calling_mod = inspect.getmodule(frm[0])
    # If calling_mod is None, this is being called from an interactive session.
    # Return that module.  (Note that __main__ doesn't have a __file__ attr,
    # but that's caught elsewhere.)
    if not calling_mod:
        import __main__ as calling_mod  # type: ignore
    return calling_mod

def subbed_keyword(identifier: str) -> str:
    """
    Append an underscore to any python reserved word.
    Prepend an underscore to any OpenSCAD identifier starting with a digit.
    No-op for all other strings, e.g. 'or' => 'or_', 'other' => 'other'
    """
    new_identifier = identifier

    if identifier in keyword.kwlist:
        new_identifier = identifier + "_"

    if identifier[0].isdigit():
        new_identifier = "_" + identifier

    if new_identifier != identifier:
        print(f"\nFound OpenSCAD code that's not compatible with Python. \n"
              f"Imported OpenSCAD code using `{keyword}` \n"
              f"can be accessed with `{new_identifier}` in SolidPython\n")
    return new_identifier

def unsubbed_keyword(identifier: str) -> str:
    """
    Remove trailing underscore for already-subbed python reserved words.
    Remove prepending underscore if remaining identifier starts with a digit.
    No-op for all other strings: e.g. 'or_' => 'or', 'other_' => 'other_'
    """
    if identifier.endswith("_") and identifier[:-1] in keyword.kwlist:
        return identifier[:-1]

    if identifier.startswith("_") and identifier[1].isdigit():
        return identifier[1:]

    return identifier

