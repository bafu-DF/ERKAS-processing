# ERKAS STATISTICS PROCESSING
# DF, 2022-06-26

import os
import warnings
import geopandas as gpd


def list_file_paths(folder_path, file_type):
    """This function creates a list of specific file paths in a directory and its subdirectories.

    Args:
        folder_path (string): Path to the folder to list files
        file_type (string): Filetype specification of type string (e.g. "*.shp"). If you want to list all files specify

    Returns:
        string: Pathlib object with specific file paths in the folder directory.
    """
    from pathlib import Path
    path = Path(folder_path)
    file_path_list = [f for f in path.rglob(file_type)]
    return file_path_list


def ilixtf2gpkg(ili_dir, gpkg_dir):
    """This function converts ILI XTF file(s) in a directory to GPKG file(s).

    Args:
        ili_dir (string): Path to the directory where ILI XTF files are stored
        gpkg_dir (string): Path to the directory where GPKG files should be stored
    """
    from osgeo import ogr
    import os
    if not os.path.exists(gpkg_dir):
        os.makedirs(gpkg_dir)

    ili_files = list_file_paths(ili_dir, '*.xtf')

    for ili_file in ili_files:
        print(f"Processing: {ili_file.stem}")
        command = ("ogr2ogr -f" + " " + 'GPKG' + " " + "-a_srs 'EPSG:2056' " +
                   str(os.path.join(gpkg_dir, ili_file.stem+".gpkg")) + " " + str(ili_file))
        print(f"Processing: {ili_file.stem}")
        os.system(command, )


def filter_df_column_names(gdf_column_list, filter):
    """Filter column names of a dataframe.

    Args:
        gdf_column_list (list): List of column names of a dataframe
        filter (string): String that partially contains the name of the column_
    """
    filter_string = [string for string in gdf_column_list if filter in string]
    return(filter_string)


def unnest_list(filter_list):
    """Unnests a list of lists.

    Args:
        filter_list (list): List of lists to unnest
    """
    from itertools import chain
    unnested = list(chain(*filter_list))
    return(unnested)


