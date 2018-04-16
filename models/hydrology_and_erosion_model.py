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

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
# - Note: No spatial variation. 
valueForFactorC = 1.0 

# regolithcode: regolith units
regolithCode = nominal("inputs/regolith.map")
# regolithTable: regolith parameters (Ksat, K, C) observed in field
regolithTable = "inputs/regolith_table.txt"

########################################################################



########################################################################
# output file names (all in pcraster formats)
########################################################################

# output file names:
# - annual precipitation (m.year-1)
precipitationYearFileName = "output/precipitation_m_per_year.map"
# - annual infiltration (m.year-1)
infiltrationYearFileName = "output/infiltration_m_per_year.map"
# - annual runoff (m.year-1)
runoffYearFileName = "output/runoff_m_per_year.map"
# - slope (m.m-1), estimated from elevation (dem) 
slopeFileName = "output/slope_m_per_m.map"
# - annual detachment by raindrop/splash (kg.m-2.year-1) - not limited by transport capacity
detachmentByRaindropFileName = "output/splash_detachment_kg_per_m2_per_year.map"
# - annual detachment by runoff (kg.m-2.year-1) - not limited by transport capacity
detachmentByRunoffFileName = "output/flow_detachment_kg_per_m2_per_year.map"
# - annual total detachment (kg.m-2.year-1) - not limited by transport capacity
totalDetachmentFileName = "output/total_detachment_kg_per_m2_per_year.map"
# - annual transport capacity (kg.m-2.year-1) 
transportCapacityFileName = "output/transport_capacity_kg_per_m2_per_year.map"
# - annual total erosion (kg.m-2.year-1) - limited by transport capacity
erosionFileName = "output/erosion_kg_per_m2_per_year.map"

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
#~ aguila(vegetationCover)

# leave area index (m2.m-2) 
leafAreaIndex = lookupscalar(vegetationTable, 2, vegetationCode)
#~ aguila(leafAreaIndex)

# plant height (m)
# - representing the height from which raindrops fall from the crop or vegetation cover to the ground surface
# - needed for estimating kinematic energy,
plantHeight = lookupscalar(vegetationTable, 3, vegetationCode)
#~ aguila(plantHeight)

# proportion/fraction of canopy cover within a cell (dimensionless, fraction 0 to 1)
canopyCover = lookupscalar(vegetationTable, 4, vegetationCode)
#~ aguila(canopyCover)
  
# ground cover percentage (dimensionless, fraction 0 to 1)
groundCover = lookupscalar(vegetationTable, 5, vegetationCode)
#~ aguila(groundCover)


####### regolith parameters: kSat, cohesion, erodibilityK, factorC 
# - Except factorC, all would be read from a lookup table (regolithTable) based on the regolith map (regolithCode).
# - Note that the factorC is defined above (see the variable: valueForFactorC). 
###################################################################################################################

# saturated conductivity of the top soil (m.hr-1), measured by students or from table
# - needed for estimating infiltration capacity
kSat = lookupscalar(regolithTable, 1, regolithCode)  
#~ aguila(kSat)

# soil cohesion (unit: kPa) of the soil - symbolyzed as COH in Morgan, 2001
cohesion = lookupscalar(regolithTable, 2, regolithCode)
#~ aguila(cohesion)

# erodibility (g.J-1) of the soil (symbolized as K in Morgan, 2001, Equation 9)
erodibilityK = lookupscalar(regolithTable, 3, regolithCode)
#~ aguila(erodibilityK)  

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account different tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
factorC = spatial(scalar(valueForFactorC))
#~ aguila(factorC)  



########################################################################
# output file names (all in pcraster formats)
########################################################################

# output file names:
# - annual precipitation (m.year-1)
precipitationYearFileName = "outputs/precipitation_m_per_year.map"
# - annual infiltration (m.year-1)
infiltrationYearFileName = "outputs/infiltration_m_per_year.map"
# - annual runoff (m.year-1)
runoffYearFileName = "outputs/runoff_m_per_year.map"
# - slope (m.m-1), estimated from elevation (dem) 
slopeFileName = "outputs/slope_m_per_m.map"
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

