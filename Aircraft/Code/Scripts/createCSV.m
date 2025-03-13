%This function is used to create a CSV file
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
            
            if strcmp(simModel,'autopilot')                
                cHeader = {'Fitness', 'Label','Type','TrainDelta','TestDelta','AP_Eng1','AP_Eng2','AP_Eng3','HDG_Mode1','HDG_Mode2','HDG_Mode3','ALT_Mode1','ALT_Mode2','ALT_Mode3','HDG_Ref1','HDG_Ref2','HDG_Ref3','TurnK1','TurnK2','TurnK3','ALT_Ref1','ALT_Ref2','ALT_Ref3','Pwheel1','Pwheel2','Pwheel3','Throttle1','Throttle2','Throttle3'};
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
end