def calculate_statistics_from_ili_gpkg(gpkg_dir, excel_export_path):
    """Calculates statistics for ILI converted GPKG file (compatible with ERKAS Strassen >V2_0)

    Args:
        gpkg_dir (string): Path to the folder location of the converted ILI_GPKG files (need to be in GPKG format)
        excel_export_path (string): Path where the excel file containing the statistics is saved to
    """
    import geopandas as gpd
    import pandas as pd

    workingdir = os.getcwd()
    gpkg_files = list_file_paths(gpkg_dir, '*.gpkg')

    df_results = pd.DataFrame()
    for gpkg_file in gpkg_files:
        print(f"Processing: {gpkg_file.stem}")

        gdf = gpd.read_file(gpkg_file, crs="EPSG:2056")
        gdf = gdf.set_crs("EPSG:2056", allow_override=True)
        print(f"Number of points: {len(gdf.length)}")
        print(f"Coordinate system: {gdf.crs}")
        print(f"Number of columns (intial dataset): {len(gdf.columns)}")

        idlaenge = filter_df_column_names(list(gdf.columns), "IDLaenge")
        kbfrei = filter_df_column_names(list(gdf.columns), "KBfrei")
        ampelcodepers = filter_df_column_names(
            list(gdf.columns), "Ergebnis_AmpelCodePers")
        ampelcodeofg = filter_df_column_names(
            list(gdf.columns), "Ergebnis_AmpelCodeOFG")
        ampelcodegw = filter_df_column_names(
            list(gdf.columns), "Ergebnis_AmpelCodeGW")

        filter_list = idlaenge, kbfrei, ampelcodepers, ampelcodeofg, ampelcodegw
        filter = unnest_list(filter_list)
        filter.append('geometry')
        canton_name_short = gpkg_file.stem.split('_')[-2]

        gdf_subset = gdf[filter]
        gdf_subset['Inhaber'] = canton_name_short
        print(f"Columns of subset: {len(gdf_subset.columns)}")
        if len(gdf_subset.columns) != 7:
            print("Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset")
            print("___________________________________________________")
            continue
        if not os.path.exists(workingdir + '/Data/ILI_GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/ILI_GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(
            workingdir, 'Data/ILI_GPKG_EXPORT_SUBSET/'+gpkg_file.stem+'.gpkg'), driver='GPKG')

        # calculate total of kilometer Durchgangsstrasse
        gdf_subset.IDLaenge = pd.to_numeric(gdf_subset.IDLaenge)
        total = gdf_subset.IDLaenge.sum()/1000
        print(f"Total Anzahl Kilometer Durchgangsstrasse: {total}")
        # calculate total KB befreit
        kbfrei_grouped = gdf_subset.groupby(
            kbfrei)[idlaenge].sum().reset_index()
        print(kbfrei_grouped)
        kb_befreit = kbfrei_grouped[kbfrei_grouped[''.join(kbfrei)] == 'true']
        kbfrei_grouped[kbfrei_grouped[''.join(kbfrei)] == 'true']
        if kb_befreit.empty:
            kb_befreit_calc = 0
        else:
            kb_befreit_calc = kb_befreit[idlaenge].values[0]/1000
        print(f"KB befreit: {kb_befreit_calc}")
        # calculate Ampelcodes
        ampelcodepers_grouped = gdf_subset.groupby(
            ampelcodepers)[idlaenge].sum().reset_index()
        ampelcodepers_calc = unnest_list(
            ampelcodepers_grouped[idlaenge].values/1000)
        ampelcodepers_calc_classes = unnest_list(
            ampelcodepers_grouped[ampelcodepers].astype(int).values)
        print(f"Ampelcode Pers Classes: {ampelcodepers_calc_classes}")
        print(f"Ampelcode Pers: {ampelcodepers_calc}")
        ampelcodeofg_grouped = gdf_subset.groupby(
            ampelcodeofg)[idlaenge].sum().reset_index()
        ampelcodeofg_calc = unnest_list(
            ampelcodeofg_grouped[idlaenge].values/1000)
        ampelcodeofg_calc_classes = unnest_list(
            ampelcodeofg_grouped[ampelcodeofg].astype(int).values)
        print(f"Ampelcode OFG Classes: {ampelcodeofg_calc_classes}")
        print(f"Ampelcode OFG: {ampelcodeofg_calc}")
        ampelcodegw_grouped = gdf_subset.groupby(
            ampelcodegw)[idlaenge].sum().reset_index()
        ampelcodegw_calc = unnest_list(
            ampelcodegw_grouped[idlaenge].values/1000)
        ampelcodegw_calc_classes = unnest_list(
            ampelcodegw_grouped[ampelcodegw].astype(int).values)
        print(f"Ampelcode GW Classes: {ampelcodegw_calc_classes}")
        print(f"Ampelcode GW: {ampelcodegw_calc}")
        ampelcodepers_dict = {ampelcodepers_calc_classes[i]: ampelcodepers_calc[i] for i in range(
            len(ampelcodepers_calc_classes))}
        ampelcodepers_dict = {
            f"AmpelcodePers{key}": val for key, val in ampelcodepers_dict.items()}
        ampelcodeofg_dict = {ampelcodeofg_calc_classes[i]: ampelcodeofg_calc[i] for i in range(
            len(ampelcodeofg_calc_classes))}
        ampelcodeofg_dict = {
            f"AmpelcodeOFG{key}": val for key, val in ampelcodeofg_dict.items()}
        ampelcodegw_dict = {ampelcodegw_calc_classes[i]: ampelcodegw_calc[i] for i in range(
            len(ampelcodegw_calc_classes))}
        ampelcodegw_dict = {f"AmpelcodeGW{key}": val for key,
                            val in ampelcodegw_dict.items()}
        df = pd.concat([pd.DataFrame([canton_name_short], columns=['Inhaber']), pd.DataFrame([total], columns=[
                       'total_km_durchgangsstrasse']), pd.DataFrame([kb_befreit_calc], columns=['kb_befreit'])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodepers_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodeofg_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodegw_dict])], axis=1)
        df_results = pd.concat([df_results, df], axis=0)
        print("___________________________________________________")

    df_results
    if not os.path.exists(os.path.join(workingdir, 'Data', 'RESULTS')):
        os.makedirs(os.path.join(workingdir, 'Data', 'RESULTS'))
    df_results.to_excel(excel_export_path, index=False)




