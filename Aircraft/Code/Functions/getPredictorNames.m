function predictorNames = getPredictorNames(problem)
    switch problem
        case 'reg'
            predictorNames = ['A1','A2','B1','B2','C1','C2','D1','D2','E1','E2','F1','F2','G1','G2','H1','H2','I1','I2','J1','J2','K1','K2','L1','L2','M1','M2','N1','N2','O1','O2','P1','P2'];
            
        case 'autopilot'
            predictorNames = ['AP_Eng1','AP_Eng2','AP_Eng3','HDG_Mode1','HDG_Mode2','HDG_Mode3','ALT_Mode1','ALT_Mode2','ALT_Mode3','HDG_Ref1','HDG_Ref2','HDG_Ref3','TurnK1','TurnK2','TurnK3','ALT_Ref1','ALT_Ref2','ALT_Ref3','Pwheel1','Pwheel2','Pwheel3'];

        case 'tustin'
            predictorNames = ["Xin1","Xin2","Xin3","Xin4","Xin5","Xin6","Xin7","Xin8","Xin9","Xin10","Xin11","TL","BL","IC"];

        case 'tustinr4'
            predictorNames = ["TL","BL","IC"];
        case 'nlguidance'
            predictorNames = ["Xt1","Xt2","Xt3","Xv1","Xv2","Xv3","Vv1","Vv2","Vv3","Vt1","Vt2","Vt3","r"];
        case 'fsm'
            predictorNames = ['Standby1','Standby2','Standby3','Apfail1','Apfail2','Apfail3','Supported1','Supported2','Supported3','Limits1','Limits2','Limits3'];

    end
end