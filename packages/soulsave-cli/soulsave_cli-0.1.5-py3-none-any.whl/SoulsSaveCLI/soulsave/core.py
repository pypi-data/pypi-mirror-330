import click
import os
import shutil
import yaml
from SoulsSaveCLI.utils import callbacks
from SoulsSaveCLI.utils import side_functions


@click.command()
@click.option(
    '--save',
    prompt="Enter the path to the game's save file",
    help="Path to game's save file",
    type=click.Path(exists=True, resolve_path=True)
)
@click.option(
    '--states',
    prompt="Enter the location to store your save states",
    default="SaveStates/",
    help="Path to directory to store save states",
    type=click.Path(exists=True, resolve_path=True)
)
def init(save, states):

    """Generate configuration file"""

    config_data = side_functions.get_data_dict('config.yaml')
    save_name = os.path.basename(save)
    game = os.path.normpath(os.path.dirname(save)) + '/'
    states = os.path.normpath(states) + '/'

    config_data['save_location'] = game
    config_data['save_file'] = save_name
    config_data['save_states_dir'] = states

    side_functions.load_data('config.yaml', config_data)
    click.echo("Successfully created file 'config.yaml'")


@click.command()
@click.option(
    '-v',
    '--verbose',
    default=False,
    is_flag=True,
    help="Show file extensions"
)
@click.argument('subdir', required=False)
def list(subdir, verbose):

    """
    List files in save states directory\n
    Use 'soulsave list SUBDIR' to list the files in the subdirectory SUBDIR\n
    Execute 'soulsave list' for all files in save states directory
    """

    try:
        config_data = side_functions.get_data('config.yaml')

    except (FileNotFoundError, KeyError, TypeError):
        click.echo(
            "File 'config.yaml' does not exist or was not created properly. "
            "Use 'soulsave init' to create the file."
        )
        quit()

    root = config_data[2]

    if subdir:
        full_path = root + str(subdir) + '/'

        # If the directory exists and is a child of SaveStates/
        if os.path.isdir(full_path) and subdir in os.listdir(root):
            click.echo(side_functions.list_files(full_path, verbose))

        else:
            click.echo(
                f"Directory '{subdir}' does not exist in '{root}'\n"
                "Use 'soulsave list' to list available options"
            )
            quit()

    else:
        click.echo(side_functions.list_files(root, verbose))


@click.command()
@click.argument('subdir')
def new(subdir):

    """Create a new subdirectory in your save states directory"""

    try:
        config_data = side_functions.get_data('config.yaml')

    except (FileNotFoundError, KeyError, TypeError):
        click.echo(
            "File 'config.yaml' does not exist or was not created properly. "
            "Use 'soulsave init' to create the file."
        )
        quit()

    new_path = f'{config_data[2]}{subdir}/'
    new_real_path = os.path.realpath(f'{config_data[2]}{subdir}/')
    root_real_path = os.path.realpath(config_data[2])

    if not new_real_path.startswith(root_real_path):
        click.echo(
            f"Directory '{subdir}' does not exist in {config_data[2]}.\n"
            "Use 'soulsave list' to list available options"
        )
        quit()

    elif not os.path.isdir(new_path):
        os.makedirs(new_path)
        click.echo(f"Successfully created '{new_path}'")

    else:
        click.echo(f"'{new_path}' already exists!")
        quit()


@click.command()
@click.argument('save_name')
@click.argument('subdir', required=False)
def add(save_name, subdir):

    """
    Create a save state\n
    Add a savestate to the specified subdirectory or do not specify subdirectory
    to add the save state to the root of the save states directory
    """

    try:
        config_data = side_functions.get_data('config.yaml')

    except (FileNotFoundError, KeyError, TypeError):
        click.echo(
            "File 'config.yaml' does not exist or was not created properly. "
            "Use 'soulsave init' to create the file."
        )
        quit()

    file_data = os.path.splitext(config_data[1])
    file_ext = file_data[1]

    org = config_data[0] + config_data[1]

    if subdir:
        dest = f"{config_data[2]}{subdir}/{save_name}{file_ext}"
    else:
        dest = f"{config_data[2]}{save_name}{file_ext}"

    if os.path.isfile(dest):
        if subdir:
            click.echo(
                f"'{subdir}/{save_name}' already exists! Please choose a "
                "different name"
            )
            quit()
        else:
            click.echo(
                f"'{config_data[2]}{save_name}' already exists! Please choose a "
                "different name"
            )
            quit()

    elif not os.path.isfile(org):
        click.echo(
            f"'{org}' does not exist. Please review the game save location in "
            "config.yaml or set the value with 'soulsave init'"
        )
        quit()

    elif not os.path.isdir(f"{config_data[2]}{subdir}/") and subdir:
        click.echo(
            f"'{config_data[2]}{subdir}/' does not exist. Use 'soulsave list' "
            "to list available save state subdirectories"
        )
        quit()

    else:
        if subdir:
            if subdir + '/' == config_data[2]:
                full_path = config_data[2]

            else:
                full_path = config_data[2] + subdir

            if not (os.path.isdir(full_path)
                    and subdir in os.listdir(config_data[2])):
                if subdir + '/' == config_data[2]:
                    pass
                else:
                    click.echo(
                        f"Directory '{subdir}' does not exist in {config_data[2]}.\n"
                        "Use 'soulsave list' to list available options"
                    )
                    quit()

        shutil.copyfile(org, dest)

        if subdir:
            click.echo(f"Successfully created save '{subdir}/{save_name}'")
        else:
            click.echo(f"Successfully created save '{config_data[2]}{save_name}'")


