import json
import os
import config
from constants import CONFIG_FILE

# Check if config file exists, load it, if not, create it
def check_config_file():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config.config_data = json.load(file)
    else:
        with open(CONFIG_FILE, "w") as file:
            json.dump(config.config_data, file, indent=0)


if __name__ == "__main__":
    check_config_file()
    print(config.config_data)
