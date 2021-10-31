import numpy as np

# #1 LMTD
# th2 = 160
# th1 = 120
# tc2 = 120
# tc1 = 75
# LMTD = ((tc2 - tc1) - (th2 - th1)) / np.log(((tc2 - tc1) / (th2 - th1)))

# #2 Fouling
# Rdg = 0.0005
# Rdk = 0.001
# hdg = 1 / Rdg
# hdk = 1 / Rdk

# #3 Flow Rate of Heating Stream
# mflowcold = 150000
# CpkSi = 0.48 * 2.20462 * 1055.06
# qk = mflowcold * CpkSi * ((tc2 - tc1) * 1.8) #F -> J/h
# newqcold = qk / 3600 #J/s 

# Cphot = 0.57 * 2.20462 * 1055.06
# #newqcold = mflowhot * Cphot * ((th2 - th1) * 1.8) #no heat loss

# solving = True
# mflowhot = 0
# while solving:
#     RHS = mflowhot * Cphot * ((th2 - th1) * 1.8)
#     LHS = newqcold
#     #print(LHS, RHS)
#     if RHS > LHS:
#         solving = False
#         print(mflowhot * 3600) #in kg/s
#     else:
#         if abs(LHS - RHS) < 1000:
#             mflowhot += 0.00001
#         else:
#             mflowhot += 0.01

# newmflowhot = mflowhot * 3600

# #4 Fg for 1-2 Exchanger
# nh = (tc2 - tc1) / (th2 - tc1)
# z = (th2 - th1) / (tc2 - tc1)
# Fg = 0.85 #from graph

# #5 Corrected LMTD
# newLMTD = LMTD * Fg #celsius

# #6 Guess U **important**
# Uguess = 100 #look at chart for common U

# #7 Outside Area
# #newqcold / Ao = Uguess * newLMTDs

# solving = True
# Ao = 1
# while solving:
#     RHS = newqcold / Ao
#     LHS = Uguess * newLMTD
#     #print(LHS, RHS)
#     if abs(LHS - RHS) < 0.01:
#         solving = False
#         print(Ao) #m^2
#     else:
#         if abs(LHS - RHS) < 100:
#             Ao += 0.001
#         else:
#             Ao += 10

# Aonew = Ao * 10.764

# #8 Number of Tubes
# Nt = Aonew / (np.pi * (1 / 12) * 8)
# Nt = np.ceil(Nt)

# #9 Tube Pitch
# Tubepitch = 1.25 * (1 / 12)
# Ki = 0.249
# Db = (1 / 12) * np.power((Nt / Ki),(1 / 2.207)) 

# #10 Clearance
# #y = mx + c
# #c 0.2 = 10, 1.2 = 20 -> every 1 x, y + 10 -> every 0.2 x, y + 2 -> at 0, y = 8
# c = 8
# m = (20 - 10) / (1.2 - 0.2)
# clearance = m * 2.336 + c #milli meter
# clearance = clearance * 10**-3

# #11 Shell Diameter
# Ds = Db + clearance

# #12 Baffle Pitch(P)
# P = 0.4 * Ds

# #13 Cross Section Flow Area(Sc)
# Sc = P * Ds * (1 - (Do / Tubepitch))

# #14 Gs
# Gs = (mflowcold * 2.20462) / Sc #convert 

# #15 De
# De = (4 * (((Tubepitch / 2) * 0.87 * Tubepitch) - (np.pi / 2 * Do**2 / 4))) / (np.pi * Do / 2)

# #16 Re
# mill = 1.6 * 2.4191
# Re = Gs * De / mill

# #17 Pr
# Kk = 0.083
# CpkIm = 0.48
# Pr = CpkIm * mill / Kk

# #18 hs from Nu
# jh = 0.018
# Twavg = (160 + 120) / 2
# millwall = 1.2 * 2.4191
# #hs * De / Kk = jh * Re * Pr**(1/3) * (mill/millwall)**0.14

# solving = True
# hs = 0
# while solving:
#     RHS = jh * Re * Pr**(1/3) * (mill/millwall)**0.14
#     LHS = hs * De / Kk
#     #print(LHS, RHS)
#     if abs(LHS - RHS) < 0.001:
#         solving = False
#         print(hs) #Btu/h*F*ft^2
#     else:
#         if abs(LHS - RHS) < 10:
#             hs += 0.001
#         elif abs(LHS - RHS) < 0.01:
#             hs += 0.0000000001
#         else:
#             hs += 10

