# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AutoComplete(Component):
    """An AutoComplete component.
Lazy loaded Autocomplete

@param {
	id,
	autoselect,
	cssNamespace,
	defaultValue,
	displayMenu,
	minLength,
	name,
	placeholder,
	onConfirm,
	confirmOnBlur,
	showNoOptionsFound,
	showAllValues,
	required,
	tNoResults,
	tAssistiveHint,
	source,
	templates,
	dropdownArrow: dropdownArrowFactory,
	tStatusQueryTooShort,
	tStatusNoResults,
	tStatusSelectedOption,
	tStatusResults,
	style,
 errorMessage,
 errorMessageWhenEmpty,
 menu_open, 
 showOptionHeadings
} [props={}]
@return {*}

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- alwaysDisplayArrow (boolean; default True):
    alwaysDisplayArrow.

- ariaLabelledBy (string; optional):
    This is the ID for the label field.

- autoselect (boolean; default False):
    Should auto select.

- confirmOnBlur (boolean; default True):
    No Description.

- cssNamespace (string; default 'autocomplete'):
    cssNamespace.

- displayMenu (string; default 'inline'):
    No Description.

- dropdownArrow (boolean | number | string | dict | list; default DropdownArrowDown):
    React component for dropdown arrow.

- errorMessage (string; default 'Invalid value entered'):
    Error message to display when invalid input entered in dropdown.

- errorMessageWhenEmpty (boolean; default False):
    Whether to display error message when query is empty in dropdown.

- menu_open (boolean; default False):
    Whether the dropdown menu is open. Used to fire a callback   when
    the menu is opened.

- minLength (number; default 0):
    No Description.

- name (string; default 'input-autocomplete'):
    No Description.

- placeholder (string; default ''):
    No Description.

- required (boolean; default False):
    No Description.

- selectElement (boolean | number | string | dict | list; optional):
    Accessible element.

- showAllValues (boolean; default False):
    No Description.

- showNoOptionsFound (boolean; default True):
    No Description.

- showOptionHeadings (boolean; default False):
    Whether the list of autocomplete options contains headings that
    are unclickable (like when disabled) but not struckthrough and
    bolded.

- source (boolean | number | string | dict | list; optional):
    No Description.

- style (boolean | number | string | dict | list; optional):
    Override the css style of the wrapper.

- tStatusNoResults (boolean | number | string | dict | list; optional):
    No Description.

- tStatusResults (boolean | number | string | dict | list; optional):
    No Description.

- templates (boolean | number | string | dict | list; optional):
    No Description.

- value (string; default ''):
    The value displayed in the input.

- wrapperRef (boolean | number | string | dict | list; optional):
    wrapperRef."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'uk_gov_dash_components'
    _type = 'AutoComplete'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, autoselect=Component.UNDEFINED, cssNamespace=Component.UNDEFINED, displayMenu=Component.UNDEFINED, minLength=Component.UNDEFINED, name=Component.UNDEFINED, placeholder=Component.UNDEFINED, onConfirm=Component.UNDEFINED, confirmOnBlur=Component.UNDEFINED, showNoOptionsFound=Component.UNDEFINED, showAllValues=Component.UNDEFINED, required=Component.UNDEFINED, tNoResults=Component.UNDEFINED, tAssistiveHint=Component.UNDEFINED, source=Component.UNDEFINED, templates=Component.UNDEFINED, tStatusQueryTooShort=Component.UNDEFINED, tStatusNoResults=Component.UNDEFINED, tStatusSelectedOption=Component.UNDEFINED, tStatusResults=Component.UNDEFINED, dropdownArrow=Component.UNDEFINED, selectElement=Component.UNDEFINED, value=Component.UNDEFINED, alwaysDisplayArrow=Component.UNDEFINED, wrapperRef=Component.UNDEFINED, style=Component.UNDEFINED, errorMessage=Component.UNDEFINED, errorMessageWhenEmpty=Component.UNDEFINED, menu_open=Component.UNDEFINED, showOptionHeadings=Component.UNDEFINED, ariaLabelledBy=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'alwaysDisplayArrow', 'ariaLabelledBy', 'autoselect', 'confirmOnBlur', 'cssNamespace', 'displayMenu', 'dropdownArrow', 'errorMessage', 'errorMessageWhenEmpty', 'menu_open', 'minLength', 'name', 'placeholder', 'required', 'selectElement', 'showAllValues', 'showNoOptionsFound', 'showOptionHeadings', 'source', 'style', 'tStatusNoResults', 'tStatusResults', 'templates', 'value', 'wrapperRef']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alwaysDisplayArrow', 'ariaLabelledBy', 'autoselect', 'confirmOnBlur', 'cssNamespace', 'displayMenu', 'dropdownArrow', 'errorMessage', 'errorMessageWhenEmpty', 'menu_open', 'minLength', 'name', 'placeholder', 'required', 'selectElement', 'showAllValues', 'showNoOptionsFound', 'showOptionHeadings', 'source', 'style', 'tStatusNoResults', 'tStatusResults', 'templates', 'value', 'wrapperRef']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AutoComplete, self).__init__(**args)
