close all
clear all
format long

dbn.sizes = [300 300 300];
opts.numepochs = 5;
opts.batchsize = 10;
opts.momentum  = 0;
opts.alpha     = 1;

% compare false and true trips
extremes = build_dbn(106, dbn, opts);
s = 2;
t = setdiff(1:200,extremes);
view_trips(105, extremes(randperm(length(extremes),s)), true);  % plot some false trips
view_trips(105, t(randperm(length(t),s)), true);                % plot some true trips










%%

% predict across drivers
% for d = 105:105
%     build_dbn(d, dbn, opts);
% end


%% test with other drivers
% get test driver's trips
% test_driver = 109;
% test_x = csvread(['feature_data/' num2str(test_driver) '.csv'], 1, 0);









