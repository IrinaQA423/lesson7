import ptbot
from pytimeparse import parse
import os
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=12,
                       fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, text, bot):
    bot.create_timer(parse(text), lambda: notify_progress(secs_left, text, bot))
   

def say_hello(chat_id, text, bot):
    secs_left = parse(text)
    total_time = secs_left
    message_id = bot.send_message(chat_id, "Запускаю таймер")
    bot.create_countdown(secs_left, notify, chat_id=chat_id,
                         message_id=message_id, total_time=total_time, bot=bot)


def notify(secs_left, chat_id, message_id, total_time, bot):
    progress = total_time - secs_left
    progressbar = render_progressbar(total_time, progress)
    bot.update_message(chat_id, message_id,
                       f"{progressbar} \nОсталось {secs_left} секунд.")
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло!")


def main():
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')

    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(say_hello, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()