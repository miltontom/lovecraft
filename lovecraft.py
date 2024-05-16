import configparser
from os.path import join
import os
import shutil
from zipfile import ZipFile
from sys import exit

import click


FILE_NOT_FOUND_ERROR = 2
CONFIG_FILE_NAME = 'conf.ini'


def set_icon(exe, icon):
    if icon is None:
        return
    
    if not os.path.exists(icon) or not icon.endswith('.ico'):
        print('Error: The icon file does not exist or is not an .ico file.')
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


def archive(game_source, game_destination, game_name):
    exclude_list = []
    if '.avoid' in os.listdir(game_source):
        with open(join(game_source, '.avoid')) as f:
            lines = f.readlines()
            for line in lines:
                pattern = os.path.join(game_source, line.rstrip())
                exclude_list.append(pattern)

    zip_file_name_old = join(game_destination, game_name + '.zip')
    zip_file_name_new = join(game_destination, game_name + '.love')
    zip_file(game_source, zip_file_name_old, exclude_list)

    return zip_file_name_old, zip_file_name_new


def zip_file(folder_path, output_path, exclude=[]):
    with ZipFile(output_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            dirs_to_exclude = [d for d in dirs if os.path.join(root, d) in exclude]
            for dir_to_exclude in dirs_to_exclude:
                dirs.remove(dir_to_exclude)

            files = [f for f in files if not f.startswith('.avoid') and f != CONFIG_FILE_NAME]
                
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in exclude:
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))


def package_game(config):
    game_name = config['name']
    game_source = config['source']
    game_destination = config['destination']
    game_icon = config['icon']

    if not os.path.exists(game_destination):
        os.mkdir(game_destination)

    zip_file_name_old, zip_file_name_new = archive(game_source, game_destination, game_name)
    os.rename(zip_file_name_old, zip_file_name_new)

    love_exe = shutil.which('love')
    exe_name = join(game_destination, game_name + '.exe')
    os.system(f'copy /b "{love_exe}" + {zip_file_name_new} {exe_name} > NUL')
    os.remove(zip_file_name_new)

    love_path = os.path.dirname(love_exe) # type: ignore
    files = os.listdir(love_path)
    dll_files = [file for file in files if file.endswith('.dll')]
    for dll_file in dll_files:
        shutil.copy(join(love_path, dll_file), game_destination)
    shutil.copy(join(love_path, 'license.txt'), game_destination)

    set_icon(exe_name, game_icon)


def parse_config(src):
    if CONFIG_FILE_NAME not in os.listdir(src): 
        print('No config file found...')
        exit(FILE_NOT_FOUND_ERROR)

    parser = configparser.ConfigParser()
    parser.read(join(src, CONFIG_FILE_NAME))

    name = parser.get('Game', 'name', fallback=os.path.basename(src)).strip().lower()
    destination = join(
        parser.get('Game', 'destination', fallback=os.path.basename(src)),
        name).replace('/', '\\')
    icon = (parser.get('Game', 'icon').replace('/', '\\')
            if parser.has_option('Game', 'icon') else None)

    return {
        'source': src,
        'name': name,
        'destination': destination,
        'icon': icon
    }


@click.command()
@click.argument('src', default='.')
def main(src):
    '''
    Packages LÖVE game for distribution.

    SRC - Path to project directory
    '''
    try:
        config = parse_config(src)
        package_game(config)
        print(f'\nPackage successfully created at \'{config['destination']}\'')
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print('An error occured.')


if __name__ == "__main__":
    main()
