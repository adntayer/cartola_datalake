# python -m cartola_datalake.mesh.landing_to_bronze.esquemas
import json
import os

import pandas as pd

from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('landing_to_bronze.esquemas')


def main():
    PATH_ESQUEMAS_SEASON = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'esquemas')
    list_files = os.listdir(PATH_ESQUEMAS_SEASON)
    _log.info("Reading 'esquemas' folder...")
    df_esquemas = pd.DataFrame()
    for file in list_files:
        file_path = os.path.join(PATH_ESQUEMAS_SEASON, file)
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        df_loop = pd.DataFrame(data)
        df_posicoes = pd.json_normalize(df_loop['posicoes'])
        df_loop = pd.concat([df_loop.drop(columns=['posicoes']), df_posicoes], axis=1)
        df_loop['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'esquemas', file)
        df_esquemas = pd.concat([df_esquemas, df_loop], ignore_index=True)

    _log.info("Saving 'esquemas.csv'...")
    os.makedirs(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'esquemas'), exist_ok=True)
    df_esquemas.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'esquemas', 'esquemas.csv'), sep=';', decimal='.', index=False)
    _log.info('Saved')


if __name__ == '__main__':
    main()
