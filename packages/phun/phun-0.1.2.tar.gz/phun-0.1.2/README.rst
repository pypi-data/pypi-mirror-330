|LT| |Docs| |PyPI|

.. |LT| image:: https://github.com/adxsrc/phun/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/adxsrc/phun/actions/workflows/python-package.yml

.. |Docs| image:: https://github.com/adxsrc/phun/actions/workflows/sphinx-pages.yml/badge.svg
   :target: https://github.com/adxsrc/phun/actions/workflows/sphinx-pages.yml

.. |PyPI| image:: https://github.com/adxsrc/phun/actions/workflows/python-publish.yml/badge.svg
   :target: https://pypi.org/project/phun/


|Phun|_: Physics Aware Functions
================================

Writing physics functions is non-trivial.
Although each physical quantity can be expressed in different units,
in computation physics, it is common to require the inputs of a
physics function in a pre-determined unit system.
This makes reusing these physics functions in different fields
challenging.
|Astropy|_ provides a powerful ``units`` sub-module to partially solve
this problem.
However, it introduces a special ``Quantity`` class, which makes it
incompatible with other high performance packages such as |JAX|.

|Phun|_ solves this problem by enabling *both* writing physics
functions with ``astropy.units`` and currying these functions into
pure functions that can ``jax.jit``.
|Phun|_ provides a standard pattern to implement these functions, as
well as python decorator to transform these physics functions.
|Phun|_ makes writing |JAX| compatible physics aware functions easier.


.. |Astropy| replace:: ``Astropy``
.. |Phun|    replace:: ``Phun``
.. |JAX|     replace:: ``JAX``

.. _Astropy: https://www.astropy.org/
.. _Phun:    https://github.com/adxsrc/phun
.. _JAX:     https://github.com/google/jax
