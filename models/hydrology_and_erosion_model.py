#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time as py_time
from pcraster import *

# get the current time (for calculating calculation time needed) 
start_time = py_time.time()

print("Model starts.")


########################################################################
# input values/maps
########################################################################


# clone map: defining the model extent (of study area), including model resolution  
cloneMap = "inputs/clone.map"

# ldd: drainage direction
ldd = "inputs/ldd.map"

# dem: elevation
dem = "inputs/dem_10m.map"


# precipitation
# - typical rainfall intensity (m.hr-1) of the event
precipitationIntensityEvent = 40./1000.
# - duration (hr) of the event
precipitationDuration = 2.0
# - number of rainfall events in a year
numberOfEvents = 10.



# vegetationCode: a map of vegetation units
vegetationCode = nominal("inputs/vegetation.map")
# vegetationTable: a table of vegetation parameters (vegetationCover, leafAreaIndex, canopyCover, groundCover, plantHeight) for each vegetation class/code observed in the field
vegetationTable = "inputs/vegetation_table.txt"
# - see also "inputs/vegetation_table_readme.txt"

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
# - Note: No spatial variation. Hence, we don't have to read it from the table. 
valueForFactorC = 1.0 


# regolithcode: a map of regolith units
regolithCode = nominal("inputs/regolith.map")
# regolithTable: a table of regolith parameters (kSat, cohesion, erodibilityK) observed in the field
regolithTable = "inputs/regolith_table.txt"
# - see also "inputs/regolith_table_readme.txt"


# other input:
# - a maximum (annual) limit of flow/runoff detachment (kg.m-2.year-1) ; needed to mask out unrealitic values (particularly in streams/gullies)
maxLimitDetachmentByRunoff = 999.


########################################################################



########################################################################
# output file names (all in pcraster formats)
########################################################################

# file names for parameters derived during the model calculation
# - slope (m.m-1), estimated from elevation (dem) 
slopeFileName = "outputs/slope_m_per_m.map"
# - kSat: saturated conductivity of the top soil (m.hr-1)
kSatFileName = "outputs/soil_saturated_conductivity_m_per_hour.map"
# - canopyInterceptionCapacity (m)
canopyInterceptionCapacityFileName = "outputs/canopy_interception_capacity_m.map"

# model simulation output file names:
# - annual precipitation (m.year-1)
precipitationYearFileName = "outputs/precipitation_m_per_year.map"
# - annual infiltration (m.year-1)
infiltrationYearFileName = "outputs/infiltration_m_per_year.map"
# - annual local runoff (m.year-1)
localRunoffYearFileName = "outputs/local_runoff_m_per_year.map"
# - annual (accumulated) runoff (m.year-1)
runoffYearFileName = "outputs/runoff_m_per_year.map"
# - annual effective/net rainfall reaching the soil (m.year-1)
effectiveRainfallYearFileName = "outputs/effective_rainfall_m_per_year.map"
# - annual leaf drainage (m.year-1): throughfall through canopy/leaf
leafDrainageYearFileName = "outputs/leaf_drainage_m_per_year.map"
# - annual direct throughfall (m.year-1)
directThroughfallYearFileName = "outputs/direct_throughfall_m_per_year.map"
# - annual detachment by raindrop/splash (kg.m-2.year-1) - not limited by transport capacity
detachmentByRaindropFileName = "outputs/splash_detachment_kg_per_m2_per_year.map"
# - annual detachment by runoff (kg.m-2.year-1) - not limited by transport capacity
detachmentByRunoffFileName = "outputs/flow_detachment_kg_per_m2_per_year.map"
# - annual total detachment (kg.m-2.year-1) - not limited by transport capacity
totalDetachmentFileName = "outputs/total_detachment_kg_per_m2_per_year.map"
# - annual transport capacity (kg.m-2.year-1) 
transportCapacityFileName = "outputs/transport_capacity_kg_per_m2_per_year.map"
# - annual total erosion (kg.m-2.year-1) - limited by transport capacity
erosionFileName = "outputs/erosion_kg_per_m2_per_year.map"

