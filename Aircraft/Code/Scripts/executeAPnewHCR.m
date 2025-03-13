%Entry point function to run test generation for Autopilot Simulink model
function executeAPnewHCR()
            curPath=fileparts(which('executeAPnewHCR.m')); 
            mainpath = strrep(curPath,'Scripts/HCvsRandom','');    
            addpath(mainpath);
            cHeader = {'Model','Requirement','Translation','Algorithm','Run', 'Iteration', 'Best Fitness', 'Current Fitness'};
            commaHeader = [cHeader;repmat({','},1,numel(cHeader))]; 
            commaHeader = commaHeader(:)';
            textHeader = cell2mat(commaHeader);
            fid = fopen('test_APnewHCR.csv','wt');
            fprintf(fid,'%s\n',textHeader);            
            fclose(fid);  
        
%% Autopilot-ars-testgeneration %%        
        
            %"runs" is an array containing integers that represents each
            %run of an approach. For example runs = [1,2,3,4,5] calls
            %eachRuns 5 times with the approach defined in "models" array.

            runs = [0];
            
            models = ["random"]; 

            req = ["R12.1"]; 
            for r = 1: length(runs)
                for i = 1: length(models)
                    for j = 1: length(req)
                    
                        timeData = [];
                        startTime = tic;
                        
                        if strcmp(models(i),"random")
                            eachRun('random',@ars,'R','AP',req(j),3500,runs(r), models(i),300,600);

                        end
                        
                    end
                end
            end

end


function eachRun(simType,algorithm,translation,model,requirement,iteration,counter,mlmodel,initialSimNum,maxSimNum)
   
    if (translation == 'R')
        switch model 
            case 'AP'
                Vmodel = 'autopilot';
        end
        Vproblem = strcat('@',Vmodel);
        Vproblem1 = str2func(Vproblem);
    end
    
    Vreq = requirement;
    
    curPath=fileparts(which('executeAPnewHCR.m')); 
    mainpath = strrep(curPath,'Scripts/HCvsRandom','');    
    addpath(mainpath);
    index = 0;
    createCSV(counter,Vmodel,requirement,iteration,mlmodel);

    main('run',counter ,'-simType',simType,'-algorithm', algorithm, '-problem', Vproblem1,'-requirement',Vreq,'-operator', @GMutation, '-evaluation', iteration,'-mlmodel', mlmodel, 'initialSimNum',initialSimNum,'maxSimNum',maxSimNum);
      
    for i=1:iteration
        index = index+1;  
           
        m = matfile('fitmat.mat');
        BestFit = m.bestfit;
        CurrFit = m.curfit;
        C = {Vmodel,requirement,translation,strtok(func2str(algorithm),'@'),counter,index, BestFit(index),CurrFit(index)};       

        C = C.';    
        fid = fopen('test_APnewHCR.csv','a');
        fprintf(fid,'%s,%s,%s,%s,%d,%d,%4f,%4f\n',C{:});
        fclose(fid);
    end
end
