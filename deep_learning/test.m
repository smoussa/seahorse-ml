close all
clear all
format long

dbn.sizes = [100 100 100];
opts.numepochs = 10;
opts.batchsize = 40;
opts.momentum  = 0;
opts.alpha     = 1;

% predict across drivers
for d = 100:100
    build_dbn(d, dbn, opts);
end






%% test with other drivers
% get test driver's trips
% test_driver = 109;
% test_x = csvread(['feature_data/' num2str(test_driver) '.csv'], 1, 0);









