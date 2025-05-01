from config_json import check_config_file
from main_ui import show_main_ui


def main():
    check_config_file()
    show_main_ui()


if __name__ == "__main__":
    main()
