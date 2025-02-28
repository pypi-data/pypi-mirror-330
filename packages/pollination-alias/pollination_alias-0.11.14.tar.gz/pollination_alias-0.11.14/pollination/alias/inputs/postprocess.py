from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for custom grid metrics used in post-processing."""
grid_metrics_input = [
    InputAlias.any(
        name='grid_metrics',
        description='A JSON file with custom metrics. This can also be a '
        'string or a list of grid metrics.',
        optional=True,
        platform=['grasshopper', 'rhino', 'revit'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.postprocess',
                function='grid_metrics'
            )
        ]
    )
]
