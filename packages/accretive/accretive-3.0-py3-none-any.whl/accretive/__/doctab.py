# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Docstrings table for reuse across entities. '''

# pylint: disable=unused-wildcard-import,wildcard-import
# ruff: noqa: F403,F405


from __future__ import annotations

from .imports import *


TABLE: types.MappingProxyType[ str, str ] = types.MappingProxyType( {

    'class attributes accretion': '''
Prevents reassignment or deletion of class attributes after they have been
assigned. Only assignment of new class attributes is permitted.
''',

    'description of class factory class': '''
Derived from :py:class:`type`, this is a metaclass. A metaclass is a class
factory class. I.e., it is a class that produces other classes as its
instances.
''',

    'description of module': '''
Derived from :py:class:`types.ModuleType`, this class is suitable for use as a
Python module class.
''',

    'description of namespace': '''
A namespace is an object, whose attributes can be determined from iterables and
keyword arguments, at initialization time. The string representation of the
namespace object reflects its current instance attributes. Modeled after
:py:class:`types.SimpleNamespace`.
''',

    'dictionary entries accretion': '''
Prevents alteration or removal of dictionary entries after they have been
added. Only addition of new dictionary entries is permitted.
''',

    'dictionary entries production': '''
When an attempt to access a missing entry is made, then the entry is added with
a default value. Modeled after :py:class:`collections.defaultdict`.
''',

    'dictionary entries validation': '''
When an attempt to add a new entry is made, then the entry is validated against
supplied criteria. If validation fails, then the entry is rejected.
''',

    'instance attributes accretion': '''
Prevents reassignment or deletion of instance attributes after they have been
assigned. Only assignment of new instance attributes is permitted.
''',

    'module attributes accretion': '''
Prevents reassignment or deletion of module attributes after they have been
assigned. Only assignment of new module attributes is permitted.

This behavior helps ensure that module-level constants remain constant and that
module interfaces remain stable during runtime.
''',

} )
