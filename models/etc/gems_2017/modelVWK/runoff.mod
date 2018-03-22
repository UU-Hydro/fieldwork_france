binding

 ## GENERAL
 T=scalar(30);                              # time of one timestep (s)
 Dem=dem.map;                               # elevation model
 Vegetation=veg.map;                       # vegetation map
 Regolith=reg.map;                         # regolith
 Ldd=ldd.map;


 ## PRECIPITATION
  PStop=scalar(20);                          # end of rainstorm (minutes)
  Prec=0.02;                                 # precipitation (m)


 ## CONSTANT INFILTRATION WITH CURVE
  KsTable=ks.txt;                           # average saturated conductivity, m/h!!
  BTable=hf.txt;                             # suction head below wetting front (negative, m)
 Poros=0.4;                                    # porosity (-)
 TauIni=0.05;                                  # initial moisture content
 Ks=ks.map;
 B=b.map;

 ## INTERCEPTION EUROSEM WITH DATA SET SIMONE
  CovTable=cov.txt;                       
  LAITable=lai.txt;                             # LAI (-)
  ICStI=scalar(0);                          # initial content interception store (m, for area
                                           # covered, 'Cov area')
  ICorr=1;                                  # correction factor canopy (0.046 * LAI, is unit correct?)
  LAI=lai.map;
  Cov=cov.map;


 ## SURFACE STORAGE WITH DATA SET SIMONE
  #RFRTable=rfr.tbl;                             #  surface roughness (cm/m) 


 ## ROUTING
  NTable=n.txt;                             #  manning's N
  N=n.map;

 QIni=scalar(0.000000000001);                 # initial streamflow (m3/s)
 Beta=scalar(0.6);                            # Beta
 ChFrac=1;                                    # area fraction of all channels ???
 NrChPerCell=1;                               # nr of channels per cell ???
 SlopeCl=slope.map;

areamap
 Dem;

timer
 1 240 1;
 reportdefault=2+2..endtime;
 #on=1,10+10..endtime;
 #off=0;

