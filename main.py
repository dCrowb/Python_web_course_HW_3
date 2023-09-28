from pathlib import Path
from threading import Thread, Event
import logging
from time import ctime, time, sleep
import shutil
import argparse
from sys import argv
import os

FOLDERS = []
logger = logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s - %(message)s')


def get_all_folders(path: Path, data: list) -> bool:
    status = False
    try:
        if len(os.listdir(path)) == 0:
            return True
        
        for folder in path.iterdir():
            if folder.is_dir():
                data.append(folder)
        
        data.append(path)
        logging.debug('Data successfully recieved.')
    except FileNotFoundError:
        logging.debug(f'Directory with name [{path}] - not found!')
        status = True
    
    return status

def sort_file(folder: Path, event: Event):
    for item in folder.iterdir():
        try:
            shutil.os.makedirs(output + '/' + item.suffix[1:])
        except FileExistsError:
            pass
        shutil.move(item, output + '/' + item.suffix[1:])
        logging.debug(f'Replace file: [{item}] To: [{output + "/" + item.suffix[1:]}]')
    event.set()

def delete_empty_folders(path: Path, event: Event):
    print(f'Waiting while sorting - {path}')
    event.wait()
    shutil.rmtree(path)
    print(f'Deleting folder [{path}]')
    sleep(1)


if __name__ == '__main__':
    source = ''
    output = ''
    
    if len(argv) > 1:
        parser = argparse.ArgumentParser(
                            description='Sorting files',
                            epilog='Also you can using [python main.py] - for working with app.')
        parser.add_argument('-s', '--source', required=True, help='Enter target folder name')
        parser.add_argument('-o', '--output', default='dist', help='Distanation to save all files, folder name')
        args = vars(parser.parse_args())

        source = args.get('source')
        output = args.get('output')
    else:
        print('Please use console for work with sorting.')

    if source == '':
        source = 'None'
    if output == '':
        output = 'default'

    start_time = time()
    event = Event()
    target_folder = Path(source)    
    status = get_all_folders(target_folder, FOLDERS)

    if not status:
        threads = []

        for folder in FOLDERS:
            th = Thread(target=sort_file, args=(folder, event))
            th.start()
            threads.append(th)
        [th.join() for th in threads]

        remover = Thread(target=delete_empty_folders, args=(target_folder, event))
        remover.start()
        remover.join()

        print(time() - start_time, 'sec.')
        print('All data successfully sorted!')
    else:
        print(f'Directory [{source}] is empty or not exist...')