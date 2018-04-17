#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time as py_time
from pcraster import *

import input_output

# get the current time (for calculating calculation time needed) 
start_time = py_time.time()

print("Model calculations starts.")

# clone map: defining the model extent (of study area), including model resolution  
cloneMap = input_output.cloneMap
setclone(cloneMap)

# ldd: drainage direction
ldd = input_output.ldd

# dem: elevation
dem = input_output.dem

# mask: area of interest
mask = defined(ldd)

# leave area index (m2.m-2) 
# - observed by students in the field
leafAreaIndex = input_output.leafAreaIndex

# proportion of the pixel containing vegetation (dimensionless, fraction 0 to 1) 
# - observed by students in the field (???) #TODO: Check this comment. 
vegetationCover = input_output.vegetationCover 


########################################################################
# static hydrology model for one event
########################################################################

# precipitation
# - typical rainfall intensity (m.hr-1) of the event
precipitationIntensityEvent = input_output.precipitationIntensityEvent
# - duration (hr) of the event
precipitationDuration = input_output.precipitationDuration
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

# infiltration capacity
# - saturated conductivity of the top soil (m.hr-1), measured by students or from table
kSat = input_output.kSat
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

# number of rainfall events in a year
numberOfEvents = input_output.numberOfEvents
# runoff in a year (m.year-1) - accumulated along ldd
runoffYear = runoffEvent * numberOfEvents
# infiltration in a year (m.year-1)
infiltrationYear = infiltrationEvent * numberOfEvents
# precipitation in a year (m.year-1)
precipitationYear = precipitationEvent * numberOfEvents

# reporting/saving yearly values to pcraster files (and displaying them via aguila) - only in the mask area (area of interest)
# - runoff
runoffYear = ifthen(mask, scalar(runoffYear))
runoffYearFileName = input_output.runoffYearFileName
report(runoffYear, runoffYearFileName)
#~ aguila(runoffYearFileName)
# - infiltration
infiltrationYear = ifthen(mask, scalar(infiltrationYear))
infiltrationYearFileName = input_output.infiltrationYearFileName
report(infiltrationYear, infiltrationYearFileName)
#~ aguila(infiltrationYearFileName)
# - precipitation
precipitationYear = ifthen(mask, scalar(precipitationYear))
precipitationYearFileName = input_output.precipitationYearFileName
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

# proportion/fraction of canopy cover within a cell (dimensionless, fraction 0 to 1)
canopyCover = input_output.canopyCover

# annual leaf drainage (m.year-1): throughfall through canopy/leaf
leafDrainageYear = effectiveRainfallYear * canopyCover

# annual direct throughfall (m.year-1)
directThroughfallYear = effectiveRainfallYear - leafDrainageYear

# plant height (m)
# - needed for estimating kinematic energy, see below
# - representing the height from which raindrops fall from the crop or vegetation cover to the ground surface
plantHeight = input_output.plantHeight

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

# erodibility (g.J-1) of the soil (symbolized as K in Morgan, 2001, Equation 9)
erodibilityK = input_output.erodibilityK

# soil particle detachment (kg.m-2) by raindrop impact (symbolized as F in Morgan, 2001, Equation 9)
# - for a year
detachmentByRaindropF = erodibilityK * kineticEnergy * 0.001 

# annual runoff in milimeter
runoffYearMilimeter = runoffYear * 1000.

# slope steepness
# - slope in m.m-1, estimated from elevation (dem) 
slope = slope(dem)
# - saving slope file
slopeFileName = input_output.slopeFileName
report(slope, slopeFileName) 
# - slope in degree (symbolized as S in Morgan, 2001, Equation 10)
slopeS = atan(slope)
#~ aguila(slopeS)

# soil resistance, based on the cohesion 
# - cohesion (unit: kPa) of the soil - symbolyzed as COH in Morgan, 2001
cohesion = input_output.cohesion
# - resistance of the soil (symbolized as Z in Morgan, 2001, Equation 10)
resistanceZ = (1.0 / (0.5 * cohesion))

# ground cover percentage (dimensionless, fraction 0 to 1)
groundCover = input_output.groundCover

# soil particle detachment (kg.m-2) by runoff (symbolized as H  in Morgan, 2001, Equation 10)
# - for a year
detachmentByRunoffH = resistanceZ * pow(runoffYearMilimeter, 1.5) * sin(slopeS) * (1.0 - groundCover) * 0.001
#~ aguila(detachmentByRunoffH)

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account different tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
factorC = input_output.factorC

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
detachmentByRaindropFileName = input_output.detachmentByRaindropFileName
report(detachmentByRaindropF, detachmentByRaindropFileName)
#~ aguila(detachmentByRaindropFileName)
# - detachment by runoff - not limited by transport capacity
detachmentByRunoffFileName = input_output.detachmentByRunoffFileName
report(detachmentByRunoffH, detachmentByRunoffFileName)
#~ aguila(detachmentByRunoffFileName)
# - total detachment  - not limited by transport capacity
totalDetachmentFileName = input_output.totalDetachmentFileName
report(totalDetachment, totalDetachmentFileName)
#~ aguila(totalDetachmentFileName)
# - transport capacity 
transportCapacityFileName = input_output.transportCapacityFileName
report(transportCapacity, transportCapacityFileName)
#~ aguila(transportCapacityFileName)
# - total erosion - limited by transport capacity
erosionFileName = input_output.erosionFileName
report(erosion, erosionFileName)
#~ aguila(erosionFileName)

print("Soil erosion calculation is done.")

# Reporting calculation time needed (seconds) 
calculation_time = round(py_time.time() - start_time, 2)
print("Total calculation time (seconds): " + str(calculation_time))
