# python -m cartola_datalake.mesh.02_landing_to_bronze.atletas_mercado
import os

import pandas as pd

from cartola_datalake.mesh.io import load_dict_from_file_compress
from cartola_datalake.mesh.io import write_if_different
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('02_landing_to_bronze.atletas_mercado')


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

    # Directory to store the files
    mercado_target_dir = os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'atletas_mercado')
    os.makedirs(mercado_target_dir, exist_ok=True)

    dict_args_mercado = {
        'df': df_files,
        'filepath': os.path.join(mercado_target_dir, 'atletas_mercado.csv.gz'),
        'sep': ';',
        'decimal': '.',
        'index': False,
        'compression': 'gzip',
    }

    dict_args_clubes = {
        'df': df_clubes,
        'filepath': os.path.join(mercado_target_dir, 'clubes.csv'),
        'sep': ';',
        'decimal': '.',
        'index': False,
    }

    dict_args_posicoes = {
        'df': df_posicoes,
        'filepath': os.path.join(mercado_target_dir, 'posicoes.csv'),
        'sep': ';',
        'decimal': '.',
        'index': False,
    }

    dict_args_status = {
        'df': df_status,
        'filepath': os.path.join(mercado_target_dir, 'status.csv'),
        'sep': ';',
        'decimal': '.',
        'index': False,
    }

    # Write files only if different
    write_if_different(**dict_args_mercado)
    write_if_different(**dict_args_clubes)
    write_if_different(**dict_args_posicoes)
    write_if_different(**dict_args_status)


if __name__ == '__main__':
    main()
