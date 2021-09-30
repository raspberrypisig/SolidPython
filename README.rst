SolidPython
-----------

.. image:: https://circleci.com/gh/SolidCode/SolidPython.svg?style=shield
    :target: https://circleci.com/gh/SolidCode/SolidPython
.. image:: https://readthedocs.org/projects/solidpython/badge/?version=latest
    :target: http://solidpython.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

-  `SolidPython: OpenSCAD for
   Python <#solidpython--openscad-for-python>`__
-  `Advantages <#advantages>`__
-  `Installing SolidPython <#installing-solidpython>`__
-  `Using SolidPython <#using-solidpython>`__
-  `Importing OpenSCAD Code <#importing-openscad-code>`__
-  `Example Code <#example-code>`__
-  `Extra syntactic sugar <#extra-syntactic-sugar>`__

   -  `Basic operators <#basic-operators>`__
   -  `First-class Negative Space
      (Holes) <#first-class-negative-space-holes>`__
   -  `Animation <#animation>`__

-  `solid.utils <#solidutils>`__

   -  `Directions: (up, down, left, right, forward, back) for arranging
      things: <#directions-up-down-left-right-forward-back-for-arranging-things>`__
   -  `Arcs <#arcs>`__
   -  `Extrude Along Path <#extrude_along_path>`__
   -  `Bill Of Materials <#bill-of-materials>`__

-  `solid.screw\_thread <#solidscrew_thread>`__
-  `solid.splines <#solidsplines>`__
-  `Jupyter Renderer <#jupyter-renderer>`__
-  `Contact <#contact>`__
-  `License <#license>`__

SolidPython: OpenSCAD for Python
================================

SolidPython is a generalization of Phillip Tiefenbacher's openscad
module, found on `Thingiverse <http://www.thingiverse.com/thing:1481>`__. It
generates valid OpenSCAD code from Python code with minimal overhead. Here's a
simple example:

This Python code:

.. code:: python

    from solid import *
    d = difference()(
        cube(10),
        sphere(15)
    )
    print(scad_render(d))

Generates this OpenSCAD code:

.. code:: python

    difference(){
        cube(10);
        sphere(15);
    }

That doesn't seem like such a savings, but the following SolidPython code is a
lot shorter (and I think clearer) than the SCAD code it compiles to:

.. code:: python

    from solid import *
    d = cube(5) + right(5)(sphere(5)) - cylinder(r=2, h=6)

Generates this OpenSCAD code:

.. code::

    difference(){
        union(){
            cube(5);
            translate( [5, 0,0]){
                sphere(5);
            }
        }
        cylinder(r=2, h=6);
    }

Advantages
==========

In contrast to OpenSCAD -- which is a constrained domain specific language --
Python is a full blown modern programming language and as such supports
pretty much all modern programming features. Furthermore a huge number of
libraries are available.

SolidPython lets you use all these fancy python features to generate your
constructive solid geometry models.

On the one hand it makes the generation of your models a lot easier, because
you don't need to learn another domain specific language and you can use all
the programming technique you're already familiar with. On the other hand it
gives you a lot more power, because you can use all the comprehensive python
libraries to generate your models.

I would almost say this enables you to do what ever you want with ease.
As (maybe little uncommon) example, you could write a program that:

  - looks up the mail adress of your actuall president (base on your ip adress)
  - writes a mail to him and asks for a portrait
  - waits for a reply
  - generates a heightmap from the picture you received and maps it onto a vase

This should be pretty straight forward with SolidPython but is impossible with
pure OpenSCAD.


Installing SolidPython
======================

-  Install latest release via
   `PyPI <https://pypi.python.org/pypi/solidpython>`__:

   .. code:: bash

       pip install solidpython

   (You may need to use ``sudo pip install solidpython``, depending on
   your environment. This is commonly discouraged though. You'll be happiest 
   working in a `virtual environment <https://docs.python.org/3/tutorial/venv.html>`__ 
   where you can easily control dependencies for a given project)

