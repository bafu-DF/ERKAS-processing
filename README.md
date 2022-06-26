# ERKAS-processing
This repository contains the code to process cantonal ERKAS data.

## Setup python environment with conda

Use the environment.yml file to setup your conda environment in a terminal.

```bash
conda env create --file environment.yml
```

## Issues

- GR and SGdo not have AmpelCodes in ILI files.

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

