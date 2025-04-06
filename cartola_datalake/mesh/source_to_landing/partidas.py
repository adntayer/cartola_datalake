# python -m cartola_datalake.mesh.source_to_landing.partidas
import os

import requests

from cartola_datalake.mesh.checksum import calculate_dict_checksum
from cartola_datalake.mesh.io import load_dict_from_file
from cartola_datalake.mesh.io import save_dict_to_file
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('source_to_landing.partidas')


def main(rodada):
    url = f'https://api.cartolafc.globo.com/partidas/{rodada}'
    _log.info(f"rodada {str(rodada).zfill(2)} | getting '{url=}'")

    r = requests.get(url)
    data = r.json()

    path_partidas = os.path.join(os.getcwd(), 'datalake', '01-landing', f'season-{SEASON_STR}', 'partidas', f'rodada-{str(rodada).zfill(2)}', f'partidas_rodada_{str(rodada).zfill(2)}.json')
    path_dir = os.path.dirname(path_partidas)
    os.makedirs(path_dir, exist_ok=True)

    data['partidas'] = sorted(data['partidas'], key=lambda x: x['partida_id'])
    hash_url = calculate_dict_checksum(data)
    _log.info(f"rodada {str(rodada).zfill(2)} | '{hash_url=}'")
    list_jsons = os.listdir(path_dir)
    if list_jsons:
        dict_hash = {}
        for file_json in list_jsons:
            dict_load = load_dict_from_file(os.path.join(path_dir, file_json))
            dict_load['partidas'] = sorted(dict_load['partidas'], key=lambda x: x['partida_id'])
            _hash = calculate_dict_checksum(dict_load)
            dict_hash[_hash] = file_json
            _log.info(f"rodada {str(rodada).zfill(2)} | '{file_json=}' -->> '{_hash}'")

        if hash_url in dict_hash:
            _log.info(f"rodada {str(rodada).zfill(2)} | no new data found... same hash/info of '{dict_hash[hash_url]}'")
            return
        save_dict_to_file(file_path=path_partidas, data=data)
    else:
        save_dict_to_file(file_path=path_partidas, data=data)


if __name__ == '__main__':
    for rodada in range(1, 39):
        main(rodada)
        _log.info('#############')