- Install current master straight from Github:

  .. code:: bash

      pip install git+https://github.com/SolidCode/SolidPython.git

Using SolidPython
=================

-  Include SolidPython at the top of your Python file:

   .. code:: python

       from solid import *

   (See `this issue <https://github.com/SolidCode/SolidPython/issues/114>`__ for 
   a discussion of other import styles)

-  OpenSCAD uses curly-brace blocks ({}) to create its tree. SolidPython
   uses parentheses with comma-delimited lists. 
   
   **OpenSCAD:**

   .. code::

       difference(){
           cube(10);
           sphere(15);
       }

   **SolidPython:**

   .. code::

       d = difference()(
           cube(10),  # Note the comma between each element!
           sphere(15)
       )

-  Call ``py_scad_obj.as_scad()`` to generate SCAD code. This returns
   a string of valid OpenSCAD code.
-  *or*: call ``py_scad_obj.save_as_scad(filepath.scad)`` to store
   that code in a file.
-  If ``filepath.scad`` is open in the OpenSCAD IDE and Design => 'Automatic
   Reload and Compile' is checked in the OpenSCAD IDE, running
   ``py_scad_obj.save_as_scad()`` from Python will load the object in the
   IDE.
-  Alternately, you could call OpenSCAD's command line and render
   straight to STL.

Importing OpenSCAD code
=======================

- Use ``solid.import_scad(path)`` to import OpenSCAD code. Relative paths will 
check the current location designated in `OpenSCAD library directories <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Libraries>`__.

**Ex:** 

``scadfile.scad``

.. code::

    module box(w,h,d){
        cube([w,h,d]);
    }

``your_file.py``

.. code:: python

    from solid import *

    scadfile = import_scad('/path/to/scadfile.scad') 
    b = scadfile.box(2,4,6)
    b.save_as_scad('out_file.scad')

- Recursively import OpenSCAD code by calling ``import_scad()`` with a directory argument.

.. code:: python

    from solid import *

    # MCAD is OpenSCAD's most common utility library: https://github.com/openscad/MCAD
    # If it's installed for OpenSCAD (on MacOS, at: ``$HOME/Documents/OpenSCAD/libraries``)
    mcad = import_scad('MCAD')

    # MCAD contains about 15 separate packages, each included as its own namespace
    print(dir(mcad)) # => ['bearing', 'bitmap', 'boxes', etc...]
    mount = mcad.motors.stepper_motor_mount(nema_standard=17)
    mount.save_as_scad('motor_mount_file.scad')

- OpenSCAD has the ``use()`` and ``include()`` statements for importing SCAD code, and SolidPython has them, too. They pollute the global namespace, though, and you may have better luck with ``import_scad()``,

**Ex:**

``scadfile.scad``

.. code::

    module box(w,h,d){
        cube([w,h,d]);
    }

``your_file.py``

.. code:: python

    from solid import *

    # use() puts the module `box()` into the global namespace
    use('/path/to/scadfile.scad') 
    b = box(2,4,6)
    scad_render_to_file(b, 'out_file.scad')


Example Code
============

The best way to learn how SolidPython works is to look at the included
example code. If you've installed SolidPython, the following line of
Python will print (the location of) the examples directory:

.. code:: python

    import os, solid; print(os.path.dirname(solid.__file__) + '/examples')
        

Or browse the example code on Github
`here <https://github.com/SolidCode/SolidPython/tree/master/solid/examples>`__

Extra syntactic sugar
=====================

Basic operators
---------------

Following Elmo Mäntynen's suggestion, SCAD objects override the basic
operators + (union), - (difference), and \* (intersection). So

.. code:: python

    c = cylinder(r=10, h=5) + cylinder(r=2, h=30)

is the same as:

.. code:: python

    c = union()(
        cylinder(r=10, h=5),
        cylinder(r=2, h=30)
    )

Likewise:

