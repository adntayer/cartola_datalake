# python -m cartola_datalake.mesh.landing_to_bronze.partidas
import json
import os

import pandas as pd

from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('landing_to_bronze.partidas')


def main():
    PATH_PARTIDAS_SEASON = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'partidas')
    _log.info("Reading 'partidas' folder...")
    df_all = pd.DataFrame()
    for root, dirs, files in os.walk(PATH_PARTIDAS_SEASON):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            for dict_partida in data['partidas']:
                df_loop = pd.json_normalize(dict_partida)
                df_loop['rodada'] = file.replace('partidas_rodada_', '').replace('.json', '')
                df_loop['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'partidas', file)
                df_all = pd.concat([df_all, df_loop], ignore_index=True)

    _log.info('All partidas got')

    _log.info("Reading 'clubes'...")
    df_clubes = pd.DataFrame(data['clubes']).T.reset_index()
    df_clubes.rename(columns={'index': 'clube_id'}, inplace=True)
    df_clubes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'partidas', file)

    _log.info("Saving 'partidas.csv' and 'clubes.csv'...")
    os.makedirs(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'partidas'), exist_ok=True)
    df_all.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'partidas', 'partidas.csv'), sep=';', decimal='.', index=False)
    df_clubes.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'partidas', 'clubes.csv'), sep=';', decimal='.', index=False)
    _log.info('Saved')


if __name__ == '__main__':
    main()
