import numpy as np

# Uguess = 100
# solvingUguess = True
# counter = 0
# AskScale = 'Me'

# while solvingUguess:

#     #heat exchanger for BitCoin farming
#     #typical temperature around 42.22 celcius
#     #want to cool to room temp 25 celcius
#     #use cold liq as water
#     #use hot liq as mineral oil (light oil)

#     #parameters BWG
#     Do = 1 * 0.0254
#     Di = 0.732 * 0.0254
#     DbarL = (Do - Di) / np.log(Do / Di)
#     Xw = 0.134 * 0.0254  
#     L = 8 * 0.3048

#     if AskScale == 'Me': #Celsius

#         #Shell Side#
#         #1 LMTD
#         ThotIn = 250 #celsius
#         ThotOut = 120 #celsius
#         TcoldOut = 100 #celsius
#         TcoldIn = 25 #celsius
#         LMTD = ((TcoldOut - TcoldIn) - (ThotIn - ThotOut)) / np.log(((TcoldOut - TcoldIn) / (ThotIn - ThotOut)))        

#         #2 Fouling
#         Rdg = 0.0005
#         Rdk = 0.001
#         hdg = 1 / Rdg
#         hdk = 1 / Rdk

#         #3 Flow Rate of Heating Stream
#         mflowcold = 100000
#         Cpcold = 0.48 * 4186.798188 #J/kg c
#         qcold = mflowcold * Cpcold * (TcoldOut - TcoldIn) #F -> J/h
#         newqcold = qcold / 3600 #J/s      

#         #newqcold = mflowhot * Cpg * ((ThotIn - ThotOut) * 1.8) #no heat loss

#         Cphot = 0.57 * 4186.798188
#         mflowhot = newqcold / (Cphot * (ThotIn - ThotOut)) #kg / s

#         #4 Fg for 1-2 Exchanger -> correction factor for LMTD
#         nh = (TcoldOut - TcoldIn) / (ThotIn - TcoldIn)
#         z = (ThotIn - ThotOut) / (TcoldOut - TcoldIn)
#         Fg = 0.85 #from graph

#         #5 Corrected LMTD
#         newLMTD = LMTD * Fg #celsius

#         #6 Guess U **important**
#         #Uguess = ? #look at chart for common U

#         #7 Outside Area
#         Ao = newqcold / (Uguess * newLMTD)

#         #8 Number of Tubes
#         Nt = Ao / (np.pi * Do * L)
#         Nt = np.ceil(Nt)

#         #9 Tube Pitch
#         Tubepitch = 1.25 * Do
#         Ki = 0.249
#         n1 = 2.207
#         Db = Do * (Nt / Ki)**(1 / n1)

#         #10 Clearance
#         #y = mx + c
#         #c 0.2 = 10, 1.2 = 20 -> every 1 x, y + 10 -> every 0.2 x, y + 2 -> at 0, y = 8
#         c = 8
#         m = (20 - 10) / (1.2 - 0.2)
#         clearance = m * Db + c #milli meter
#         clearance = clearance * 10**-3

#         #11 Shell Diameter
#         Ds = Db + clearance

#         #12 Baffle Pitch(P)
#         P = 0.4 * Ds

#         #13 Cross Section Flow Area(Sc)
#         Sc = P * Ds * (1 - (Do / Tubepitch))

#         #14 Gs
#         Gs = mflowcold / (Sc * 3600) #kg/m^2 s

#         #15 De
#         De = (4 * (((Tubepitch / 2) * 0.87 * Tubepitch) - (np.pi / 2 * Do**2 / 4))) / (np.pi * Do / 2)

#         #16 Re
#         millshell = 1.6 * 10**-3 #N * s
#         Re = (Gs * De) / millshell

#         #17 Pr  
#         Kk = 0.083 * 1.7295772056 #btu/h ft F -> w /m k
#         Pr = (Cpcold * millshell) / Kk

#         #18 hs from Nu -> individual heat transfer shell
#         jh = 0.018
#         Twavg = (ThotIn + TcoldIn) / 2
#         millshellwall = 1.2 * 10**-3 #N * s

#         hs = (jh * Re * Pr**(1/3) * (millshell/millshellwall)**0.14) * Kk / De #w / m^2 k 

#         #19 Pressure drop shell side
#         Jfshell = 0.07
#         roushell = 807.5 #kg / m^3, density of kerosene
#         Us = (mflowcold/(Sc * 3600)) / roushell #* 3600 to convert to seconds
#         ShellDeltaP = 8 * Jfshell * (Ds/De) * (L/P) * (roushell*(Us**2)/2) * (millshell/millshellwall)**-0.14 #kg/m s^2

