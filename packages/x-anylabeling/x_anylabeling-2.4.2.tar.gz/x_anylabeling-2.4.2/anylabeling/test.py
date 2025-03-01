from anylabeling.config import get_config
from anylabeling import config as anylabeling_config
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    config_from_args = args.__dict__
    reset_config = config_from_args.pop("reset_config")
    filename = config_from_args.pop("filename")
    output = config_from_args.pop("output")
    config_file_or_yaml = config_from_args.pop("config")
    anylabeling_config.current_config_file = config_file_or_yaml
    config = get_config(config_file_or_yaml, config_from_args)
    # print(URLProvider.get_url()+"/user/login")