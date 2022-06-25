# ERKAS Excel tpo GPKG export
# DF, 2022-03-29. Contact: florian.denzinger@bafu.admin.ch

import pandas as pd
import geopandas as gpd
import numpy as np
import os

import warnings
warnings.filterwarnings("ignore")

def list_file_paths(folder_path, file_type):
    """
        Creates a list of specific file paths in a directory and its subdirectories
        Inputs:
            folder_path: Path to the folder to list files
            file_type: Filetype specification of type string (e.g. "*.shp"). If you want to list all files specify
            file_type like this: "*"
        Outputs:
            file_path_list: List with specific file paths in the folder directory.
    """
    from pathlib import Path
    path = Path(folder_path)
    file_path_list = [f for f in path.rglob(file_type)]
    return file_path_list


erkas_csv_filepaths = list_file_paths(r"O:\GIS\GEP\RLS\_Mitarbeitende\DF2020\ERKAS\01_csv_bereinigt", "*.csv")

for erkas_csv_filepath in erkas_csv_filepaths:
    print(erkas_csv_filepath)
    df = pd.read_csv(erkas_csv_filepath, skiprows=2)
    header = df.iloc[0]
    df.columns = header
    df = df.drop(df.index[[0,1,2]])
    df.reset_index(drop=True, inplace=True)
    df = df.drop(df.columns[[0]], axis=1)

    # set value '<Nul>' to Nodata
    df = df.replace('<Nul>', np.NaN)

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.loc[:, 'Ort_E-Coord'], df.loc[:,'Ort_N-Coord']))
    gdf = gdf.set_crs('epsg:2056')
    gdf.to_file(os.path.join(r"O:\GIS\GEP\RLS\_Mitarbeitende\DF2020\ERKAS\02_csv_gpkg_export",
                             erkas_csv_filepath.stem +".gpkg"), driver = 'GPKG')

erkas_csvgpkgs_filepaths = list_file_paths(r'O:\GIS\GEP\RLS\_Mitarbeitende\DF2020\ERKAS Verkehrswege 2021_Bereinigt_DF\02_csv_gpkg_export', "*.gpkg")

for erkas_csvgpkgs_filepath in erkas_csvgpkgs_filepaths:
    #print(erkas_csvgpkgs_filepath)
    df = gpd.read_file(erkas_csvgpkgs_filepath)
    #df = df.fillna(9999)
    canton_name_short = erkas_csvgpkgs_filepath.name.split('_')[2]
    print("Canton:", canton_name_short)
    # convert column IDLaenge to int
    df['IDLaenge'] = pd.to_numeric(df['IDLaenge'])
    # get total sum of Strassenkilometer
    total_sum_strassenkilometer = df['IDLaenge'].sum()/1000
    print("Strassenkilometer:", total_sum_strassenkilometer)
    # replace
    df['KBfrei'] = df['KBfrei'].replace('false', 0)
    df['KBfrei'] = df['KBfrei'].replace('true', 1)
    df['KBfrei'] = df['KBfrei'].replace('FALSE', 0)
    df['KBfrei'] = df['KBfrei'].replace('TRUE', 1)
    df['KBfrei'] = df['KBfrei'].replace('N', 0)
    df['KBfrei'] = df['KBfrei'].replace('0', 0)
    df['KBfrei'] = df['KBfrei'].replace('1', 1)
    sum_KBfrei = df.groupby(['KBfrei'])['IDLaenge'].sum().reset_index()
    if not sum_KBfrei[sum_KBfrei['KBfrei'] == 1].values.tolist() == []:
        sum_KBfrei = sum_KBfrei[sum_KBfrei['KBfrei']==1].values.tolist()[0][1]
    else:
        sum_KBfrei = 0
    sum_KBfrei = sum_KBfrei/1000
    print("KB befreit:", sum_KBfrei)
    # get total sum of AmpelCode classes
    sum_ampel_codes = df.groupby(['AmpelCodePers'])['IDLaenge'].sum().reset_index()
    sum_ampel_codes = sum_ampel_codes['IDLaenge'].values.tolist()
    print("Ampel Codes:", sum_ampel_codes)
    row = canton_name_short, total_sum_strassenkilometer, sum_KBfrei , *sum_ampel_codes

erkas_csvgpkgs_filepaths = list_file_paths(r'O:\GIS\GEP\RLS\_Mitarbeitende\DF2020\ERKAS Verkehrswege 2021_Bereinigt_DF\02_xtf_gpkg_export', "*.gpkg")

for erkas_csvgpkgs_filepath in erkas_csvgpkgs_filepaths:
    #print(erkas_csvgpkgs_filepath)
    df = gpd.read_file(erkas_csvgpkgs_filepath)
    #df = df.fillna(9999)
    canton_name_short = erkas_csvgpkgs_filepath.name.split('_')[2]
    print("Canton:", canton_name_short)
    # convert column IDLaenge to int
    df['IDLaenge'] = pd.to_numeric(df['IDLaenge'])
    # get total sum of Strassenkilometer
    total_sum_strassenkilometer = df['IDLaenge'].sum()/1000
    print("Strassenkilometer:", total_sum_strassenkilometer)
    # replace
    df['KBfrei'] = df['KBfrei'].replace('false', 0)
    df['KBfrei'] = df['KBfrei'].replace('true', 1)
    df['KBfrei'] = df['KBfrei'].replace('FALSE', 0)
    df['KBfrei'] = df['KBfrei'].replace('TRUE', 1)
    df['KBfrei'] = df['KBfrei'].replace('N', 0)
    df['KBfrei'] = df['KBfrei'].replace('0', 0)
    df['KBfrei'] = df['KBfrei'].replace('1', 1)
    sum_KBfrei = df.groupby(['KBfrei'])['IDLaenge'].sum().reset_index()
    if not sum_KBfrei[sum_KBfrei['KBfrei'] == 1].values.tolist() == []:
        sum_KBfrei = sum_KBfrei[sum_KBfrei['KBfrei']==1].values.tolist()[0][1]
    else:
        sum_KBfrei = 0
    sum_KBfrei = sum_KBfrei/1000
    print("KB befreit:", sum_KBfrei)
    # get total sum of AmpelCode classes
    sum_ampel_codes = df.groupby(['AmpelCodePers'])['IDLaenge'].sum().reset_index()
    sum_ampel_codes = sum_ampel_codes['IDLaenge'].values.tolist()
    print("Ampel Codes:", sum_ampel_codes)
    row = canton_name_short, total_sum_strassenkilometer, sum_KBfrei , *sum_ampel_codes