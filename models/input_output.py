#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
# input values/maps
########################################################################

# clone map: defining the model extent (of study area), including model resolution  
cloneMap = "input_maps/clone.map"

# ldd: drainage direction
ldd = "input_maps/ldd.map"

# dem: elevation
dem = "input_maps/dem_10m.map"

# leave area index (m2.m-2) 
# - observed by students in the field
leafAreaIndex = 5.0

# proportion of the pixel containing vegetation (dimensionless, fraction 0 to 1) 
# - observed by students in the field (???) #TODO: Check this comment. 
vegetationCover = 0.8 

# precipitation
# - typical rainfall intensity (m.hr-1) of the event
precipitationIntensityEvent = 40./1000.
# - duration (hr) of the event
precipitationDuration = 2.0
# - number of rainfall events in a year
numberOfEvents = 10.

# saturated conductivity of the top soil (m.hr-1), measured by students or from table
# - needed for estimating infiltration capacity
kSat = 0.01  

# proportion/fraction of canopy cover within a cell (dimensionless, fraction 0 to 1)
canopyCover = 0.2  

# plant height (m)
# - representing the height from which raindrops fall from the crop or vegetation cover to the ground surface
# - needed for estimating kinematic energy,
plantHeight = 12.

# erodibility (g.J-1) of the soil (symbolized as K in Morgan, 2001, Equation 9)
erodibilityK = 0.5  

# soil cohesion (unit: kPa) of the soil - symbolyzed as COH in Morgan, 2001
cohesion = 2.

# ground cover percentage (dimensionless, fraction 0 to 1)
groundCover = 0.4

# crop or plant cover factor (symbolized as C in Morgan, 2001)
# - this factor is to take account different tillage practices and levels of crop residue retention
# - needed to estimate transport capacity (Equation 12 in Morgan, 2001)
factorC = 1.0 


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


