  
 --------------------------------------------
 Physics Parameters:
 -------------------
    gravity:   9.8100000000000005     
    density water:   1025.0000000000000     
    density air:   1.1499999999999999     
    ambient pressure:   101300.00000000000     
    earth_radius:   6367500.0000000000     
    coordinate_system:           1
    sea_level:   0.0000000000000000     
  
    coriolis_forcing: F
    theta_0:   0.0000000000000000     
    friction_forcing: T
    manning_coefficient:   2.5000000000000001E-002
    friction_depth:   20.000000000000000     
  
    dry_tolerance:   1.0000000000000000E-004
  
 --------------------------------------------
 Refinement Control Parameters:
 ------------------------------
    wave_tolerance:   1.0000000000000000E-002
    speed_tolerance:   1000000000000.0000        1000000000000.0000        1000000000000.0000        1000000000000.0000        1000000000000.0000        1000000000000.0000     
    Variable dt Refinement Ratios: T
 
  
 --------------------------------------------
 SETDTOPO:
 -------------
    num dtopo files =            0
  
 --------------------------------------------
 SETTOPO:
 ---------
    mtopofiles =            1
    
    /home/axel/Documents/EPFL/PDM/Trift/TriftGeoclaw/AVAC/bathymetry.xyz                                                                                  
   itopotype =            1
   mx =          250   x = (   5.0000000001091394E-003 ,   2.4949999999998909      )
   my =          180   y = (   5.0000000001091394E-003 ,   1.7950000000000728      )
   dx, dy (meters/degrees) =    9.9999999999991242E-003   9.9999999999997972E-003
  
   Ranking of topography files  finest to coarsest:            1
  
  
 --------------------------------------------
 SETQINIT:
 -------------
 /home/axel/Documents/EPFL/PDM/Trift/TriftGeoclaw/AVAC/qinit.xyz                                                                                       
   
 Reading qinit data from
 /home/axel/Documents/EPFL/PDM/Trift/TriftGeoclaw/AVAC/qinit.xyz                                                                                       
   
  
 --------------------------------------------
 Multilayer Parameters:
 ----------------------
    check_richardson: T
    richardson_tolerance:  0.94999999999999996     
    eigen_method:           4
    inundation_method:           2
    dry_tolerance:   1.0000000000000000E-004
