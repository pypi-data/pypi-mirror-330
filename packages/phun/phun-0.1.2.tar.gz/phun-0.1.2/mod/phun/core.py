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


"""Implementation of physics aware functions decorators and helpers."""


from functools import wraps
from astropy   import units

from .helper import *


def partial(f, params={}):
    """An improved version of `functools.partial()`."""

    fargs = get_argnames(f)
    fkeys = get_keywords(f)

    pargs   = {}
    pkwargs = {}
    for k, v in params.items():
        if isinstance(k, int):
            pargs[k] = v
        elif isinstance(k, str):
            pkwargs[k] = v
        else:
            raise ValueError(
                f"Do not know how to interpret key {k} for `args` or `kwargs`")

    assert len(pargs)   <= len(fargs)
    assert set(pkwargs) <= set(fkeys)

    n = len(fargs)

    @wraps(f)
    def p(*args, **kwargs): # closure on `pargs`, `pkwargs`, and `n`
        assert len(args) + len(pargs) == n
        args = list(args)
        args = tuple(params[i] if i in params else args.pop(0) for i in range(n))
        kwargs = {**pkwargs, **kwargs}
        return f(*args, **kwargs)

    return p


def optdec(dec):
    """Make decorator support optional arguments and keywords."""

    @wraps(dec)
    def wrap(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return dec(args[0])
        else:
            return lambda f: dec(f, *args, **kwargs)

    return wrap


@optdec
def phun(mkf, u_res=None):
    """Physics aware function generator transformer.

    ``phun`` is a decorator that transforms a restricted physics aware
    function generator ``mkf()`` into a more flexible function
    generator ``mkph()``.

    """

    @wraps(mkf)
    def mkph(*args, **kwargs):

        uargs = []
        vargs = {}
        for i, v in enumerate(args):
            if v == 1:
                uargs.append(units.dimensionless_unscaled)
            elif isinstance(v, units.UnitBase):
                uargs.append(v)
            else:
                uargs.append(v.unit)
                vargs[i] = v.value

        u = get_default(kwargs, 'u_res', mkf)
        b = get_default(kwargs, 'backend', mkf)

        kwargs['u_res']   = get_unit(u, u_res)
        kwargs['backend'] = get_backend(b)

        ph = partial(mkf(*uargs, **kwargs), vargs)
        ph.unit = kwargs['u_res']
        return ph

    return mkph