@click.command()
@click.option(
    '-l',
    '--last',
    is_flag=True,
    callback=callbacks.load_last,
    expose_value=False,
    is_eager=True,
    help="Reload the last loaded save file"
)
@click.argument('save_name')
@click.argument('subdir', required=False)
def load(save_name, subdir):

    """
    Load save state

    Loads the specified save file from the specified subdirectory. If SAVE_NAME
    is unique you can execute 'soulsave load SAVE_NAME' to load the save state.

    If X is a unique substring of SAVE_NAME, you can also load the save state
    with 'soulsave load X'
    """

    try:
        config_data = side_functions.get_data_dict('config.yaml')
        config_data_list = side_functions.get_data('config.yaml')

    except (FileNotFoundError, KeyError, TypeError):
        click.echo(
            "File 'config.yaml' does not exist or was not created properly. "
            "Use 'soulsave init' to create the file."
        )
        quit()

    if subdir:
        file_data = os.path.splitext(config_data_list[1])
        file_ext = file_data[1]

        org = f"{config_data_list[2]}{subdir}/{save_name}{file_ext}"
        dest = config_data_list[0] + config_data_list[1]

        if not os.path.isfile(org):
            click.echo(
                f"'{org}' does not exist. Use 'soulsave list' to list\n"
                "available options"
            )
            quit()

        elif not os.path.isfile(dest):
            click.echo(
                f"'{dest}' does not exist. Please review the game save location\n"
                "in config.yaml or set the value with 'soulsave init'"
            )
            quit()

        else:
            shutil.copyfile(org, dest)

            config_data["last_loaded"] = org
            side_functions.load_data('config.yaml', config_data)
            click.echo(f"Successfully loaded {org}")

    else:
        test_unique = side_functions.load_unique(save_name, config_data_list[2])

        if test_unique[0]:
            save_name = test_unique[1]
            org = f"{save_name}"
            dest = config_data_list[0] + config_data_list[1]


            if not os.path.isfile(save_name):
                click.echo(
                    f"{save_name} is a directory, not a save file name.\n"
                    "Use 'soulsave list' for a list of available options or use "
                    "'soulsave --help' for more information on how to use the "
                    "command"
                )
                quit()

            else:
                shutil.copyfile(org, dest)

        elif test_unique[1]:
            click.echo(
                "Save name is not unique; please include the subdirectory "
                "name to load"
            )
            quit()

        else:
            click.echo(
                "Save name does not exist; please try again or use 'soulsave list' "
                "to check available save states"
            )
            quit()

        config_data["last_loaded"] = org
        side_functions.load_data('config.yaml', config_data)
        click.echo(f"Successfully loaded {test_unique[1]}")


@click.command()
@click.argument('parent_dir')
@click.argument('save_name', required=False)
def rm(parent_dir, save_name):

    """
    Delete specified save file or subdirectory\n
    To delete an entire directory, do not enter a save name\n
    To delete a single save file, provide its parent directory and the save file
    name\n
    To delete a single save file in the root directory, you may either enter the
    path to the save states directory or use 'root' as an alias (if you are
    using the default save states directory 'SaveStates/', you can just type
    'SaveStates')
    """

    try:
        config_data = side_functions.get_data('config.yaml')

    except (FileNotFoundError, KeyError, TypeError):
        click.echo(
            "File 'config.yaml' does not exist or was not created properly. "
            "Use 'soulsave init' to create the file."
        )
        quit()

    file_data = os.path.splitext(config_data[1])
    file_ext = file_data[1]

    if parent_dir == "root":
        parent_dir = config_data[2][:-1]

    if parent_dir + '/' == config_data[2]:
        full_path = config_data[2]

    else:
        full_path = config_data[2] + parent_dir

    if not (os.path.isdir(full_path) and parent_dir in os.listdir(config_data[2])):
        if parent_dir + '/' == config_data[2] and save_name:
            pass
        else:
            click.echo(
                f"Directory '{parent_dir}' does not exist in {config_data[2]}.\n"
                "Use 'soulsave list' to list available options"
            )
            quit()

    if parent_dir + '/' == config_data[2]:
        full_file_path = f'{config_data[2]}/{save_name}{file_ext}'
        full_dir_path = f'{config_data[2]}'

    else:
        full_file_path = f'{config_data[2]}{parent_dir}/{save_name}{file_ext}'
        full_dir_path = f'{config_data[2]}{parent_dir}'

    if save_name:
        if not os.path.isfile(full_file_path):
            click.echo(
                f"'{full_file_path}' does not exist. Please try again or use "
                "'soulsave list' to review the contents of your save "
                "states directory."
            )
        else:
            if parent_dir == config_data[2]:
                click.confirm(
                    f"Are you sure you want to delete {parent_dir}{save_name}?",
                    abort=True
                )
                os.remove(full_file_path)
                click.echo(f"Successfully removed {parent_dir}{save_name}{file_ext}")
            else:
                click.confirm(
                    f"Are you sure you want to delete {parent_dir}/{save_name}?",
                    abort=True
                )
                os.remove(full_file_path)
                click.echo(
                    f"Successfully removed {parent_dir}/{save_name}{file_ext}"
                )
    else:
        if not os.path.isdir(full_dir_path):
            click.echo(
                f"'{full_dir_path}' does not exist. Please try again or use "
                "'soulsave list' to review the contents of your save"
                "state directory."
            )
        else:
            click.echo(side_functions.list_files(full_dir_path, True))
            click.confirm(
                f"Are you sure you want to delete {parent_dir}? "
                "This will erase all of its contents!",
                abort=True
            )
            shutil.rmtree(full_dir_path)
            click.echo(f"\nSuccessfully removed directory {parent_dir}")
