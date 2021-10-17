import logging
import requests

logger = logging.getLogger('aiohttp.server')


def telegram_bot_send_msg(app, bot_msg):
    """Send messages by telegram bot."""
    tg_cfg = app['config'].get('telegram', None)
    if tg_cfg:
        bot_token = tg_cfg.get('bot_token', None)
        bot_chat_id = tg_cfg.get('bot_chat_id', None)

        if bot_token and bot_chat_id:
            try:
                send_text = 'https://api.telegram.org/bot' + str(bot_token) + \
                            '/sendMessage?chat_id=' + str(bot_chat_id) + \
                            '&parse_mode=Markdown&text=' + str(bot_msg)
                response = requests.get(send_text)
                return response.json()
            except requests.ConnectionError as err:
                logger.error(
                    'ConnectionError while sending message: {0}'.format(err)
                )
        else:
            logger.info(
                'The message was not sent. '
                'bot_token or bot_chat_id not specified.'
            )
    else:
        logger.info(
            'The message was not sent. `telegram` config not specified.'
        )
