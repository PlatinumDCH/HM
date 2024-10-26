from parser_arg import parse_args
from shutil import copyfile
from threading import Thread
from pathlib import Path
import logging

folders = []
def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)

def ensure_extension_folder(ex_folder: Path)-> None:
    try:
        ex_folder.mkdir(exist_ok=True, parents=True)
    except OSError as err:
        logging.error(err)

def copy_file(path: Path) -> None:
    extension_folders = {}

    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext

            if ext not in extension_folders:
                ensure_extension_folder(ext_folder)
                extension_folders[ext] = ext_folder
            try:
                copyfile(el, extension_folders[ext] / el.name) 
                logging.info(f"Copied: {el} -> {extension_folders[ext]}")
            except OSError as err:
                logging.error(err)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    try:
        source, output = parse_args()
    except (FileNotFoundError, NotADirectoryError) as e:
        print(e)
        exit(1)

    folders.append(source)
    grabs_folder(source)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads] # type: ignore