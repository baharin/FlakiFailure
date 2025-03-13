function PopObj = callSimulator(X,req,simModel)
    switch simModel
        case 'autopilot'
            PopObj=autopilotModel(X,req);
    end
end