initial

 # amount of rainfall of event (mm)
 report Pevent=Prec*1000;
 report Ldd=lddcreate(Dem,1e31,1e31,1e31,1e31);

 ## GENERAL
 # cell area (m2)
 CA=cellarea();
 


 ## PRECIPITATION                                         ######### INITIAL ##################

              # # conversion mm/h to m/timestep for rain
              # RainConv=1/((60*60*1000)/T);
 # end of rainstorm (s)
 PStopSec=PStop*60;
 # precipitation per timestep (m)
 Rain=(Prec/PStopSec)*T;
 # end of rainstorm (timesteps)
 PStopSt=PStopSec/T;

 # cumulative rain (m)
 PCum=if(defined(Dem),0);
 RNCum=if(defined(Dem),0);
 # initial duration of rainstorm (h)
 PDur=0.000000001;
 # nr of timesteps with discharge
 QDurTS=0;



 ## INFILTRATION GREEN & AMPT 

 # sat. inf. rate (m/h)
 report Ks=lookupscalar(KsTable,Regolith);
 # total amount of water on surface (m)
 SurW=scalar(0);
 # saturated conductivity (m/timestep)
 $4 KsSt=(Ks/3600)*T;
 # actual initial infiltration per timestep ('rate', m/timestep)
 FcA=scalar(0.00000001);
 # cumulative initial infiltration ('rate', m/timestep)
 FCum=scalar(0.0000000001);
 # suction head at wetting front (negative, m)
 B=lookupscalar(BTable,Regolith);
 report hf.map=B;

 # available pore space
 DTau=Poros-TauIni;  
 
 
 ## INTERCEPTION
 # initial content of interception store (m, for area covered, 'Cov area')
 ICSt=ICStI;
 # leaf area index
 report LAI=lookupscalar(LAITable,Vegetation);
 # maximum content of interception store (m, for area covered, 'Cov area'), m
 ICStM=max(0.935+0.498*LAI-0.00575*sqr(LAI),0.0000001)/1000;
 # initial intercepted water, cumulative (m)
 S=scalar(0);
 # area covered with vegetation
 report Cov=lookupscalar(CovTable,Vegetation);


 # SURFACE STORAGE
 # Surface roughness in direction of flow (cm/m).
 #report RFR=lookupscalar(RFRTable,Regolith);
 # maximum surface storage (m)
 #report D=exp(-6.6+0.27*RFR);
 D=0.001;
 # amount of water in surface storage (m)
 DSt=scalar(0);
 # surface storage is full
 #SurfStF=boolean(0);



  ## ROUTING

  # cell size (m)
  CL=celllength(); 

  # distance to downstream cell (m)
  $4 DCL=max(downstreamdist(Ldd),CL);
  # classic slope (m/m), must be larger than 0
  report SlopeCl=max(0.001,slope(Dem));
  # slope to downstream neighbour
  $4 SlopeDS=(Dem-downstream(Ldd,Dem))/downstreamdist(Ldd);
  $4 Slope=cover(max(0.0001,SlopeDS),0.0001);
 
  # initial streamflow (m3/s)
  Q=QIni;
  # initial flow out of cell (m/T)
  QR=scalar(0);
  # cumulative amount of water added to streamflow (m) 
  qCum=scalar(0);

 # manning's n
 report N=lookupscalar(NTable,Regolith);
 
  # term for Alpha
  $4 AlpTerm=(N/(sqrt(Slope)))**Beta;
  # power for Alpha
  $4 AlpPow=(2/3)*Beta;

  # initial water height (m)
  H=scalar(0.000000001);
  # bottom width for routing (m)
  $4 Bw=ChFrac*CL; 
  # initial approximation for Alpha
  # wetted perimeter (m) assume 8 channels per cell!
  P=Bw+2*NrChPerCell*H;
  $4 PIni=P;
  # Alpha
  Alpha=AlpTerm*(P**AlpPow);
  $4 AlphaIni=Alpha;

  # simulated cumulative runoff (m3)
  QRCum=scalar(0);

 # derivatives of dem
 # upstream area (m2)
 $4 Up=accuflux(Ldd,cellarea()); 
 $4 LogUp=log10(Up+0.0001); 
 # slope
 $4 SlopeReal=slope(Dem);
 # aspect
 $4 Aspect=aspect(Dem);
 # profile curvature
 $4 ProfCurv=profcurv(Dem);
 # planform curvature
 $4 PlanCurv=plancurv(Dem);



  #### BUDGET CHECK ####
  # cumulative actual infiltration per timestep (m), averaged over whole cell
  FcACCum=scalar(0);
  # cumulative runoff (m3)
  #QrCum=scalar(0);


 # m/timestep to m/hour
 ConTH=3600/T;
 #RUGenCum=0;


