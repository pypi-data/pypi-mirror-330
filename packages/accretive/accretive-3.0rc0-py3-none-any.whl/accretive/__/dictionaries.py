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


''' Internal dictionary. '''

# pylint: disable=unused-import
# ruff: noqa: F401


# TODO: Consider a dictionary factory to allow 'mutables' closure
#       to be referenced in the '__setitem__' and '__delitem__' methods.


from __future__ import annotations

from . import imports as __
from . import immutables as _immutables


_H = __.typx.TypeVar( '_H' )
_V = __.typx.TypeVar( '_V' )


class AccretiveDictionary(
    _immutables.ConcealerExtension,
    dict[ _H, _V ],
    __.typx.Generic[ _H, _V ],
):
    ''' Accretive subclass of :py:class:`dict`.

        Can be used as an instance dictionary.

        Prevents attempts to mutate dictionary via inherited interface.
    '''

    def __init__(
        self,
        *iterables: __.DictionaryPositionalArgument[ _H, _V ],
        **entries: __.DictionaryNominativeArgument[ _V ],
    ):
        super( ).__init__( )
        self.update( *iterables, **entries )

    def __delitem__( self, key: _H ) -> None:
        from .exceptions import EntryImmutabilityError
        raise EntryImmutabilityError( key )

    def __setitem__( self, key: _H, value: _V ) -> None:
        from .exceptions import EntryImmutabilityError
        if key in self: raise EntryImmutabilityError( key )
        super( ).__setitem__( key, value )

    def clear( self ) -> __.typx.Never:
        ''' Raises exception. Cannot clear immutable entries. '''
        from .exceptions import OperationInvalidity
        raise OperationInvalidity( 'clear' )

    def copy( self ) -> __.typx.Self:
        ''' Provides fresh copy of dictionary. '''
        return type( self )( self )

    def pop( # pylint: disable=unused-argument
        self, key: _H, default: __.Absential[ _V ] = __.absent
    ) -> __.typx.Never:
        ''' Raises exception. Cannot pop immutable entry. '''
        from .exceptions import OperationInvalidity
        raise OperationInvalidity( 'pop' )

    def popitem( self ) -> __.typx.Never:
        ''' Raises exception. Cannot pop immutable entry. '''
        from .exceptions import OperationInvalidity
        raise OperationInvalidity( 'popitem' )

    def update( # type: ignore
        self,
        *iterables: __.DictionaryPositionalArgument[ _H, _V ],
        **entries: __.DictionaryNominativeArgument[ _V ],
    ) -> None:
        ''' Adds new entries as a batch. '''
        from itertools import chain
        # Add values in order received, enforcing no alteration.
        for indicator, value in chain.from_iterable( map( # type: ignore
            lambda element: ( # pyright: ignore
                element.items( )
                if isinstance( element, __.cabc.Mapping )
                else element
            ),
            ( *iterables, entries )
        ) ): self[ indicator ] = value # type: ignore
