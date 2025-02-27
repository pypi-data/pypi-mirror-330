import glob
import os
import yaml


def get_data(config):
    try:
        with open(config, 'r') as file:
            config_data = yaml.safe_load(file)

        data_list = [
            config_data['save_location'],
            config_data['save_file'],
            config_data['save_states_dir'],
            config_data['last_loaded']
        ]

    except FileNotFoundError:
        with open('config.yaml', 'w') as file:
            config_data = {
                "last_loaded": "",
                "save_file": "",
                "save_location": "",
                "save_states_dir": ""
            }
            yaml.safe_dump(config_data, file)
            data_list = ['', '', '', '']

    return data_list


def get_data_dict(config):
    try:
        with open(config, 'r') as file:
            config_data = yaml.safe_load(file)

    except FileNotFoundError:
        with open('config.yaml', 'w') as file:
            config_data = {
                "last_loaded": "",
                "save_file": "",
                "save_location": "",
                "save_states_dir": ""
            }
            yaml.safe_dump(config_data, file)

    return config_data


def load_data(config, config_dict):
    with open(config, 'w') as file:
        yaml.safe_dump(config_dict, file)


def load_unique(save_name, parent_dir):
    files_recursive = glob.glob(parent_dir + "**/*", recursive=True)
    target = [True]

    for file in files_recursive:
        if save_name.lower() in file.lower():
            target.append(file)

    if len(target) > 2:
        target = [False, True]

    elif len(target) == 1:
        target = [False, False]

    return target


def list_files(dir, show_ext):
    # Remove trailing slash, if necessary
    norm_path = os.path.normpath(dir)

    # Find the base directory in path
    path_base = os.path.basename(norm_path)

    # If dir is the parent directory for save states, remove the '/'
    if path_base == '':
        path_base = dir.replace('/', '')

    string_list = [path_base]
    list_dir = os.listdir(dir)

    for files in list_dir:
        full_path = f'{dir}/{files}'

        if os.path.isdir(full_path):
            # Recursion: Append each line of the string given by function evaluated
            # at the subdirectory
            for line in list_files(full_path, show_ext).splitlines():
                string_list.append(line)

        else:
            if show_ext:
                string_list.append(files)
            else:
                file_and_ext = os.path.splitext(files)
                string_list.append(file_and_ext[0])

    for i in range(1, len(string_list)):
        tree_chars = ['├──', '└──', '│']

        if i != len(string_list) - 1:
            # If the first 3 non-blank characters of the string are in tree_chars,
            # add a vertical pipe
            if string_list[i].strip()[:3].strip() in tree_chars:
                string_list[i] = f'│   {string_list[i]}'

            else:
                string_list[i] = f'├── {string_list[i]}'

        elif i == len(string_list) - 1:
            if string_list[i].strip()[:3].strip() in tree_chars:
                string_list[i] = f'└── {string_list[i]}'

            else:
                string_list[i] = f'└── {string_list[i]}'

    file_string = '\n'.join(string_list)

    return file_string
