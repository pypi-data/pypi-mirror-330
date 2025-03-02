# Copyright 2022 Chi-kwan Chan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Extra helper functions for ``phun``."""


from inspect import signature
from astropy import units


def istreeof(t, c):
    """Test if ``t`` is a tree of only class ``c``."""

    if isinstance(t, tuple):
        return all(istreeof(n, c) for n in t)
    else:
        return isinstance(t, c)


def get_argnames(f):
    """Get argument names from function signature.

    Using the ``inspect`` module, it is possible to obtain the names
    of position arguments ``a1``, ``a2``, ..., from a function

        def f(a1, a2, ...):
            ...

    This helper function return these names in a tuple.

    """
    return tuple(k for k, v in signature(f).parameters.items() if v.default is v.empty)


def get_keywords(f):
    """Get keywords from function signature.

    Using the ``inspect`` module, it is possible to obtain the names
    of keyworded arguments ``k1``, ``k2``, ..., from a function

        def f(..., k1=..., k2=..., ...):
            ...

    This helper function return these names in a tuple.

    """
    return tuple(k for k, v in signature(f).parameters.items() if v.default is not v.empty)


def get_default(kwargs, name, f):
    """Get keyworded argument.

    Return the default keyworded argument of function ``f()`` if that
    value is not set in ``kwargs``.

    """
    return kwargs.get(name, signature(f).parameters[name].default)


def get_unit(unit, default):
    """Select the right unit."""

    if unit is None and istreeof(default, units.UnitBase):
        return default
    elif istreeof(unit, units.UnitBase):
        return unit
    elif isinstance(default, dict) and unit in default:
        return default[unit]
    else:
        raise ValueError(
            f"Do not know what to do with type(unit) = {type(unit)} and type(default) = {type(default)}")


def get_backend(backend):
    """Deduce backend from loaded module(s)."""

    if backend is None:
        import sys
        if 'jax' in sys.modules:
            import jax.numpy as backend
        else:
            import numpy as backend
    return backend
