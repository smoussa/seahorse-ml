close all
clear all
format long

% initialise parameters of dbn
dbn.sizes = [250 250 250];
opts.numepochs = 5;
opts.batchsize = 10;    % large batches are more strict
opts.momentum  = 0;
opts.alpha     = 1;

driver_num = 105;

% frequency of commonly false trips
F = zeros(200,1);
for i = 1:30
	extremes = apply_dbn(driver_num, dbn, opts);
	F(extremes) = F(extremes) + 1;
end

% find trips that come up false at least f times;
f = 20;
common = find(F >= f);
[common F(common)]

disp(['Found '  num2str(numel(common)) ' frequently false trips'])

% plot
s = 6;
true_trips = setdiff(1:200,common);
view_trips(driver_num, common(randperm(length(common),s)), true);  	% plot some false trips (Fig 1)
view_trips(driver_num, true_trips(randperm(length(true_trips),s)), true);	% plot some true trips (Fig 2)










%%

% predict across drivers
% for d = 105:105
%     build_dbn(d, dbn, opts);
% end


%% test with other drivers
% get test driver's trips
% test_driver = 109;
% test_x = csvread(['feature_data/' num2str(test_driver) '.csv'], 1, 0);








