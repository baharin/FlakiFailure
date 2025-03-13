function PopObj = callSimulator(X,req,simModel)
    switch simModel
        case 'reg'
            PopObj=regModel(X,req);
        case 'autopilot'
            PopObj=autopilotModel(X,req);

        case 'tustin'
            PopObj=tustinModel(X,req);
        case 'tustinr4'
            PopObj=tustinr4Model(X,req);
        case 'twotanks'
            PopObj = twotanksModel(X,req);
        case 'nlguidance'
            PopObj = nlguidanceModel(X,req);
        case 'fsm'
            PopObj = fsmModel(X,req);
    end
end