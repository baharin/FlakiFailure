function label = labelPF(PopObj,high,req)
    %Label data point into B or NB using PopObj

%For certain requirements only
    if (strcmp(req,'R1b')) || (strcmp(req,'R1e')) || (strcmp(req,'R2a')) || (strcmp(req,'R2b')) || (strcmp(req,'R7'))
        if (PopObj >= high)
            label = 1; %B
            disp("pass");
        else
            label = 0; %NB
            disp("fail");
        end
    else
        if (PopObj >= 0)
            label = 1; %B
            disp("pass");
        else
            label = 0; %NB
            disp("fail");
        end
    end

end