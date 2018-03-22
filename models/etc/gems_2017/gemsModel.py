from gem.model import *

class Model(GemModel):
    """
    Models the runoff produced by rainfall and the resulting potential erosion based on vegetation and regolith properties
    """
    meta={
        #
        # Metadata
        #
        'name':                 'rainfall_runoff_erosion',
        'author':               'Wouter Marra',
        'contact':              'w.a.marra@uu.nl',
        'abstract':             'Models the runoff produced by rainfall and the resulting potential erosion based on vegetation and regolith properties',
        'license':              '',
        'tags':                 ['erosion','rainfall','hydrology', 'runoff'],
        'discretization':       'frankrijk_vwk_2017_50m',
        'maxchunks':            1
    }
    parameters={
        #
        # These are default params that will be overwritten by params
        # specified in the web application.
        #
        'precipitationIntensity' : 40,
        'precipitationDuration':       0.5,
        
        'cov': '{ 1: 0.1, 2: 0.8, 3: 0.2, 4: 0.4}',
        'lai': '{ 1: 1.0, 2: 2.0, 3: 3.0, 4: 4.0}',
        'cc': '{ 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}',
        'gc': '{ 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}',
        'ph': '{ 1: 5, 2: 12, 3: 8, 4: 2}',
        'ksat': '{ 1: 0.01, 2: 0.02, 3: 0.03, 4: 0.04}',
        'hf': '{ 1: -0.01, 2: -0.02, 3: -0.03, 4: -0.04}',        
        'K': '{ 1: 0.05, 2: 0.2, 3: 0.6, 4: 0.4}',
        'C': '{ 1: 12.0, 2: 3.0, 3: 3.0, 4: 2.0}',
        'areaNumber': 99
    }
    time={
        'start':                 '2000-01-01T00:00:00',
        'timesteps':             121,                 
        'timesteplength':        60,
        'reportevery':           5,                    
    }
    datasources={      
        'wcs':[
            'http://turbo.geo.uu.nl/cgi-bin/mapserv?MAP=/data/projectdata/globaldata/globaldata.map'        
        ]
    }
    reporting={
        'precip': {
            'title':        "Precipitation",
            'units':        "mm/hr",
            'info':            "Precipitation in mm per hr.",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-.00001,100.00001],
                'labels':    []
            }
        },                       
        'interc': {
            'title':        "Interception",
            'units':        "mm/hr",
            'info':            "Interception in mm per hr.",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.00001, 50.00001],
                'labels':    []
            }
        },
        'thrghf': {
            'title':        "Throughfall",
            'units':        "mm/hr",
            'info':            "Throughfall in mm per hr.",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.00001,50.00001],
                'labels':    []
            }
        },
        'infilt': {
            'title':        "Infiltration",
            'units':        "mm/hr",
            'info':            "Infiltration in mm per hr.",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.00001,50.00001],
                'labels':    []
            }
        },
        'rnfgen': {
            'title':        "Runoff generated",
            'units':        "mm/hr",
            'info':            "Runoff generated in mm per hr.",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-50.00001,50.00001],
                'labels':    []
            }
        },
        'runoff': {
            'title':        "Runoff",
            'units':        "log10(m3/s)",
            'info':            "Shifted logarithmic scale: log10(Q+0.001). So Q = 0 > -3, Q = 0.1 > -1, Q = 1 > 0, etc. ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    7, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                #'values':    [-0.00001,6],
                'values':    [-3.00001,3.00001],
                'labels':    []
            }
        },
        'spladet': {
            'title':        "Splash Detachment",
            'units':        "log10(kg/m2/yr)",
            'info':            "Shifted logarithmic scale: log10(D+1). So D = 0 -> 0, D = 1 ~> 0.3, D = 10 ~> 1, D = 100 ~> 2, etc. ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2.000001],
                'labels':    []
            }   
        },
        'flowdet': {
            'title':        "Flow Detachment",
            'units':        "log10(kg/m2/yr)",
            'info':            "Shifted logarithmic scale: log10(D+1). So D = 0 -> 0, D = 1 ~> 0.3, D = 10 ~> 1, D = 100 ~> 2, etc. ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2.000001],
                'labels':    []
            }   
        },
        'totdet': {
            'title':        "Total Detachment",
            'units':        "log10(kg/m2/yr)",
            'info':            "Shifted logarithmic scale: log10(D+1). So D = 0 -> 0, D = 1 ~> 0.3, D = 10 ~> 1, D = 100 ~> 2, etc. ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2.000001],
                'labels':    []
            }   
        },
        'trancap': {
            'title':        "Transport capacity",
            'units':        "log10(kg/m2/yr)",
            'info':            "Shifted logarithmic scale: log10(D+1). So D = 0 -> 0, D = 1 ~> 0.3, D = 10 ~> 1, D = 100 ~> 2, etc. ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2.000001],
                'labels':    []
            }   
        },
        'erosion': {
            'title':        "Erosion",
            'units':        "log10(kg/m2/yr)",
            'info':            "Shifted logarithmic scale: log10(D+1). So D = 0 -> 0, D = 1 ~> 0.3, D = 10 ~> 1 ",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2.000001],
                'labels':    []
            }   
        }
    }
 
    def initial(self):
        logger.debug("Starting initial")
        
        ## Load maps from WCS provider              
        areanr = self.readparam("areaNumber")    
        self.dem = self.readmap("france.elevation")                       
        self.veg = self.readmap("france.veg.%g" % areanr)
        self.geom = self.readmap("france.geom.%g" % areanr)        
        
        
        ## Read model parameters                      
        # Vegetation and regolith properties
        covdict = self.readparam("cov")
        laidict = self.readparam("lai")
        ccdict = self.readparam("cc")
        gcdict = self.readparam("gc")
        phdict = self.readparam("ph")             
        
        ksatdict = self.readparam("ksat")
        hfdict = self.readparam("hf")
        kdict = self.readparam("K")
        cdict = self.readparam("C")
        
        # Precipitation
        precipitationIntensity = self.readparam("precipitationIntensity")   
        self.precipitationIntensityMeters = precipitationIntensity / 1000.0
        
        precipitationDuration = self.readparam("precipitationDuration")     
        self.precipitationDurationSeconds = precipitationDuration * 3600.0
        
                
        ## lookup maps
        # syntax: lookupdict(input-map-categories, lookup-table-as-dict, default-value)
        # Vegetation-related parameters
        self.cov = self.lookupdict(self.veg, covdict, 0)
        self.lai = self.lookupdict(self.veg, laidict, 0)
        self.cc = self.lookupdict(self.veg, ccdict, 0)
        self.gc = self.lookupdict(self.veg, gcdict, 0)
        self.ph = self.lookupdict(self.veg, phdict, 0)        
                
        # Geomorphological-related parameters
        self.ks = self.lookupdict(self.geom, ksatdict, 0)     
        self.hf = self.lookupdict(self.geom, hfdict, 0)        
        self.K = self.lookupdict(self.geom, kdict, 0)
        self.C = self.lookupdict(self.geom, cdict, 0)
        
             
        ## usefull dimentions        
        self.CA = cellarea()
        self.CL = celllength()
        self.T = self.timesteplength        
                   
        ## Intitialize cummulative precipitation variables
        self.PCum = scalar(0.0)
        self.PrNetCum = scalar(0.0)

                     
        ## Interception
        # initial content of interception store  (m, for vegetated part of cell)
        self.ICSt = scalar(0.0)
        # maximum content of interception store  (m, for vegetated part of cell)
        self.ICStM = max(0.935 + 0.498 * self.lai - 0.00575 * sqr(self.lai), 0.0000001) / 1000
        # correction factor canopy (0.046 * LAI, is unit correct?)        
        self.ICorr=1;                                                 

        # Cumulative infiltration (m)
        self.FCum = scalar(0.01)
        
        # Available pore space
        porosity = 0.4
        initialMoistureContent = 0.1
        self.DTau = porosity - initialMoistureContent
        
        # maximum surface storage (m)
        self.D = 0.001
        # amount of water in surface storage (m)
        self.DSt = scalar(0)
        # total generated runoff (m/timestep)
        self.q = scalar(0)
        self.qCum = scalar(0)
       
                
        ## Runoff routing
        # local drainage direction
        self.ldd = lddrepair(lddcreate(self.dem, 1e31, 1e31, 1e31, 1e31))      
        # distance to downstream cell (m)
        self.DCL=max(downstreamdist(self.ldd),self.CL)                     
        # slope to downstream cell (m/m)
        Slope = (self.dem - downstream(self.ldd,self.dem)) / self.DCL
        # limit slope
        Slope = cover(max(0.0001, Slope), 0.0001)                      
        
        # routing paramters                
        self.Beta=0.6        
        self.n = 0.05
        # term for Alpha
        self.AlpTerm=(self.n / (sqrt(Slope)))**self.Beta
        # power for Alpha
        self.AlpPow=(2/3)*self.Beta      
        # Channel  width (m)
        self.W = self.CL * 0.5; 
        
        # Streamflow (m3/s)
        self.Q = scalar(1e-12)
        self.QCum = scalar(0.0)        
        # water height (m)
        self.H = scalar(1E-9)
        
    def dynamic(self):
        logger.debug("Dynamic! Timestep: %d, Timestep length: %d, Total: )" % (self.timestep, self.timesteplength))
        self.status()
        
        # hours per timestep
        hTimestep = self.timesteplength / 3600.0
        # timesteps per hour 
        tHour = 3600.0 / self.timesteplength       

        
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

        # Interception (m / timestep)
        Int = Pr * self.cov       

        # In interception storage (m, for vegetated part of cell)
        ICStOld=self.ICSt
        self.ICSt=self.ICStM*(1-exp((-self.ICorr * self.PCum) / self.ICStM))

        # To interception storage (m/timestep, for vegetated part of cell)
        ToICSt = self.ICSt-ICStOld            
        # To interception store (m/timestep, for entire cell)
        ToICStC = self.cov*ToICSt
        
        # Canopy drainage (m/timestep, for entire cell)
        CD = Int - ToICStC        
        
        # Througfall (m/timestep spreaded over whole cell)
        TF = (Pr - Int) + CD
              
        # cumulative net rain (m, spreaded over whole cell)
        self.PrNetCum = self.PrNetCum + TF



        ### Infiltration and surface hydrology ###
        # Net flow in/out of cell - routing from previous timestep (m/timestep)
        QR = (self.Q * self.T) / self.CA
        
        # Total amount of water on surface (m)
        SurW = TF + self.DSt + QR
             
        # Potential infiltration per timestep (m/timestep)        
        Fc = self.ks * hTimestep * ((-self.hf * self.DTau + self.FCum) / self.FCum)
                            
        # Actual infiltration per timestep (m/timestep)
        FcA = ifthenelse(SurW > Fc, Fc, SurW)
        
        # Cumulative infiltration (m)
        self.FCum = self.FCum + FcA
               
        # Total amount of water on surface after infiltration (m)
        SurW = max(SurW - FcA, 0)
        
        # Surface storage (m)
        # DStO = self.DSt; # FOR budget check
        self.DSt = ifthenelse(SurW > self.D, self.D, SurW)             
        # flux to surface storage (m/timestep)
        # DStCh = self.DSt-DStO #  change in surface storage - for budget check

        # Total amount of water on surface after infiltration and surface storage (m)
        SurW = max(SurW - self.DSt, 0)
         
        # runoff generated - amount of water added to streamflow (m/timestep)
        q = SurW - QR
        self.qCum = self.qCum + q;
        
        ## Budget checks
        # at this point, all per-cell calculations are finished for the hydrology
        # fluxes per timestep: rain = toInterception + Infiltration + To surface + generate runoff
        # BudFl = Pr - (ToICStC+ FcA + DStCh + q) 
        # storage total: total rain = Interception + Cum Infiltration + Surface + Cumulative generatred runoff
        # BudSto = PCum - (ICStC + FCum + DSt + qCum)
        
           
           
        ### Routing
        # amount of water added to streamflow (m3/s)
        QIn = (q * self.CA) / self.T;

        # Routing parameters 
        # wetted perimeter (m) 
        P = (self.W + 2 * self.H)
        # Alpha
        self.Alpha = self.AlpTerm * (P**self.AlpPow)

        # discharge (m3/s) - kinematic routing
        self.Q = kinematic(self.ldd, self.Q, QIn/self.DCL, self.Alpha, self.Beta, 1, self.T, self.DCL)
        # cumulative discharge m3
        self.QCum = self.QCum + self.Q * self.T; 
        
        # Water depth (m)
        self.H = (self.Alpha*(self.Q**self.Beta))/self.W
        
        
      
        ### Reports        
        # only report every 10 th timestep (5 minutes)        
        if ((self.timestep-1) % self.time['reportevery']) == 0:            
            # report precipitation in mm/h
            self.report(PrH * 1000.0, "precip")          
            # report interception in mm/h
            self.report(Int * tHour * 1000.0, "interc")
            # report throughfall in mm/h
            self.report(TF * tHour * 1000.0, "thrghf")              
            # Report infiltration in mm/h
            self.report(FcA * tHour * 1000.0, "infilt")
            # Surface storage (mm)
            # self.report(self.DSt * 1000.0, 'surfSt')        
            # runoff generated (mm/h)
            self.report(q * tHour * 1000.0, 'rnfgen')
            # discharge (m3/s)
            self.report(log10(self.Q + 0.001), 'runoff')        
            # self.report(self.H, 'waterd')            
        

    def postdynamic(self):
        logger.debug("Starting postdynamic!")
        
        
        ### Erosion model
                       
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
        