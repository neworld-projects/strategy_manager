from services.telegram.send_message import send_message


def create_key(key: str, message_mode: str) -> str:
    if message_mode == 'html':
        return f'<em><b>{key.replace("_", " ")}:</b></em>\n'


def create_value(value: dict or str, message_mode: str) -> str:
    if type(value) == dict:
        return convert_dict_to_str(value, message_mode)
    else:
        if message_mode == 'html':
            return f'{value}\n'


def convert_dict_to_str(message: dict, message_mode: str) -> str:
    str_message = ""
    for key, value in message.items():
        str_message += create_key(key, message_mode) + create_value(value, message_mode)
    return str_message


def third_party_call(message: dict, target: str, message_mode: str = 'html', *args, **kwargs) -> None:
    str_message = convert_dict_to_str(message, message_mode)
    globals()[target](str_message, **kwargs)


def telegram_sender(message: str, *args, **kwargs) -> None:
    send_message(kwargs['chat_id'], message)
