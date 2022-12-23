import logging

from celery import shared_task

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


@shared_task
def third_party_manager(message: dict, target: str, requeue=False, message_mode='html', *args, **kwargs) -> None:
    str_message = convert_dict_to_str(message, message_mode)
    try:
        globals()[target](str_message, **kwargs)
    except Exception as e:
        logging.error(e)
        if requeue:
            third_party_manager.apply_async(
                args=(message, target, False, message_mode),
                kwargs=kwargs
            )


def telegram_sender(message: str, *args, **kwargs) -> None:
    send_message(kwargs['chat_id'], message)