########################################################################




########################################################################
# static hydrology model for one event
########################################################################

# precipitation
# - amount of precipitation of the event (m)
precipitationEvent = precipitationIntensityEvent * precipitationDuration

# interception storage capacity
# - maximum content of interception store (m, for vegetated part of cell), from reader #TODO: Need reference 
canopyInterceptionCapacity = max(0.935 + 0.498 * leafAreaIndex - 0.00575 * sqr(leafAreaIndex), 0.0000001) / 1000.

# amount of water reaching the soil (m) during the event
# - throughfall (m, for vegetated part of cell)
throughfall = max(0.0, precipitationEvent - canopyInterceptionCapacity)
# - amount of water reaching the soil (m)
netRainfall = vegetationCover * throughfall + (1.0 - vegetationCover) * precipitationEvent

# infiltration capacity (based on the saturated conductivity of the top soil (m.hr-1), measured by students or from table
# - infiltration capacity of the event (m)
infiltrationCapacity = kSat * precipitationDuration

# runoff (accumulated) and actual infiltration during the event
# - runoff (m) - accumulated along ldd
runoffEvent = accuthresholdflux(ldd, netRainfall, infiltrationCapacity)
# - actual infiltration (m)
infiltrationEvent = accuthresholdstate(ldd, netRainfall, infiltrationCapacity)
# PS: To understand the function, see http://pcraster.geo.uu.nl/pcraster/4.1.0/doc/manual/op_accuthreshold.html


########################################################################
# total values over a year
########################################################################

# runoff in a year (m.year-1) - accumulated along ldd
runoffYear = runoffEvent * numberOfEvents
# infiltration in a year (m.year-1)
infiltrationYear = infiltrationEvent * numberOfEvents
# precipitation in a year (m.year-1)
precipitationYear = precipitationEvent * numberOfEvents

# reporting/saving yearly values to pcraster files (and displaying them via aguila) - only in the mask area (area of interest)
# - runoff
runoffYear = ifthen(mask, scalar(runoffYear))
report(runoffYear, runoffYearFileName)
#~ aguila(runoffYearFileName)
# - infiltration
infiltrationYear = ifthen(mask, scalar(infiltrationYear))
report(infiltrationYear, infiltrationYearFileName)
#~ aguila(infiltrationYearFileName)
# - precipitation
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
# - energy by leaf drainage                                             #TODO: Need reference. Morgan 2001 EQ 5 ???
kineticEnergyByLeafDrainage = (15.8 * plantHeight ** 0.5) - 5.87
kineticEnergyByLeafDrainage = max(0.0, kineticEnergyByLeafDrainage)
# - total kinetic energy
kineticEnergy = kineticEnergyByDirectThroughfall + kineticEnergyByLeafDrainage

# soil particle detachment (kg.m-2) by raindrop impact (symbolized as F in Morgan, 2001, Equation 9)
# - for a year
detachmentByRaindropF = erodibilityK * kineticEnergy * 0.001 

# annual runoff in milimeter
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

# soil particle detachment (kg.m-2) by runoff (symbolized as H  in Morgan, 2001, Equation 10)
# - for a year
detachmentByRunoffH = resistanceZ * pow(runoffYearMilimeter, 1.5) * sin(slopeS) * (1.0 - groundCover) * 0.001
#~ aguila(detachmentByRunoffH)

# transport capacity (kg.m-2) of erosion (symbolized as TC in Morgan, 2001, Equation 12)
# - for a year
transportCapacity = factorC * pow(runoffYearMilimeter, 2.0) * sin(slopeS) * 0.001

# estimate of total particle detachment (kg.m-2) - not limited by transport capacity
# - for a year
totalDetachment = detachmentByRaindropF + detachmentByRunoffH 

# limit erosion (kg.m-2) by transport capacity
# - for a year
erosion = min(transportCapacity, totalDetachment)

# reporting/saving yearly values to pcraster files (and displaying them via aguila) - only in the mask area (area of interest)
# - detachment by raindrop/splash - not limited by transport capacity
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