#~ # file names for additional output maps ; Note: Comment (#) signs indicate no active. 
#~ # - vegetationCover (dimensionless, fraction 0 to 1)
#~ vegetationCoverFileName = "outputs/vegetation_cover_fraction.map"
#~ # - leafAreaIndex (m2.m-2)
#~ leafAreaIndexFileName = "outputs/leaf_area_index_m2_per_m2.map"
#~ # - plantHeight (m)
#~ plantHeightFileName = "outputs/plant_height_m.map"
#~ # - canopyCover (dimensionless, fraction 0 to 1)
#~ canopyCoverFileName = "outputs/canopy_cover_fraction.map"
#~ # - groundCover (dimensionless, fraction 0 to 1)
#~ groundCoverFileName = "outputs/ground_cover_fraction.map"
#~ # - factorC: this factor is to take account tillage practices and levels of crop residue retention - needed to estimate transport capacity - Equation 12 in Morgan, 2001
#~ factorCFileName = "outputs/factor_c_transport_capacity.map"
#~ # - cohesion: soil cohesion (unit: kPa) of the soil - symbolyzed as COH in Morgan, 2001
#~ cohesionFileName = "outputs/soil_cohesion_kilo_pascal.map"
#~ # - erodibilityK: erodibility (g.J-1) of the soil - symbolized as K in Morgan, 2001, Equation 9
#~ erodibilityFileName = "outputs/soil_erodibility_gram_per_joule.map"



########################################################################



# set the clone map 
setclone(cloneMap)

# set the mask: area of interest
mask = defined(ldd)



# set the global option to "matrixtable" in order to read the vegetation and regolith parametes from tables in matrix format
# - see http://pcraster.geo.uu.nl/pcraster/4.1.0/doc/manual/op_lookup.html#operation-with-a-matrix-table-with-global-option-matrixtable
setglobaloption("matrixtable")



####### vegetation parameters: vegetationCover, leafAreaIndex, plantHeight, canopyCover, groundCover 
# - All of them are read from a lookup table (vegetationTable) based on the vegetation map (vegetationCode).
############################################################################################################

# proportion of the pixel containing vegetation (dimensionless, fraction 0 to 1) 
vegetationCover = lookupscalar(vegetationTable, 1, vegetationCode)

# leave area index (m2.m-2) 
leafAreaIndex = lookupscalar(vegetationTable, 2, vegetationCode)

# plant height (m)
# - representing the height from which raindrops fall from the crop or vegetation cover to the ground surface
# - needed for estimating kinematic energy,
plantHeight = lookupscalar(vegetationTable, 3, vegetationCode)

# proportion/fraction of canopy cover within a cell (dimensionless, fraction 0 to 1)
canopyCover = lookupscalar(vegetationTable, 4, vegetationCode)

# ground cover percentage (dimensionless, fraction 0 to 1)
groundCover = lookupscalar(vegetationTable, 5, vegetationCode)


####### regolith parameters: kSat, cohesion, erodibilityK, factorC 
# - Except factorC, all would be read from a lookup table (regolithTable) based on the regolith map (regolithCode).
# - Note that the factorC is defined above (see the variable: valueForFactorC). 
###################################################################################################################

# saturated conductivity of the top soil (m.hr-1), needed for estimating infiltration capacity
kSat = lookupscalar(regolithTable, 1, regolithCode)  

# soil cohesion (unit: kPa) of the soil - symbolyzed as COH in Morgan, 2001
cohesion = lookupscalar(regolithTable, 2, regolithCode)

# erodibility (g.J-1) of the soil (symbolized as K in Morgan, 2001, Equation 9)
erodibilityK = lookupscalar(regolithTable, 3, regolithCode)

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account different tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
factorC = spatial(scalar(valueForFactorC))

# reporting/saving kSat to a pcraster file (and display it via aguila)
report(kSat, kSatFileName)
#~ aguila(kSatFileName)

#~ # reporting/saving model (e.g. vegetation and regolith) parameters to pcraster files (and displaying them via aguila)
#~ report(vegetationCover, vegetationCoverFileName)
#~ aguila(vegetationCoverFileName)
#~ report(leafAreaIndex, leafAreaIndexFileName)
#~ aguila(leafAreaIndexFileName)
#~ report(plantHeight, plantHeightFileName)
#~ aguila(plantHeightFileName)
#~ report(canopyCover, canopyCoverFileName)
#~ aguila(canopyCoverFileName)
#~ report(groundCover, groundCoverFileName)
#~ aguila(groundCoverFileName)
#~ report(cohesion, cohesionFileName)
#~ aguila(cohesionFileName)
#~ report(erodibilityK, erodibilityFileName)
#~ aguila(erodibilityKFileName)  
#~ report(factorC, factorCFileName)
#~ aguila(factorCFileName)  