.. code:: python

    c = cylinder(r=10, h=5)
    c -= cylinder(r=2, h=30)

is the same as:

.. code:: python

    c = difference()(
        cylinder(r=10, h=5),
        cylinder(r=2, h=30)
    )

Access Style Syntax
-------------------

TODO: ...

Convinience functions
---------------------

SolidPython includes a number of convinience functions. Currently these
include:

Directions: (up, down, left, right, forward, fwd, back) for arranging things:

.. code:: python

    up(10)(
        cylinder()
    )

seems a lot clearer to me than:

.. code:: python

    translate( [0,0,10])(
        cylinder()
    )

| I took this from someone's SCAD work and have lost track of the
  original author.
| My apologies.

Features
========

BOSL2
-----

TODO: should replace Holes & Parts, extrude_along_path, splines, screw_threads,...

Animation, Customizer, custom Fonts, ImplicitCad
------------------------------------------------

TODO:... SolidPython 2 supports all these features, take a look at the examples....


Jupyter Renderer
----------------

Render SolidPython or OpenSCAD code in Jupyter notebooks using `ViewSCAD <https://github.com/nickc92/ViewSCAD>`__, or install directly via:

.. code:: bash

    pip install viewscad

(Take a look at the `repo page <https://github.com/nickc92/ViewSCAD>`__, though, since there's a tiny bit more installation required)

Version 2.0.0
=============

TODO: change expSolid -> SolidPython 2.0.0

This is an experimental SolidPython branch. It's a
refactored version of SolidPython. Since -- I guess -- this branch will never make it back to
SolidPython:master it's now kind of a "thing" of its own - an experimental
SolidPython fork.

It is based on the following proposal:
https://github.com/SolidCode/SolidPython/issues/169

The goal was to

* extract the "core" from SolidPython
* make a solid package that only contains the fundamentals (+ a few convenience features) 
* make it extendible
* try to get complex libraries working properly (mcad, bosl, bosl2)
* **KISS**: ``from solid import *`` -> imports only ~1000 lines of source code and has (almost?) all the feautres SolidPython:master has
* be a drop in replacement for SolidPython:master -- as far as possible, see Backwards Compatibility Section
* get all kinds of nice feature working (see Features section)
* let's see what's next

Take a look at the `example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/>`_ to get an impression what this library can do. The interesting stuff starts with the 7th example.

Features
========

In difference to SolidPython:master this branch has support for the following features:

* **bosl2** - the "scad import stuff" was improved so it is now capable of handling bosl2 properly. This seems to me like SolidPython++ because you can now use all the fancy stuff from the bosl2 library. `bosl2 example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/07-libs-bosl2.py>`_ `mazebox example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/16-mazebox-bosl2.py>`_
* native **OpenSCAD customizer** support `customizer example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/10-customizer.py>`_
* native **OpenSCAD animation** support `animation example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/12-animation.py>`_ and `animation example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/13-animated-bouncing-ball.py>`_
* **custom fonts** `fonts example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/11-fonts.py>`_
* supports **ImplicitCAD** `implicitCAD example <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/14-implicitCAD.py>`_ `implicitCAD example 2 <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples/15-implicitCAD2.py>`_

Furthermore it has several minor improvements, like these which are based on ideas from *posts* from the SolidPython universe:

* use invert operator (~) as # in OpenSCAD `#167 <https://github.com/SolidCode/SolidPython/pull/167>`_
* convenience function including to pass sizes as integer parameters (``translate(10, 20, 30)``) `#63 <https://github.com/SolidCode/SolidPython/pull/63#issuecomment-688171416>`_
* *access-style* syntax: ``cube(1).up(5).rotate(45, 0, 0)`` `#66 <https://github.com/SolidCode/SolidPython/pull/66>`_ This is additional! The OpenSCAD / SolidPython style syntax is still fully supported.

Take a look at the `examples <https://github.com/jeff-dh/SolidPython/blob/exp_solid/solid/examples>`_ to see what's possible.

You need to install BOSL2 into your OpenSCAD libraries folder (`~/.local/share/OpenSCAD/libraries/`) for the bosl2 exteions to work. Grab it from `bosl2 github <https://github.com/revarbat/BOSL2>`_.

Another nice little feature especially to play around and debug it is that the ``__repr__`` operator of each "OpenSCADObject" now calls ``scad_render``. With this the python shell becomes pretty good in debuging and playing around with solid code and the library itself:

.. code:: python

  >>> from solid import *
  >>> c = cube(5)
  >>> c.up(5)
  translate(v = [0, 0, 5]) {
          cube(size = 5);
  };
  >>> c.up(5).save_as_scad()
  '/home/xxx/xxx/xxx/SolidPython/expsolid_out.scad'
  >>>

Backwards compatibility
=======================

It should be a pretty complete and backwards compatible drop in replacement for
SolidPython. The backwards compatibility is not 100%. Somethings (and even
interfaces) changed. I tried to stay as backward compatible as possible.
The package should behave 98% the same as SolidPython unless you do some "deep
access" -- that's by 99% chance not backward compatible (like modifying
OpenSCADObjects or import internal modules).