dynamic
 
 ## PRECIPITATION
 # rain per timestep, constant rain (m/timestep)
 Pr=if(time() lt PStopSt,Rain,0);
 #$4 pr.tss=timeoutput(Out,Pr);

 # rain (m/h)
 report PrH=Pr*ConTH*scalar(defined(Regolith));
 #report PrHTss=timeoutput(,PrH);
 
 # cumulative rain (m)
 report(endtime) PCum=Pr+PCum;
 #report PCumTss=timeoutput(LandUnit,PCum);

 ## INTERCEPTION
 # intercepted water per timestep (m, spreaded over whole cell)
 Int=Pr*Cov;
 #report int.tss=timeoutput(Out,Int);


 # amount in interception store (m, for area covered (for 'Cov area'))
 ICStOld=ICSt;
 ICSt=ICStM*(1-exp((-ICorr*PCum)/ICStM));
 #report icst.tss=timeoutput(Out,ICSt);

 # to interception store (m/timestep, for area covered (for 'Cov area'))
 ToICSt=ICSt-ICStOld;
 #report toicst.tss=timeoutput(Out,ToICSt);

 # to interception store (m/timestep, spreaded over whole cell)
 ToICStC=Cov*ToICSt;
 #report toicstc.tss=timeoutput(Out,ToICStC);
 # to interception store (m/timestep, spreaded over whole cell)
 ToICStCH=ToICStC*ConTH;
 # to interception store (m/h, spreaded over whole cell)
 #report IntTss=timeoutput(LandUnit,ToICStCH);
 
 # throughfall (m, spreaded over whole cell)
 TF=Int-ToICStC;
 #report tf.tss=timeoutput(Out,TF);
 
 # total net rain per timestep (m, spreaded over whole cell)                            ########## DYNAMIC ################
 RainNet=TF+(Pr-Int);
 #report rainnet.tss=timeoutput(Out,RainNet);

 # net rain (m/h), also referred to as throughfall
 report TF=RainNet*ConTH*scalar(defined(Regolith));

 # cumulative net rain (m, spreaded over whole cell)
 report(endtime) RNCum=RNCum+RainNet;

 # amount in interception store (m, spreaded over whole cell)
 ICStC=Cov*ICSt;
 #report icstc.tss=timeoutput(Out,ICStC);
 report SCell=ICStC;

 
            #  	 ## NO INTERCEPTION
            #  	 #  to interception store (m/timestep)
            #  	 ToICStC=scalar(0);
            #  	 $11 $4 toicstc.tss=timeoutput(Out,ToICStC);
            #  	  
            #  	 # total net rain per timestep (m)         
            #  	 report RainNet=Pr;
            #  	 $11 $4 rainnet.tss=timeoutput(Out,RainNet);
            #  	  
            #  	 # amount in interception store (m, spreaded over whole cell)
            #  	 ICStC=scalar(0);
            #  	 $11 $4 icstc.tss=timeoutput(Out,ICStC);






 ## INFILTRATION                                       ############## DYNAMIC ###############
 
 # flow out off the cell (m/timestep)
 QR=(Q*T)/CA;

 # total amount of water on surface, waterslice (m)
 SurW=RainNet+DSt+QR;

 # cumulative infiltration (m)
 FCum=FCum+FcA;
 ##CQB report fcum.tss=timeoutput(Out,FCum);

 # potential infiltration per timestep ('rate', m/timestep)
 Fc = KsSt*((-B*DTau+FCum)/FCum);
 ###CQB report fc.tss=timeoutput(Out,Fc);

 # actual infiltration per timestep ('rate', m/timestep)
 FcA=if(SurW gt Fc,Fc,SurW);
 ###CQB report fca.tss=timeoutput(Out,FcA);
 # actual infiltration ('rate', m/h)
 report I=FcA*ConTH;
 #report FcATss=timeoutput(LandUnit,FcAH);

 # total amount of water on surface after infiltration (m)
 SurW=max(SurW-FcA,0);
 

        #   ## NO INFILTRATION
 
        #   # flow out off the cell (m/timestep)
        #   report QR=(Q*T)/CA;
        #  
        #   # total amount of water on surface, waterslice (m)
        #   report SurW=RainNet+DSt+QR;



