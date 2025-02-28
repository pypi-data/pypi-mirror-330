import os
import argparse
import re

from mellerikatedge.edge_app import Emulator
import mellerikatedge.edge_utils as edge_utils

def validate_input(prompt, pattern, error_message):
    while True:
        user_input = input(prompt)
        if re.match(pattern, user_input):
            return user_input
        else:
            print(error_message)

def edge_inference():
    print("Performing edge inference...")

def edge_init():
    current_directory = os.getcwd()
    print(current_directory)

    alo_version = None
    experiments_yaml_path = os.path.join(current_directory, 'experimental_plan.yaml')
    settings_folder_path = os.path.join(current_directory, 'setting')
    infra_config_path = os.path.join(settings_folder_path, 'infra_config.yaml')
    solution_config_path = os.path.join(settings_folder_path, 'solution_info.yaml')

    if os.path.isfile(experiments_yaml_path) and os.path.isdir(settings_folder_path):
        if os.path.isfile(infra_config_path) and os.path.isfile(solution_config_path):
            alo_version = "v3"

    if alo_version is None:
        main_py_path = os.path.join(current_directory, 'main.py')
        register_notebook_path = os.path.join(current_directory, 'register-ai-solution.ipynb')

        if os.path.isfile(main_py_path) and os.path.isfile(register_notebook_path):
            with open(main_py_path, 'r') as file:
                content = file.read()
                if "from src.alo import ALO" in content:
                    alo_version = "v2"

    if alo_version is None:
        print("Please run init in the folder where ALO is executed.")
        return

    edge_serial_name = validate_input(
        "Enter Edge Serial Name (alphanumeric and dashes only): ",
        r'^[a-zA-Z0-9\-]+$',
        "Edge Serial Name must contain only alphanumeric characters and dashes."
    )

    # Edge Conductor 주소 입력 받기 (http 또는 https로 시작)
    edge_conductor_url = validate_input(
        "Enter Edge Conductor Address (e.g., https://edgecond.try-mellerikat.com): ",
        r'^(http|https)://[^\s]+$',
        "Edge Conductor Address must be a valid URL starting with http or https."
    )

    # Edge Conductor 설치 위치 입력 받기 (1 또는 2만 허용)
    edge_conductor_location = validate_input(
        "Enter Edge Conductor Installation Location (1 for Cloud, 2 for On-premise): ",
        r'^[12]$',
        "Installation Location must be 1 (Cloud) or 2 (On-premise)."
    )

    model_info = {
        'model_seq' : None,
        'model_version' : None,
        'stream_name' : None
    }

    # 데이터 저장
    config_data = {
        'solution_dir' : current_directory,
        'alo_version' : alo_version,
        'edge_security_key': edge_serial_name,
        'edge_conductor_url': edge_conductor_url,
        'edge_conductor_location': "cloud" if edge_conductor_location == '1' else "on-premise",
        'model_info' : model_info
    }

    edge_utils.save_yaml('edge_config.yaml', config_data)

    print(f"Configuration file 'edge_config.yaml' created with the following details:")
    print(f"Edge Serial Name: {edge_serial_name}")
    print(f"Edge Conductor URL: {edge_conductor_url}")
    print(f"Edge Conductor Installation Location: {'cloud' if edge_conductor_location == '1' else 'on-premise'}")
    print("Please connect to Edge Conductor and register the Edge.")

def main():
    parser = argparse.ArgumentParser(description="Mellerikat Edge CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_inference = subparsers.add_parser("inference")
    parser_init = subparsers.add_parser("init")

    args = parser.parse_args()

    if args.command == "inference":
        edge_inference()
    elif args.command == "init":
        edge_init()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()