def calculate_statistics_from_xlsx_file(xlsx_dir, excel_export_path):
    """Calculates statistics for ERKAS Excel files (compatible with ERKAS Strassen >V2_0)

    Args:
        xlsx_dir (string): Path to the folder location of the Excel files (need to have a compatible header)
        excel_export_path (string): Path where the excel file containing the statistics is saved to
    """

    import pandas as pd

    workingdir = os.getcwd()
    xlsx_files = list_file_paths(xlsx_dir, "*.xlsx")
    df_results = pd.DataFrame()

    for xlsx_file in xlsx_files:
        print(f"Processing: {xlsx_file}")
        df = pd.read_excel(xlsx_file, skiprows =2)
        header = df.iloc[0]
        df.columns = header
        df = df.drop(df.index[[0, 1, 2]])
        df.reset_index(drop=True, inplace=True)
        df = df.drop(df.columns[[0]], axis=1)

        # create gdf from excel data
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.loc[:, 'Ort_E-Coord'], df.loc[:, 'Ort_N-Coord']))
        gdf = gdf.set_crs('epsg:2056')
        print(f"Number of points: {len(gdf.length)}")
        print(f"Coordinate system: {gdf.crs}")
        print(f"Number of columns (intial dataset): {len(gdf.columns)}")

        if not os.path.exists(workingdir + '/Data/XLSX_GPKG_EXPORT_ALL/'):
            os.makedirs(os.path.join(workingdir + '/Data/XLSX_GPKG_EXPORT_ALL/'))
        #gdf.to_file(os.path.join(workingdir, 'Data/XLSX_GPKG_EXPORT_ALL/'+xlsx_file.stem+'.gpkg'), driver='GPKG')

        filter_list = ['Inhaber', 'IDLaenge', 'KBfrei', 'AmpelCodePers', 'AmpelCodeOFG', 'AmpelCodeGW', 'geometry']
        gdf_subset = gdf[filter_list]
        print(f"Columns of subset: {len(gdf_subset.columns)}")
        if len(gdf_subset.columns) != 7:
            print(
                "File will not be analysed as used file has a geodatamodel with version < V2_0 (Hint: check if field IDLaenge exists in dataset")
            print("___________________________________________________")
            continue
        if not os.path.exists(workingdir + '/Data/XLSX_GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/XLSX_GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(workingdir, 'Data/XLSX_GPKG_EXPORT_SUBSET/' + xlsx_file.stem + '.gpkg'),
                           driver='GPKG')

        # calculate total of kilometer Durchgangsstrasse
        total = gdf_subset.IDLaenge.sum() / 1000
        print(f"Total Anzahl Kilometer Durchgangsstrasse: {total}")
        # calculate total KB befreit
        kbfrei_grouped = gdf_subset.groupby('KBfrei')['IDLaenge'].sum().reset_index()
        print(kbfrei_grouped)
        kb_befreit = kbfrei_grouped[kbfrei_grouped['KBfrei'] == 'True']
        print(len(kb_befreit))
        if kb_befreit.empty:
            kb_befreit_calc = 0
        else:
            kb_befreit_calc = kb_befreit.IDLaenge.values[0]/1000
        print(f"KB befreit: {kb_befreit_calc}")

        # calculate Ampelcodes
        ampelcodepers_grouped = gdf_subset.groupby(['AmpelCodePers'])['IDLaenge'].sum().reset_index()
        ampelcodepers_calc = ampelcodepers_grouped['IDLaenge'].values / 1000
        ampelcodepers_calc_classes = ampelcodepers_grouped['AmpelCodePers'].astype(int).values
        print(f"Ampelcode Pers Classes: {ampelcodepers_calc_classes}")
        print(f"Ampelcode Pers: {ampelcodepers_calc}")
        ampelcodeofg_grouped = gdf_subset.groupby(['AmpelCodeOFG'])['IDLaenge'].sum().reset_index()
        ampelcodeofg_calc = ampelcodeofg_grouped['IDLaenge'].values / 1000
        ampelcodeofg_calc_classes = ampelcodeofg_grouped['AmpelCodeOFG'].astype(int).values
        print(f"Ampelcode OFG Classes: {ampelcodeofg_calc_classes}")
        print(f"Ampelcode OFG: {ampelcodeofg_calc}")
        ampelcodegw_grouped = gdf_subset.groupby(['AmpelCodeGW'])['IDLaenge'].sum().reset_index()
        ampelcodegw_calc = ampelcodegw_grouped['IDLaenge'].values / 1000
        ampelcodegw_calc_classes = ampelcodegw_grouped['AmpelCodeGW'].astype(int).values
        print(f"Ampelcode GW Classes: {ampelcodegw_calc_classes}")
        print(f"Ampelcode GW: {ampelcodegw_calc}")

        ampelcodepers_dict = {ampelcodepers_calc_classes[i]: ampelcodepers_calc[i] for i in range(len(ampelcodepers_calc_classes))}
        ampelcodepers_dict = {f"AmpelcodePers{key}": val for key, val in ampelcodepers_dict.items()}
        ampelcodeofg_dict = {ampelcodeofg_calc_classes[i]: ampelcodeofg_calc[i] for i in range(
            len(ampelcodeofg_calc_classes))}
        ampelcodeofg_dict = {
            f"AmpelcodeOFG{key}": val for key, val in ampelcodeofg_dict.items()}
        ampelcodegw_dict = {ampelcodegw_calc_classes[i]: ampelcodegw_calc[i] for i in range(
            len(ampelcodegw_calc_classes))}
        ampelcodegw_dict = {f"AmpelcodeGW{key}": val for key,
                                                         val in ampelcodegw_dict.items()}

        canton_name_short = gdf_subset['Inhaber'].values[0]

        df = pd.concat([pd.DataFrame([canton_name_short], columns=['Inhaber']), pd.DataFrame([total], columns=[
            'total_km_durchgangsstrasse']), pd.DataFrame([kb_befreit_calc], columns=['kb_befreit'])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodepers_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodeofg_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodegw_dict])], axis=1)
        df_results = pd.concat([df_results, df], axis=0)
        print("___________________________________________________")

    if not os.path.exists(os.path.join(workingdir, 'Data', 'RESULTS')):
        os.makedirs(os.path.join(workingdir, 'Data', 'RESULTS'))
    df_results.to_excel(excel_export_path, index=False)

