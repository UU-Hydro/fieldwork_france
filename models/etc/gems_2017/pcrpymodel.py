from pcraster import *
from pcraster.framework import *
# from osgeo import gdal


class Model(DynamicModel):
    def __init__(self, cloneMap):
        DynamicModel.__init__(self)
        setclone(cloneMap)

    def initial(self):
        
        # Fetch data from WCS provider
        #logger.debug("Loading elevation")
        #self.dem =  self.readmap("srtm.elevation")
        #        self.dem =  self.readmap("1")
        #        self.report(self.dem, 'dem')
        self.dem = 'dem_50m_gems.map'

        
        # usefull dimentions        
        self.CA = cellarea()
        self.CL = celllength()
        self.T = self.timesteplength
        
        print("CA:%f, CL:%f, T:%f" % (self.CA, self.CL, self.T))
                
        ## Pecipitation 
        precipitationIntensity = 50 #self.readparam("precipitationIntensity")   # 10
        self.precipitationIntensityMeters = precipitationIntensity / 1000.0
        
        precipitationDuration = 0.5 #self.readparam("precipitationDuration")         # 0.1
        self.precipitationDurationSeconds = precipitationDuration * 3600.0
        
        self.PCum = scalar(0.0)
        self.PrNetCum = scalar(0.0)
                
        # Vegetation properties
        # TODO: convert to lookup tables
        self.cov = scalar(0.8) # scalar(self.readparam("cov"))
        self.lai = scalar(5.0) # scalar(self.readparam("lai"))

        
        ## Interception
        # initial content of interception store  (m, for vegetated part of cell)
        self.ICSt = scalar(0.0)
        # maximum content of interception store  (m, for vegetated part of cell)
        self.ICStM = max(0.935 + 0.498 * self.lai - 0.00575 * sqr(self.lai), 0.0000001) / 1000
        # correction factor canopy (0.046 * LAI, is unit correct?)        
        self.ICorr=1;                                 
           
        
        ## Infiltration and Surface storage
        # saturated conductivity (m/h)
        # TODO: convert to lookup tables
        self.ks = scalar(0.01) # scalar(self.readparam("ksat"))
        # suction head (m)
        self.hf = scalar(-0.05) #scalar(self.readparam("hf")) 

      
        # Cumulative infiltration (m)
        self.FCum = scalar(0.01)
        
        # Available pore space
        porosity = 0.4
        initialMoistureContent = 0.05
        self.DTau = porosity - initialMoistureContent
        
        # maximum surface storage (m)
        self.D = 0.001
        # amount of water in surface storage (m)
        self.DSt = scalar(0)
        # total generated runoff (m/timestep)
        self.q = scalar(0)
        self.qCum = scalar(0)
       
                
        ## Routing
        # local drainage direction
        self.ldd = lddcreate(self.dem, 1e31, 1e31, 1e31, 1e31)
        self.report(self.ldd, 'ldd')
        # distance to downstream cell (m)
        self.DCL=max(downstreamdist(self.ldd),self.CL)                     
        # slope to downstream cell (m/s)
        Slope = (self.dem - downstream(self.ldd,self.dem)) / self.DCL
        # limit slope
        Slope = cover(max(0.0001, Slope), 0.0001)
        
        self.report(Slope, 'slope')
        
        # mannings n 
        # TODO: convert to lookup tables
        self.n = scalar(0.1) #scalar(self.readparam("n"))           
        
        # routing paramters                
        self.Beta=0.6        
        # term for Alpha
        self.AlpTerm=(self.n / (sqrt(Slope)))**self.Beta
        # power for Alpha
        self.AlpPow=(2/3)*self.Beta
        
        # Channel bottom with (m)
        self.Bw = self.CL * 0.5; 
        
        # Streamflow (m3/s)
        self.Q = scalar(1e-12)
        self.QCum = scalar(0.0)
        
        # wahter height (m)
        self.H = scalar(1E-9);

        
    def dynamic(self):
        self.timestep = self.currentTimeStep()
        #logger.debug("Dynamic! Timestep: %d, Timestep length: %d, Total: )" % (self.timestep, self.timesteplength))
        
        # hours per timestep
        hTimestep = self.timesteplength / 3600.0
        # timesteps per hour 
        tHour = 3600.0 / self.timesteplength       

        # print(self.timesteplength, hTimestep, tHour)
        
        ### Hydrology above ground ###       
        # Precipitation (m/h)     
        if (self.timestep * self.timesteplength) < self.precipitationDurationSeconds:
            PrH = scalar(self.precipitationIntensityMeters)
        else:
            PrH = scalar(0.0)

        # Precipitation (m/timestep)
        Pr = PrH * hTimestep            
            
        # Cumulative in m
        self.PCum = self.PCum + Pr

        # report precipitation in mm/h
        self.report(PrH * 1000.0, "precip")          

        # Interception (m / timestep)
        Int = Pr * self.cov
       
        # report interception in mm/h
        self.report(Int * tHour * 1000.0, "interc")

        # In interception storage (m, for vegetated part of cell)
        ICStOld=self.ICSt
        self.ICSt=self.ICStM*(1-exp((-self.ICorr * self.PCum) / self.ICStM))

        # In interception storage (m, for entire cell)
        # TODO: report total S and flux TS (ToICStC in mm/hr);
        # ICStC=Cov*ICSt      
        #report SCell=ICStC;  
        
        # To interception storage (m/timestep, for vegetated part of cell)
        ToICSt = self.ICSt-ICStOld            
        # To interception store (m/timestep, for entire cell)
        ToICStC = self.cov*ToICSt
        
        # Canopy drainage (m/timestep, for entire cell)
        # TODO: report CD in mm/hr
        CD = Int - ToICStC        
        
        # Througfall (m/timestep spreaded over whole cell)
        TF = (Pr - Int) + CD

        # report throughfall in mm/h
        self.report(TF * tHour * 1000.0, "thrghf")

        # net rain (m)
        # total net rain per timestep (m/timestep spreaded over whole cell)                            ########## DYNAMIC ################
        PrNet = TF + (Pr - Int)
        
        # cumulative net rain (m, spreaded over whole cell)
        self.PrNetCum = self.PrNetCum + PrNet


        ### Infiltration and surface hydrology ###

        # Net flow in/out of cell - routing from previous timestep (m/timestep)
        QR = (self.Q * self.T) / self.CA
        
        # Total amount of water on surface (m)
        SurW = TF + self.DSt + QR
             
        # Potential infiltration per timestep (m/timestep)        
        Fc = self.ks * hTimestep * ((-self.hf * self.DTau + self.FCum) / self.FCum)
                
        self.report(Fc * tHour * 1000.0, "pinfil")
                
        # Actual infiltration per timestep (m/timestep)
        FcA = ifthenelse(SurW > Fc, Fc, SurW)
        
        # Cumulative infiltration (m)
        self.FCum = self.FCum + FcA
        
        self.report(self.FCum * 1000.0, "cinfil")

              
        # Report infiltration in mm/h
        self.report(FcA * tHour * 1000.0, "infilt")
        
        # Total amount of water on surface after infiltration (m)
        SurW = max(SurW - FcA, 0)
        
        # Surface storage (m)
        DStO=self.DSt;
        self.DSt = ifthenelse(SurW > self.D, self.D, SurW)
        
        # Surface storage (mm)
        self.report(self.DSt * 1000.0, 'surfSt')
        
        # flux to surface storage (m/timestep)
        DStCh=self.DSt-DStO

        # Total amount of water on surface after infiltration and surface storage (m)
        SurW = max(SurW - self.DSt, 0)
         
        # runoff generated - amount of water added to streamflow (m/timestep)
        q = SurW - QR
        self.qCum = self.qCum + q;
        
        # runoff generated (mm/h)
        self.report(q * tHour * 1000.0, 'rnfgen')


        ## Budget checks
        # at this point, all per-cell calculations are finished for the hydrology
        # fluxer per timestep: rain = toInterception + Infiltration + To surface + generate runoff
        # BudFl = Pr - (ToICStC+ FcA + DStCh + q) 
        # storage total: total rain = Interception + Cum Infiltration + Surface + Cumulative generatred runoff
        # BudSto = PCum - (ICStC + FCum + DSt + qCum)
        
           
        ## Routing
        # amount of water added to streamflow (m3/s)
        QIn = (q * self.CA) / self.T;

        # Routing parameters 
        # wetted perimeter (m) 
        P = (self.Bw + 2 * self.H)
        # Alpha
        self.Alpha = self.AlpTerm * (P**self.AlpPow)


        # discharge (m3/s) - kinematic routing
        self.Q = kinematic(self.ldd, self.Q, QIn/self.DCL, self.Alpha, self.Beta, 1, self.T, self.DCL)
        self.report(self.Q, 'discha')
        self.QCum = self.QCum + self.Q * self.T; 
        
        # Water depth (m)
        self.H = (self.Alpha*(self.Q**self.Beta))/self.Bw
        self.report(self.H, 'waterd')

        if self.timestep == self.nrTimeSteps():
            print 'starting postdynamic'
            self.postdynamic()
        
    def postdynamic(self):
        print 'hello postdynamic!'
        PAnn=857      # annual rainfall
        I=40          # typical value of intensity of rain (mm/h)

        # Discharge of the event (mm waterslice)
        qevent = (self.QCum / self.CA) * 1000
        
        # Estimated yearly runoff (mm waterslice)
        Q = qevent * (PAnn/self.precipitationIntensityMeters*1000)
        
        # percentage of rainfall contributing to interception or stemflow
        A=((self.PCum - self.PrNetCum) / self.PCum)
        
        # Kinetic energy of the rainfall
        E = PAnn * (11.9 + 8.7 * log10(I))
        
        # TODOL initial and lookup Soil detachability index and cohesion
        self.K = scalar(0.5)
        self.C = scalar(2)
        
        # Soil particle detachment by raindrop impact
        F = self.K * E * exp(-0.05*A) * 0.001
        
        # slope in degrees
        Slope = atan(slope(self.dem))         
       
        # soil particle detachment by flow (kg/m2 per year)
        GC=0.4
        H = (1/(0.5*self.C))*pow(Q,1.5) * sin(Slope) * (1-GC)*0.001
        
        # soil particle detachment by flow (ton/ha/yr)
        # report HTon=(H*10000)/1000;
        
        # total particle detachment (ton / ha / yr)
        D = (H + F) / 1E7
        
        #self.report(H, 'flodet')
        #self.report(F, 'impdet')
        self.report(log10(D), 'totdet')


dem = 'dem_50m_gems.map'
myModel = Model(dem)
Model.timesteplength = 60.0 # seconds
dynModelFw = DynamicFramework(myModel, lastTimeStep=60, firstTimestep=1)
dynModelFw.run()
        