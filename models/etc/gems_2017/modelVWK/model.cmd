del vegLa.map regLa.map tmp.map tmp.tif cloneLa.map demLa.map vegLa.tif regLa.tif
PATH=%PATH%;%cd%\gdal\bin;%cd%\gdal\bin\gdal\apps;

rem generate empty .map based on DEM
gdal_translate -scale 9999 9999 0 0 -a_nodata 0 DEM_Fieldwork-France.img tmp.tif
rem convert tmp.map to .tif
gdal_translate -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 tmp.tif tmp.map

rem convert dem to .map
gdal_translate -of PCRaster -co "PCRASTER_VALUESCALE=VS_SCALAR" -ot Float32 DEM_Fieldwork-France.img demLa.map

rem convert polygons to raster maps
rem 1) copy dummy map
copy tmp.tif vegLa.tif
copy tmp.tif regLa.tif

rem 2) burn in vector maps
gdal_rasterize -a class -l vegetation vegetation.sqlite vegLa.tif
gdal_rasterize -a class -l regolith regolith.sqlite regLa.tif

rem 3) convert to .map
gdal_translate -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 vegLa.tif vegLa.map
gdal_translate -of PCRaster -co "PCRASTER_VALUESCALE=VS_NOMINAL" -ot Int32 regLa.tif regLa.map

rem generate clone map from reg and veg
pcrcalc cloneLa.map=if(defined(regLa.map) and defined(vegLa.map), boolean(1))

rem contract maps to area with values
resample -c 0 cloneLa.map clone.map
resample vegLa.map veg.map --clone clone.map
resample regLa.map reg.map --clone clone.map
resample demLa.map tmp.map --clone clone.map
pcrcalc dem.map=if(clone.map,tmp.map)

del vegLa.map regLa.map vegLa.tif regLa.tif tmp.map tmp.tif cloneLa.map demLa.map
del *.aux.xml

rem run model
rem pcrcalc -f runoff.mod
rem pcrcalc -f erosion.mod

pause