print("Input parameters/maps are ready.")


########################################################################
# static hydrology model for one event
########################################################################

# precipitation
# - amount of precipitation of the event (m)
precipitationEvent = precipitationIntensityEvent * precipitationDuration

# interception storage capacity
# - maximum content of interception store (m, for vegetated part of cell), from reader, see also e.g. von Hoyningen-Huene (1981) and Kozak et al. (2007)
canopyInterceptionCapacity = max(0.935 + 0.498 * leafAreaIndex - 0.00575 * sqr(leafAreaIndex), 0.0000001) / 1000.
# - saving it to file (and display it using aguila)
report(canopyInterceptionCapacity, canopyInterceptionCapacityFileName)
#~ aguila(canopyInterceptionCapacityFileName)

# amount of water reaching the soil (m) during the event
# - throughfall (m, for vegetated part of cell)
throughfall = max(0.0, precipitationEvent - canopyInterceptionCapacity)
# - amount of water reaching the soil (m)
netRainfall = vegetationCover * throughfall + (1.0 - vegetationCover) * precipitationEvent

# infiltration capacity (based on the saturated conductivity of the top soil (m.hr-1), measured by students or from table
# - infiltration capacity of the event (m)
infiltrationCapacity = kSat * precipitationDuration

# local runoff (m): local amount of water reaching soil and above infiltration capacity
localRunoffEvent = max(0.0, netRainfall - infiltrationCapacity)

# runoff (accumulated) and actual infiltration during the event
# - runoff (m) - accumulated along ldd
runoffEvent = accuthresholdflux(ldd, netRainfall, infiltrationCapacity)
# - actual infiltration (m)
infiltrationEvent = accuthresholdstate(ldd, netRainfall, infiltrationCapacity)
# PS: To understand the function, see http://pcraster.geo.uu.nl/pcraster/4.1.0/doc/manual/op_accuthreshold.html


########################################################################
# total values over a year
########################################################################

# local runoff in a year (m.year-1)
localRunoffYear = localRunoffEvent * numberOfEvents
# runoff in a year (m.year-1) - accumulated along ldd
runoffYear = runoffEvent * numberOfEvents
# infiltration in a year (m.year-1)
infiltrationYear = infiltrationEvent * numberOfEvents
# precipitation in a year (m.year-1)
precipitationYear = precipitationEvent * numberOfEvents

# reporting/saving yearly values to pcraster files (and displaying them via aguila) - only in the mask area (area of interest)
# - annual local runoff 
localRunoffYear = ifthen(mask, scalar(localRunoffYear))
report(localRunoffYear, localRunoffYearFileName)
#~ aguila(localRunoffYearFileName)
# - annual runoff - accumulated along ldd
runoffYear = ifthen(mask, scalar(runoffYear))
report(runoffYear, runoffYearFileName)
#~ aguila(runoffYearFileName)
# - annual infiltration
infiltrationYear = ifthen(mask, scalar(infiltrationYear))
report(infiltrationYear, infiltrationYearFileName)
#~ aguila(infiltrationYearFileName)
# - annual precipitation
precipitationYear = ifthen(mask, scalar(precipitationYear))
report(precipitationYear, precipitationYearFileName)
#~ aguila(precipitationYearFileName)

print("Hydrology calculation is done.")

########################################################################
# soil erosion model
########################################################################

# estimate of proportion of rain intercepted (dimensionless, fraction 0 to 1)
fractionInterceptedRain = (precipitationEvent - netRainfall) / precipitationEvent

# annual effective/net rainfall reaching the soil (m.year-1)
effectiveRainfallYear = fractionInterceptedRain * precipitationYear

# annual leaf drainage (m.year-1): throughfall through canopy/leaf
leafDrainageYear = effectiveRainfallYear * canopyCover

# annual direct throughfall (m.year-1)
directThroughfallYear = effectiveRainfallYear - leafDrainageYear

# typical rainfall intensity of the event in mm.hr-1
# - needed for estimating kinematic energy, see below
precipitationIntensityEventMilimeterPerHour = precipitationIntensityEvent * 1000.