### SURFACE STORAGE
 
 # amount of water in surface storage (m)
 DStO=DSt;
 report DSt=if(SurW gt D,D,SurW);
 #report dst.tss=timeoutput(Out,DSt); 
 
 # flux to surface storage (m/timestep)
 DStCh=DSt-DStO;
 #report dstch.tss=timeoutput(Out,DStCh); 
 # flux to surface storage (m/h)
 DStChH=DStCh*ConTH;
 #report DStChTss=timeoutput(LandUnit,DStChH);
 # surface storage is full
 #report SurfStF=not(DSt lt D);
 #report surfst_f.tss=timeoutput(Out,SurfStF);                      ########### DYNAMIC ###############


        #      ## NO SURFACE STORAGE
        #     
        #      # amount of water in surface storage
        #      DSt=scalar(0);  
        #      # flux to surface storage (m/timestep)
        #      DStCh=scalar(0);
        #      $11 $4 dstch.tss=timeoutput(Out,DStCh);                      


 ## POST SURFACE STORAGE

 # total amount of water on surface after infiltration and surface storage (m)
 SurW=max(SurW-DSt,0);
 # amount of water added to streamflow (m/timestep)
 q=SurW-QR;
 #report q.tss=timeoutput(Out,q);
 # runoff generated (m/h)
 report RG=q*ConTH*scalar(defined(Regolith));
 # cumulative amount of water added to streamflow (m)
 qCum=qCum+q;
 #report qcum.tss=timeoutput(Out,qCum);


 # BUDGET CHECK

 # FLUXES rain minus (to interception store + act. infil + surface stor)
 BudFl=Pr-(ToICStC+FcA+DStCh+q); 
 #report budfl.tss=timeoutput(Out,BudFl);

 #  STORAGES rain minus (to interception store + act. infil + surface stor + avai ro)
 BudSto=PCum-(ICStC+FCum+DSt+qCum);
 #report budsto.tss=timeoutput(Out,BudSto);
 

 
 ## ROUTING
 # amount of water added to streamflow (m3/s)
 QIn=(q*CA)/T;
 #report qin.tss=timeoutput(Out,QIn);

 # discharge (m3/s)
 report Q=kinematic(Ldd,Q,QIn/DCL,Alpha,Beta,1,T,DCL);
 #report qr.tss=timeoutput(Out,Q);

 # water depth (m)
 H=(Alpha*(Q**Beta))/Bw;
 #report h.tss=timeoutput(Out,H);

 # wetted perimeter (m) 
 P=Bw+2*NrChPerCell*H;
 #report p.tss=timeoutput(Out,P);

 # Alpha
 Alpha=AlpTerm*(P**AlpPow);
 #report alpha.tss=timeoutput(Out,Alpha);

 # total area A
 A=Bw*H;


 ## reports
 # discharge (litre/s)
 #report QL=Q*1000;
 #report QL1Tss=timeoutput(Out,QL);
 #report LogQL=log10(QL+0.001);
 # discharge (m/h)
 #QH=(Q/Up)*3600;
 #report QHTss=timeoutput(Out,QH);
 
 
 # simulated cumulative runoff (m3)
 report(endtime) QRCum=QRCum+Q*T; 
 #report QRCum1_Tss=timeoutput(Out,QRCum1);


         # ## GENERAL INFO
         # # flow velocity (m/s)
         # $11 report V=(Q/A);
         # $11 $4 v.tss=timeoutput(Out,V);


 ## INTERFACE 
 # runoff generated per unit (m/h)
 #report RUGen=(Pr-ToICStC-FcA-DStCh)*ConTH;
 #report RUGenTss=timeoutput(LandUnit,RUGen);
 # cumulative runoff generated (m)
 #RUGenCum=RUGenCum+RUGen/ConTH;
 #report RUGenCumTss=timeoutput(LandUnit,RUGenCum);
 
 # cumulative runoff (m3)
 #report QrCum=QrCum+Q*T; 
 #report qrcum.tss=timeoutput(Out,QrCum);
 # cumulative runoff (m)
 #QrCumM=QrCum/Up;
 #report QrCMTss=timeoutput(Out,QrCumM);

 # cumulative interception (m3)
 ICStV=ICStC*CA;
 # cumulative interception in subcatchment (m3)
 ICSub=catchmenttotal(ICStV,Ldd);
 #report icsub.tss=timeoutput(Out,ICSub);
 # cumulative interception (m)
 #report ICSMTss=timeoutput(LandUnit,ICStC);

 # cumulative actual infiltration (m3)
 FcACCumV=FCum*CA;
 # cumulative actual infiltration in subcatchment (m3)
 #report FcSub=catchmenttotal(FcACCumV,Ldd);
 #report fcsub.tss=timeoutput(Out,FcSub);
 # cumulative actual infiltration (m3)
 #report FSMTss=timeoutput(LandUnit,FCum);

 # amount in surface storage (m3)
 DStV=DSt*CA;
 # amount in surface storage in subcatchment (m3)
 DStSub=catchmenttotal(DStV,Ldd); 
 #report dstsub.tss=timeoutput(Out,DStSub);
 # amount in surface storage (m)
 #report DSSMTss=timeoutput(LandUnit,DSt);

 
 ## BUDGET CHECK

 # in subcatchment, cumulative rain = cumulative interception + cumulative infiltration +
 # surface storage + cumulative runoff + cumulative evapotranspiration
 # everything in cubic metres
  
 # cumulative rain (m3) 
 PCumV=PCum*CA;
 # cumulative rain in subcatchment (m3)
 #report PSub=catchmenttotal(PCumV,Ldd);
 #report psub.tss=timeoutput(Out,PSub);

 #report BudTot=PSub-(ICSub+FcSub+DStSub+QrCum);
 #report budtot.tss=timeoutput(Out,BudTot);

              #    ## and...
              #    # cumulative amount of water added to streamflow (m3)
              #    report qCumV=qCum*CA;
              #    # cumulative amount of water added to streamflow (m3)  in subcatchment, compare with QrCum!, qrcum.tss
              #    report qCumSub=catchmenttotal(qCumV,Ldd);
              #    $11 report qcumsub.tss=timeoutput(Out,qCumSub);


 ## REPORTS
 # budget check for all locations
 #report BTTss=timeoutput(Out,BudTot);

