# ERKAS-processing
This repository contains the code to process cantonal ERKAS data.

## Setup python environment with conda

Use the environment.yml file to setup your conda environment in a terminal.

```bash
conda env create --file environment.yml
```
# ILI XTF Files
## Issues

- GR and SG do not have AmpelCodes in ILI files.

- AG, BE, SO and TI do not have field _IDLaenge_.

- BL (manually removed two additional files), LU and TG fullfill all conditions. 

```txt
Processing: ERKAS_Strassen_AG_2021
Number of points: 61475
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
___________________________________________________
Processing: ERKAS_Strassen_TI_2021
Number of points: 5963
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
___________________________________________________
Processing: ERKAS_Strassen_SO_2021
Number of points: 25828
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
___________________________________________________
Processing: ERKAS_Strassen_BE_2021
Number of points: 133369
Coordinate system: EPSG:2056
Number of columns (intial dataset): 23
Columns of subset: 6
___________________________________________________
Processing: ERKAS_Strassen_LU_2021
Number of points: 36618
Coordinate system: EPSG:2056
Number of columns (intial dataset): 32
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 365.898
KB befreit: 0
Ampelcode Pers Classes: [1, 2, 3, 4, 5]
Ampelcode Pers: [346.457, 8.952, 7.513, 2.971, 0.005]
Ampelcode OFG Classes: [1, 2, 3, 5]
Ampelcode OFG: [343.37, 8.133, 14.39, 0.005]
Ampelcode GW Classes: [1, 3, 4, 5]
Ampelcode GW: [344.948, 4.605, 16.34, 0.005]
___________________________________________________
Processing: ERKAS_Strassen_SG_2021
Number of points: 4697
Coordinate system: EPSG:2056
Number of columns (intial dataset): 27
Columns of subset: 3
___________________________________________________
Processing: ERKAS_Strassen_TG_2021
Number of points: 34460
Coordinate system: EPSG:2056
Number of columns (intial dataset): 32
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 344.233
KB befreit: 0
Ampelcode Pers Classes: [1, 2, 3, 4, 5]
Ampelcode Pers: [333.885, 6.685, 1.66, 0.54, 1.463]
Ampelcode OFG Classes: [1, 2, 3, 5]
Ampelcode OFG: [335.28, 5.345, 2.145, 1.463]
Ampelcode GW Classes: [1, 3, 4, 5]
Ampelcode GW: [284.425, 2.928, 55.417, 1.463]
___________________________________________________
Processing: ERKAS_Strassen_GR_2021
Number of points: 7311
Coordinate system: EPSG:2056
Number of columns (intial dataset): 15
Columns of subset: 3
___________________________________________________
Processing: ERKAS_Strassen_BL_2021
Number of points: 1161
Coordinate system: EPSG:2056
Number of columns (intial dataset): 34
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 176.2151
KB befreit: 0
Ampelcode Pers Classes: [1, 2]
Ampelcode Pers: [162.7862, 13.4289]
Ampelcode OFG Classes: [1, 2, 3]
Ampelcode OFG: [131.8565, 26.0675, 18.2911]
Ampelcode GW Classes: [1, 3, 4]
Ampelcode GW: [169.27870000000001, 2.9284, 4.008]
___________________________________________________
````

# XLSX Files Blablaba

Changelog for values in column _KBfrei_ (default: True/False)
- FR: TRUE/FALSE to True/False
- GE: TRUE/FALSE to True/False
- JU: TRUE/FALSE to True/False: header differs
- NE: N to False
- VD: no changes
- VS: no changes: header differs
- BS: nein to False
- NW: ja/nein to True/False
- OW: ja/nein to True/False
- SH: no changes
- SZ: ja/nein to True/False
- UR: false to False: header differs
- ZG: nein to False
- ZH: false to False: header differs

Changelog for values in column _Ampelwerte_:
- GE: emptied nul and Nul values

Changelog vor values in column _IDLaenge_
- OW: multiplied column by value 1000 to get km
- UR: column IDLaenge is missing

Structural changelog
- JU: adjusted header to french header template and added empty field _ASKLSMineraloel_
- VS: adjusted header to french header template
  VD: changed value of field _Inhaber_ from CH22 to VD
- BL: deleted comment at the end of the document
- NW: deleted comment at the end of the document, deleted Aussschlusskriterien gemäss Screening-Methodik EBP (columns AM ff.), changed field name from IDLänge to _IDLaenge_
- OW: deleted comment at the end of the document, deleted Aussschlusskriterien gemäss Screening-Methodik EBP (columns AM ff.)
- SZ: deleted field _DTV_ (Analyse EBP is kept) and _DTV Faktor_, changed value of field _Inhaber_ from CH-SZ to SZ
- SH: deleted hidden tab with screening results from EBP, changed value of field _Inhaber_ from CH-SH to SH
- UR: adjusted header to german header template
- ZH: adjusted header to german header template

````txt
Processing: ERKAS_Strassen_AG_2021
Number of points: 61475
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: ERKAS_Strassen_BE_2021
Number of points: 133369
Coordinate system: EPSG:2056
Number of columns (intial dataset): 23
Columns of subset: 6
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: ERKAS_Strassen_BL_2021
Number of points: 1161
Coordinate system: EPSG:2056
Number of columns (intial dataset): 34
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 176.2151
  ERKAS_Strassen_Kataster_LV95_V2_0.ERKAS_Strassen_Kataster.Vollzug_KBfrei  IDLaenge
0                                              false                        176215.1
KB befreit: 0
Ampelcode Pers Classes: [1, 2]
Ampelcode Pers: [162.7862, 13.4289]
Ampelcode OFG Classes: [1, 2, 3]
Ampelcode OFG: [131.8565, 26.0675, 18.2911]
Ampelcode GW Classes: [1, 3, 4]
Ampelcode GW: [169.27870000000001, 2.9284, 4.008]
___________________________________________________
Processing: ERKAS_Strassen_GR_2021
Number of points: 7311
Coordinate system: EPSG:2056
Number of columns (intial dataset): 15
Columns of subset: 3
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: ERKAS_Strassen_LU_2021
Number of points: 36618
Coordinate system: EPSG:2056
Number of columns (intial dataset): 32
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 365.898
  ERKAS_Strassen_Kataster_LV95_V2_0.ERKAS_Strassen_Kataster.Vollzug_KBfrei  IDLaenge
0                                              false                          365898
KB befreit: 0
Ampelcode Pers Classes: [1, 2, 3, 4, 5]
Ampelcode Pers: [346.457, 8.952, 7.513, 2.971, 0.005]
Ampelcode OFG Classes: [1, 2, 3, 5]
Ampelcode OFG: [343.37, 8.133, 14.39, 0.005]
Ampelcode GW Classes: [1, 3, 4, 5]
Ampelcode GW: [344.948, 4.605, 16.34, 0.005]
___________________________________________________
Processing: ERKAS_Strassen_SG_2021
Number of points: 4697
Coordinate system: EPSG:2056
Number of columns (intial dataset): 27
Columns of subset: 3
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: ERKAS_Strassen_SO_2021
Number of points: 25828
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: ERKAS_Strassen_TG_2021
Number of points: 34460
Coordinate system: EPSG:2056
Number of columns (intial dataset): 32
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 344.233
  ERKAS_Strassen_Kataster_LV95_V2_0.ERKAS_Strassen_Kataster.Vollzug_KBfrei  IDLaenge
0                                              false                          344233
KB befreit: 0
Ampelcode Pers Classes: [1, 2, 3, 4, 5]
Ampelcode Pers: [333.885, 6.685, 1.66, 0.54, 1.463]
Ampelcode OFG Classes: [1, 2, 3, 5]
Ampelcode OFG: [335.28, 5.345, 2.145, 1.463]
Ampelcode GW Classes: [1, 3, 4, 5]
Ampelcode GW: [284.425, 2.928, 55.417, 1.463]
___________________________________________________
Processing: ERKAS_Strassen_TI_2021
Number of points: 5963
Coordinate system: EPSG:2056
Number of columns (intial dataset): 31
Columns of subset: 6
Will not be analysed as used file has a geodatamodel with version <2_0 (Hint: check if field IDLaenge exists in dataset
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_FR_2021.xlsx
Number of points: 6619
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 457.403
  KBfrei IDLaenge
0  False   240023
1   True   217380
1
KB befreit: 217.38
Ampelcode Pers Classes: [1 2]
Ampelcode Pers: [220.34 19.683]
Ampelcode OFG Classes: [1 2 3]
Ampelcode OFG: [35.251 36.029 168.743]
Ampelcode GW Classes: [1 2 3 4]
Ampelcode GW: [204.123 10.941 18.39 6.569]
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_GE_2021.xlsx
Number of points: 1402
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 140.2
  KBfrei IDLaenge
0  False   132400
1   True     7800
1
KB befreit: 7.8
Ampelcode Pers Classes: [0 1 2 3 4]
Ampelcode Pers: [7.8 31.8 19.1 1.7 0.5]
Ampelcode OFG Classes: [0 1 2 3 4]
Ampelcode OFG: [6.6 11.3 42.1 27.7 1.5]
Ampelcode GW Classes: [0 1 4]
Ampelcode GW: [6.6 66.6 0.5]
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_JU_2021.xlsx
Number of points: 2783
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 278.3
  KBfrei IDLaenge
0  False     7800
1   True   270500
1
KB befreit: 270.5
Ampelcode Pers Classes: [0]
Ampelcode Pers: [7.8]
Ampelcode OFG Classes: [0]
Ampelcode OFG: [7.8]
Ampelcode GW Classes: [0]
Ampelcode GW: [7.8]
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_NE_2021.xlsx
Number of points: 1482
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 212.1
  KBfrei IDLaenge
0  False   212100
0
KB befreit: 0
Ampelcode Pers Classes: [0 1 2]
Ampelcode Pers: [101.0 8.9 5.0]
Ampelcode OFG Classes: [0 1 3]
Ampelcode OFG: [101.0 5.9 8.0]
Ampelcode GW Classes: [0 1]
Ampelcode GW: [101.0 13.9]
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_VD_2017.xlsx
Number of points: 11517
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 1151.7
  KBfrei IDLaenge
0  False   523800
1   True   627900
1
KB befreit: 627.9
Ampelcode Pers Classes: [0]
Ampelcode Pers: [523.8]
Ampelcode OFG Classes: [0]
Ampelcode OFG: [523.8]
Ampelcode GW Classes: [0]
Ampelcode GW: [523.8]
___________________________________________________
Processing: Data\XLSX_CORRECTED\CARAM_routes_VS_2021.xlsx
Number of points: 5086
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 481.863
  KBfrei IDLaenge
0  False   235586
1   True   246277
1
KB befreit: 246.277
Ampelcode Pers Classes: [0 1 2]
Ampelcode Pers: [232.271 1.633 1.682]
Ampelcode OFG Classes: [0]
Ampelcode OFG: [235.586]
Ampelcode GW Classes: [0 2]
Ampelcode GW: [234.486 1.1]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_BS_2021.xlsx
Number of points: 30
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 19.057
  KBfrei IDLaenge
0  False    19057
0
KB befreit: 0
Ampelcode Pers Classes: [1 2 3]
Ampelcode Pers: [0.731 8.538 9.788]
Ampelcode OFG Classes: [1 2 3]
Ampelcode OFG: [11.491 5.082 2.484]
Ampelcode GW Classes: [1 3]
Ampelcode GW: [18.411 0.646]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_NW_2017.xlsx
Number of points: 99
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 49.5
  KBfrei IDLaenge
0  False    22500
1   True    27000
1
KB befreit: 27.0
Ampelcode Pers Classes: [0]
Ampelcode Pers: [22.5]
Ampelcode OFG Classes: [0]
Ampelcode OFG: [22.5]
Ampelcode GW Classes: [0]
Ampelcode GW: [22.5]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_OW_2021.xlsx
Number of points: 87
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 60.795
  KBfrei IDLaenge
0  False    12418
1   True  48377.0
1
KB befreit: 48.377
Ampelcode Pers Classes: [1]
Ampelcode Pers: [12.418]
Ampelcode OFG Classes: [0 1]
Ampelcode OFG: [10.764 1.654]
Ampelcode GW Classes: [0 1]
Ampelcode GW: [1.593 10.825]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_SH_2021.xlsx
Number of points: 828
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 82.8
  KBfrei IDLaenge
0  False    35200
1   True    47600
1
KB befreit: 47.6
Ampelcode Pers Classes: [1 2 3]
Ampelcode Pers: [79.8 2.7 0.3]
Ampelcode OFG Classes: [0 1 2 3]
Ampelcode OFG: [36.6 9.4 14.7 22.1]
Ampelcode GW Classes: [0 3 4]
Ampelcode GW: [82.0 0.3 0.5]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_SZ_2021.xlsx
Number of points: 304
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 30.34
  KBfrei IDLaenge
0  False    30340
0
KB befreit: 0
Ampelcode Pers Classes: [1]
Ampelcode Pers: [30.34]
Ampelcode OFG Classes: [1 2 3]
Ampelcode OFG: [1.8 3.5 25.04]
Ampelcode GW Classes: [0 2 3 4]
Ampelcode GW: [26.94 0.8 1.0 1.6]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_ZG_2021.xlsx
Number of points: 754
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 75.626
  KBfrei IDLaenge
0  False    75626
0
KB befreit: 0
Ampelcode Pers Classes: [0 1 2]
Ampelcode Pers: [3.177 53.817 13.753]
Ampelcode OFG Classes: [0 1]
Ampelcode OFG: [3.177 67.57]
Ampelcode GW Classes: [0 1 2]
Ampelcode GW: [7.6 66.131 1.582]
___________________________________________________
Processing: Data\XLSX_CORRECTED\ERKAS_Strassen_ZH_2021.xlsx
Number of points: 67584
Coordinate system: epsg:2056
Number of columns (intial dataset): 38
Columns of subset: 7
Total Anzahl Kilometer Durchgangsstrasse: 675.84
  KBfrei IDLaenge
0  False   387280
1   True   288560
1
KB befreit: 288.56
Ampelcode Pers Classes: [1 2 3 4]
Ampelcode Pers: [344.8 31.34 10.68 0.46]
Ampelcode OFG Classes: [0]
Ampelcode OFG: [387.29]
Ampelcode GW Classes: [0]
Ampelcode GW: [387.29]
___________________________________________________

````



