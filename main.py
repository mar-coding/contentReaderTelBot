from module.BotAPI import BotAPI


def main():
    ba = BotAPI()
    ba.updater.start_polling()


if __name__ == "__main__":
    main()
    print("Bot's Host Started Successfully.")