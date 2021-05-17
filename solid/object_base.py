import tempfile
import sys
import os
import subprocess
import keyword

from typing import Dict, Optional, List, Union, Sequence, Iterable

from solid.helpers import unsubbed_keyword, indent

# These are features added to SolidPython but NOT in OpenSCAD.
# Mark them for special treatment

non_rendered_classes = ['hole', 'part']

class OpenSCADObject:

    def __init__(self, name: str, params: dict):
        self.name = name
        self.params = params
        self.children: List["OpenSCADObject"] = []
        self.modifier = ""
        self.parent: Optional["OpenSCADObject"] = None
        self.is_hole = False
        self.has_hole_children = False
        self.is_part_root = False
        self.traits: Dict[str, Dict[str, float]] = {}

    def add_trait(self, trait_name:str, trait_data:Dict[str, float]):
        self.traits[trait_name] = trait_data

    def get_trait(self, trait_name:str) -> Optional[Dict[str, float]]:
        return self.traits.get(trait_name)

    def set_hole(self, is_hole: bool = True) -> "OpenSCADObject":
        self.is_hole = is_hole
        return self

    def set_part_root(self, is_root: bool = True) -> "OpenSCADObject":
        self.is_part_root = is_root
        return self

    def find_hole_children(self, path: List["OpenSCADObject"] = None) -> List["OpenSCADObject"]:
        """
        Because we don't force a copy every time we re-use a node
        (e.g a = cylinder(2, 6);  b = right(10) (a)
         the identical 'a' object appears in the tree twice),
        we can't count on an object's 'parent' field to trace its
        path to the root.  Instead, keep track explicitly
        """
        path = path if path else [self]
        hole_kids = []

        for child in self.children:
            path.append(child)
            if child.is_hole:
                hole_kids.append(child)
                # Mark all parents as having a hole child
                for p in path:
                    p.has_hole_children = True
            # Don't append holes from separate parts below us
            elif child.is_part_root:
                continue
            # Otherwise, look below us for children
            else:
                hole_kids += child.find_hole_children(path)
            path.pop()

        return hole_kids

    def set_modifier(self, m: str) -> "OpenSCADObject":
        """
        Used to add one of the 4 single-character modifiers:
        #(debug) !(root) %(background) or *(disable)
        """
        string_vals = {'disable': '*',
                       'debug': '#',
                       'background': '%',
                       'root': '!',
                       '*': '*',
                       '#': '#',
                       '%': '%',
                       '!': '!'}

        self.modifier = string_vals.get(m.lower(), '')
        return self

    def _render(self, render_holes: bool = False) -> str:
        """
        NOTE: In general, you won't want to call this method. For most purposes,
        you really want scad_render(), 
        Calling obj._render won't include necessary 'use' or 'include' statements
        """
        # First, render all children
        s = ""
        for child in self.children:
            # Don't immediately render hole children.
            # Add them to the parent's hole list,
            # And render after everything else
            if not render_holes and child.is_hole:
                continue
            s += child._render(render_holes)

        # Then render self and prepend/wrap it around the children
        # I've added designated parts and explicit holes to SolidPython.
        # OpenSCAD has neither, so don't render anything from these objects
        if self.name in non_rendered_classes:
            pass
        elif not self.children:
            s = self._render_str_no_children() + ";"
        else:
            s = self._render_str_no_children() + " {" + indent(s) + "\n}"

        # If this is the root object or the top of a separate part,
        # find all holes and subtract them after all positive geometry
        # is rendered
        if (not self.parent) or self.is_part_root:
            hole_children = self.find_hole_children()

            if len(hole_children) > 0:
                s += "\n/* Holes Below*/"
                s += self._render_hole_children()

                # wrap everything in the difference
                s = "\ndifference(){" + indent(s) + " /* End Holes */ \n}"
        return s

    def _render_str_no_children(self) -> str:
        callable_name = unsubbed_keyword(self.name)
        s = "\n" + self.modifier + callable_name + "("
        first = True

        # Re: https://github.com/SolidCode/SolidPython/issues/99
        # OpenSCAD will accept Python reserved words as callables or argument names,
        # but they won't compile in Python. Those have already been substituted
        # out (e.g 'or' => 'or_'). Sub them back here.
        self.params = {unsubbed_keyword(k): v for k, v in self.params.items()}

        # OpenSCAD doesn't have a 'segments' argument, but it does
        # have '$fn'.  Swap one for the other
        if 'segments' in self.params:
            self.params['$fn'] = self.params.pop('segments')

        valid_keys = self.params.keys()

        # intkeys are the positional parameters
        intkeys = list(filter(lambda x: type(x) == int, valid_keys))
        intkeys.sort()

        # named parameters
        nonintkeys = list(filter(lambda x: not type(x) == int, valid_keys))
        all_params_sorted = intkeys + nonintkeys
        if all_params_sorted:
            all_params_sorted = sorted(all_params_sorted)

        for k in all_params_sorted:
            v = self.params[k]
            if v is None:
                continue

            if not first:
                s += ", "
            first = False

            if type(k) == int:
                s += py2openscad(v)
            else:
                s += k + " = " + py2openscad(v)

        s += ")"
        return s

    def _render_hole_children(self) -> str:
        # Run down the tree, rendering only those nodes
        # that are holes or have holes beneath them
        if not self.has_hole_children:
            return ""
        s = ""
        for child in self.children:
            if child.is_hole:
                s += child._render(render_holes=True)
            elif child.has_hole_children:
                s += child._render_hole_children()
        if self.name in non_rendered_classes:
            pass
        else:
            s = self._render_str_no_children() + "{" + indent(s) + "\n}"

        # Holes exist in the compiled tree in two pieces:
        # The shapes of the holes themselves, (an object for which
        # obj.is_hole is True, and all its children) and the
        # transforms necessary to put that hole in place, which
        # are inherited from non-hole geometry.

        # Non-hole Intersections & differences can change (shrink)
        # the size of holes, and that shouldn't happen: an
        # intersection/difference with an empty space should be the
        # entirety of the empty space.
        #  In fact, the intersection of two empty spaces should be
        # everything contained in both of them:  their union.
        # So... replace all super-hole intersection/diff transforms
        # with union in the hole segment of the compiled tree.
        # And if you figure out a better way to explain this,
        # please, please do... because I think this works, but I
        # also think my rationale is shaky and imprecise. 
        # -ETJ 19 Feb 2013
        s = s.replace("intersection", "union")
        s = s.replace("difference", "union")

        return s

    def add(self, child: Union["OpenSCADObject", Sequence["OpenSCADObject"]]) -> "OpenSCADObject":
        """
        if child is a single object, assume it's an OpenSCADObjects and 
        add it to self.children

        if child is a list, assume its members are all OpenSCADObjects and
        add them all to self.children
        """
        if isinstance(child, (list, tuple)):
            # __call__ passes us a list inside a tuple, but we only care
            # about the list, so skip single-member tuples containing lists
            if len(child) == 1 and isinstance(child[0], (list, tuple)):
                child = child[0]
            [self.add(c) for c in child]
        elif isinstance(child, int):
            # Allowing for creating object by adding to 0 (as in sum())
            if child != 0:
                raise ValueError
        else:
            self.children.append(child)  # type: ignore
            child.set_parent(self)  # type: ignore
        return self

    def set_parent(self, parent: "OpenSCADObject"):
        self.parent = parent

    def add_param(self, k: str, v: float) -> "OpenSCADObject":
        if k == '$fn':
            k = 'segments'
        self.params[k] = v
        return self

    def copy(self) -> "OpenSCADObject":
        """
        Provides a copy of this object and all children,
        but doesn't copy self.parent, meaning the new object belongs
        to a different tree
        Initialize an instance of this class with the same params
        that created self, the object being copied.
        """

        # Python can't handle an '$fn' argument, while openSCAD only wants
        # '$fn'.  Swap back and forth as needed; the final renderer will
        # sort this out.
        if '$fn' in self.params:
            self.params['segments'] = self.params.pop('$fn')

        other = type(self)(**self.params)
        other.set_modifier(self.modifier)
        other.set_hole(self.is_hole)
        other.set_part_root(self.is_part_root)
        other.has_hole_children = self.has_hole_children
        for c in self.children:
            other.add(c.copy())
        return other

    def __call__(self, *args: "OpenSCADObject") -> "OpenSCADObject":
        """
        Adds all objects in args to self.  This enables OpenSCAD-like syntax,
        e.g.:
        union()(
            cube(),
            sphere()
        )
        """
        return self.add(args)

    def __add__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a+b identical to:
        u = union()(a, b )
        """
        import solid.builtins
        return solid.builtins.union()(self, x)

    def __radd__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a+b identical to:
        u = union()(a, b )
        """
        import solid.builtins
        return solid.builtins.union()(self, x)

    def __sub__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a - b identical to:
        u = difference()(a, b )
        """
        import solid.builtins
        return builtins.difference()(self, x)

    def __mul__(self, x: "OpenSCADObject") -> "OpenSCADObject":
        """
        This makes u = a * b identical to:
        u = intersection()(a, b )
        """
        import solid.builtins
        return builtins.intersection()(self, x)

    # Mapping of transformations into cascade operations
    def union(self, x):
        '''
        Creates a union of the current object and the provided one
        '''
        return objects.union()(self, x)

    def intersection(self, x):
        '''
        Creates the intersection of the current object and the provided one
        '''
        return objects.intersection()(self, x)

    def difference(self, x):
        '''
        Creates the difference of the current object with the provided one
        '''
        return objects.difference()(self, x)

    def translate(self, v=None):
        '''
        Translates (moves) the current object by the specified vector

        :param v: X, Y and Z translation
        :type v: 3 value sequence
        '''
        return objects.translate(v)(self)

    def scale(self, v=None):
        '''
        Scales this object using the specified vector.

        :param v: X, Y and Z translation
        :type v: 3 value sequence        '''
        return objects.scale(v)(self)

    def rotate(self, a=None, v=None):
        '''
        Rotates the object 'a' degrees about the origin of the coordinate system
        or around an arbitrary axis.

        :param a: degrees of rotation, or sequence for degrees of rotation in each of the X, Y and Z axis.
        :type a: number or 3 value sequence

        :param v: sequence specifying 0 or 1 to indicate which axis to rotate by 'a' degrees. Ignored if 'a' is a sequence.
        :type v: 3 value sequence
        '''

        return objects.rotate(a, v)(self)

    def mirror(self, v):
        '''
        Mirrors the object on a plane through the origin.

        :param v: the normal vector of a plane intersecting the origin through which to mirror the object.
        :type v: 3 number sequence

        '''
        return objects.mirror(v)(self)

    def resize(self, newsize):
        '''
        Modify the size of the object to match the given new size.

        :param newsize: X, Y and Z values
        :type newsize: 3 value sequence
        '''
        return objects.resize(newsize)(self)

    def multmatrix(self, m):
        '''
        Multiplies the geometry of the object with the given 4x4
        transformation matrix.

        :param m: transformation matrix
        :type m: sequence of 4 sequences, each containing 4 numbers.
        '''
        return objects.multmatrix(m)(self)

    def color(self, c, alpha):
        '''
        Displays the object using the specified RGB color + alpha value.
        This is only used for the F5 preview as CGAL and STL (F6) do not
        currently support color. The alpha value will default to 1.0 (opaque) if
        not specified.

        :param c: RGB color + alpha value.
        :type c: sequence of 3 or 4 numbers between 0 and 1
        '''
        return objects.color(c, alpha)(self)

    def minkowski(self, x):
        '''
        Renders the `minkowski
        sum <http://www.cgal.org/Manual/latest/doc_html/cgal_manual/Minkowski_sum_3/Chapter_main.html>`__
        of the object.
        '''
        return objects.minkowski()(self, x)

    def offset(self, r=None, delta=None, chamfer=False):
        '''

        :param r: Amount to offset the polygon (rounded corners). When negative,
            the polygon is offset inwards. The parameter r specifies the radius
            that is used to generate rounded corners, using delta gives straight edges.
        :type r: number

        :param delta: Amount to offset the polygon (sharp corners). When negative,
            the polygon is offset inwards. The parameter r specifies the radius
            that is used to generate rounded corners, using delta gives straight edges.
        :type delta: number

        :param chamfer: When using the delta parameter, this flag defines if edges
            should be chamfered (cut off with a straight line) or not (extended to
            their intersection).
        :type chamfer: bool
        '''
        return objects.offset(r, delta, chamfer)(self)

    def hull(self, x):
        '''
        Renders the `convex
        hull <http://www.cgal.org/Manual/latest/doc_html/cgal_manual/Convex_hull_2/Chapter_main.html>`__
        of the object with a given one.
        '''
        return objects.hull()(self, x)

    def down(self, x):
        return objects.translate((0, 0, -x))(self)
    def up(self, x):
        return objects.translate((0, 0, x))(self)
    def left(self, x):
        return objects.translate((-x, 0, 0))(self)
    def right(self, x):
        return objects.translate((x, 0, 0))(self)
    def back(self, x):
        return objects.translate((0, x, 0))(self)
    def forward(self, x):
        return objects.translate((0, -x, 0))(self)

    def render(self, convexity=None):
        '''
        Always calculate the CSG model for this object (even in OpenCSG preview
        mode).

        :param convexity: The convexity parameter specifies the maximum number of front sides (back sides) a ray intersecting the object might penetrate. This parameter is only needed for correctly displaying the object in OpenCSG preview mode and has no effect on the polyhedron rendering.
        :type convexity: int
        '''
        return objects.render(convexity)(self)

    def linear_extrude(self, height=None, center=None, convexity=None, twist=None,
                       slices=None, scale=None):
        '''
        Linear Extrusion is a modeling operation that takes a 2D polygon as
        input and extends it in the third dimension. This way a 3D shape is
        created.

        :param height: the extrusion height.
        :type height: number

        :param center: determines if the object is centered on the Z-axis after extrusion.
        :type center: boolean

        :param convexity: The convexity parameter specifies the maximum number of front sides (back sides) a ray intersecting the object might penetrate. This parameter is only needed for correctly displaying the object in OpenCSG preview mode and has no effect on the polyhedron rendering.
        :type convexity: int

        :param twist: Twist is the number of degrees of through which the shape is extruded.  Setting to 360 will extrude through one revolution.  The twist direction follows the left hand rule.
        :type twist: number

        :param slices: number of slices to extrude. Can be used to improve the output.
        :type slices: int

        :param scale: relative size of the top of the extrusion compared to the start
        :type scale: number

        '''

        return objects.linear_extrude(height, center, convexity, twist, slices, scale)(self)

    def rotate_extrude(self,convexity=None, segments=None):
        '''
        A rotational extrusion is a Linear Extrusion with a twist, literally.
        Unfortunately, it can not be used to produce a helix for screw threads
        as the 2D outline must be normal to the axis of rotation, ie they need
        to be flat in 2D space.

        The 2D shape needs to be either completely on the positive, or negative
        side (not recommended), of the X axis. It can touch the axis, i.e. zero,
        however if the shape crosses the X axis a warning will be shown in the
        console windows and the rotate\_extrude() will be ignored. If the shape
        is in the negative axis the faces will be inside-out, you probably don't
        want to do that; it may be fixed in the future.

        :param convexity: The convexity parameter specifies the maximum number of front sides (back sides) a ray intersecting the object might penetrate. This parameter is only needed for correctly displaying the object in OpenCSG preview mode and has no effect on the polyhedron rendering.
        :type convexity: int

        :param segments: The fixed number of fragments to use.
        :type segments: int

        '''
        return objects.rotate_extrude(convexity, segments)(self)

    def dxf_linear_extrude(self, file, layer=None, height=None, center=None,
                           convexity=None, twist=None, slices=None):
        return objects.dxf_linear_extrude(file, layer, height, center,
                                          convexity, twis, slices)(self)

    def projection(self, cut=None):
        '''
        Creates 2d shapes from 3d models, and export them to the dxf format.
        It works by projecting a 3D model to the (x,y) plane, with z at 0.

        :param cut: when True only points with z=0 will be considered (effectively cutting the object) When False points above and below the plane will be considered as well (creating a proper projection).
        :type cut: boolean
        '''
        return objects.projection(cut)(self)

    def debug(self):
        self.set_modifier("#")
        return self

    def background(self):
        self.set_modifier('%')
        return self

    def root(self):
        self.set_modifier('!')
        return self

    def disable(self):
        self.set_modifier('*')
        return self

    def _repr_png_(self) -> Optional[bytes]:
        """
        Allow rich clients such as the IPython Notebook, to display the current
        OpenSCAD rendering of this object.
        """
        png_data = None
        tmp = tempfile.NamedTemporaryFile(suffix=".scad", delete=False)
        tmp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        try:
            scad_text = scad_render(self).encode("utf-8")
            tmp.write(scad_text)
            tmp.close()
            tmp_png.close()
            subprocess.Popen([
                "openscad",
                "--preview",
                "-o", tmp_png.name,
                tmp.name
            ]).communicate()

            with open(tmp_png.name, "rb") as png:
                png_data = png.read()
        finally:
            os.unlink(tmp.name)
            os.unlink(tmp_png.name)

        return png_data

class IncludedOpenSCADObject(OpenSCADObject):
    """
    Identical to OpenSCADObject, but each subclass of IncludedOpenSCADObject
    represents imported scad code, so each instance needs to store the path
    to the scad file it's included from.
    """

    def __init__(self, name, params, include_file_path, use_not_include=False, **kwargs):
        self.include_file_path = self._get_include_path(include_file_path)

        use_str = 'use' if use_not_include else 'include'
        self.include_string = f'{use_str} <{self.include_file_path}>\n'

        # Just pass any extra arguments straight on to OpenSCAD; it'll accept
        # them
        if kwargs:
            params.update(kwargs)

        OpenSCADObject.__init__(self, name, params)

    def _get_include_path(self, include_file_path):
        # Look through sys.path for anyplace we can find a valid file ending
        # in include_file_path.  Return that absolute path
        if os.path.isabs(include_file_path) and os.path.isfile(include_file_path):
            return include_file_path
        else:
            for p in sys.path:
                whole_path = os.path.join(p, include_file_path)
                if os.path.isfile(whole_path):
                    return os.path.abspath(whole_path)

        # No loadable SCAD file was found in sys.path.  Raise an error
        raise ValueError(f"Unable to find included SCAD file: {include_file_path} in sys.path")

def py2openscad(o: Union[bool, float, str, Iterable]) -> str:
    if type(o) == bool:
        return str(o).lower()
    if type(o) == float:
        return f"{o:.10f}"  # type: ignore
    if type(o) == str:
        return f'\"{o}\"'  # type: ignore
    if type(o).__name__ == "ndarray":
        import numpy  # type: ignore
        return numpy.array2string(o, separator=",", threshold=1000000000)
    if isinstance(o, IncludedOpenSCADObject):
        return o._render()[1:-1]
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

