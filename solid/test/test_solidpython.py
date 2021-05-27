#! /usr/bin/env python
import os
import tempfile
import unittest
from pathlib import Path

from solid.builtins import background, debug, disable, root
from solid.builtins import rotate, sphere, circle, cube, cylinder
from solid.builtins import square, translate, color, difference, hull
from solid.builtins import _import, intersection, intersection_for, linear_extrude, import_dxf
from solid.builtins import import_stl, minkowski, mirror, multmatrix, offset, polygon
from solid.builtins import polyhedron, projection, render, resize, rotate_extrude
from solid.builtins import scale, surface, union

from solid.helpers import resolve_scad_filename
from solid.scad_import import import_scad, include, use

from solid.scad_render import scad_render, scad_render_animated_file, scad_render_to_file
from solid.test.ExpandedTestCase import DiffOutput

scad_test_case_templates = [
    {'name': 'polygon', 'class': 'polygon' , 'kwargs': {'paths': [[0, 1, 2]]}, 'expected': 'polygon(paths = [[0, 1, 2]], points = [[0, 0], [1, 0], [0, 1]]);\n', 'args': {'points': [[0, 0], [1, 0], [0, 1]]}, },
    {'name': 'polygon', 'class': 'polygon' , 'kwargs': {}, 'expected': 'polygon(points = [[0, 0], [1, 0], [0, 1]]);\n', 'args': {'points': [[0, 0], [1, 0], [0, 1]]}, },
    {'name': 'polygon', 'class': 'polygon' , 'kwargs': {}, 'expected': 'polygon(convexity = 3, points = [[0, 0], [1, 0], [0, 1]]);\n', 'args': {'points': [[0, 0], [1, 0], [0, 1]], 'convexity': 3}, },
    {'name': 'circle', 'class': 'circle' , 'kwargs': {'_fn': 12, 'r': 1}, 'expected': 'circle($fn = 12, r = 1);\n', 'args': {}, },
    {'name': 'circle_diam', 'class': 'circle' , 'kwargs': {'_fn': 12, 'd': 1}, 'expected': 'circle($fn = 12, d = 1);\n', 'args': {}, },
    {'name': 'square', 'class': 'square' , 'kwargs': {'center': False, 'size': 1}, 'expected': 'square(center = false, size = 1);\n', 'args': {}, },
    {'name': 'sphere', 'class': 'sphere' , 'kwargs': {'_fn': 12, 'r': 1}, 'expected': 'sphere($fn = 12, r = 1);\n', 'args': {}, },
    {'name': 'sphere_diam', 'class': 'sphere' , 'kwargs': {'d': 1, '_fn': 12}, 'expected': 'sphere($fn = 12, d = 1);\n', 'args': {}, },
    {'name': 'cube', 'class': 'cube' , 'kwargs': {'center': False, 'size': 1}, 'expected': 'cube(center = false, size = 1);\n', 'args': {}, },
    {'name': 'cylinder', 'class': 'cylinder' , 'kwargs': {'r1': None, 'r2': None, 'h': 1, '_fn': 12, 'r': 1, 'center': False}, 'expected': 'cylinder($fn = 12, center = false, h = 1, r = 1);\n', 'args': {}, },
    {'name': 'cylinder_d1d2', 'class': 'cylinder' , 'kwargs': {'d1': 4, 'd2': 2, 'h': 1, '_fn': 12, 'center': False}, 'expected': 'cylinder($fn = 12, center = false, d1 = 4, d2 = 2, h = 1);\n', 'args': {}, },
    {'name': 'polyhedron', 'class': 'polyhedron' , 'kwargs': {'convexity': None}, 'expected': 'polyhedron(faces = [[0, 1, 2]], points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]);\n', 'args': {'points': [[0, 0, 0], [1, 0, 0], [0, 1, 0]], 'faces': [[0, 1, 2]]}, },
    {'name': 'union', 'class': 'union' , 'kwargs': {}, 'expected': 'union();\n', 'args': {}, },
    {'name': 'intersection', 'class': 'intersection' , 'kwargs': {}, 'expected': 'intersection();\n', 'args': {}, },
    {'name': 'difference', 'class': 'difference' , 'kwargs': {}, 'expected': 'difference();\n', 'args': {}, },
    {'name': 'translate', 'class': 'translate' , 'kwargs': {'v': [1, 0, 0]}, 'expected': 'translate(v = [1, 0, 0]);\n', 'args': {}, },
    {'name': 'scale', 'class': 'scale' , 'kwargs': {'v': 0.5}, 'expected': 'scale(v = 0.5000000000);\n', 'args': {}, },
    {'name': 'rotate', 'class': 'rotate' , 'kwargs': {'a': 45, 'v': [0, 0, 1]}, 'expected': 'rotate(a = 45, v = [0, 0, 1]);\n', 'args': {}, },
    {'name': 'mirror', 'class': 'mirror' , 'kwargs': {}, 'expected': 'mirror(v = [0, 0, 1]);\n', 'args': {'v': [0, 0, 1]}, },
    {'name': 'resize', 'class': 'resize' , 'kwargs': {'newsize': [5, 5, 5], 'auto': [True, True, False]}, 'expected': 'resize(auto = [true, true, false], newsize = [5, 5, 5]);\n', 'args': {}, },
    {'name': 'multmatrix', 'class': 'multmatrix' , 'kwargs': {}, 'expected': 'multmatrix(m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]);\n', 'args': {'m': [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]}, },
    {'name': 'minkowski', 'class': 'minkowski' , 'kwargs': {}, 'expected': 'minkowski();\n', 'args': {}, },
    {'name': 'offset', 'class': 'offset' , 'kwargs': {'r': 1}, 'expected': 'offset(r = 1);\n', 'args': {}, },
    {'name': 'offset_segments', 'class': 'offset' , 'kwargs': {'r': 1, '_fn': 12}, 'expected': 'offset($fn = 12, r = 1);\n', 'args': {}, },
    {'name': 'offset_chamfer', 'class': 'offset' , 'kwargs': {'delta': 1, 'chamfer' : 'False'}, 'expected': 'offset(chamfer = false, delta = 1);\n', 'args': {}, },
    {'name': 'offset_zero_delta', 'class': 'offset' , 'kwargs': {'r': 0}, 'expected': 'offset(r = 0);\n', 'args': {}, },
    {'name': 'hull', 'class': 'hull' , 'kwargs': {}, 'expected': 'hull();\n', 'args': {}, },
    {'name': 'render', 'class': 'render' , 'kwargs': {'convexity': None}, 'expected': 'render();\n', 'args': {}, },
    {'name': 'projection', 'class': 'projection' , 'kwargs': {'cut': None}, 'expected': 'projection();\n', 'args': {}, },
    {'name': 'surface', 'class': 'surface' , 'kwargs': {'center': False, 'convexity': None}, 'expected': 'surface(center = false, file = "/Path/to/dummy.dxf");\n', 'args': {'file': "'/Path/to/dummy.dxf'"}, },
    {'name': 'import_stl', 'class': 'import_stl' , 'kwargs': {'layer': None, 'origin': (0, 0)}, 'expected': 'import_stl(file = "/Path/to/dummy.stl", origin = [0, 0]);\n', 'args': {'file': "'/Path/to/dummy.stl'"}, },
    {'name': 'import_dxf', 'class': 'import_dxf' , 'kwargs': {'layer': None, 'origin': (0, 0)}, 'expected': 'import_dxf(file = "/Path/to/dummy.dxf", origin = [0, 0]);\n', 'args': {'file': "'/Path/to/dummy.dxf'"}, },
    {'name': 'import_', 'class': '_import' , 'kwargs': {'layer': None, 'origin': (0, 0)}, 'expected': 'import(file = "/Path/to/dummy.dxf", origin = [0, 0]);\n', 'args': {'file': "'/Path/to/dummy.dxf'"}, },
    {'name': 'import__convexity', 'class': '_import' , 'kwargs': {'layer': None, 'origin': (0, 0), 'convexity': 2}, 'expected': 'import(convexity = 2, file = "/Path/to/dummy.dxf", origin = [0, 0]);\n', 'args': {'file': "'/Path/to/dummy.dxf'"}, },
    {'name': 'linear_extrude', 'class': 'linear_extrude' , 'kwargs': {'twist': None, 'slices': None, 'center': False, 'convexity': None, 'height': 1, 'scale': 0.9}, 'expected': 'linear_extrude(center = false, height = 1, scale = 0.9000000000);\n', 'args': {}, },
    {'name': 'rotate_extrude', 'class': 'rotate_extrude' , 'kwargs': {'angle': 90, '_fn': 4, 'convexity': None}, 'expected': 'rotate_extrude($fn = 4, angle = 90);\n', 'args': {}, },
    {'name': 'intersection_for', 'class': 'intersection_for' , 'kwargs': {}, 'expected': 'intersection_for(n = [0, 1, 2]);\n', 'args': {'n': [0, 1, 2]}, },
]


