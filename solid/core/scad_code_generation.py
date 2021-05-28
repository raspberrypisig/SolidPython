from .helpers import unescape_openscad_identifier, indent

def generate_scad_node_head(name, params):
    """
        for a given function name and dict of params it returns:
            {name}(p1=v1, p2=v2,...)
            -> translate(v = [1, 2, 3])
    """
    param_strings = []
    for p in sorted(params.keys()):
        scad_value = py2openscad(params[p])
        scad_identifier = unescape_openscad_identifier(p)

        param_strings.append(f'{scad_identifier} = {scad_value}')

    scad_identifier = unescape_openscad_identifier(name)
    param_str = ", ".join(param_strings)

    return f'{scad_identifier}({param_str})'

def generate_scad_node(name, params, children):
    """
        returns the scad code for a given node tuple consiting of name, params
        and children list.

        -> translate(v = [1, 2, 3]) {children[0]; children[1]; ...};\n
    """
    s = generate_scad_node_head(name, params)

    if children:
        s += " {\n"
        for child in children:
            s += indent(child._render())
        s += "}"

    return s + ";\n"

def py2openscad(o):
    if type(o) == bool:
        return str(o).lower()
    if type(o) == float:
        return f"{o:.10f}"  # type: ignore
    if type(o) == str:
        return f'\"{o}\"'  # type: ignore
    if type(o).__name__ == "ndarray":
        import numpy  # type: ignore
        return numpy.array2string(o, separator=",", threshold=1000000000)
    if hasattr(o, "__iter__"):
        s = "["
        first = True
        for i in o:  # type: ignore
            if not first:
                s += ", "
            first = False
            s += py2openscad(i)
        s += "]"
        return s
    return str(o)