# kinetic energy (unit: J.m-2) - for a year
# - energy by direct throughfall (Morgan, 2001, Equation 4 and Table 2, data from Zanchi and Torri, 1980)
kineticEnergyByDirectThroughfall = \
               directThroughfallYear * (9.81 + 11.25 * log10(precipitationIntensityEventMilimeterPerHour)) 
# - energy by leaf drainage (Morgan 2001, Equation 5)
kineticEnergyByLeafDrainage = (15.8 * plantHeight ** 0.5) - 5.87
kineticEnergyByLeafDrainage = max(0.0, kineticEnergyByLeafDrainage)
# - total kinetic energy
kineticEnergy = kineticEnergyByDirectThroughfall + kineticEnergyByLeafDrainage

# annual soil particle detachment (kg.m-2.year-1) by raindrop impact (symbolized as F in Morgan, 2001, Equation 9)
# - for a year
detachmentByRaindropF = erodibilityK * kineticEnergy * 0.001 

# annual runoff in milimeter (mm.year-1)
runoffYearMilimeter = runoffYear * 1000.

# slope steepness
# - slope in m.m-1, estimated from elevation (dem) 
slope = slope(dem)
# - saving slope file
report(slope, slopeFileName) 
# - slope in degree (symbolized as S in Morgan, 2001, Equation 10)
slopeS = atan(slope)
#~ aguila(slopeS)

# soil resistance, based on the cohesion 
# - resistance of the soil (symbolized as Z in Morgan, 2001, Equation 10)
resistanceZ = (1.0 / (0.5 * cohesion))

# annual soil particle detachment (kg.m-2.year-1) by runoff, symbolized as H  in Morgan, 2001, Equation 10 - modified by Wiebe (runoffYear in meter)
# - for a year
detachmentByRunoffH = resistanceZ * pow(runoffYear, 1.5) * sin(slopeS) * (1.0 - groundCover)
# - constrained by a maximum (annual) limit of flow/runoff detachment (kg.m-2.year-1)
detachmentByRunoffH = min(maxLimitDetachmentByRunoff, detachmentByRunoffH)

# annual transport capacity (kg.m-2.year-1) of erosion, symbolized as TC in Morgan, 2001, Equation 12 - modified by Wiebe (runoffYear in meter)
transportCapacity = factorC * pow(runoffYear, 2.0) * sin(slopeS)

# annual estimate of total particle detachment (kg.m-2.year-1) - not limited by transport capacity
# - for a year
totalDetachment = detachmentByRaindropF + detachmentByRunoffH 

# limit annual erosion (kg.m-2.year-1) by annual transport capacity
# - for a year
erosion = min(transportCapacity, totalDetachment)

# reporting/saving yearly values to pcraster files (and displaying them via aguila)
# - annual effective/net rainfall reaching the soil
report(effectiveRainfallYear, effectiveRainfallYearFileName)
#~ aguila(effectiveRainfallYearFileName)
# - annual leaf drainage: throughfall through canopy/leaf
report(leafDrainageYear, leafDrainageYearFileName)
#~ aguila(leafDrainageYearFileName)
# - annual direct throughfall (m.year-1)
report(directThroughfallYear, directThroughfallYearFileName)
#~ aguila(directThroughfallYearFileName)
# - annual detachment by raindrop/splash - not limited by transport capacity
report(detachmentByRaindropF, detachmentByRaindropFileName)
#~ aguila(detachmentByRaindropFileName)
# - detachment by runoff - not limited by transport capacity
report(detachmentByRunoffH, detachmentByRunoffFileName)
#~ aguila(detachmentByRunoffFileName)
# - total detachment  - not limited by transport capacity
report(totalDetachment, totalDetachmentFileName)
#~ aguila(totalDetachmentFileName)
# - transport capacity 
report(transportCapacity, transportCapacityFileName)
#~ aguila(transportCapacityFileName)
# - total erosion - limited by transport capacity
report(erosion, erosionFileName)
#~ aguila(erosionFileName)


print("Soil erosion calculation is done.")


# Reporting calculation time needed (seconds) 
calculation_time = round(py_time.time() - start_time, 2)
print("Total calculation time (seconds): " + str(calculation_time))
