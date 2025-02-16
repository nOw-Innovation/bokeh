#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2022, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Various kinds of button widgets.

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from typing import TYPE_CHECKING, Callable

# Bokeh imports
from ...core.enums import ButtonType
from ...core.has_props import HasProps, abstract
from ...core.properties import (
    Bool,
    Either,
    Enum,
    Instance,
    List,
    Null,
    Nullable,
    Override,
    String,
    Tuple,
)
from ...events import ButtonClick, MenuItemClick
from ...util.deprecation import deprecated
from ..callbacks import Callback
from .icons import AbstractIcon
from .widget import Widget

if TYPE_CHECKING:
    from ...util.callback_manager import EventCallback

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'AbstractButton',
    'Button',
    'ButtonLike',
    'Dropdown',
    'Toggle',
)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

@abstract
class ButtonLike(HasProps):
    ''' Shared properties for button-like widgets.

    '''

    button_type = Enum(ButtonType, help="""
    A style for the button, signifying it's role.
    """)

@abstract
class AbstractButton(Widget, ButtonLike):
    ''' A base class that defines common properties for all button types.

    '''

    label = String("Button", help="""
    The text label for the button to display.
    """)

    icon = Nullable(Instance(AbstractIcon), help="""
    An optional image appearing to the left of button's text.
    """)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Button(AbstractButton):
    ''' A click button.

    '''

    label = Override(default="Button")

    def on_click(self, handler: EventCallback) -> None:
        ''' Set up a handler for button clicks.

        Args:
            handler (func) : handler function to call when button is clicked.

        Returns:
            None

        '''
        deprecated((3, 0, 0), 'on_click(handler)', 'on_event("button_click", handler)')
        self.on_event(ButtonClick, handler)

    def js_on_click(self, handler: Callback) -> None:
        ''' Set up a JavaScript handler for button clicks. '''
        deprecated((3, 0, 0), 'js_on_click(handler)', 'js_on_event("button_click", handler)')
        self.js_on_event(ButtonClick, handler)

class Toggle(AbstractButton):
    ''' A two-state toggle button.

    '''

    label = Override(default="Toggle")

    active = Bool(False, help="""
    The state of the toggle button.
    """)

    def on_click(self, handler: Callable[[bool], None]) -> None:
        """ Set up a handler for button state changes (clicks).

        Args:
            handler (func) : handler function to call when button is toggled.

        Returns:
            None
        """
        deprecated((3, 0, 0), 'on_click(handler)', 'on_event("button_click", handler)')
        self.on_change('active', lambda attr, old, new: handler(new))

    def js_on_click(self, handler: Callback) -> None:
        """ Set up a JavaScript handler for button state changes (clicks). """
        deprecated((3, 0, 0), 'js_on_click(handler)', 'js_on_event("button_click", handler)')
        self.js_on_change('active', handler)

class Dropdown(AbstractButton):
    ''' A dropdown button.

    '''

    label = Override(default="Dropdown")

    split = Bool(default=False, help="""
    """)

    menu = List(Either(Null, String, Tuple(String, Either(String, Instance(Callback)))), help="""
    Button's dropdown menu consisting of entries containing item's text and
    value name. Use ``None`` as a menu separator.
    """)

    def on_click(self, handler: EventCallback) -> None:
        ''' Set up a handler for button or menu item clicks.

        Args:
            handler (func) : handler function to call when button is activated.

        Returns:
            None

        '''
        deprecated((3, 0, 0), 'on_click(handler)', 'on_event("button_click", handler) OR on_event("menu_item_click", handler)')
        self.on_event(ButtonClick, handler)
        self.on_event(MenuItemClick, handler)

    def js_on_click(self, handler: Callback) -> None:
        ''' Set up a JavaScript handler for button or menu item clicks. '''
        deprecated((3, 0, 0), 'js_on_click(handler)', 'js_on_event("button_click", handler) OR js_on_event("menu_item_click", handler)')
        self.js_on_event(ButtonClick, handler)
        self.js_on_event(MenuItemClick, handler)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