def combine_results_xlsx(results_dir, excel_export_path):
    """Combine excel files in a directory into one

    Args:
        results_dir (string): Path to the folder location of the Excel files
        excel_export_path (string): Path where the excel file containing the statistics is saved to
    """
    import pandas as pd

    results_files = list_file_paths(results_dir, "*.xlsx")
    excl_list = []
    for file in results_files:
        excl_list.append(pd.read_excel(file))
    excl_merged = pd.DataFrame()
    for excl_file in excl_list:
        # appends the data into the excl_merged
        # dataframe.
        excl_merged = excl_merged.append(excl_file, ignore_index=True)
    excl_merged.to_excel(excel_export_path, index=False)


def main():
    warnings.filterwarnings("ignore")

    # execute the script

    # calculate the statistics from ILI files (only compatible with model version >2_0)
    gpkg_dir = r'Data/ILI_GPKG_CONVERT/'
    calculate_statistics_from_ili_gpkg(gpkg_dir, excel_export_path=r'Data/RESULTS/ILI_GPKG_STATISTICS.xlsx')

    xlsx_dir = r'Data/XLSX_CORRECTED/'
    calculate_statistics_from_xlsx_file(xlsx_dir, excel_export_path=r'Data/RESULTS/XLSX_GPKG_STATISTICS.xlsx')

    # combine two Excel files into one
    results_dir = r'Data/RESULTS'
    combine_results_xlsx(results_dir, excel_export_path='Data/RESULTS/Results.xlsx')

if __name__ == main():
    main()