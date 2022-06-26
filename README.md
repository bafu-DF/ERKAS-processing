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
Number of columns: 31
Columns of subset: 5
_________________
Processing: ERKAS_Strassen_TI_2021
Number of points: 5963
Coordinate system: EPSG:2056
Number of columns: 31
Columns of subset: 5
_________________
Processing: ERKAS_Strassen_SO_2021
Number of points: 25828
Coordinate system: EPSG:2056
Number of columns: 31
Columns of subset: 5
_________________
Processing: ERKAS_Strassen_BE_2021
Number of points: 133369
Coordinate system: EPSG:2056
Number of columns: 23
Columns of subset: 5
_________________
Processing: ERKAS_Strassen_LU_2021
Number of points: 36618
Coordinate system: EPSG:2056
Number of columns: 32
Columns of subset: 6
_________________
Processing: ERKAS_Strassen_SG_2021
Number of points: 4697
Coordinate system: EPSG:2056
Number of columns: 27
Columns of subset: 2
_________________
Processing: ERKAS_Strassen_TG_2021
Number of points: 34460
Coordinate system: EPSG:2056
Number of columns: 32
Columns of subset: 6
_________________
Processing: ERKAS_Strassen_GR_2021
Number of points: 7311
Coordinate system: EPSG:2056
Number of columns: 15
Columns of subset: 2
_________________
Processing: ERKAS_Strassen_BL_2021
Number of points: 1161
Coordinate system: EPSG:2056
Number of columns: 34
Columns of subset: 6
_________________
````

