from .helpers import unescape_openscad_identifier, indent

def scad_call_code(name, params):
    """
        for a given function name and dict of params it returns:
            {name}(p1=v1, p2=v2,...)
            -> translate(v = [1, 2, 3])
    """
    s = unescape_openscad_identifier(name) + "("

    parameter_count = 0
    for p in sorted(params.keys()):
        v = params[p]
        if v is None:
            continue

        parameter_count += 1

        vv = py2openscad(v)
        up = unescape_openscad_identifier(p)
        s += f'{up} = {vv}, '

    #remove trailing ,
    if parameter_count:
        s = s[:-2]

    s += ")"

    return s

def scad_code(name, params, children):
    """
        returns the scad code for a given node tuple consiting of name, params
        and children list.

        translate(v = [1, 2, 3]) (children[0] children[1]...)\n
    """
    s = scad_call_code(name, params)

    if not children:
        return s + ";\n"

    s += " {\n"

    for child in children:
        s += indent(child._render())

    return s + "};\n"

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

