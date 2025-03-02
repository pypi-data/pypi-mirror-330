.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+

*******************************************************************************
                                  accretive
*******************************************************************************

.. image:: https://img.shields.io/pypi/v/accretive
   :alt: Package Version
   :target: https://pypi.org/project/accretive/

.. image:: https://img.shields.io/pypi/status/accretive
   :alt: PyPI - Status
   :target: https://pypi.org/project/accretive/

.. image:: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml/badge.svg?branch=master&event=push
   :alt: Tests Status
   :target: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml

.. image:: https://emcd.github.io/python-accretive/coverage.svg
   :alt: Code Coverage Percentage
   :target: https://github.com/emcd/python-accretive/actions/workflows/tester.yaml

.. image:: https://img.shields.io/github/license/emcd/python-accretive
   :alt: Project License
   :target: https://github.com/emcd/python-accretive/blob/master/LICENSE.txt

.. image:: https://img.shields.io/pypi/pyversions/accretive
   :alt: Python Versions
   :target: https://pypi.org/project/accretive/


🌌 A Python library package which provides **accretive data structures** -
collections which can grow but never shrink.


Key Features ⭐
===============================================================================

* 📖 **Accretive Dictionary**: Like a regular `dict
  <https://docs.python.org/3/library/stdtypes.html#dict>`_, but entries cannot
  be modified or removed once added. Also has variants with defaults and
  validation.
* 🗃️ **Accretive Namespace**: Similar to `SimpleNamespace
  <https://docs.python.org/3/library/types.html#types.SimpleNamespace>`_, but
  attributes become immutable after assignment.
* 🧱 **Additional Types**: Classes (including abstract base classes), modules,
  and objects with accretive behavior.
* 🏗️ **Flexible Initialization**: Support for unprotected attributes during
  initialization; useful for compatibility with class decorators, such as
  `dataclasses
  <https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass>`_.


Note on Immutability 📢
===============================================================================

   Enforcement of immutability is quite difficult in Python. While this library
   encourages immutability by default, it can be circumvented by anyone who has
   intermediate knowledge of Python machinery and who is determined to
   circumvent the immutability. Use the library in the spirit of making
   programs safer, but understand that it cannot truly prevent unwanted state
   tampering.


Installation 📦
===============================================================================

::

    pip install accretive


Examples 💡
===============================================================================


Accretive Namespace 🗃️
-------------------------------------------------------------------------------

An accretive namespace, similar to ``types.SimpleNamespace``, is available.
This namespace can be initialized from multiple iterables and from keyword
arguments. (Keyword arguments shown below; see documentation for additional
forms of initialization.)

>>> from accretive import Namespace
>>> ns = Namespace( apples = 12, bananas = 6 )
>>> ns.cherries = 42  # ✅ Allows new attributes.
>>> ns.apples = 14    # ❌ Attempted reassignment raises error.
Traceback (most recent call last):
...
accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'apples'.
>>> del ns.apples     # ❌ Attempted deletion raises error.
Traceback (most recent call last):
...
accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'apples'.
>>> ns
accretive.namespaces.Namespace( apples = 12, bananas = 6, cherries = 42 )


Accretive Dictionary 📖
-------------------------------------------------------------------------------

An accretive dictionary, similar to ``dict``, is available. This dictionary can
be initialized from multiple iterables and from keyword arguments. (Keyword
arguments shown below; see documentation for additional forms of
initialization.)

>>> from accretive import Dictionary
>>> dct = Dictionary( apples = 12, bananas = 6 )
>>> dct[ 'cherries' ] = 42  # ✅ Allows new entries.
>>> dct.update( blueberries = 96, strawberries = 24 )
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )
>>> dct[ 'bananas' ] = 11   # ❌ Attempted alteration raises error.
Traceback (most recent call last):
...
accretive.exceptions.EntryImmutabilityError: Cannot alter or remove existing entry for 'bananas'.
>>> del dct[ 'bananas' ]    # ❌ Attempted removal raises error.
Traceback (most recent call last):
...
accretive.exceptions.EntryImmutabilityError: Cannot alter or remove existing entry for 'bananas'.
>>> dct
accretive.dictionaries.Dictionary( {'apples': 12, 'bananas': 6, 'cherries': 42, 'blueberries': 96, 'strawberries': 24} )


Accretive Objects 🧱
-------------------------------------------------------------------------------

The ``accretive`` decorator can be applied to any class to make its instances enforce attribute immutability after assignment.

>>> from accretive import accretive
>>> @accretive
... class Config:
...     def __init__( self, debug = False ):
...         self.debug = debug
...
>>> config = Config( debug = True )
>>> config.verbose = True  # ✅ Allows new attributes
>>> config.debug = False   # ❌ Attempted reassignment raises error
Traceback (most recent call last):
...
accretive.exceptions.AttributeImmutabilityError: Cannot reassign or delete existing attribute 'debug'.


Use Cases 🎯
===============================================================================

* 📝 **Configuration Registries**: Registries which can accumulate entries but
  never remove them, thereby guaranteeing sticky state.
* 🔌 **Plugin Systems**: Register extensions which are then guaranteed to be
  available from the time of registration to the end of the process.
* 🔒 **Immutable Collections**: Many scenarios requiring grow-only collections
  with immutability guarantees.


`More Flair <https://www.imdb.com/title/tt0151804/characters/nm0431918>`_
===============================================================================

.. image:: https://img.shields.io/github/last-commit/emcd/python-accretive
   :alt: GitHub last commit
   :target: https://github.com/emcd/python-accretive

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json
   :alt: Copier
   :target: https://github.com/copier-org/copier

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
   :alt: Hatch
   :target: https://github.com/pypa/hatch

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :alt: pre-commit
   :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
   :alt: Bandit
   :target: https://github.com/PyCQA/bandit

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
   :alt: Pylint
   :target: https://github.com/pylint-dev/pylint

.. image:: https://microsoft.github.io/pyright/img/pyright_badge.svg
   :alt: Pyright
   :target: https://microsoft.github.io/pyright

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :alt: Ruff
   :target: https://github.com/astral-sh/ruff

.. image:: https://img.shields.io/pypi/implementation/accretive
   :alt: PyPI - Implementation
   :target: https://pypi.org/project/accretive/

.. image:: https://img.shields.io/pypi/wheel/accretive
   :alt: PyPI - Wheel
   :target: https://pypi.org/project/accretive/
