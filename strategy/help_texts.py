import json

from strategy.enums import PositionKeys

strategy_model_help_text = \
    'you can add bellow keys\n  {}\nuse like this format {} \nif has many use number in key'.format(
        "\n   ".join(PositionKeys.values),
        json.dumps({'0': "open_position_value"})
    )