# #19 Pressure Drop
# Jf = 0.07
# L = 8
# rouShell = 50 #lb/ft^3
# Di = (0.732 / 12)
# #since Re = rouShell * Us * Di / mill
# Us = (Re * mill) / (rouShell * Di)
# DeltaPs = 8 * Jf * (Ds/De) * (L/P) * (rouShell*Us/2)**2 * (mill/millwall)**0.14
# #DeltaPs => lbm / ft * hr^2
# #1psi = 6.004 * 10^10 lbm / ft * hr^2
# #?psi = 2 * 10^11 lbm / ft * hr^2
# DeltaPs = DeltaPs / (6.004 * 10**10) #psi

# #Tube side#
# #20 Nt per pass
# Ntpp = Nt / 2

# #21 Tube side velocity (Gi)
# Gi = mflowhot / ((Ntpp * np.pi * Di**2) / 4)

# #22 Ui
# rouTube = 47 #lb/ft^3
# Ui = Gi / rouTube

# #23 Pr and Re of tube side
# Kg = 0.075 #Btu/h*ft*F
# millTube = 0.4 * 2.4191 #n-octane
# PrTube = (millTube * Cpg) / Kg
# ReTube = (Gi * Di) / millTube

# #24 Estimate tube-side heat trans. coeff.
# millTubewall = 0.4 * 2.4191
# if Re < 2100:
#     hi = 1.86 * (Kg / Di) * (ReTube * PrTube)**0.33 * (Di / 8)**0.33 * (millTube/millTubewall)**0.14
# else:
#     hi = 0.023 * (Kg / Di) * ReTube**0.8 * PrTube**0.33 * (Di / 8)**0.33 * (1 + (Di / 8))**0.7 

# Do = 1/12
# Di = 0.732/12
# DbarL = (Do - Di) / np.log(Do/Di)
# Xw = 0.134 / 12
# GasolineHeatTransCoeff = hi
# KeroseneHeatTransCoeff = hs
# FoulingFactorGasoline = hdg * 0.1761
# FoulingFactorKerosene = hdk * 0.1761
# Km = 26 #steel pipe
# Uo = 1 / ((1/FoulingFactorKerosene)*(Do/Di) + (1/GasolineHeatTransCoeff)*(Do/Di) + (Xw/Km)*(Do/DbarL) + (1/KeroseneHeatTransCoeff) + (1/FoulingFactorGasoline))
# print(Uo)

