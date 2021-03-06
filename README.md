# ERKAS-processing
This repository contains the code to process cantonal ERKAS data.

## Setup python environment with conda

Use the environment.yml file to setup your conda environment in a terminal.

```bash
conda env create --file environment.yml
```
# ILI XTF Files
ILI XTF files were opened in QGIS. The different layers were joined (Layer Properties/Joins) with tables 
_Verkehrsaufkommen_, _Vollzug_ and _Ergebnis_. The resulting layer was exported as .gpkg file.
## Open issues
- GR and SG do not have AmpelCodes in ILI files. Exported to Excel and sent to CI for clarification.


## Changelog for ILI GPKG files:
The following changes were performed on ILI GPKG files.
- AG: Added field _IDLaenge_ with a length of 10 m in QGIS.
- BE: Added field _IDLaenge_ with a length of 10 m in QGIS.
- GR: Added field _IDLaenge_ with a length of 100 m in QGIS.
- SG: Added field _IDLaenge_ with a length of 100 m in QGIS.
- SO: Added field _IDLaenge_ with a length of 10 m in QGIS.
- TI: Added field _IDLaenge_ with a length of 10 m in QGIS.
- BL: Manually removed two additional layers in QGIS. 

# XLSX Files

## Open issues
- UR: column IDLaenge is not included in the file, quick fix: measured segment length in QGIS and added three resulting values of 803.047 m, 697.106 m and 594.919 m to the xlsx file. Last point was set to 0 m.
  
## Changelog for values in column _KBfrei_ 
The following changes were performed on XLSX files in the column _KBfrei_ in Microsoft Excel:

(default: True/False)
- FR: TRUE/FALSE to True/False
- GE: TRUE/FALSE to True/False
- JU: TRUE/FALSE to True/False
- NE: N to False
- BS: nein to False
- NW: ja/nein to True/False
- OW: ja/nein to True/False
- SZ: ja/nein to True/False
- UR: false to False
- ZG: nein to False
- ZH: false to False

## Changelog for values in column _Ampelwerte_:
The following changes were performed on XLSX files in the column _Ampelwerte_ in Microsoft Excel:
- GE: emptied nul and Nul values

## Changelog vor values in column _IDLaenge_
The following changes were performed on XLSX files in the column _IDLaenge_ in Microsoft Excel:
- OW: multiplied column by value 1000 to get km

## Changelog for values in coordinates:
- GE: swapped easting and northing coordinates
- FR: swapped easting and northing coordinates 
- SZ: swapped easting and northing coordinates 
- VD: swapped easting and northing coordinates


## Structural changelog
The following structural changes were made directly in the XLSX files:
- JU: adjusted header to french header template and added empty field _ASKLSMineraloel_
- VS: adjusted header to french header template
  VD: changed value of field _Inhaber_ from CH22 to VD
- BL: deleted comment at the end of the document
- NW: deleted comment at the end of the document, deleted Aussschlusskriterien gem??ss Screening-Methodik EBP (columns AM ff.), changed field name from IDL??nge to _IDLaenge_
- OW: deleted comment at the end of the document, deleted Aussschlusskriterien gem??ss Screening-Methodik EBP (columns AM ff.)
- SZ: deleted field _DTV_ (Analyse EBP is kept) and _DTV Faktor_, changed value of field _Inhaber_ from CH-SZ to SZ
- SH: deleted hidden tab with screening results from EBP, changed value of field _Inhaber_ from CH-SH to SH
- UR: adjusted header to german header template
- ZH: adjusted header to german header template




