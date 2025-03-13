function varargout = autopilot(Operation,Global,element) 
    switch Operation
        case 'init'
            if strcmp(Global.requirement,"R12.1")
                urangeTurnKmax      = 45;          %Input Turn Knob value 
                urangeTurnKmin      = 0;        %Input Turn Knob  value
                urangeHDGRefmax     = 180;         %Input HDG Ref value 
                urangeHDGRefmin     = -180;        %Input HDG Ref value        
                urangeALTRefmin     = 6700;            %Input ALT Ref value 
                urangeALTRefmax     = 6700;         %Input ALT Ref value
                urangePitchWmax     = 30;          %Input Pitch wheel value 
                urangePitchWmin     = -30;         %Input Pitch wheel value
                urangethrottlemin   = 0;
                urangethrottlemax   = 1;
                Global.D        = 24;
                Global.lower    = [zeros(1,9),urangeHDGRefmin*ones(1,3),urangeTurnKmin*ones(1,3),urangeALTRefmin*ones(1,3),urangePitchWmin*ones(1,3),urangethrottlemin*ones(1,3)];
                Global.upper    = [ones(1,9),urangeHDGRefmax*ones(1,3),urangeTurnKmax*ones(1,3),urangeALTRefmax*ones(1,3),urangePitchWmax*ones(1,3),urangethrottlemax*ones(1,3)];
                Global.operator = @AutopilotMutation;
                Global.localop = 35;
                Global.law = 47;         % for hcrr alg
    
                PopDec = rand(1,Global.D);                
               
                for i = 1:9                
                    PopDec(:,i) = round(rand);
                end            
                for i = 10:12                 
                    PopDec(:,i) = (PopDec(:,i) * (urangeHDGRefmax - urangeHDGRefmin)) + urangeHDGRefmin;  
                end
                for i = 13:15                 
                    PopDec(:,i) = (PopDec(:,i) * (urangeTurnKmax - urangeTurnKmin)) + urangeTurnKmin; 
                end
                for i = 16:18                
                    PopDec(:,i) = (PopDec(:,i) * (urangeALTRefmax - urangeALTRefmin)) + urangeALTRefmin;  
                end
                for i = 19:21                 
                    PopDec(:,i) = (PopDec(:,i) * (urangePitchWmax - urangePitchWmin)) + urangePitchWmin;  
                end
                for i = 22:24
                    PopDec(:,i) = (PopDec(:,i) * (urangethrottlemax - urangethrottlemin)) + urangethrottlemin;
                end
                varargout = {PopDec};
            else
                urangeTurnKmax      = 45;           %Input Turn Knob value 
                urangeTurnKmin      = 0;          %Input Turn Knob  value
                urangeHDGRefmax     = 180;          %Input HDG Ref value 
                urangeHDGRefmin     = -180;         %Input HDG Ref value        
                urangeALTRefmin     = 0;            %Input ALT Ref value 
                urangeALTRefmax     = 1000;         %Input ALT Ref value
                urangePitchWmax     = 30;           %Input Pitch wheel value 
                urangePitchWmin     = -30;          %Input Pitch wheel value
                Global.D        = 21; 
                Global.lower    = [zeros(1,9),urangeHDGRefmin*ones(1,3),urangeTurnKmin*ones(1,3),urangeALTRefmin*ones(1,3),urangePitchWmin*ones(1,3)];
                Global.upper    = [ones(1,9),urangeHDGRefmax*ones(1,3),urangeTurnKmax*ones(1,3),urangeALTRefmax*ones(1,3),urangePitchWmax*ones(1,3)];
                Global.operator = @AutopilotMutation;
                Global.localop = 35;
                Global.law = 47;         % for hcrr alg
                PopDec = rand(1,Global.D);                
               
                for i = 1:9                
                    PopDec(:,i) = round(rand);
                end            
                for i = 10:12                 
                    PopDec(:,i) = (PopDec(:,i) * (urangeHDGRefmax - urangeHDGRefmin)) + urangeHDGRefmin;  
                end
                for i = 13:15                 
                    PopDec(:,i) = (PopDec(:,i) * (urangeTurnKmax - urangeTurnKmin)) + urangeTurnKmin; 
                end
                for i = 16:18                
                    PopDec(:,i) = (PopDec(:,i) * (urangeALTRefmax - urangeALTRefmin)) + urangeALTRefmin;  
                end
                for i = 19:21                 
                    PopDec(:,i) = (PopDec(:,i) * (urangePitchWmax - urangePitchWmin)) + urangePitchWmin;  
                end
                varargout = {PopDec};
            end

        case 'random'  
            disp('Called Random Search');
            PopObj = randomSearch(Global.run,element,Global.problem,Global.requirement,Global.evaluation);
            varargout = {PopObj};

        case 'optimize_r'  
            disp('Called regression');
            PopObj = individualSurrogate(Global.run,element,Global.mlmodel,Global.initialSimNum,Global.problem,Global.requirement,Global.evaluation);
            varargout = {PopObj};


        case 'ensemble'
            disp('Called ensemble');
            PopObj = dynamicSurrogate(Global.run,element,Global.mlmodel,Global.initialSimNum,Global.problem,Global.requirement,Global.evaluation);
            varargout = {PopObj};

        case 'verify'      
            disp('Called verify case');
            PopObj = verify(Global.run,element,Global.mlmodel,Global.problem,Global.requirement);
            varargout = {PopObj};

        case 'generate'
            disp('Called generate case');
            PopObj = regressionTree(Global.run,element,Global.mlmodel,Global.initialSimNum,Global.problem,Global.requirement,Global.evaluation);
            varargout = {PopObj};

        case 'generateLog'
            disp('Called generate case');
            PopObj = logisticRegression(Global.run,element,Global.mlmodel,Global.initialSimNum,Global.problem,Global.requirement,Global.evaluation);
            varargout = {PopObj};
    end
end