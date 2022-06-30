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
                   str(os.path.join(gpkg_dir, ili_file.stem + ".gpkg")) + " " + str(ili_file))
        print(f"Processing: {ili_file.stem}")
        os.system(command, )


def filter_df_column_names(gdf_column_list, filter):
    """Filter column names of a dataframe.

    Args:
        gdf_column_list (list): List of column names of a dataframe
        filter (string): String that partially contains the name of the column_
    """
    filter_string = [string for string in gdf_column_list if filter in string]
    return (filter_string)


def unnest_list(filter_list):
    """Unnests a list of lists.

    Args:
        filter_list (list): List of lists to unnest
    """
    from itertools import chain
    unnested = list(chain(*filter_list))
    return (unnested)


def list_to_string_for_df_indexing(in_list_el):
    """Converts a list element to string for use in indexing of a (geo)pandas dataframe.

    Args:
        in_list_el (list): List element (e.g. column names of a (geo)pandas dataframe)
    """
    list_el = ''.join(in_list_el)
    return list_el


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

        # read in .gpkg file as a geodataframe
        gdf = gpd.read_file(gpkg_file, crs="EPSG:2056")
        gdf = gdf.set_crs("EPSG:2056", allow_override=True)
        print(f"Number of points: {len(gdf.length)}")
        print(f"Coordinate system: {gdf.crs}")
        print(f"Number of columns (initial dataset): {len(gdf.columns)}")

        # get variable for indexing
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

        # create subset with columns needed for statistical analysis
        gdf_subset = gdf[filter]
        gdf_subset['Kanton'] = canton_name_short
        gdf_subset['Format'] = "ILI_XTF"
        file_format = "ILI_XTF"
        unique_value_idlaenge = gdf_subset['IDLaenge'].unique()
        if len(unique_value_idlaenge) == 1:
            berechnungsintervall = gdf_subset['IDLaenge'][0]
        else:
            berechnungsintervall = "variabel"
        gdf_subset['Berechnungsintervall'] = berechnungsintervall
        cols = gdf_subset.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        gdf_subset = gdf_subset[cols]
        print(f"Columns of subset: {len(gdf_subset.columns)}")
        if len(gdf_subset.columns) != 9:
            print(
                "Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field "
                "IDLaenge exists in dataset")
            print("___________________________________________________")
            continue
        if not os.path.exists(workingdir + '/Data/ILI_GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/ILI_GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(
            workingdir, 'Data/ILI_GPKG_EXPORT_SUBSET/' + gpkg_file.stem + '.gpkg'), driver='GPKG')
        if not os.path.exists(workingdir + '/Data/RESULTS/GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/RESULTS/GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(
            workingdir, 'Data/RESULTS/GPKG_EXPORT_SUBSET/' + gpkg_file.stem + '.gpkg'), driver='GPKG')

        # calculate total of kilometer Durchgangsstrasse
        gdf_subset.IDLaenge = pd.to_numeric(gdf_subset.IDLaenge)
        total = gdf_subset.IDLaenge.sum() / 1000
        print(f"Total Durchgangsstrasse: {total} [km]")

        # calculate total KB befreit
        kbfrei_grouped = gdf_subset.groupby(
            kbfrei)[idlaenge].sum().reset_index()
        print(kbfrei_grouped)
        kb_befreit = kbfrei_grouped[kbfrei_grouped[''.join(kbfrei)] == 'true']
        kbfrei_grouped[kbfrei_grouped[''.join(kbfrei)] == 'true']
        if kb_befreit.empty:
            kb_befreit_calc = 0
        else:
            kb_befreit_calc = kb_befreit[idlaenge].values[0] / 1000
        print(f"KB befreit: {kb_befreit_calc} km")

        # calculate statistics for AmpelcodePers
        ampelcodepers_grouped = gdf_subset.groupby(
            ampelcodepers)[idlaenge].sum().reset_index()
        ampelcodepers_calc = unnest_list(
            ampelcodepers_grouped[idlaenge].values / 1000)
        ampelcodepers_calc_classes = unnest_list(
            ampelcodepers_grouped[ampelcodepers].astype(int).values)
        ampelcodepers_dict = {ampelcodepers_calc_classes[i]: ampelcodepers_calc[i] for i in range(
            len(ampelcodepers_calc_classes))}
        ampelcodepers_dict = {
            f"AmpelcodePers{key}": val for key, val in ampelcodepers_dict.items()}
        beurteilt_pers = \
            ampelcodepers_grouped[
                (ampelcodepers_grouped[''.join(list_to_string_for_df_indexing(ampelcodepers))] == "1") | (
                        ampelcodepers_grouped[''.join(list_to_string_for_df_indexing(ampelcodepers))] == "2") | (
                        ampelcodepers_grouped[
                            ''.join(list_to_string_for_df_indexing(ampelcodepers))] == "3") | (
                        ampelcodepers_grouped[''.join(
                            list_to_string_for_df_indexing(ampelcodepers))] == "4")].sum().values[
                1] / 1000
        zu_beurteilen_pers = total - kb_befreit_calc - beurteilt_pers
        print(f"AmpelcodePers Classes: {ampelcodepers_calc_classes}")
        print(f"AmpelcodePers Values: {ampelcodepers_calc}")
        print(f"Beurteilt AmpelcodePers: {beurteilt_pers} km")
        print(f"Zu beurteilen AmpelcodePers: {zu_beurteilen_pers} km")

        # calculate statistics for AmpelcodeOFG
        ampelcodeofg_grouped = gdf_subset.groupby(
            ampelcodeofg)[idlaenge].sum().reset_index()
        ampelcodeofg_calc = unnest_list(
            ampelcodeofg_grouped[idlaenge].values / 1000)
        ampelcodeofg_calc_classes = unnest_list(
            ampelcodeofg_grouped[ampelcodeofg].astype(int).values)
        ampelcodeofg_dict = {ampelcodeofg_calc_classes[i]: ampelcodeofg_calc[i] for i in range(
            len(ampelcodeofg_calc_classes))}
        ampelcodeofg_dict = {
            f"AmpelcodeOFG{key}": val for key, val in ampelcodeofg_dict.items()}
        beurteilt_ofg = \
            ampelcodeofg_grouped[
                (ampelcodeofg_grouped[''.join(list_to_string_for_df_indexing(ampelcodeofg))] == "1") | (
                        ampelcodeofg_grouped[''.join(list_to_string_for_df_indexing(ampelcodeofg))] == "2") | (
                        ampelcodeofg_grouped[
                            ''.join(list_to_string_for_df_indexing(ampelcodeofg))] == "3") | (
                        ampelcodeofg_grouped[''.join(
                            list_to_string_for_df_indexing(ampelcodeofg))] == "4")].sum().values[
                1] / 1000
        zu_beurteilen_ofg = total - kb_befreit_calc - beurteilt_ofg
        print(f"AmpelcodeOFG Classes: {ampelcodeofg_calc_classes}")
        print(f"AmpelcodeOFG Values: {ampelcodeofg_calc}")
        print(f"Beurteilt AmpelcodeOFG: {beurteilt_pers} km")
        print(f"Zu beurteilen AmpelcodeOFG: {zu_beurteilen_ofg} km")

        # calculate statistics for AmpelcodeGW
        ampelcodegw_grouped = gdf_subset.groupby(
            ampelcodegw)[idlaenge].sum().reset_index()
        ampelcodegw_calc = unnest_list(
            ampelcodegw_grouped[idlaenge].values / 1000)
        ampelcodegw_calc_classes = unnest_list(
            ampelcodegw_grouped[ampelcodegw].astype(int).values)
        ampelcodegw_dict = {ampelcodegw_calc_classes[i]: ampelcodegw_calc[i] for i in range(
            len(ampelcodegw_calc_classes))}
        ampelcodegw_dict = {
            f"AmpelcodeGW{key}": val for key, val in ampelcodegw_dict.items()}
        beurteilt_gw = \
            ampelcodegw_grouped[
                (ampelcodegw_grouped[''.join(list_to_string_for_df_indexing(ampelcodegw))] == "1") | (
                        ampelcodegw_grouped[''.join(list_to_string_for_df_indexing(ampelcodegw))] == "2") | (
                        ampelcodegw_grouped[
                            ''.join(list_to_string_for_df_indexing(ampelcodegw))] == "3") | (
                        ampelcodegw_grouped[''.join(
                            list_to_string_for_df_indexing(ampelcodegw))] == "4")].sum().values[
                1] / 1000
        zu_beurteilen_gw = total - kb_befreit_calc - beurteilt_gw
        print(f"AmpelcodeGW Classes: {ampelcodegw_calc_classes}")
        print(f"AmpelcodeGW Values: {ampelcodegw_calc}")
        print(f"Beurteilt AmpelcodeGW: {beurteilt_pers} km")
        print(f"Zu beurteilen AmpelcodeGW: {zu_beurteilen_gw} km")

        # summarise statistical results in a dataframe (row)
        df = pd.concat([pd.DataFrame([canton_name_short], columns=['Kanton']),
                        pd.DataFrame([file_format], columns=['Format']),
                        pd.DataFrame([berechnungsintervall], columns=['Berechnungsintervall [m]']),
                        pd.DataFrame([total], columns=['Durchgangsstrasse [km]']),
                        pd.DataFrame([kb_befreit_calc], columns=['KB-befreit [km]']),
                        pd.DataFrame([zu_beurteilen_pers], columns=['Zu beurteilen AmpelcodePers [km]']),
                        pd.DataFrame([beurteilt_pers], columns=['Beurteilt AmpelcodePers [km]']),
                        ], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodepers_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([zu_beurteilen_ofg], columns=['Zu beurteilen AmpelcodeOFG [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([beurteilt_ofg], columns=['Beurteilt AmpelcodeOFG [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodeofg_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([zu_beurteilen_gw], columns=['Zu beurteilen AmpelcodeGW [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([beurteilt_gw], columns=['Beurteilt AmpelcodeGW [km]'])], axis=1)
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
        df = pd.read_excel(xlsx_file, skiprows=2)
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
        print(f"Number of columns (initial dataset): {len(gdf.columns)}")

        if not os.path.exists(workingdir + '/Data/XLSX_GPKG_EXPORT_ALL/'):
            os.makedirs(os.path.join(workingdir + '/Data/XLSX_GPKG_EXPORT_ALL/'))
        # gdf.to_file(os.path.join(workingdir, 'Data/XLSX_GPKG_EXPORT_ALL/'+xlsx_file.stem+'.gpkg'), driver='GPKG')

        filter_list = ['Inhaber', 'IDLaenge', 'KBfrei', 'AmpelCodePers', 'AmpelCodeOFG', 'AmpelCodeGW', 'geometry']
        gdf_subset = gdf[filter_list]
        canton_name_short = gdf_subset['Inhaber'].values[0]
        gdf_subset = gdf_subset.drop(gdf_subset.columns[[0]], axis=1)
        gdf_subset['Kanton'] = canton_name_short
        gdf_subset['Format'] = "XLSX"
        file_format = "XLSX"
        unique_value_idlaenge = gdf_subset['IDLaenge'].unique()
        if len(unique_value_idlaenge) == 1:
            berechnungsintervall = gdf_subset['IDLaenge'][0]
        else:
            berechnungsintervall = "variabel"
        gdf_subset['Berechnungsintervall'] = berechnungsintervall
        gdf_subset.drop(gdf_subset.columns[[0]], axis=1)
        cols = gdf_subset.columns.tolist()
        cols = cols[-3:] + cols[:-3]
        gdf_subset = gdf_subset[cols]
        print(f"Columns of subset: {len(gdf_subset.columns)}")
        if len(gdf_subset.columns) != 9:
            print(
                "File will not be analysed as used file has a geodatamodel with version < V2_0 (Hint: check if field "
                "IDLaenge exists in dataset")
            print("___________________________________________________")
            continue
        if not os.path.exists(workingdir + '/Data/XLSX_GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/XLSX_GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(workingdir, 'Data/XLSX_GPKG_EXPORT_SUBSET/' + xlsx_file.stem + '.gpkg'),
                           driver='GPKG')
        if not os.path.exists(workingdir + '/Data/RESULTS/GPKG_EXPORT_SUBSET/'):
            os.makedirs(os.path.join(workingdir + '/Data/RESULTS/GPKG_EXPORT_SUBSET/'))
        gdf_subset.to_file(os.path.join(workingdir, 'Data/RESULTS/GPKG_EXPORT_SUBSET/' + xlsx_file.stem + '.gpkg'),
                           driver='GPKG')

        # calculate total of kilometer Durchgangsstrasse
        total = gdf_subset.IDLaenge.sum() / 1000
        print(f"Total Durchgangsstrasse: {total} [km]")

        # calculate total KB befreit
        kbfrei_grouped = gdf_subset.groupby('KBfrei')['IDLaenge'].sum().reset_index()
        print(kbfrei_grouped)
        kb_befreit = kbfrei_grouped[kbfrei_grouped['KBfrei'] == 'True']
        if kb_befreit.empty:
            kb_befreit_calc = 0
        else:
            kb_befreit_calc = kb_befreit.IDLaenge.values[0] / 1000
        print(f"KB befreit: {kb_befreit_calc} km")

        # calculate statistics for AmpelcodePers
        ampelcodepers_grouped = gdf_subset.groupby(['AmpelCodePers'])['IDLaenge'].sum().reset_index()
        ampelcodepers_calc = ampelcodepers_grouped['IDLaenge'].values / 1000
        ampelcodepers_calc_classes = ampelcodepers_grouped['AmpelCodePers'].astype(int).values
        ampelcodepers_dict = {ampelcodepers_calc_classes[i]: ampelcodepers_calc[i] for i in
                              range(len(ampelcodepers_calc_classes))}
        ampelcodepers_dict = {f"AmpelcodePers{key}": val for key, val in ampelcodepers_dict.items()}
        beurteilt_pers = ampelcodepers_grouped[(ampelcodepers_grouped['AmpelCodePers'] == 1) |
                                               (ampelcodepers_grouped['AmpelCodePers'] == 2) |
                                               (ampelcodepers_grouped['AmpelCodePers'] == 3) |
                                               (ampelcodepers_grouped['AmpelCodePers'] == 4)
                         ].sum().values[1] / 1000
        zu_beurteilen_pers = total - kb_befreit_calc - beurteilt_pers
        print(f"AmpelcodePers Classes: {ampelcodepers_calc_classes}")
        print(f"AmpelcodePers Values: {ampelcodepers_calc}")
        print(f"Beurteilt AmpelcodePers: {beurteilt_pers} km")
        print(f"Zu beurteilen AmpelcodePers: {zu_beurteilen_pers} km")

        # calculate statistics for AmpelcodeOFG
        ampelcodeofg_grouped = gdf_subset.groupby(['AmpelCodeOFG'])['IDLaenge'].sum().reset_index()
        ampelcodeofg_calc = ampelcodeofg_grouped['IDLaenge'].values / 1000
        ampelcodeofg_calc_classes = ampelcodeofg_grouped['AmpelCodeOFG'].astype(int).values
        ampelcodeofg_dict = {ampelcodeofg_calc_classes[i]: ampelcodeofg_calc[i] for i in
                              range(len(ampelcodeofg_calc_classes))}
        ampelcodeofg_dict = {f"AmpelcodeOFG{key}": val for key, val in ampelcodeofg_dict.items()}
        beurteilt_ofg = ampelcodeofg_grouped[(ampelcodeofg_grouped['AmpelCodeOFG'] == 1) |
                                               (ampelcodeofg_grouped['AmpelCodeOFG'] == 2) |
                                               (ampelcodeofg_grouped['AmpelCodeOFG'] == 3) |
                                               (ampelcodeofg_grouped['AmpelCodeOFG'] == 4)
                         ].sum().values[1] / 1000
        zu_beurteilen_ofg = total - kb_befreit_calc - beurteilt_ofg
        print(f"AmpelcodeOFG Classes: {ampelcodeofg_calc_classes}")
        print(f"AmpelcodeOFG Values: {ampelcodeofg_calc}")
        print(f"Beurteilt AmpelcodeoOFG: {beurteilt_ofg} km")
        print(f"Zu beurteilen AmpelcodeOFG: {zu_beurteilen_ofg} km")

        # calculate statistics for AmpelcodeGW
        ampelcodegw_grouped = gdf_subset.groupby(['AmpelCodeGW'])['IDLaenge'].sum().reset_index()
        ampelcodegw_calc = ampelcodegw_grouped['IDLaenge'].values / 1000
        ampelcodegw_calc_classes = ampelcodegw_grouped['AmpelCodeGW'].astype(int).values
        ampelcodegw_dict = {ampelcodegw_calc_classes[i]: ampelcodegw_calc[i] for i in
                              range(len(ampelcodegw_calc_classes))}
        ampelcodegw_dict = {f"AmpelcodeGW{key}": val for key, val in ampelcodegw_dict.items()}
        beurteilt_gw = ampelcodegw_grouped[(ampelcodegw_grouped['AmpelCodeGW'] == 1) |
                                               (ampelcodegw_grouped['AmpelCodeGW'] == 2) |
                                               (ampelcodegw_grouped['AmpelCodeGW'] == 3) |
                                               (ampelcodegw_grouped['AmpelCodeGW'] == 4)
                         ].sum().values[1] / 1000
        zu_beurteilen_gw = total - kb_befreit_calc - beurteilt_gw
        print(f"AmpelcodeGW Classes: {ampelcodegw_calc_classes}")
        print(f"AmpelcodeGW Values: {ampelcodegw_calc}")
        print(f"Beurteilt AmpelcodeoGW: {beurteilt_gw} km")
        print(f"Zu beurteilen AmpelcodeGW: {zu_beurteilen_gw} km")

        # summarise statistical results in a dataframe (row)
        df = pd.concat([pd.DataFrame([canton_name_short], columns=['Kanton']),
                        pd.DataFrame([file_format], columns=['Format']),
                        pd.DataFrame([berechnungsintervall], columns=['Berechnungsintervall [m]']),
                        pd.DataFrame([total], columns=['Durchgangsstrasse [km]']),
                        pd.DataFrame([kb_befreit_calc], columns=['KB-befreit [km]']),
                        pd.DataFrame([zu_beurteilen_pers], columns=['Zu beurteilen AmpelcodePers [km]']),
                        pd.DataFrame([beurteilt_pers], columns=['Beurteilt AmpelcodePers [km]']),
                        ], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodepers_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([zu_beurteilen_ofg], columns=['Zu beurteilen AmpelcodeOFG [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([beurteilt_ofg], columns=['Beurteilt AmpelcodeOFG [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodeofg_dict])], axis=1)
        df = pd.concat([df, pd.DataFrame([zu_beurteilen_gw], columns=['Zu beurteilen AmpelcodeGW [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([beurteilt_gw], columns=['Beurteilt AmpelcodeGW [km]'])], axis=1)
        df = pd.concat([df, pd.DataFrame([ampelcodegw_dict])], axis=1)
        df_results = pd.concat([df_results, df], axis=0)
        print("___________________________________________________")

    if not os.path.exists(os.path.join(workingdir, 'Data', 'RESULTS')):
        os.makedirs(os.path.join(workingdir, 'Data', 'RESULTS'))
    df_results.to_excel(excel_export_path, index=False)


def combine_results_xlsx(result_files, excel_export_path):
    """Combine excel files in a directory into one and sort them according to predefined colum order

    Args:
        result_files (List): List containing the paths to the Excel files to combine
        excel_export_path (string): Path where the excel file containing the statistics is saved to
    """
    import pandas as pd

    excl_list = []
    for file in result_files:
        excl_list.append(pd.read_excel(file))
    excl_merged = pd.DataFrame()
    for excl_file in excl_list:
        # appends the data into the excl_merged
        # dataframe.
        excl_merged = excl_merged.append(excl_file, ignore_index=True)
    # sort columns
    columns_sorted = ['Kanton', 'Format', 'Berechnungsintervall [m]', 'Durchgangsstrasse [km]', 'KB-befreit [km]',
     'Zu beurteilen AmpelcodePers [km]', 'Beurteilt AmpelcodePers [km]', 'AmpelcodePers0', 'AmpelcodePers1',
     'AmpelcodePers2', 'AmpelcodePers3', 'AmpelcodePers4', 'AmpelcodePers5', 'Zu beurteilen AmpelcodeOFG [km]',
     'Beurteilt AmpelcodeOFG [km]', 'AmpelcodeOFG0', 'AmpelcodeOFG1', 'AmpelcodeOFG2', 'AmpelcodeOFG3', 'AmpelcodeOFG4',
     'AmpelcodeOFG5', 'Zu beurteilen AmpelcodeGW [km]', 'Beurteilt AmpelcodeGW [km]', 'AmpelcodeGW0', 'AmpelcodeGW1',
     'AmpelcodeGW2', 'AmpelcodeGW3', 'AmpelcodeGW4', 'AmpelcodeGW5']
    excl_merged = excl_merged.reindex(columns = columns_sorted)
    excl_merged.to_excel(excel_export_path, index=False)


def combine_gpkgs(gpkg_result_dir, gpkg_out_path):
    """Combines mutiple geopackage into one dataset (.gpkgs need to have the same structure)

        Args:
            gpkg_results_dir (string): Path to the folder location of the GPKG files to merge
    """
    import pandas as pd
    import geopandas as gpd
    gpkg_result_files = list_file_paths(gpkg_result_dir, "*.gpkg")
    gdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(i) for i in gpkg_result_files],
                                     ignore_index=True), crs=gpd.read_file(gpkg_result_files[0]).crs)
    gdf.to_file(gpkg_out_path, driver='GPKG')


def main():
    warnings.filterwarnings("ignore")

    # execute the script

    # calculate the statistics from ILI files (only compatible with model version >2_0)
    gpkg_dir = r'Data/ILI_GPKG_CONVERT/'
    calculate_statistics_from_ili_gpkg(gpkg_dir, excel_export_path=r'Data/RESULTS/ILI_GPKG_STATISTICS.xlsx')

    xlsx_dir = r'Data/XLSX_CORRECTED/'
    calculate_statistics_from_xlsx_file(xlsx_dir, excel_export_path=r'Data/RESULTS/XLSX_GPKG_STATISTICS.xlsx')

    # combine two Excel files into one
    result_files = ['Data/RESULTS/ILI_GPKG_STATISTICS.xlsx', 'Data/RESULTS/XLSX_GPKG_STATISTICS.xlsx']
    combine_results_xlsx(result_files, excel_export_path='Data/RESULTS/ERKAS_Strassen_Analyse_2021.xlsx')

    # write a combined .gpkg of all processed files
    print("Write combined .gpkg file for entire Switzerland")
    gpkg_result_dir = r'O:\GIS\GEP\RLS\_Mitarbeitende\DF2020\ERKAS-processing\Data\RESULTS\GPKG_EXPORT_SUBSET'
    gpkg_out_path = r'Data/RESULTS/ERKAS_Strassen_2021_CH.gpkg'
    combine_gpkgs(gpkg_result_dir, gpkg_out_path)

if __name__ == main():
    main()
