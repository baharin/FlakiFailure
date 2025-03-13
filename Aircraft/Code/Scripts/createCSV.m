%This function is used to create a CSV file before initiating test suite
%generation irrespective of the strategy (i.e. SA, RS, LR or RT)
function createCSV(run,simModel,requirement,iteration,mlmodel)

        %Set path where CSV needs to be created. 
        p = '..\..\Results\';
%         if strcmp(string(iteration),'3500')
        maxIterationNum = iteration;
%         else
%             maxIterationNum = 3500;
%         end
        mlModelName = mlmodel;
        if not(isfolder(strcat(p,simModel)))
            mkdir(strcat(p,simModel))
        end
        if isfolder(strcat(p,simModel))
            if not(isfolder(strcat(p,simModel,'\verify')))
                mkdir(strcat(p,simModel,'\verify'))
            end
        end
        base_path = strcat(p,simModel,'\');
        disp(base_path)
        replace_dot = strrep(requirement,'.','_');
        path = strcat(base_path,simModel,'_',replace_dot,'_regression_',string(maxIterationNum),'_',mlModelName,'_',string(run),'.csv');
        if isfile(path)
            disp(strcat('file exists:', path)); 
        else
        %If file doesnt exist, define the columns and then create an empty
        %CSV file
            if strcmp(simModel,'tustin')
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','Xin1','Xin2','Xin3','Xin4','Xin5','Xin6','Xin7','Xin8','Xin9','Xin10','Xin11','TL','BL','IC'};
            elseif strcmp(simModel,'tustinr4')
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','TL','BL','IC'};
            elseif strcmp(simModel,'autopilot')                
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','AP_Eng1','AP_Eng2','AP_Eng3','HDG_Mode1','HDG_Mode2','HDG_Mode3','ALT_Mode1','ALT_Mode2','ALT_Mode3','HDG_Ref1','HDG_Ref2','HDG_Ref3','TurnK1','TurnK2','TurnK3','ALT_Ref1','ALT_Ref2','ALT_Ref3','Pwheel1','Pwheel2','Pwheel3','Throttle1','Throttle2','Throttle3'};
            elseif strcmp(simModel,'reg')
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','A1','A2','B1','B2','C1','C2','D1','D2','E1','E2','F1','F2','G1','G2','H1','H2','I1','I2','J1','J2','K1','K2','L1','L2','M1','M2','N1','N2','O1','O2','P1','P2'};
            elseif strcmp(simModel,'nlguidance')
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','Xt1','Xt2','Xt3','Xv1','Xv2','Xv3','Vv1','Vv2','Vv3','Vt1','Vt2','Vt3','r'};
            elseif strcmp(simModel,'fsm')
                rhs = {'Fitness', 'Label','Type','TrainDelta','TestDelta','Standby1','Standby2','Standby3','Apfail1','Apfail2','Apfail3','Supported1','Supported2','Supported3','Limits1','Limits2','Limits3'};
                cHeader = rhs;
            end
            commaHeader = [cHeader;repmat({','},1,numel(cHeader))];
            disp(commaHeader);
            commaHeader = commaHeader(:)';
            disp(commaHeader);
            textHeader = cell2mat(commaHeader);
            textHeader = textHeader(1:end-1);
            disp(textHeader);
            %Creating an empty CSV file with the columns specified above
            fid = fopen(path,'wt');
            fprintf(fid,'%s\n',textHeader);
            fclose(fid);  
        end


        %Code similar to above. Used to create verify file to evaluate the
        %accuracy of surrogate technique. 

        verify_path = strcat(base_path,'verify\');
        verify_file = strcat(verify_path,simModel,'_',replace_dot,'_verify_',string(maxIterationNum),'_',mlModelName,'_',string(run),'.csv');
        
        if isfile(verify_file)
            disp(strcat('file exists:', verify_file));
            
        else
            %Define the columns for the CSV file
            if strcmp(simModel,'tustin')
                cHeader = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','Xin1','Xin2','Xin3','Xin4','Xin5','Xin6','Xin7','Xin8','Xin9','Xin10','Xin11','TL','BL','IC'};
            elseif strcmp(simModel,'tustinr4')
                cHeader = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','TL','BL','IC'};
            elseif strcmp(simModel,'autopilot')
                cHeader = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','AP_Eng1','AP_Eng2','AP_Eng3','HDG_Mode1','HDG_Mode2','HDG_Mode3','ALT_Mode1','ALT_Mode2','ALT_Mode3','HDG_Ref1','HDG_Ref2','HDG_Ref3','TurnK1','TurnK2','TurnK3','ALT_Ref1','ALT_Ref2','ALT_Ref3','Pwheel1','Pwheel2','Pwheel3','Throttle1','Throttle2','Throttle3'};
            elseif strcmp(simModel,'reg')
                cHeader = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','A1','A2','B1','B2','C1','C2','D1','D2','E1','E2','F1','F2','G1','G2','H1','H2','I1','I2','J1','J2','K1','K2','L1','L2','M1','M2','N1','N2','O1','O2','P1','P2'};
            elseif strcmp(simModel,'nlguidance')
                cHeader = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','Xt1','Xt2','Xt3','Xv1','Xv2','Xv3','Vv1','Vv2','Vv3','Vt1','Vt2','Vt3','r'};
            elseif strcmp(simModel,'fsm')
                rhs = {'PredictedFitness','PredictedLabel','SimulatedFitness','SimulatedLabel','Same/Different','Index','Standby1','Standby2','Standby3','Apfail1','Apfail2','Apfail3','Supported1','Supported2','Supported3','Limits1','Limits2','Limits3'};
                cHeader = rhs;
            end
            commaHeader = [cHeader;repmat({','},1,numel(cHeader))]; 
            commaHeader = commaHeader(:)';
            textHeader = cell2mat(commaHeader);
            textHeader = textHeader(1:end-1);
            %Create an empty CSV file
            fid = fopen(verify_file,'wt');
            fprintf(fid,'%s\n',textHeader);            
            fclose(fid);  
        end