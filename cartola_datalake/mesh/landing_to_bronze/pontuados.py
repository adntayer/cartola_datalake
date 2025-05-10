# python -m cartola_datalake.mesh.landing_to_bronze.pontuados
import os

import pandas as pd

from cartola_datalake.mesh.io import load_dict_from_file_compress
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE
from cartola_datalake.mesh.settings import FOLDER_LANDING
from cartola_datalake.mesh.settings import SEASON_STR

_log = SetupLogger('landing_to_bronze.pontuados')


def main():
    PATH_PONTUADOS_SEASON = os.path.join(os.getcwd(), 'datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'pontuados')
    os.listdir(PATH_PONTUADOS_SEASON)
    _log.info("Reading 'pontuados' folder...")
    df_files = pd.DataFrame()
    for root, dirs, files in os.walk(PATH_PONTUADOS_SEASON):
        for file in files:
            file_path = os.path.join(root, file)
            dict_load = load_dict_from_file_compress(file_path)
            df_loop = pd.DataFrame(dict_load['atletas']).T
            df_loop['rodada_id'] = dict_load['rodada']
            df_loop['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'pontuados', file)
            df_files = pd.concat([df_files, df_loop], ignore_index=True)

    df_scouts = pd.json_normalize(df_files['scout']).fillna(0)
    df_scouts.columns = [f'scout_{col}' for col in df_scouts.columns]
    df_files = pd.concat([df_files.drop(columns=['scout']), df_scouts], axis=1)

    df_clubes = pd.DataFrame(dict_load['clubes']).T.reset_index()
    df_clubes.rename(columns={'index': 'clube_id'}, inplace=True)
    df_clubes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'pontuados', file)

    df_posicoes = pd.DataFrame(dict_load['posicoes']).T
    df_posicoes['file_source'] = os.path.join('datalake', FOLDER_LANDING, f'season-{SEASON_STR}', 'pontuados', file)

    _log.info("Saving all files '.csv'...")
    os.makedirs(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'pontuados'), exist_ok=True)
    df_files.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'pontuados', 'pontuados.csv.gz'), sep=';', decimal='.', index=False, compression='gzip')
    df_clubes.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'pontuados', 'clubes.csv'), sep=';', decimal='.', index=False)
    df_posicoes.to_csv(os.path.join(os.getcwd(), 'datalake', FOLDER_BRONZE, f'season-{SEASON_STR}', 'pontuados', 'posicoes.csv'), sep=';', decimal='.', index=False)
    _log.info('Saved')


if __name__ == '__main__':
    main()
