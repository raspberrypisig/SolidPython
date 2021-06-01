from .bill_of_materials import *
from .part_hole import *
from .repr_png import __nothing__
from .types import *
from .utils import *
from . import splines
from . import screw_thread

from ...core.object_base import ObjectBase

ObjectBase.set_modifier = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_modifier!" +\
          "This call will be ignored! Use debug()(...).")

ObjectBase.add_param = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.add_param!" +\
          "This call will be ignored! You should not need it ;)")

ObjectBase.set_parent = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_parent!" +\
          "This call will be ignored! You should not need it ;)")

ObjectBase.set_trait = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_trait!" +\
          "This call will be ignored!")

ObjectBase.get_trait = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.get_trait!" +\
          "This call will be ignored!")

ObjectBase.set_hole = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_hole!" +\
          "This call will be ignored! Use solid.extensions.legacy.part_hole")

ObjectBase.set_part_root = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.set_part_root!" +\
          "This call will be ignored! Use solid.extensions.legacy.part_hole")

ObjectBase.find_hole_children = lambda self, *args, **kwargs: \
    print("WARNING: ExpSolid does not support OpenSCADObject.find_hole_children!" +\
          "This call will be ignored! Use solid.extensions.legacy.part_hole")

