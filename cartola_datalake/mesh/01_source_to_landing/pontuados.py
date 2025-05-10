# python -m cartola_datalake.mesh.01_source_to_landing.pontuados
import os
from datetime import datetime

import requests

from cartola_datalake.mesh.checksum import calculate_dict_checksum
from cartola_datalake.mesh.io import load_dict_from_file_compress
from cartola_datalake.mesh.io import save_dict_to_file_compress
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger("01_source_to_landing.pontuados")


def main(rodada):
    url = f"https://api.cartolafc.globo.com/atletas/pontuados/{rodada}"
    _log.info(f"rodada {str(rodada).zfill(2)} | getting '{url=}'")

    r = requests.get(url)
    data = r.json()

    if "mensagem" in data and data["mensagem"] == "Rodada inválida.":
        _log.info(f"rodada {str(rodada).zfill(2)} | '{data['mensagem']=}' - exiting...")
        return

    hash_url = calculate_dict_checksum(data)
    now = datetime.now().strftime("%Y_%m_%d_%H_%M")
    path_pontuados = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "pontuados",
        f"rodada-{str(rodada).zfill(2)}",
        f"{now}_pontuados_rodada_{str(rodada).zfill(2)}.json.gz",
    )
    path_dir = os.path.dirname(path_pontuados)
    os.makedirs(path_dir, exist_ok=True)

    _log.info(f"rodada {str(rodada).zfill(2)} | '{hash_url=}'")
    list_jsons = os.listdir(path_dir)
    if list_jsons:
        dict_hash = {}
        for file_json in list_jsons:
            _hash = calculate_dict_checksum(
                load_dict_from_file_compress(os.path.join(path_dir, file_json)),
            )
            dict_hash[_hash] = file_json
            _log.info(f"rodada {str(rodada).zfill(2)} | '{file_json=}' -->> '{_hash}'")

        if hash_url in dict_hash:
            _log.info(
                f"rodada {str(rodada).zfill(2)} | no new data found... same hash/info of '{dict_hash[hash_url]}'",
            )
            return
        save_dict_to_file_compress(file_path=path_pontuados, data=data)
    else:
        save_dict_to_file_compress(file_path=path_pontuados, data=data)


if __name__ == "__main__":
    for rodada in range(1, 39):
        main(rodada)
        _log.info("#############")