As long as you stick to:

.. code:: python

  from solid import *

you shoul be fine.

If you want "more backwards compatibility" (like `solid.utils, holes feature, set_modifier, __radd__`....) there's the legacy extension which is supposed to create backwards compatibility as far as possible:
If you need / want more of the SolidPython:master interface (like `solid.utils, holes feature, set_modifier, add_trait, add_param, __radd__`....) import `solid.extensions.legacy`. It tries to fill the gap as good as possible:

.. code:: python

  from solid.extensions.legacy import *

I was able to get the examples from SolidPython:master running just by changing the imports and they all (except for the splines example which seems to have an internal issue) worked "out of the box".


The interface changed in a few minor aspects:

* OpenSCAD identifier escaping:
        * all *illegal* python idetifiers are escape with a single prepending underscore
        * special variables ``$fn -> _fn`` (*note*: ``segments`` still works)
        * identifier starting with a digit ``module 12ptStar() -> _12ptStar()`` (*note*: ``__12ptStar`` still works)
        * python keywords ``module import() -> _import()`` (*note*: ``import\_``  still works)

* import paths have changed (a lot)
    * as long as you only import the root package it should be fine, otherwise probably not
    
    .. code:: python
    
            from solid import * #fine
            from solid import objects #crash
            from solid import solidpython #crash
            from solid import splines #crash
            from solid import utils #crash

* all extensions have been moved:
    * solid.utils has been moved to ``solid.extensions.legacy``. If you want to use them import that extension
    * there are some example implementations of the part / hole feature and
      bill of materials in ``solid.extensions.legacy``. They seem to work but are
      not tested extensively. Take a look at ``examples/xx_legacy*``.
    * please take a look at the bosl2 example. BOSL2 provides many features which
      might be alternatives.

* OpenSCADObject internally changed a lot
    If you access it directly
    (e.g. mycube.set_modifier) this might not work. But if you import
    ``solid.extensions.legacy`` some dummy methods will be monkey patched onto
    OpenSCADObject so you might be able to at least run the code, but it
    might render not correctly.

* maybe some more things I can't remember right now. Some function
  signatures changed slightly. But as long as as you stick to the
  regular public interface everything should be fine.


Contact
=======

Enjoy, and please send any questions or bug reports to me at
``evan_t_jones@mac.com``.

Cheers!

Evan

License
=======

This library is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

`Full text of the
license <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt>`__.

Some class docstrings are derived from the `OpenSCAD User Manual
<https://en.wikibooks.org/wiki/OpenSCAD_User_Manual>`__, so 
are available under the `Creative Commons Attribution-ShareAlike License
<https://creativecommons.org/licenses/by-sa/3.0/>`__. 
