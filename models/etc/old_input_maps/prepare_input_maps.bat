
REM clean any existing map files
del *.map

REM convert DEM in *.tif to pcraster map using pcrcalc
REM TODO: Fixing the dem in *.tif (current issue: pixel sizes in x and y directions are not the same). 
REM - Currently, we just use/copy the existing one.
copy ldd_and_dem_version_2017_03_27_from_wiebe\dem_10m.map dem_10m.map
REM - making sure that the pcraster projection is "yb2t" (as commonly used). 
mapattr -s -P yb2t dem_10m.map

REM making the clone map based on DEM
pcrcalc --clone dem_10m.map clone.map = "boolean(1.0)"

REM creating ldd based on DEM
REM TODO: Get the parameter values for lddcreatedem from Wiebe.
REM - Currently, we just use/copy the existing one.
copy ldd_and_dem_version_2017_03_27_from_wiebe\ldd.map ldd.map

REM convert vegetation and regional classes in *.tif to pcraster files (nominal)
pcrcalc regolith.map = "nominal(regolith.tif)"
REM making sure that the map have the same mapattr properties as the clone map (particularly -P yb2t)
mapattr -c clone.map regolith.map
pcrcalc vegetation.map = "nominal(regolith.tif)"
REM making sure that the map have the same mapattr properties as the clone map (particularly -P yb2t)
mapattr -c clone.map vegetation.map
REM an extra check by visualizing the files
aguila clone.map regolith.map vegetation.map

pause
