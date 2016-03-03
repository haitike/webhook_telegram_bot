from telegrambot.bot import Bot

def main():
    bot = Bot()
    bot.start_polling_loop()

if __name__ == '__main__':
    main()