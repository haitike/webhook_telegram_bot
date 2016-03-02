from dungeon_world.bot import Bot

def main():
    bot = Bot()
    bot.start_webhook_server()

if __name__ == '__main__':
    main()