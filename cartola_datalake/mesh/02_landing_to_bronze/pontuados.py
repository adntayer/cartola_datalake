# python -m cartola_datalake.mesh.02_landing_to_bronze.pontuados
import os

import pandas as pd

from cartola_datalake.mesh.io import load_dict_from_file_compress, write_if_different
from cartola_datalake.mesh.logger import SetupLogger
from cartola_datalake.mesh.settings import FOLDER_BRONZE, FOLDER_LANDING, SEASON_STR

_log = SetupLogger("02_landing_to_bronze.pontuados")


def main():
    path_pontuados_season = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "pontuados",
    )
    _log.info("Reading 'pontuados' folder...")
    df_files = pd.DataFrame()
    for root, dirs, files in os.walk(path_pontuados_season):
        for file in files:
            file_path = os.path.join(root, file)
            dict_load = load_dict_from_file_compress(file_path)
            df_loop = pd.DataFrame(dict_load["atletas"]).T
            df_loop["rodada_id"] = dict_load["rodada"]
            df_loop["file_source"] = os.path.join(
                "datalake",
                FOLDER_LANDING,
                f"season-{SEASON_STR}",
                "pontuados",
                file,
            )
            df_files = pd.concat([df_files, df_loop], ignore_index=True)

    df_scouts = pd.json_normalize(df_files["scout"]).fillna(0)
    df_scouts.columns = [f"scout_{col}" for col in df_scouts.columns]
    df_files = pd.concat([df_files.drop(columns=["scout"]), df_scouts], axis=1)

    df_clubes = pd.DataFrame(dict_load["clubes"]).T.reset_index()
    df_clubes.rename(columns={"index": "clube_id"}, inplace=True)
    df_clubes["file_source"] = os.path.join(
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "pontuados",
        file,
    )

    df_posicoes = pd.DataFrame(dict_load["posicoes"]).T
    df_posicoes["file_source"] = os.path.join(
        "datalake",
        FOLDER_LANDING,
        f"season-{SEASON_STR}",
        "pontuados",
        file,
    )

    _log.info("Saving all files '.csv'...")

    # Directory to store the files
    target_dir = os.path.join(
        os.getcwd(),
        "datalake",
        FOLDER_BRONZE,
        f"season-{SEASON_STR}",
        "pontuados",
    )
    os.makedirs(target_dir, exist_ok=True)

    dict_args_pontuados = {
        "df": df_files,
        "filepath": os.path.join(target_dir, "pontuados.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    dict_args_clubes = {
        "df": df_clubes,
        "filepath": os.path.join(target_dir, "clubes.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    dict_args_posicoes = {
        "df": df_posicoes,
        "filepath": os.path.join(target_dir, "posicoes.csv"),
        "sep": ";",
        "decimal": ".",
        "index": False,
    }

    write_if_different(**dict_args_pontuados)
    write_if_different(**dict_args_clubes)
    write_if_different(**dict_args_posicoes)


if __name__ == "__main__":
    main()
