from gem.model import *

class Model(GemModel):
    """
    Models the runoff produced by rainfall and the resulting potential erosion based on vegetation and regolith properties
    """
    meta={
        #
        # Metadata
        #
        'name':                 'input_test_rainfall_runoff_erosion',
        'author':               'Wouter Marra',
        'contact':              '',
        'abstract':             'Models the runoff produced by rainfall and the resulting potential erosion based on vegetation and regolith properties',
        'license':              '',
        'tags':                 ['erosion','rainfall','hydrology', 'runoff'],
        'discretization':       'frankrijk_vwk_2017_50m',
        'maxchunks':            1
    }
    parameters={
        'COV': '{ 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}',
        'LAI': '{ 1: 1.0, 2: 2.0, 3: 3.0, 4: 4.0}',
        'cc': '{ 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}',
        'gc': '{ 1: 0.1, 2: 0.2, 3: 0.3, 4: 0.4}',
        'ph': '{ 1: 5, 2: 12, 3: 8, 4: 2}',
        'ksat': '{ 1: 0.01, 2: 0.02, 3: 0.03, 4: 0.02}',
        'hf': '{ 1: -0.01, 2: -0.02, 3: -0.03, 4: -0.02}',        
        'K': '{ 1: 0.05, 2: 0.4, 3: 0.8, 4: 1.2}',
        'C': '{ 1: 12.0, 2: 3.0, 3: 3.0, 4: 2.0}',
        'areaNumber': 99
    }
    time={
        'start':                 '2000-01-01T00:00:00',
        'timesteps':             1,
        'timesteplength':        60
    }
    datasources={
        #
        # Refer to the documentation for information on datasources
        #
        
        'wcs':[
            #'http://arcgis-server.geo.uu.nl:6080/arcgis/services/FieldworkFrance/FieldworkFrance/MapServer/WCSServer'
            'http://turbo.geo.uu.nl/cgi-bin/mapserv?MAP=/data/projectdata/globaldata/globaldata.map'        
        ]
    }
    reporting={                   

        'veg': {
            'title':        "Vegetation map",
            'units':        "-",
            'info':            "Vegetation classes",
            'datatype':		"Byte",
            'symbolizer':{
                'type':		"categorical", #categorical data must have Byte datatype!!
                'colors':	["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"],
                'values':	[1,2,3,4,5,6,7,8,9],
                'labels':	["1","2","3","4","5","6","7","8","9"]
            }
        },
        'geom': {
            'title':        "Geomorphology map",
            'units':        "-",
            'info':            "Geomorphology classes",
            'datatype':		"Byte",
            'symbolizer':{
                'type':		"categorical", #categorical data must have Byte datatype!!
                'colors':	["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"],
                'values':	[1,2,3,4,5,6,7,8,9],
                'labels':	["1","2","3","4","5","6","7","8","9"]
            }
        },
        'cov': {
            'title':        "Total Vegetation Cover (COV)",
            'units':        "-",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    ["#440154", "#2a788e", "#7ad151", "#bddf26", "#fde725"],
                'values':    [-0.000001, 1.000001],
                'labels':    []
            }
        },
        'lai': {
            'title':        "Leaf-area index (LAI)",
            'units':        "m2/m2",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    ["#440154", "#2a788e", "#7ad151", "#bddf26", "#fde725"],
                'values':    [-0.000001, 20],
                'labels':    []
            }
        },
        'cc': {
            'title':        "Canopy Cover (cc)",
            'units':        "-",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    ["#440154", "#2a788e", "#7ad151", "#bddf26", "#fde725"],
                'values':    [-0.000001, 1.000001],
                'labels':    []
            }
        },  
        'gc': {
            'title':        "Ground Cover (gc)",
            'units':        "-",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    ["#440154", "#2a788e", "#7ad151", "#bddf26", "#fde725"],
                'values':    [-0.000001, 1.000001],
                'labels':    []
            }
        },       
        'ph': {
            'title':        "Plant Height (ph)",
            'units':        "m",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    ["#440154", "#2a788e", "#7ad151", "#bddf26", "#fde725"],
                'values':    [-0.000001, 20.000001],
                'labels':    []
            }
        },          
        'ks': {
            'title':        "Saturated conductivity (ks)",
            'units':        "m/hr",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    3, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-.000001,0.2],
                'labels':    []
            }
        },
        'hf': {
            'title':        "Soil suction (hf)",
            'units':        "m",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    9, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.05, 0.000001],
                'labels':    []
            }
        },
        'K': {
            'title':        "Soil detachability (K)",
            'units':        "g/J",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    5, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 2],
                'labels':    []
            }
        },
        'C': {
            'title':        "Soil cohesion (C)",
            'units':        "kPa",
            'info':            "",
            'datatype':        "Float32",
            'symbolizer':{
                'type':        "pseudocolor",
                'clamp':    True,
                'ticks':    6, #ticks only works on pseudocolor symbolizers
                'colors':    [ "#000004", "#8c2981", "#fe9f6d", "#fecf92", "#fcfdbf"],
                'values':    [-0.000001, 15],
                'labels':    []
            }
        }
    }
    def initial(self):
        logger.debug("Starting initial")
        
        areanr = self.readparam("areaNumber")        

        # Fetch data from WCS provider              
        self.veg = self.readmap("france.veg.%g" % areanr)
        self.geom = self.readmap("france.geom.%g" % areanr)
                            
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
        
        # lookup maps
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
        
    
       
        ### report initial maps and boundary conditions                          
        self.report(self.veg, 'veg')        
        self.report(self.geom, 'geom')        
        
        self.report(self.cov, 'cov')         
        self.report(self.lai, 'lai')         
        self.report(self.cc, 'cc')         
        self.report(self.gc, 'gc')         
        self.report(self.ph, 'ph')         
        
        self.report(self.ks, 'ks')         
        self.report(self.hf, 'hf')        
        self.report(self.K, 'K') 
        self.report(self.C, 'C')                 
        
        
    def dynamic(self):
        logger.debug('dynamic')
        
    def postdynamic(self):
        logger.debug('postdynamic')