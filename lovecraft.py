import configparser
from os.path import join, normpath, isabs
import os
import shutil
from zipfile import ZipFile
from sys import exit

import click


VERSION = '0.2.0'
CONFIG_FILE_NAME = 'craft.ini'
EXCLUSIONS_FILE_NAME = '.exclude'
CRAFTS_DIR = join(os.getenv('USERPROFILE'), 'crafts')
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def set_icon(exe, icon):
    if icon is None:
        return
    
    if not os.path.exists(icon) or not icon.endswith('.ico'):
        print('Error: The icon file does not exist or is not an .ico file')
        return
    
    rh_exe = shutil.which('ResourceHacker')
    if not rh_exe:
        print('Error: ResourceHacker.exe not found in PATH')
        return

    # ICONGROUP - Resource type
    # 1 - Resource name
    os.system((
        f'"{rh_exe}" -open {exe} -action modify -mask ICONGROUP,1, '
        f'-resource {icon} -save {exe} -log NUL'
    ))


def zip_file(folder_path, output_path, exclude=[]):
    with ZipFile(output_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            dirs_to_exclude = [d for d in dirs if join(root, d) in exclude]
            for dir_to_exclude in dirs_to_exclude:
                dirs.remove(dir_to_exclude)

            files = [f for f in files if f not in exclude]
                
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in exclude:
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))


def parse_exclusions(game_source):
    # files to be excluded by default
    excluded_list = [EXCLUSIONS_FILE_NAME, CONFIG_FILE_NAME]

    if EXCLUSIONS_FILE_NAME not in os.listdir(game_source):
        return excluded_list

    with open(join(game_source, EXCLUSIONS_FILE_NAME)) as f:
        lines = f.readlines()
        for line in lines:
            pattern = join(game_source, line.rstrip())
            excluded_list.append(pattern)

    return excluded_list


def package_game(config):
    game_name = config['name']
    game_source = config['source']
    game_destination = join(CRAFTS_DIR, game_name)
    game_icon = config['icon']

    love_exe = shutil.which('love')
    if not love_exe:
        print('Error: love.exe is not in PATH')
        return EXIT_FAILURE

    if not os.path.exists(CRAFTS_DIR):
        os.mkdir(CRAFTS_DIR)
    
    # paths are case insensitive in Windows
    if os.path.exists(game_destination):
        shutil.rmtree(game_destination)

    if not os.path.exists(game_destination):
        os.mkdir(game_destination)

    archive_name = f'{join(game_destination, game_name)}.love'
    excluded_list = parse_exclusions(game_source)
    zip_file(game_source, archive_name, excluded_list)

    exe_name = f'{join(game_destination, game_name.lower())}.exe'
    os.system(f'copy /b "{love_exe}" + {archive_name} {exe_name} > NUL')
    os.remove(archive_name)

    love_path = os.path.dirname(love_exe) # type: ignore
    files = os.listdir(love_path)
    dll_files = [file for file in files if file.endswith('.dll')]
    for dll_file in dll_files:
        shutil.copy(join(love_path, dll_file), game_destination)
    shutil.copy(join(love_path, 'license.txt'), game_destination)

    set_icon(exe_name, game_icon)

    return EXIT_SUCCESS


def parse_config(src):
    fallbacks = {
        'source': src,
        'name': os.path.basename(src),
        'icon': None
    }

    if CONFIG_FILE_NAME not in os.listdir(src): 
        print('No config file found... Using fallback values')
        return fallbacks

    parser = configparser.ConfigParser()
    parser.read(join(src, CONFIG_FILE_NAME))

    name = parser.get('Game', 'name', fallback=fallbacks['name'])
    icon = parser.get('Game', 'icon', fallback=fallbacks['icon'])
    if icon and not isabs(icon):
        icon = join(src, icon)

    return {
        'source': src,
        'name': name,
        'icon': normpath(icon) if icon else None
    }


def is_love2d_project(src):
    files = os.listdir(src)
    return 'main.lua' in files or 'conf.lua' in files


@click.command()
@click.option('--name', '-n', help='Name for the game.')
@click.option('--icon', '-i', help='Path to \'.ico\' file.', type=click.Path())
@click.option('--crafts-dir', is_flag = True, help='Show the packaging location and exit.')
@click.version_option(VERSION)
@click.argument('src', default='.')
def main(src, name, icon, crafts_dir):
    '''
    Packages LÖVE game for distribution.

    SRC - Path to project directory
    '''
    try:
        if crafts_dir:
            print(CRAFTS_DIR)
            exit(EXIT_SUCCESS)

        src = os.path.abspath(src)
        if not is_love2d_project(src):
            print('Error: Not a LÖVE game project directory')
            exit(EXIT_FAILURE)

        if name or icon:
            config = {'source': src, 'name': name, 'icon': icon}
        else:
            config = parse_config(src)

        exit_status = package_game(config)
        if exit_status == EXIT_SUCCESS:
            print(f'Package successfully created at \'{join(CRAFTS_DIR, config['name'])}\'')
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
