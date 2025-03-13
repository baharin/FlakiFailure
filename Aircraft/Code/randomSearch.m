%Function implements baseline algorithm ie. Naive Random Search algorithm
%that generates an input randomly from input search space and simulates the
%inputs iteratively till the simulation budget is reached. 
function PopObj = randomSearch(run,element,problem,req,evaluation)
    p = '..\..\Results\';
    data_path = strcat(p,func2str(problem),'\');
    replace_dot = strrep(req,'.','_');
    high = 0;
    path = strcat(data_path,func2str(problem),'_',replace_dot,'_regression_',string(evaluation),'_','value','_',string(run),'.csv');
    inputArray = [];    
    X = element;
    PopObj=callSimulator(X,req,func2str(problem));
    label = labelPF(PopObj,high,replace_dot);
    inputArray(1) = PopObj;
    inputArray(2) = label;
    inputArray(3) = 0;
    inputArray(4) = 0;
    inputArray(5) = 0;
    inputArray(6:length(X)+5) = X;
    writematrix(inputArray,path,'WriteMode', 'append');
end
