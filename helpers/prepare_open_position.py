from services.binance.send_request import SendRequest as SendRequestBinance


class PrepareOpenPosition:
    def __init__(self, broker_name: str, coin_name: str, telegram_id: str, clear: bool = False):
        self.broker_name = broker_name
        self.coin_name = coin_name
        self.telegram_id = telegram_id
        self.clear = clear

    def clear_broker_positions(self):
        if self.broker_name == 'binance':
            check, status_code, message, start, end = SendRequestBinance().get_all_position()
            if check:
                if message['symbol'] == self.coin_name:
                    check = SendRequestBinance().create_market_position(self.coin_name, message['positionAmt'])
                    if check:
                        return True, "clear broker successful"
                    else:
                        return False, "can't market last position"

            else:
                return False, "can't get data for clear"

    def change_leverage(self, leverage: int):
        if self.broker_name == 'binance':
            check, status_code, message, start, end = SendRequestBinance().change_leverage(leverage, self.coin_name)
            if check:
                return True, "change leverage was successful"
            else:
                return False, "can't change leverage"

    def change_margin_type(self, margin_type: str):
        if self.broker_name == 'binance':
            check, status_code, message, start, end = SendRequestBinance().change_margin_type(self.coin_name,
                                                                                              margin_type)
            if check:
                return True, "change margin was successful"
            else:
                return False, "can't change margin"

    def prepare_open_position(self, leverage: int, margin_type: str):
        if self.clear:
            check, message = self.clear_broker_positions()
            if not check:
                return check, message
        check, message = self.change_leverage(leverage)
        if not check:
            return check, message
        check, message = self.change_margin_type(margin_type)
        if not check:
            return check, message
        return True, ""
