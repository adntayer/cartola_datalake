# python -m cartola_datalake.mesh.landing_to_bronze.atletas_mercado
import os

import pandas as pd

from cartola_datalake.mesh.io import load_dict_from_file_compress
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('landing_to_bronze.atletas_mercado')


def main():
    PATH_ATLETAS_MERCADO_SEASON = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado')
    os.listdir(PATH_ATLETAS_MERCADO_SEASON)
    _log.info("Reading 'atletas_mercado' folder...")
    df_files = pd.DataFrame()
    for root, dirs, files in os.walk(PATH_ATLETAS_MERCADO_SEASON):
        for file in files:
            file_path = os.path.join(root, file)
            dict_load = load_dict_from_file_compress(file_path)

            df_loop = pd.DataFrame(dict_load['atletas'])
            df_loop['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado', file)
            df_files = pd.concat([df_files, df_loop], ignore_index=True)

    df_clubes = pd.DataFrame(dict_load['clubes']).T.reset_index()
    df_clubes.rename(columns={'index': 'clube_id'}, inplace=True)
    df_clubes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado', file)

    df_posicoes = pd.DataFrame(dict_load['posicoes']).T
    df_posicoes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado', file)

    df_status = pd.DataFrame(dict_load['status']).T
    df_status['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'atletas_mercado', file)

    _log.info("Saving all files '.csv'...")
    os.makedirs(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado'), exist_ok=True)
    df_files.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado', 'atletas_mercado.csv.gz'), sep=';', decimal='.', index=False, compression='gzip')
    df_clubes.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado', 'clubes.csv'), sep=';', decimal='.', index=False)
    df_posicoes.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado', 'posicoes.csv'), sep=';', decimal='.', index=False)
    df_status.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado', 'status.csv'), sep=';', decimal='.', index=False)
    _log.info('Saved')


if __name__ == '__main__':
    main()
