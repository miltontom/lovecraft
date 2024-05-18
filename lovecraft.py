import configparser
from os.path import join
import os
import shutil
from zipfile import ZipFile
from sys import exit

import click


VERSION = '0.1.0'
CONFIG_FILE_NAME = 'conf.ini'
EXCLUSIONS_FILE_NAME = '.exclude'
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

            files = [f for f in files if not f.startswith(EXCLUSIONS_FILE_NAME) and f != CONFIG_FILE_NAME]
                
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in exclude:
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))


def parse_exclusions(game_source):
    excluded_list = []

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
    game_destination = config['destination']
    game_icon = config['icon']

    love_exe = shutil.which('love')
    if not love_exe:
        print('Error: love.exe is not in PATH')
        return EXIT_FAILURE

    if not os.path.exists(game_destination):
        os.mkdir(game_destination)

    archive_name = f'{join(game_destination, game_name)}.love'
    zip_file(game_source, archive_name, parse_exclusions(game_source))

    exe_name = f'{join(game_destination, game_name)}.exe'
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
    if CONFIG_FILE_NAME not in os.listdir(src): 
        print('No config file found... Using fallback values')

    parser = configparser.ConfigParser()
    parser.read(join(src, CONFIG_FILE_NAME))

    name = parser.get('Game', 'name', fallback=os.path.basename(src)).strip().lower()
    destination = join(
        parser.get('Game', 'destination', fallback=os.getenv('USERPROFILE')),
        name).replace('/', '\\')
    icon = (parser.get('Game', 'icon').replace('/', '\\')
            if parser.has_option('Game', 'icon') else None)

    return {
        'source': src,
        'name': name,
        'destination': destination,
        'icon': icon
    }


def is_love2d_project(src):
    files = os.listdir(src)
    return 'main.lua' in files or 'conf.lua' in files


@click.command()
@click.version_option(VERSION)
@click.argument('src', default='.')
def main(src):
    '''
    Packages LÖVE game for distribution.

    SRC - Path to project directory
    '''
    try:
        src = os.path.abspath(src)
        if not is_love2d_project(src):
            print('Error: Not a LÖVE game project directory')
            exit(EXIT_FAILURE)
        
        config = parse_config(src)
        exit_status = package_game(config)

        if exit_status == EXIT_SUCCESS:
            print(f'\nPackage successfully created at \'{os.path.abspath(config['destination'])}\'')
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
