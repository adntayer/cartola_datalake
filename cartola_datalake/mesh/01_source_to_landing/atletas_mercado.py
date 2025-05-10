# python -m cartola_datalake.mesh.01_source_to_landing.atletas_mercado
import os
from datetime import datetime

import requests

from cartola_datalake.mesh.checksum import calculate_dict_checksum
from cartola_datalake.mesh.io import load_dict_from_file_compress
from cartola_datalake.mesh.io import save_dict_to_file_compress
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('01_source_to_landing.atletas_mercado')


def main():
    url = 'https://api.cartola.globo.com/mercado/status'
    r = requests.get(url)
    data = r.json()
    rodada = data['rodada_atual'] - 1

    url = 'https://api.cartolafc.globo.com/atletas/mercado'
    _log.info(f"rodada {str(rodada).zfill(2)} | getting '{url=}'")

    r = requests.get(url)
    data = r.json()

    if 'mensagem' in data and data['mensagem'] == 'Rodada inválida.':
        _log.info(f"rodada {str(rodada).zfill(2)} | '{data['mensagem']=}' - exiting...")
        return

    now = datetime.now().strftime('%Y_%m_%d')
    path_atletas_mercado = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado', f'rodada-{str(rodada).zfill(2)}', f'{now}_atletas_mercado_rodada_{str(rodada).zfill(2)}.json.gz')
    path_dir = os.path.dirname(path_atletas_mercado)
    os.makedirs(path_dir, exist_ok=True)

    data['atleta'] = sorted(data['atletas'], key=lambda x: x['atleta_id'])
    hash_url = calculate_dict_checksum(data)
    _log.info(f"'{hash_url=}'")

    list_jsons = os.listdir(path_dir)
    if list_jsons:
        dict_hash = {}
        for file_json in list_jsons:
            dict_load = load_dict_from_file_compress(os.path.join(path_dir, file_json))
            dict_load['atletas'] = sorted(dict_load['atletas'], key=lambda x: x['atleta_id'])
            _hash = calculate_dict_checksum(dict_load)
            dict_hash[_hash] = file_json
            _log.info(f"rodada {str(rodada).zfill(2)} | '{file_json=}' -->> '{_hash}'")

        _log.info(f'rodada {str(rodada).zfill(2)} | checking for save')
        if hash_url in dict_hash:
            _log.info(f"rodada {str(rodada).zfill(2)} | no new data found... same hash/info of '{dict_hash[hash_url]}'")
            return
        _log.info(f'rodada {str(rodada).zfill(2)} | saving...')
        save_dict_to_file_compress(file_path=path_atletas_mercado, data=data)
    else:
        _log.info(f'rodada {str(rodada).zfill(2)} | saving...')
        save_dict_to_file_compress(file_path=path_atletas_mercado, data=data)


if __name__ == '__main__':
    main()
