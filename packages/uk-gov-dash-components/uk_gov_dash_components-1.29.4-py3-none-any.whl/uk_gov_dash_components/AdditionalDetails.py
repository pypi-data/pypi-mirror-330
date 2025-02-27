# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AdditionalDetails(Component):
    """An AdditionalDetails component.


Keyword arguments:

- id (string; required):
    Id of component.

- detailsText (string; default "Add details text"):
    Detailed text to be shown when expanded.

- hidden (boolean; default False):
    Whether the component renders or not.

- summaryText (string; default "Add summary text"):
    Text to be shown as a summary."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'uk_gov_dash_components'
    _type = 'AdditionalDetails'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, summaryText=Component.UNDEFINED, detailsText=Component.UNDEFINED, hidden=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'detailsText', 'hidden', 'summaryText']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'detailsText', 'hidden', 'summaryText']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(AdditionalDetails, self).__init__(**args)