Uguess = 100
solvingUguess = True
AskScale = 'Me'
while solvingUguess:

    #parameters
    Do = 1 * 0.0254
    Di = 0.732 * 0.0254
    DbarL = (Do - Di) / np.log(Do / Di)
    Xw = 0.134 * 0.0254  
    L = 8 * 0.3048

    if AskScale == 'Me': #Celsius

        #1 LMTD
        th2 = 160
        th1 = 120
        tc2 = 120
        tc1 = 75
        LMTD = ((tc2 - tc1) - (th2 - th1)) / np.log(((tc2 - tc1) / (th2 - th1)))        

        #2 Fouling
        Rdg = 0.0005
        Rdk = 0.001
        hdg = 1 / Rdg
        hdk = 1 / Rdk

        #3 Flow Rate of Heating Stream
        mflowcold = 150000
        Cpcold = 0.48 * 4186.798188 #J/kg c
        qcold = mflowcold * Cpcold * (tc2 - tc1) #F -> J/h
        newqcold = qcold / 3600 #J/s      

        #newqcold = mflowhot * Cpg * ((th2 - th1) * 1.8) #no heat loss

        Cphot = 0.57 * 4186.798188
        mflowhot = newqcold / (Cphot * (th2 - th1))

        #4 Fg for 1-2 Exchanger -> correction factor for LMTD
        nh = (tc2 - tc1) / (th2 - tc1)
        z = (th2 - th1) / (tc2 - tc1)
        Fg = 0.85 #from graph

        #5 Corrected LMTD
        newLMTD = LMTD * Fg #celsius

        #6 Guess U **important**
        #Uguess = ? #look at chart for common U

        #7 Outside Area
        #newqcold / Ao = Uguess * newLMTD

        Ao = newqcold / (Uguess * newLMTD)

        #8 Number of Tubes
        Nt = Ao / (np.pi * Do * L)
        Nt = np.ceil(Nt)

        #9 Tube Pitch
        Tubepitch = 1.25 * Do
        Ki = 0.249
        n1 = 2.207
        Db = Do * (Nt / Ki)**(1 / n1)

        #10 Clearance
        #y = mx + c
        #c 0.2 = 10, 1.2 = 20 -> every 1 x, y + 10 -> every 0.2 x, y + 2 -> at 0, y = 8
        c = 8
        m = (20 - 10) / (1.2 - 0.2)
        clearance = m * Db + c #milli meter
        clearance = clearance * 10**-3

        #11 Shell Diameter
        Ds = Db + clearance

        #12 Baffle Pitch(P)
        P = 0.4 * Ds

        #13 Cross Section Flow Area(Sc)
        Sc = P * Ds * (1 - (Do / Tubepitch))

        #14 Gs
        Gs = mflowcold / Sc #kg/m^2 h

        #15 De
        De = (4 * (((Tubepitch / 2) * 0.87 * Tubepitch) - (np.pi / 2 * Do**2 / 4))) / (np.pi * Do / 2)

        #16 Re
        mill = 1.6 * 10**-3 #N * s
        Re = (Gs * De) / (mill * 3600)

        #17 Pr  
        Kk = 0.083 * 1.7295772056 #btu/h ft F -> w /m k
        Pr = (Cpcold * mill) / Kk

        #18 hs from Nu -> individual heat transfer shell
        jh = 0.018
        Twavg = (th2 + tc1) / 2
        millwall = 1.2 * 10**-3 #N * s

        hs = (jh * Re * Pr**(1/3) * (mill/millwall)**0.14) * Kk / De #w / m^2 k 

        #19 Pressure Drop
        Jf = 0.07
        rouShell = 807.5 #kg / m^3, density of kerosene
        Q = mflowcold / (rouShell * 3600) #m^3 / s
        Us = Q / Ao
        DeltaPs = 8 * Jf * (Ds/De) * (L/P) * (rouShell*Us/2)**2 * (mill/millwall)**0.14 #kg/m s^2

        #Tube side#
        #20 Nt per pass
        Ntpp = Nt / 2

        #21 Tube side volumetric velocity (Gi)
        Gi = mflowhot / ((Ntpp * np.pi * Di**2) / 4)

        #22 Tube side velocity (Ui)
        rouTube = 47 #lb/ft^3
        Ui = Gi / rouTube

        #23 Pr and Re of tube side
        Kg = 0.075 #Btu/h*ft*F
        millTube = 0.4 * 2.4191 #n-octane
        PrTube = (millTube * Cphot) / Kg
        ReTube = (Gi * Di) / millTube

        #24 Estimate tube-side heat trans. coeff.
        millTubewall = 0.4 * 2.4191
        if Re < 2100:
            hi = 1.86 * (Kg / Di) * (ReTube * PrTube)**0.33 * (Di / L)**0.33 * (millTube/millTubewall)**0.14
        else:
            hi = 0.023 * (Kg / Di) * ReTube**0.8 * PrTube**0.33 * (Di / L)**0.33 * (1 + (Di / 8))**0.7 

        Do = 1/12
        Di = 0.732/12
        DbarL = (Do - Di) / np.log(Do/Di)
        Xw = 0.134 / 12
        GasolineHeatTransCoeff = hi
        KeroseneHeatTransCoeff = hs
        FoulingFactorGasoline = hdg * 0.1761
        FoulingFactorKerosene = hdk * 0.1761
        Km = 26 #steel pipe
        Uo = 1 / ((1/FoulingFactorKerosene)*(Do/Di) + (1/GasolineHeatTransCoeff)*(Do/Di) + (Xw/Km)*(Do/DbarL) + (1/KeroseneHeatTransCoeff) + (1/FoulingFactorGasoline))
        #print(Uo, Uguess)      
        break
    #Uo = 200, Uguess = 400
    if abs(Uo - Uguess) < 0.000000001:
        solvingUguess = False
        #print(Uo, Uguess)
    else:
        Uguess = Uo
          
