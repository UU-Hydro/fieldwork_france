#####
# NEW HYDROLOGICAL MODEL
#####

# observed by students in the field
# leave area index
lai = ..
# proportion of the pixel containing vegetation (that is 1 - gap fraction)
cov = ..

##
# static model for one event
##

## precipitation
# rainfall intensity m/h of the event
pIntensityEvent = ...
# duration h of the event
pDuration = ...
# amount of precipitation of the event (m)
pEvent = pIntensityEvent * pDuration

## interception storage capacity
# maximum content of interception store  (m, for vegetated part of cell), from reader
ICStM = max(0.935 + 0.498 * lai - 0.00575 * sqr(lai), 0.0000001) / 1000

## amount of water reaching the soil
# throughfall (m, for vegetated part of cell)
tF = max(0.0, pEvent - ICStM)
# amount of water reaching the soil
netRain = cov * tF + (1.0-cov) * pEvent

## infiltration capacity
# saturated conductivity of the top soil
ksat = ..                                     # measured by student or from table
# infiltration capacity of the event (m)
iCap = ksat * pDuration

## runoff and actual infiltration (m)
runoff = accuthresholdflux(ldd, netRain, iCap)
infiltration = accuthresholdstate(ldd, netRain, iCap)

##
# total values over a year
##

# number of rainfall events
nEvents = 10.0
# runoff (m per year)
runoffYear = runoff * nEvents
# infiltration (m per year)
infiltrationYear = infiltration * nEvents
# precipitation (m per year)
pYear = pEvent * nEvents

--> pass this to erosion model (see below) 



######
# EXISTING MODEL
######

## Rainfall
# annual rainfall (mm) - Morgan 2001 Table 1        
R = 857      
# typical value of intensity of rain (mm/h) - Morgan 2001 Table 1
I = 40       

# proportion of rain intercepted - Morgan 2001 Table 1
A = ((self.PCum - self.PrNetCum) / self.PCum) 

ER = R * (1-A) # effective rain (mm) - Morgan 2001 EQ 1
LD = ER * self.cc # leaf drainage  - Morgan 2001 EQ 2
DT = ER - LD  # direct throughfall  - Morgan 2001 EQ 3


## Kinetic energy of the rainfall   
KE_DT = DT * (9.81 + 11.25 * log10(I)) # enerygy by direct throughfall - Morgan 2001 EQ 4 / Table 2, data from Zanchi en Torri 1980
KE_LD = (15.8 * self.ph ** 0.5) - 5.87 # enerygy by leaf drainage - Morgan 2001 EQ 5
KE_LD = ifthenelse(KE_LD < 0, scalar(0.0), KE_LD)       
KE = KE_DT + KE_LD


## Discharge comes from dynamic model
# This is not part of the MMF model
# Discharge of the modelled event (mm waterslice)
qevent = (self.QCum / self.CA) * 1000        
# Rough estimate: 12 of such event in a year
Q = qevent * 12.0 # mm

       
       
### Erosion   
       
# Soil particle detachment by raindrop impact
F = self.K * KE * 0.001     # kg / m2 - Morgan 2001 EQ 9

# soil particle detachment by runoff
Slope = slope(self.dem) # slope steepness 

# soil particle detachment by flow (kg/m2 per year)
# fraction of ground cover - Morgan 2001 Table 1
Z = (1.0 / (0.5*self.C)) # soil resistance  - Morgan 2001 EQ 11   
H = Z * pow(Q, 1.5) * sin(Slope) * (1-self.gc) * 0.001 # detachment kg/m2 - Morgan 2001 EQ 10
    
# transport capacity
C = 1.0  # crop cover factor TODO: use lookup tables
TC = C * Q**2 * sin(Slope) * 0.001 # transport capacity kg/m2  - Morgan 2001 EQ 12
              
# total particle detachment (kg/m2)
D = (H + F) 

# limit erosion by transport capacity
Erosion = ifthenelse(D < TC, D, TC)


self.report(log10(F + 1), 'spladet')
self.report(log10(H + 1), 'flowdet')
self.report(log10(D + 1), 'totdet')               
self.report(log10(TC + 1), 'trancap')          
self.report(log10(Erosion + 1), 'erosion')        

