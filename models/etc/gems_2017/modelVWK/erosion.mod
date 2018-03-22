binding

PAnn=857;      # annual rainfall
I=40;          # typical value of intensity of rain (mm/h)
Dem=dem.map;

COH=c.map;
K=k.map;
Q=qyear.map;
F=f.map;
A=a.map;
H=h.map;
D=d.map;

initial

# qevent (mm)
report qevent.map=(QRCum000.240/cellarea())*1000;

# runoff (mm)
report Q=1000*(QRCum000.240/cellarea())*(PAnn/Pevent);

# percentage of rainfall contributing to interception or stemflow
report A=((PCum0000.240-RNCum000.240)/PCum0000.240);
#report A=(RNCum000.240/PCum0000.240);

# kinetic energy of the rainfall
E=PAnn*(11.9+8.7*log10(I));

# soil detachability index 
report K=lookupscalar(k.txt,reg.map);

# soil particle detachment by raindrop impact
report F=K*E*exp(-0.05*A)*0.001;

# slope as fraction
Slope=slope(Dem);

# slope in degrees
SlopeDeg=atan(Slope);

report COH=lookupscalar(c.txt,reg.map);
GC=0.4;

# soil particle detachment by flow (kg/m2 per year)
report H=(1/(0.5*COH))*(Q**1.5)*sin(SlopeDeg)*(1-GC)*0.001;

# soil particle detachment by flow (ton/ha/yr)
report HTon=(H*10000)/1000;

# total particle detachment
report D=H+F;
