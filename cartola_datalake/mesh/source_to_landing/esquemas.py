# python -m cartola_datalake.mesh.source_to_landing.esquemas
import os
from datetime import datetime

import requests

from cartola_datalake.mesh.checksum import calculate_dict_checksum
from cartola_datalake.mesh.io import load_dict_from_file
from cartola_datalake.mesh.io import save_dict_to_file
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('source_to_landing.esquemas')


def main():
    url = 'https://api.cartolafc.globo.com/esquemas'
    _log.info(f"esquemas | getting '{url=}'")

    r = requests.get(url)
    data = r.json()

    hash_url = calculate_dict_checksum(data)
    now = datetime.now().strftime('%Y_%m_%d')
    path_esquemas = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'esquemas', f'{now}_esquemas.json')
    path_dir = os.path.dirname(path_esquemas)
    os.makedirs(path_dir, exist_ok=True)

    _log.info(f"esquemas | '{hash_url=}'")
    list_jsons = os.listdir(path_dir)
    if list_jsons:
        dict_hash = {}
        for file_json in list_jsons:
            _hash = calculate_dict_checksum(load_dict_from_file(os.path.join(path_dir, file_json)))
            dict_hash[_hash] = file_json
            _log.info(f"esquemas | '{file_json=}' -->> '{_hash}'")

        if hash_url in dict_hash:
            _log.info(f"esquemas | no new data found... same hash/info of '{dict_hash[hash_url]}'")
            return
        save_dict_to_file(file_path=path_esquemas, data=data)
    else:
        save_dict_to_file(file_path=path_esquemas, data=data)


if __name__ == '__main__':
    main()