class TemporaryFileBuffer(object):
    name = None
    contents = None

    def __enter__(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.name = f.name
        try:
            f.close()
        except:
            self._cleanup()
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            with open(self.name, 'r') as f:
                self.contents = f.read()
        finally:
            self._cleanup()

    def _cleanup(self):
        try:
            os.unlink(self.name)
        except:
            pass


class TestSolidPython(DiffOutput):
    # test cases will be dynamically added to this instance

    def expand_scad_path(self, filename):
        path = Path(__file__).absolute().parent.parent / filename
        return path

    def test_infix_union(self):
        a = cube(2)
        b = sphere(2)
        expected = 'union() {\n\tcube(size = 2);\n\tsphere(r = 2);\n}\n'
        actual = scad_render(a + b)
        self.assertEqual(expected, actual)

    def test_infix_difference(self):
        a = cube(2)
        b = sphere(2)
        expected = 'difference() {\n\tcube(size = 2);\n\tsphere(r = 2);\n}\n'
        actual = scad_render(a - b)
        self.assertEqual(expected, actual)

    def test_infix_intersection(self):
        a = cube(2)
        b = sphere(2)
        expected = 'intersection() {\n\tcube(size = 2);\n\tsphere(r = 2);\n}\n'
        actual = scad_render(a * b)
        self.assertEqual(expected, actual)

    def test_parse_scad_callables(self):
        test_str = """
                    module hex (width=10, height=10,
                                flats= true, center=false){}
                    function righty (angle=90) = 1;
                    function lefty(avar) = 2;
                    module more(a=[something, other]) {}
                    module pyramid(side=10, height=-1, square=false, centerHorizontal=true, centerVertical=false){}
                    module no_comments(arg=10,   //test comment
                    other_arg=2, /* some extra comments
                    on empty lines */
                    last_arg=4){}
                    module float_arg(arg=1.0){}
                    module arg_var(var5){}
                    module kwarg_var(var2=78){}
                    module var_true(var_true = true){}
                    module var_false(var_false = false){}
                    module var_int(var_int = 5){}
                    module var_negative(var_negative = -5){}
                    module var_float(var_float = 5.5){}
                    module var_number(var_number = -5e89){}
                    module var_empty_vector(var_empty_vector = []){}
                    module var_simple_string(var_simple_string = "simple string"){}
                    module var_complex_string(var_complex_string = "a \\"complex\\"\\tstring with a\\\\"){}
                    module var_vector(var_vector = [5454445, 565, [44545]]){}
                    module var_complex_vector(var_complex_vector = [545 + 4445, 565, [cos(75) + len("yes", 45)]]){}
                    module var_vector(var_vector = [5, 6, "string\\twith\\ttab"]){}
                    module var_range(var_range = [0:10e10]){}
                    module var_range_step(var_range_step = [-10:0.5:10]){}
                    module var_with_arithmetic(var_with_arithmetic = 8 * 9 - 1 + 89 / 15){}
                    module var_with_parentheses(var_with_parentheses = 8 * ((9 - 1) + 89) / 15){}
                    module var_with_functions(var_with_functions = abs(min(chamferHeight2, 0)) / 1){}
                    module var_with_conditional_assignment(var_with_conditional_assignment = mytest ? 45 : yop){}

                   """

        scad_file = ""
        with tempfile.NamedTemporaryFile(suffix=".scad", delete=False) as f:
            f.write(test_str.encode("utf-8"))
            scad_file = f.name

        expected = [
            {'name': 'hex', 'args': [], 'kwargs': ['width', 'height', 'flats', 'center']},
            {'name': 'righty', 'args': [], 'kwargs': ['angle']},
            {'name': 'lefty', 'args': [], 'kwargs': ['avar']},
            {'name': 'more', 'args': [], 'kwargs': ['a']},
            {'name': 'pyramid', 'args': [], 'kwargs': ['side', 'height', 'square', 'centerHorizontal', 'centerVertical']},
            {'name': 'no_comments', 'args': [], 'kwargs': ['arg', 'other_arg', 'last_arg']},
            {'name': 'float_arg', 'args': [], 'kwargs': ['arg']},
            {'name': 'arg_var', 'args': [], 'kwargs': ['var5']},
            {'name': 'kwarg_var', 'args': [], 'kwargs': ['var2']},
            {'name': 'var_true', 'args': [], 'kwargs': ['var_true']},
            {'name': 'var_false', 'args': [], 'kwargs': ['var_false']},
            {'name': 'var_int', 'args': [], 'kwargs': ['var_int']},
            {'name': 'var_negative', 'args': [], 'kwargs': ['var_negative']},
            {'name': 'var_float', 'args': [], 'kwargs': ['var_float']},
            {'name': 'var_number', 'args': [], 'kwargs': ['var_number']},
            {'name': 'var_empty_vector', 'args': [], 'kwargs': ['var_empty_vector']},
            {'name': 'var_simple_string', 'args': [], 'kwargs': ['var_simple_string']},
            {'name': 'var_complex_string', 'args': [], 'kwargs': ['var_complex_string']},
            {'name': 'var_vector', 'args': [], 'kwargs': ['var_vector']},
            {'name': 'var_complex_vector', 'args': [], 'kwargs': ['var_complex_vector']},
            {'name': 'var_vector', 'args': [], 'kwargs': ['var_vector']},
            {'name': 'var_range', 'args': [], 'kwargs': ['var_range']},
            {'name': 'var_range_step', 'args': [], 'kwargs': ['var_range_step']},
            {'name': 'var_with_arithmetic', 'args': [], 'kwargs': ['var_with_arithmetic']},
            {'name': 'var_with_parentheses', 'args': [], 'kwargs': ['var_with_parentheses']},
            {'name': 'var_with_functions', 'args': [], 'kwargs': ['var_with_functions']},
            {'name': 'var_with_conditional_assignment', 'args': [], 'kwargs': ['var_with_conditional_assignment']}
        ]

        from solid.scad_import import parse_scad_callables
        actual = parse_scad_callables(scad_file)

        for e in expected:
            self.assertEqual(e in actual, True)

        os.unlink(scad_file)

    def test_use(self):
        include_file = self.expand_scad_path("examples/scad_to_include.scad")
        use(include_file)

        a = steps(3) # type: ignore
        actual = scad_render(a)

        abs_path = resolve_scad_filename(include_file)
        expected = f"use <{abs_path}>\n\n\nsteps(howmany = 3);\n"
        self.assertEqual(expected, actual)

    def test_import_scad(self):
        include_file = self.expand_scad_path("examples/scad_to_include.scad")
        mod = import_scad(include_file)
        a = mod.steps(3)
        actual = scad_render(a)

        abs_path = resolve_scad_filename(include_file)
        expected = f"use <{abs_path}>\n\n\nsteps(howmany = 3);\n"
        self.assertEqual(expected, actual)

        # Make sure this plays nicely with `scad_render()`'s `file_header` arg
        header = '$fn = 24;'
        actual = scad_render(a, file_header=header)
        expected = f"{header}\nuse <{abs_path}>\n\n\nsteps(howmany = 3);\n"
        self.assertEqual(expected, actual)

        # Confirm that we can leave out even non-default arguments in OpenSCAD
        a = mod.optional_nondefault_arg();
        actual = scad_render(a)
        expected = f'use <{abs_path}>\n\n\noptional_nondefault_arg();\n'
        self.assertEqual(expected, actual);

        # Make sure we throw ValueError on nonexistent imports
        self.assertRaises(ValueError, import_scad, 'path/doesnt/exist.scad')

        # Test that we recursively import directories correctly
        examples = import_scad(include_file.parent)
        self.assertTrue(hasattr(examples, 'scad_to_include'))
        self.assertTrue(hasattr(examples.scad_to_include, 'steps'))

        # TODO: we should test that:
        # A) scad files in the designated OpenSCAD library directories
        #       (path-dependent, see: solid.objects._openscad_library_paths())
        #       are imported correctly. Not sure how to do this without writing
        #       temp files to those directories. Seems like overkill for the moment

    def test_imported_scad_arguments(self):
        include_file = self.expand_scad_path("examples/scad_to_include.scad")
        mod = import_scad(include_file)
        points = mod.scad_points();
        poly = polygon(points);
        actual = scad_render(poly);
        abs_path = resolve_scad_filename(include_file)
        expected = f'use <{abs_path}>\n\n\npolygon(points = scad_points());\n'
        self.assertEqual(expected, actual)

    def test_use_reserved_words(self):
        scad_str = '''module reserved_word_arg(or=3){\n\tcube(or);\n}\nmodule or(arg=3){\n\tcube(arg);\n}\n'''

        fd, path = tempfile.mkstemp(text=True)
        try:
            os.close(fd)
            with open(path, "w") as f:
                f.write(scad_str)

            use(path)
            a = reserved_word_arg(_or=5) # type: ignore
            actual = scad_render(a)
            expected = f"use <{path}>\n\n\nreserved_word_arg(or = 5);\n"
            self.assertEqual(expected, actual)

            b = _or(arg=5) # type: ignore
            actual = scad_render(b)
            expected = f"use <{path}>\n\n\nor(arg = 5);\n"
            self.assertEqual(expected, actual)
        finally:
            os.remove(path)

    def test_include(self):
        include_file = self.expand_scad_path("examples/scad_to_include.scad")
        self.assertIsNotNone(include_file, 'examples/scad_to_include.scad not found')
        include(include_file)
        a = steps(3) # type: ignore

        actual = scad_render(a)
        abs_path = resolve_scad_filename(include_file)
        expected = f"include <{abs_path}>\n\n\nsteps(howmany = 3);\n"
        self.assertEqual(expected, actual)

    """
    def test_extra_args_to_included_scad(self):
        include_file = self.expand_scad_path("examples/scad_to_include.scad")
        mod = import_scad(include_file)
        a = mod.steps(3, external_var=True)
        actual = scad_render(a)

        abs_path = resolve_scad_filename(include_file)
        expected = f"use <{abs_path}>\n\nsteps(external_var = true, howmany = 3);"
        self.assertEqual(expected, actual)
    """

    def test_background(self):
        a = cube(10)
        expected = '%cube(size = 10);\n'
        actual = scad_render(background(a))
        self.assertEqual(expected, actual)

    def test_debug(self):
        a = cube(10)
        expected = '#cube(size = 10);\n'
        actual = scad_render(debug(a))
        self.assertEqual(expected, actual)

    def test_disable(self):
        a = cube(10)
        expected = '*cube(size = 10);\n'
        actual = scad_render(disable(a))
        self.assertEqual(expected, actual)

    def test_root(self):
        a = cube(10)
        expected = '!cube(size = 10);\n'
        actual = scad_render(root(a))
        self.assertEqual(expected, actual)

    def test_color(self):
        all_args = [
            {'c': [1, 0, 0]},
            {'c': [1, 0, 0], 'alpha': 0.5},
            {'c': "#66F"},
            {'c': "Teal", 'alpha': 0.5},
        ]

        expecteds = [
            'color(c = [1, 0, 0]);\n',
            'color(alpha = 0.5000000000, c = [1, 0, 0]);\n',
            'color(c = "#66F");\n',
            'color(alpha = 0.5000000000, c = "Teal");\n',
        ]
        for args, expected in zip(all_args, expecteds):
            col = color(**args)
            actual = scad_render(col)
            self.assertEqual(expected, actual)

    def test_scad_render_animated_file(self):
        def my_animate(_time=0):
            import math
            # _time will range from 0 to 1, not including 1
            rads = _time * 2 * math.pi
            rad = 15
            c = translate([rad * math.cos(rads), rad * math.sin(rads)])(square(10))
            return c

        with TemporaryFileBuffer() as tmp:
            scad_render_animated_file(my_animate, steps=2, back_and_forth=False,
                                      filepath=tmp.name, include_orig_code=False)

        actual = tmp.contents
        expected = '\nif ($t >= 0.0 && $t < 0.5){\n\ttranslate(v = [15.0000000000, 0.0000000000]) {\n\t\tsquare(size = 10);\n\t}\n}\nif ($t >= 0.5 && $t < 1.0){\n\ttranslate(v = [-15.0000000000, 0.0000000000]) {\n\t\tsquare(size = 10);\n\t}\n}\n'

        self.assertEqual(expected, actual)

    def test_scad_render_to_file(self):
        a = circle(10)

        # No header, no included original code
        with TemporaryFileBuffer() as tmp:
            scad_render_to_file(a, filepath=tmp.name, include_orig_code=False)

        actual = tmp.contents
        expected = 'circle(r = 10);\n'

        # scad_render_to_file also adds a date & version stamp before scad code;
        # That won't match here, so just make sure the correct code is at the end
        self.assertTrue(actual.endswith(expected))

        # Header
        with TemporaryFileBuffer() as tmp:
            scad_render_to_file(a, filepath=tmp.name, include_orig_code=False,
                                file_header='$fn = 24;')

        actual = tmp.contents
        expected = '$fn = 24;\ncircle(r = 10);\n'

        self.assertTrue(actual.endswith(expected))

        # Test out_dir specification, both using an existing dir & creating one
        # Using existing directory
        with TemporaryFileBuffer() as tmp:
            out_dir = Path(tmp.name).parent
            expected = (out_dir / 'test_solidpython.scad').as_posix()
            actual = scad_render_to_file(a, out_dir=out_dir)
            self.assertEqual(expected, actual)

        # Creating a directory on demand
        with TemporaryFileBuffer() as tmp:
            out_dir = Path(tmp.name).parent / 'SCAD'
            expected = (out_dir / 'test_solidpython.scad').as_posix()
            actual = scad_render_to_file(a, out_dir=out_dir)
            self.assertEqual(expected, actual)

        # TODO: test include_orig_code=True, but that would have to
        # be done from a separate file, or include everything in this one

    def test_numpy_type(self):
        try:
            import numpy # type: ignore
            numpy_cube = cube(size=numpy.array([1, 2, 3]))
            expected = 'cube(size = [1,2,3]);\n'
            actual = scad_render(numpy_cube)
            self.assertEqual(expected, actual, 'Numpy SolidPython not rendered correctly')
        except ImportError:
            pass

    def test_custom_iterables(self):
        from euclid3 import Vector3

        class CustomIterable:
            def __iter__(self):
                return iter([1, 2, 3])

        expected = 'cube(size = [1, 2, 3]);\n'
        iterables = [
            [1, 2, 3],
            (1, 2, 3),
            Vector3(1, 2, 3),
            CustomIterable(),
        ]

        for iterable in iterables:
            name = type(iterable).__name__
            actual = scad_render(cube(size=iterable))
            self.assertEqual(expected, actual, f'{name} SolidPython not rendered correctly')


def single_test(test_dict):
    name, cls, args, kwargs, expected = test_dict['name'], test_dict['class'], test_dict['args'], test_dict['kwargs'], test_dict['expected']

    def test(self):
        call_str = cls + "("
        for k, v in args.items():
            call_str += f"{k}={v}, "
        for k, v in kwargs.items():
            call_str += f"{k}={v}, "
        call_str += ')'

        scad_obj = eval(call_str)
        actual = scad_render(scad_obj)

        self.assertEqual(expected, actual)

    return test


def generate_cases_from_templates():
    for test_dict in scad_test_case_templates:
        test = single_test(test_dict)
        test_name = f"test_{test_dict['name']}"
        setattr(TestSolidPython, test_name, test)


if __name__ == '__main__':
    generate_cases_from_templates()
    unittest.main()
