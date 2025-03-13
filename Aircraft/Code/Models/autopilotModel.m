%% Main
function FR = autopilotModel(X,req)
    t = 0:0.025:25; %%%%
    if strcmp(req,'R12.1')
        nbrInputs = 8;
    else
        nbrInputs = 7;
    end

    TimeSteps = 1001; %%%%
    apin.time = t';
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Open Models 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
    curPath=fileparts(which('autopilot.m'));
    addpath(curPath);
    modelpath = strrep(curPath,'Code\Simulink\Models','Benchmark\Simulink Models\autopilot\aprevised\');
    addpath(modelpath);
    if strcmp(req,'R12.1')
        models = {strcat(modelpath,'roll_ap_rev.slx'),strcat(modelpath,'yaw_damper_rev.slx'),strcat(modelpath,'pitch_ap_rev.slx'),strcat(modelpath,'Autopilot_rev.slx'),strcat(modelpath,'AP_Lib_rev.slx'),strcat(modelpath,'Heading_Mode_rev.slx'),strcat(modelpath,'attitude_controller_rev.slx'),strcat(modelpath,'Altitude_Mode_rev.slx'),strcat(modelpath,'do178b_dhc2_rev_new.slx')};
    else
        models = {strcat(modelpath,'roll_ap_rev.slx'),strcat(modelpath,'yaw_damper_rev.slx'),strcat(modelpath,'pitch_ap_rev.slx'),strcat(modelpath,'Autopilot_rev.slx'),strcat(modelpath,'AP_Lib_rev.slx'),strcat(modelpath,'Heading_Mode_rev.slx'),strcat(modelpath,'attitude_controller_rev.slx'),strcat(modelpath,'Altitude_Mode_rev.slx'),strcat(modelpath,'do178b_dhc2_rev.slx')};
    end
    open_system(models);
       % load data file
    save apin_ap.mat apin;
    load('apin_ap.mat', 'apin');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Signals building 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    for j = 1:nbrInputs
        apin.signals(j).values = zeros(TimeSteps,1);
        apin.signals(j).dimensions =  1;
    end

        d=1;
        for j = 1:nbrInputs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Specific for performance requirement  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%            
%             a1(1:100) = X(1,d)*ones(1,100);
%             a1(101:200) = X(1,d+1)*ones(1,100);
%             a1(201:1001) = X(1,d+2)*ones(1,801);
%             apin.signals(j).values = a1';
%             d=d+3;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Else
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
            i=1;
            while i <= 901
                a=X(1,d);
                a1(i:i+332) = a*ones(1,333);
                i = i + 333;
                d = d+1;
            end
            a1(1,1001)= a; 
            apin.signals(j).values = a1';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Scenarios: Fixing inputs 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%         apin.signals(1).values = ones(TimeSteps,1);
%         apin.signals(2).values = zeros(TimeSteps,1);
%         apin.signals(3).values = zeros(TimeSteps,1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        % solving the prob of unrecognized inputs
        if strcmp(req,'R12.1')
            hws = get_param('do178b_dhc2_rev_new', 'modelworkspace');
        else
            hws = get_param('do178b_dhc2_rev', 'modelworkspace');
        end
        list = whos;       
        N = length(list);
        for  i = 1:N
            hws.assignin(list(i).name,eval(list(i).name));
        end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Run Simulation 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        if strcmp(req,'R12.1')
            simOut = sim(fullfile(modelpath,'do178b_dhc2_rev_new.slx'),'ReturnWorkspaceOutputs','on','SaveOutput','on','OutputSaveName','apsOut');
    
        %%%%%%%
            rollOut= simOut.get('apsOut');
            AP_Eng      = apin.signals(1).values;
            HDG_Mode    = apin.signals(2).values;
            ALT_Mode    = apin.signals(3).values;
            HDG_Ref     = apin.signals(4).values;
            TurnK       = apin.signals(5).values;
            ALT_Ref     = apin.signals(6).values;
            Pwheel      = apin.signals(7).values;
            Throttle    = apin.signals(8).values;
            
            Ail_cmd     = simOut.get('AilCmd');
            inertial    = simOut.get('inert');
            Phi_Ref     = simOut.get('PhiRef');
            isRoll     = simOut.get('isRoll');
            AirDataa     = simOut.get('AirDataa');
            alt = AirDataa.alt.Data;
            tout = apin.time;
        else
            simOut = sim(fullfile(modelpath,'do178b_dhc2_rev.slx'),'ReturnWorkspaceOutputs','on','SaveOutput','on','OutputSaveName','apsOut');
            rollOut= simOut.get('apsOut');
            AP_Eng      = apin.signals(1).values;
            HDG_Mode    = apin.signals(2).values;
            ALT_Mode    = apin.signals(3).values;
            HDG_Ref     = apin.signals(4).values;
            TurnK       = apin.signals(5).values;
            ALT_Ref     = apin.signals(6).values;
            Pwheel      = apin.signals(7).values;

            Ail_cmd     = simOut.get('AilCmd');
            inertial    = simOut.get('inert');
            Phi_Ref     = simOut.get('PhiRef');
            isRoll     = simOut.get('isRoll');
            tout = apin.time;
        end
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Assumptions 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        Roll_Mode = zeros(TimeSteps,1);
        for t =1:1001
            if (HDG_Mode(t)==0)&&(ALT_Mode(t)==0)
                Roll_Mode(t) = 1;
            else
                Roll_Mode(t) = 0;
            end 
        end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        TkDiff = zeros(1000,1);
        for i = 2:1001
            TkDiff(i) = TurnK(i) - TurnK(i-1);
        end
       % TkDiffMax = max(TkDiff);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

        Ft = 1000 * ones(TimeSteps,1); 
        
        switch req
            case 'R1.1'
                for t = 2:1001
                    Ft(t) = R11Obj(AP_Eng(t-1),AP_Eng(t), Ail_cmd.Data(t));
                end
            case 'R1.2'
                for t = 1:1001
                    Ft(t) = R12Obj(AP_Eng(t),HDG_Mode(t), ALT_Mode(t),isRoll.Data(t));
                end            
            case 'R1.3'
                for t = 1:1001
                    Ft(t) = R13Obj(inertial.phi.Data(t),TurnK(t),Phi_Ref.Data(t));
                end
            case 'R1.4.1'
                Ft(1) = R141Obj(inertial.phi.Data(1:333),Phi_Ref.Data(1:333)); 
            case 'R1.4.2'
                Ft(1) = R142Obj(inertial.phi.Data(1:333),Phi_Ref.Data(1:333));    
            case 'R1.5'
                Ft(1) = R15Obj(TurnK,inertial.p.Data); 
            case 'R1.6'
                for t = 1:1001
                    Ft(t) = R16Obj(inertial.phi.Data(t));
                end 
            case 'R1.7'
                for t = 1:1001
                    Ft(t) = R17Obj(Ail_cmd.Data(t));
                end  
            case 'R1.8'
                for t = 1:1001
                    Ft(t) = R18Obj(HDG_Mode(t),isRoll.Data(t));
                end
            case 'R1.10.1'
                Ft(1) = R1101Obj(inertial.psi.Data(1:333),HDG_Ref(1:333)); 
            case 'R1.10.2'
                Ft(1) = R1102Obj(inertial.psi.Data(1:333),HDG_Ref(1:333)); 

            %New requirement
            case 'R12.1'
                for t = 1:1001
                    Ft(t) = R121Obj(AP_Eng(1:1001), alt(1:1001), ALT_Ref(1:1001));
                end
            otherwise % by default R1.1
                for t = 1:1001
                    Ft(t) = R11Obj(AP_Eng(t), Ail_cmd.Data(t));
                end
        end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        FR=  min(Ft);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    Requirements
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%% Requirement #1.1; 
 
function R11 = R11Obj(APEngP,APEng, AilCmd)
 
% Req:          % APEng[t-1]=1 AND APEng[t]=0 ==>  AilCmd[t]=0 
                % APEng[t-1]=0 AND APEng[t]=1 ==> AilCmd[t]~=0
% Violation:    % (APEng[t-1]=1 AND APEng[t]=0 AND (AilCmd[t]~=0)) 
                % OR (APEng[t-1]=0 AND APEng[t]=1 AND(AilCmd[t]=0))
 
term1 = zeros(3,1);
term2 = zeros(3,1);
 
if (APEngP ==1)
    term1(1) = -1;
else
    term1(1) = 1;
end 
 
if (APEng ==0)
    term1(2) = -1;
else
    term1(2) = 1;
end

term1(3) = 0.0001 - abs(AilCmd);


if (APEngP ==0)
    term2(1) = -1;
else
    term2(1) = 1;
end
 
if (APEng ==1)
    term2(2) = -1;
else
    term2(2) = 1;
end

term2(3) = abs(AilCmd);
 
R11 = min(max(term1),max(term2));  
 
 
end

%% Requirement #1.2; 
function R12 = R12Obj(APEng, HDGMode, ALTMode, isRoll)

% Req:          APEng[t] = 1 AND HDGMode[t] = 0 AND ALTMode[t] = 0 ==> isRoll[t] == 1
% Violation:    APEng[t] = 1 AND HDGMode[t] = 0 AND ALTMode[t] = 0 AND isRoll[t] == 0
    term = zeros(4,1);   
    
    if(APEng == 1) 
        term(1) = -1;
    else
        term(1) = 1;
    end
    
    if (HDGMode == 0)
        term(2) = -1;
    else
        term(2) = 1;
    end
    
    if (ALTMode == 0)
        term(3) = -1;
    else
        term(3) = 1;
    end
    
    
    if (isRoll == 0)
        term(4) = -1;
    else 
        term(4) = 1;
    end
    
    R12 = max(term);
 
end


%% Requirement #1.3; 
function R13 = R13Obj(Phi, Tk, PhiRef)
    
%if (RollMode==1) then

% Req :         % -6<Phi[t]<6                    ==> PhiRef[t]= 0
                % Phi[t]>30                      ==> PhiRef[t]= 30
                % Phi[t] < -30                   ==> PhiRef[t]= -30
                % -30<=Tk[t]<=-3                 ==> PhiRef[t]= Tk[t] 
                % 3<=Tk[t]<=30                   ==> PhiRef[t]= Tk[t]
                
% Violation :   % -6<Phi[t]<6       AND         PhiRef[t] ~= 0              : term1
                % Phi[t]>30         AND         PhiRef[t] ~= 30             : term2
                % Phi[t] < -30      AND         PhiRef[t] ~= -30            : term3
                % -30<=Tk[t]<=-3    AND         PhiRef[t] ~= Tk[t]          : term4
                % 3<=Tk[t]<=30      AND         PhiRef[t] ~= Tk[t]          : term5
                 
    term = zeros(5,1); 
    term(1) = max(max(Phi-6,0.0001-(Phi+6)), 0.0001 - PhiRef);
    term(2) = max(0.0001 - Phi, 0.0001 -abs(PhiRef-30));
    term(3) = max(0.0001 + Phi + 30, 0.0001 - abs(PhiRef+30));
    term(4) = max(max(Tk + 3, (-1) * (Tk + 30)),0.0001 - abs(PhiRef-Tk));
    term(5) = max(max(Tk - 30, Tk - 3), 0.0001 - abs(PhiRef-Tk));
    R13 = min(term);
                       
end

%% Requirement #1.4.1;
function R141 = R141Obj(Phi, Phi_Ref)

% Req:          GF(stable)
% Violation:    FG(~stable)

    xmin = zeros(size(Phi,1),1);   
    for t=1:333
        x = 1000*ones(334-t,1);
        for i=t:333
            x(i)=1 - abs(Phi(i) - Phi_Ref(i));
        end
        xmin(t) = min(x);         
    end
    R141 = max(xmin);
end

%% Requirement #1.4.2;
function R142 = R142Obj(Phi, Phi_Ref)
   
% Req:          G(|(Phi - Phi_Ref)/Phi_Ref| = 0.1) ==> G(|(Phi - Phi_Ref)/Phi_Ref| < 0.1)
% Violation:    F(|(Phi - Phi_Ref)/Phi_Ref| = 0.1 AND F(|(Phi - Phi_Ref)/Phi_Ref| >= 0.1))

    xmin = 1000;
    for t=1:size(Phi,1)
       
        min1 = 1000;
        for i=t:size(Phi,1)
            term = abs(Phi(i) - Phi_Ref(i)) / Phi_Ref(i);
            x=0.1 - term;
            min1 = min(min1,x);
        end
        term1 = max(abs(term - 0.1), min1);
        if (term1>=0)
            term2 = term1/(term1+1);
        else
            term2 = (-1)*abs(term1)/(abs(term1)+1);
        end
        xmin = min(xmin,term2);         
    end
    R142 = xmin;
    
end
%% Requirement #1.5; 
function R15 = R15Obj(Tk,P)

% Req:          G((Tk(t) - Tk(t-1) >= 30 ==> G(|P(t)| <= 6.6)
% Violation:    F((Tk(t) - Tk(t-1) >= 30 AND F(|P(t)| > 6.6)

    min1 = 1000;
    for i=2:size(Tk,1) 

        term1 = 30 - abs(Tk(i)-Tk(i-1));
        
        min2 = 1000;
        for j=i:size(Tk,1)

            term2 = 6.6 - P(j)+ 0.0001;

            term3 = P(j) + 6.6 + 0.0001;

            term4 = min(term2,term3);
            min2 = min(min2,term4);
        end
        min1 = min(min1,max(term1,min2));
    end
    R15 = min1;  
   
end


%% Requirement #1.6; 
function R16 = R16Obj(Phi)

% Req:           -33 <= Phi[t] <= 33
% Violation:     |Phi[t]|>33

    R16 = 33 - abs(Phi) + 0.0001;

end


%% Requirement #1.7; 
function R17 = R17Obj(AilCmd)

%Req:            -15 <= AilCmd[t] <= 15
% Violation:     |AilCmd[t]|>15

    R17 = 15 - abs(AilCmd) + 0.0001;

end

%% Requirement #1.8; 
function R18 = R18Obj(HDGMode, isRoll)

% Req:          % HDGMode[t]=0 ==> isRoll[t]=1 
                % HDGMode[t]=1 ==> isRoll[t]=0
% Violation:    % (HDGMode[t]=0 AND isRoll[t]=0) OR (HDGMode[t]=1 AND isRoll[t]=1)
  
    
    if(HDGMode == 0) 
        term11 = -1;
    else
        term11 = 1;
    end 
    
    if(isRoll == 0) 
        term12 = -1;
    else
        term12 = 1;
    end
    
    term1 = max(term11,term12);
    
    if(HDGMode == 1) 
        term21 = -1;
    else
        term21 = 1;
    end 
    
    if(isRoll == 1) 
        term22 = -1;
    else
        term22 = 1;
    end
    
    term2 = max(term21,term22);
    
    R18 = min(term1,term2);
     
end

%% Requirement #1.10.1;
function R1101 = R1101Obj(Psi, HDG_Ref)

% Req:          GF(stable)
% Violation:    FG(~stable)

    xmin = zeros(size(Psi,1),1);   
    for t=1:333
        x = 1000*ones(334-t,1);
        for i=t:333
            x(i)=1 - abs(Psi(i) - HDG_Ref(i));
        end
        xmin(t) = min(x);         
    end
    R1101 = max(xmin);
end

%% Requirement #1.10.2;
function R1102 = R1102Obj(Psi, HDG_Ref)

% Req:          G(|(Psi - HDG_Ref)/HDG_Ref| = 0.1) ==> G(|(Psi - HDG_Ref)/HDG_Ref| < 0.1)
% Violation:    F(|(Psi - HDG_Ref)/HDG_Ref| = 0.1 AND FPsiPhi - HDG_Ref)/HDG_Ref| >= 0.1))

    xmin = 1000;
    for t=1:size(Psi,1)
       
        min1 = 1000;
        for i=t:size(Psi,1)
            if HDG_Ref(i) == 0
                term = abs(Psi(i));
            else
                term = abs(Psi(i) - HDG_Ref(i)) / HDG_Ref(i);
            end
            x=0.1 - term;
            min1= min(min1,x);
        end
        term1 = max(abs(term - 0.1), min1);
        if (term1>=0)
            term2 = term1/(term1+1);
        else
            term2 = (-1)*abs(term1)/(abs(term1)+1);
        end
        xmin = min(xmin,term2);         
    end
    R1102 = xmin;   
end

%Requirement 12.1
function R121 = R121Obj(AP_Eng, alt, ALT_Ref)

% Req:          AP_Eng = 1 => F(G(alt - ALT_Ref => 0.0))
    
    minterms = [];
    [maxvalue , maxindex] = max(AP_Eng);
    
    if maxvalue == 1
    
        for i = maxindex:min((maxindex + 500),1001)
        
            for j = i:min((maxindex + 500),1001)
            
                term = 0.05 - (ALT_Ref - alt);

            end
     
            minterms(i) = min(term);
            
        end
        a = minterms(maxindex:end);
        R121 = max(a);
     
    else
        R121 = 10; % a random number
    end

end