#         #Tube Side#
#         #20 Nt per pass
#         Ntpp = Nt / 2

#         #21 Tube side volumetric velocity (Gi)
#         Gi = mflowhot / ((Ntpp * np.pi * Di**2) / 4) #mflowhot already in seconds

#         #22 Tube side velocity (Ui)
#         routube = 750 #kg / m^3
#         Ui = Gi / routube

#         #23 Pr and Re of tube side
#         Kg = 0.075 * 1.7295772056 #btu/h ft F -> w /m k
#         milltube = 0.4 * 10**-3 #n-octane #N * s
#         PrTube = (milltube * Cphot) / Kg
#         ReTube = (Gi * Di) / milltube

#         #24 Estimate tube-side heat trans. coeff.
#         milltubewall = 0.4 * 10**-3

#         if ReTube < 2100:
#             hi = 1.86 * (Kg / Di) * (ReTube * PrTube)**0.33 * (Di / L)**0.33 * (milltube/milltubewall)**0.14
#         else:
#             hi = 0.023 * (Kg / Di) * ReTube**0.8 * PrTube**0.33 * (1 + (Di / L))**0.7 

#         GasolineHeatTransCoeff = hs
#         KeroseneHeatTransCoeff = hi
#         FoulingFactorGasoline = hdg
#         FoulingFactorKerosene = hdk
#         Km = 26 * 1.7295772056 #btu/h ft F -> w /m k steel pipe
#         Uo = 1 / ((1/FoulingFactorGasoline)*(Do/Di) + (1/GasolineHeatTransCoeff)*(Do/Di) + (Xw/Km)*(Do/DbarL) + (1/KeroseneHeatTransCoeff) + (1/FoulingFactorKerosene))
#         #w / m^2 s

#         #25 Pressure drop tube side
#         Jftube = 0.009
#         TubeDeltaP = 1.5 + (Nt * (2.5 + (8 * Jftube * L / Di) + ((milltube/milltubewall)**-0.14))) * (routube * Ui**2 / 2)
#         print(f'Kerosene Pressure {ShellDeltaP} Pascal, Pressure {ShellDeltaP / 6895} PSI')    
#         print(f'Gasoline Pressure {TubeDeltaP} Pascal, Pressure {TubeDeltaP / 6895} PSI')
#         #keep count of iterations
#         counter += 1

#     if abs(Uo - Uguess) < 0.000000001:
#         solvingUguess = False
#         print(f'{counter} Final Answer {Uguess} {Uo}')
#     else:
#         print(f'{counter} Iterating {Uguess} {Uo}')
#         Uguess = Uo

Uguess = 800
solvingUguess = True
counter = 0

#heat exchanger for nuclear reactor (1-2)
#typical temperature around 300 +- 20% celcius (safety factor) -> 360 celcius
#want to cool to around 100 celcius
#use cold liq as brine outside
#use hot liq as water inside
#tungsten as tube material

#pipe parameters BWG no.10, 1.5 inch pipe
Do = 2 / 39.37 #1.5 inch to meter
Di = 1.732 / 39.37 #1.2322 inch to meter
Xw = 0.134 / 39.37 #0.134 inch to meter
L = 5 #5 meters of tube pipe -> 2.5 meter long tube 
DbarL = (Do - Di) / np.log(Do / Di)

typeofhead = [
    'Pull-Through',
    'Split-Ring',
    'Outside-Packed',
    'Fixed-UTube'
]

head = typeofhead[0]

while solvingUguess:

