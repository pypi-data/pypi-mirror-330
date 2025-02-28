from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for inputs that expect a .wea file as the recipe input."""
wea_input = [
    InputAlias.any(
        name='wea',
        description='A Wea object produced from the Wea components that are under '
        'the Light Sources tab. This can also be the path to a .wea or a .epw file.',
        platform=['grasshopper', 'revit'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.wea',
                function='wea_handler'
            )
        ]
    ),
    InputAlias.linked(
        name='wea',
        description='A Wea object produced from the Wea components that are under '
        'the Light Sources tab. This can also be the path to a .wea or a .epw file.',
        platform=['rhino'],
        handler=[
            IOAliasHandler(
                language='csharp',
                module='Pollination.RhinoHandlers',
                function='RhinoModelProjectInfoWeather'
            )
        ]
    )
]


"""Alias for inputs that expect a .wea file at a timestep of 1."""
wea_input_timestep_check = [
    InputAlias.any(
        name='wea',
        description='A Wea object produced from the Wea components that are under '
        'the Light Sources tab. This can also be the path to a .wea or a .epw file.',
        platform=['grasshopper', 'rhino', 'revit'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.wea',
                function='wea_handler_timestep_check'
            )
        ]
    )
]


"""Alias for inputs that expect a .wea file at a timestep of 1 and annual data."""
wea_input_timestep_annual_check = [
    InputAlias.any(
        name='wea',
        description='A Wea object produced from the Wea components that are under '
        'the Light Sources tab. This can also be the path to a .wea or a .epw file.',
        platform=['grasshopper', 'rhino', 'revit'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.wea',
                function='wea_handler_timestep_annual_check'
            )
        ]
    )
]