#-------------------------------------------------------------------------------------------#

    #Shell Side#
    #1 LMTD
    ThotIn = 360 #celsius
    ThotOut = 120 #celsius
    TcoldOut = 100 #celsius
    TcoldIn = 25 #celsius
    LMTD = ((TcoldOut - TcoldIn) - (ThotIn - ThotOut)) / np.log(((TcoldOut - TcoldIn) / (ThotIn - ThotOut)))        

    #2 Fouling
    Rdcold = 0.00025 #resistance of brine
    Rdhot = 0.0001 #resistance of water
    hdcold = 1 / Rdcold
    hdhot = 1 / Rdhot

    #2.1 Cp of salt solution -> cold stream
    #total weight of salt solution flow = 100000
    #25% salt solution -> 75000 water, 25000 salt
    #therefore, Cpmixture = (m1/mmixture)*Cp1 + (m2/mmixture)*Cp2
    mass1 = 75000 / 3600 #water kg / s
    mass2 = 25000 / 3600 #salt kg / s
    massmixture = 100000 / 3600 #brine stream kg / s
    Cp1 = 4180 #J / kg K
    Cp2 = 880 #J / kg K
    Cpmixture = (mass1/massmixture)*Cp1 + (mass2/massmixture)*Cp2

    #3 Flow Rate of Heating Stream
    mflowcold = 100000 / 3600 #kg / s
    Cpcold = Cpmixture #J/kg K
    qcold = mflowcold * Cpcold * (TcoldOut - TcoldIn) #J / s

    #qcold = mflowhot * Cpg * ((ThotIn - ThotOut) * 1.8) #no heat loss

    Cphot = 4180 #J / kg K
    mflowhot = qcold / (Cphot * (ThotIn - ThotOut)) #kg / s

    #4 Fg for 1-2 Exchanger -> correction factor for LMTD
    nh = (TcoldOut - TcoldIn) / (ThotIn - TcoldIn)
    z = (ThotIn - ThotOut) / (TcoldOut - TcoldIn)
    Fg = 0.9 #from graph

    #5 Corrected LMTD
    newLMTD = LMTD * Fg #celsius

    #6 Guess U **important**
    #Uguess = ? #look at chart for common U

    #7 Outside Area
    Ao = qcold / (Uguess * newLMTD)

    #8 Number of Tubes
    Nt = Ao / (np.pi * Do * L)
    Nt = np.ceil(Nt)

    #9 Tube Pitch -> triangular pitch 1-2 exchanger
    Tubepitch = 1.25 * Do
    Ki = 0.249
    n1 = 2.207
    Db = Do * (Nt / Ki)**(1 / n1)

    #10 Clearance http://www.wermac.org/equipment/heatexchanger_part5.html -> depends on head
  
    if head == typeofhead[0]: #Pull through
        #y = mx + c
        #c 0.2 = 88, 1.2 = 96 -> every 1 x, y + 8 -> every 0.2 x, y + 1.6 -> at 0, y = 88 - 1.6
        c = 88 - 1.6
        m = (96 - 88) / (1.2 - 0.2)
    elif head == typeofhead[1]: #Split ring
        #y = mx + c
        #c 0.2 = 50, 1.2 = 77 -> every 1 x, y + 27 -> every 0.2 x, y + 5.4 -> at 0, y = 50 - 5.4
        c = 50 - 5.4
        m = (77 - 50) / (1.2 - 0.2)
    elif head == typeofhead[2]: #Outside packed
        c = 38
        m = 0      
    elif head == typeofhead[3]: #Fixed u tube
        #y = mx + c
        #c 0.2 = 10, 1.2 = 20 -> every 1 x, y + 10 -> every 0.2 x, y + 2 -> at 0, y = 10 - 2
        c = 10 - 2
        m = (20 - 10) / (1.2 - 0.2)

    clearance = (m * Db) + c 
    clearance = clearance * 10**-3 #milli meter

    #11 Shell Diameter
    Ds = Db + clearance

    #12 Baffle Pitch(P)
    P = 0.4 * Ds

    #13 Cross Section Flow Area(Sc)
    Sc = P * Ds * (1 - (Do / Tubepitch))

    #14 Gs
    Gs = mflowcold / Sc #kg/m^2 s

    #15 De
    De = (4 * (((Tubepitch / 2) * 0.87 * Tubepitch) - (np.pi / 2 * Do**2 / 4))) / (np.pi * Do / 2)

    #16 Re
    millshell = 1.2 * 10**-3 #N * s, temp of brine around 100 + 25 / 2 = 62.5 celsius
    Re = (Gs * De) / millshell

    #17 Pr 
    #K value of saltwater decreases with increasing salinity, but increase with temperature
    #https://www.google.com/search?q=The+thermal+conductivity+of+seawater&hl=en&sxsrf=AOaemvKWJvPyI9SCpZIG3u5SRB-GGI4_YQ:1635936424041&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjv8LeLgvzzAhUp63MBHWi_B_QQ_AUoAXoECAEQAw&biw=958&bih=959&dpr=1#imgrc=c3Ac_9sBpaQQKM
    #equation is approximately y = (0.57 - 0.535 / 310 - 290)x + c
    #to find c we guess from 5% to 6% solution decrease in y by around 0.01
    #therefore, from 5% to 25% decrease by 0.2
    #which is 0.54 - 0.2 = 0.34
    Kk = 0.34 #w /m k
    Pr = (Cpcold * millshell) / Kk

    #18 hs from Nu -> individual heat transfer shell
    jh = 4 * 10**-2 #find from graph
    #temp at wall avg = (ThotIn + TcoldIn) / 2 -> 192.5
    millshellwall = 0.24 * 10**-3 #N * s

    hshell = (jh * Re * Pr**(1/3) * (millshell/millshellwall)**0.14) * Kk / De #w / m^2 k 

    #19 Pressure drop shell side
    Jfshell = 0.042 #find from graph
    roushell = 1150 #kg / m^3, density of brine
    Us = (mflowcold / Sc) / roushell
    ShellDeltaP = 8 * Jfshell * (Ds/De) * (L/P) * (roushell*(Us**2)/2) * (millshell/millshellwall)**-0.14 #kg/m s^2

    #Tube Side#
    #20 Nt per pass
    Ntpp = Nt / 2

    #21 Tube side volumetric velocity (Gi)
    Gi = mflowhot / ((Ntpp * np.pi * Di**2) / 4) #mflowhot already in seconds

    #22 Tube side velocity (Ui)
    routube = 997 #kg / m^3 density of water
    Ui = Gi / routube

    #23 Pr and Re of tube side https://www.engineeringtoolbox.com/water-liquid-gas-thermal-conductivity-temperature-pressure-d_2012.html
    #at 0.01 celsius K water = 0.55575 -> c
    #at 99.6 celsius, K water = 0.67703
    #therefore y = mx + c, y = (0.67703 - 0.55575 / 99.6 - 0.01)(240) + 0.55575 = 0.848
    Kg = 0.848 #thermal conduct of water w /m k at 360 + 120 / 2 = 240 celcius with no phase change
    milltube = 0.05 * 10**-3 #water #N * s
    PrTube = (milltube * Cphot) / Kg
    ReTube = (Gi * Di) / milltube

    #24 Estimate tube-side heat trans. coeff.
    milltubewall = 0.14 * 10**-3 #water at 192.5 celsius

    if ReTube < 2100:
        htube = 1.86 * (Kg / Di) * (ReTube * PrTube)**0.33 * (Di / L)**0.33 * (milltube/milltubewall)**0.14
    else:
        htube = 0.023 * (Kg / Di) * ReTube**0.8 * PrTube**0.33 * (1 + (Di / L))**0.7 

    GasolineHeatTransCoeff = hshell
    KeroseneHeatTransCoeff = htube
    FoulingFactorGasoline = hdhot
    FoulingFactorKerosene = hdcold
    Km = 164 #w /m k tungsten pipe
    Uo = 1 / ((1/FoulingFactorGasoline)*(Do/Di) + (1/GasolineHeatTransCoeff)*(Do/Di) + (Xw/Km)*(Do/DbarL) + (1/KeroseneHeatTransCoeff) + (1/FoulingFactorKerosene))
    #w / m^2 s

    #25 Pressure drop tube side
    #relative roughness https://www.researchgate.net/figure/Surface-texture-of-direct-laser-deposited-tungsten-carbide-a-2D-surface-profile-b_fig1_249994402
    #lowest = 100 micro meters
    #highest = 80 micro meters
    #avg = 100 + 80 / 2 = 90 micro meters of roughness
    #inside pipe diameter = 0.0135128
    #k / D = avg / inside pipe diameter = 90 micro meters / 0.0135128 = 6.66 * 10^-3
    Jftube = 0.008
    TubeDeltaP = 1.5 + (Nt * (2.5 + (8 * Jftube * L / Di) + ((milltube/milltubewall)**-0.14))) * (routube * Ui**2 / 2)
    #print(f'Brine (Outside) Pressure {ShellDeltaP} Pascal, Pressure {ShellDeltaP / 6895} PSI')    
    #print(f'Water (Inside) Pressure {TubeDeltaP} Pascal, Pressure {TubeDeltaP / 6895} PSI')
 
    #keep count of iterations
    counter += 1

#-------------------------------------------------------------------------------------------#
   
    #end conditions

    if abs(Uo - Uguess) < 0.000000001:
        solvingUguess = False
        print(f'({counter}) (Final U - {Uguess} {Uo}) (Outside P - {ShellDeltaP} Pa {ShellDeltaP / 6895} PSI) (Inside P - {TubeDeltaP} Pa {TubeDeltaP / 6895} PSI) (Head - {head})')
    else:
        print(f'({counter}) (Iterating U - {Uguess} {Uo}) (Outside P - {ShellDeltaP} Pa {ShellDeltaP / 6895} PSI) (Inside P - {TubeDeltaP} Pa {TubeDeltaP / 6895} PSI)')
        Uguess = Uo
          
