close all
clear all
format long

setup_paths;

%{
	HOW TO RUN:
	(1) Add this directory and libraries directory to MATLAB path
	(2) Run extract_all.m to extract feature data
	(2) Run predict_trips.m to predict on all extracted drivers
%}

% initialise parameters of dbn
dbn.sizes = [250 250 250];
opts.numepochs = 5;
opts.batchsize = 50;    % large batches are more strict
opts.momentum  = 0;
opts.alpha     = 1;

fname = 'submission_file.csv';
fid = fopen(fname, 'w+');
fprintf(fid, '%s\n', 'driver_trip,prob');

timestart = tic;

for d = 1:3612

	srcpath = ['feature_data/' num2str(d) '.csv'];
    if exist(srcpath)

		%{
			Run DBN
		%}

		% frequency of commonly false trips (SERIAL)
		% F = zeros(200,1);
		% iterations = 30;
		% for i = 1:iterations
		% 	extremes = apply_dbn(d, dbn, opts);
		% 	F(extremes) = F(extremes) + 1;
		% end

		% frequency of commonly false trips (PARALLEL)
		F = zeros(200,1);
		iterations = 50;
		W = cell(iterations,1);
		parfor i = 1:iterations
			extremes = apply_dbn(d, dbn, opts);
			W{i} = extremes;
		end
		% sum up workers' results
		for i = 1:size(W,1)
			F(W{i}) = F(W{i}) + 1;
		end

		




		%{
			Save trip data
		%}

		% find trips that belong to the driver;
		f = fix(iterations / 2);
		truthy = (F < f); % 1: true, 0: false
		% [truthy F(truthy)]

		% disp(['Driver: ' num2str(d) ' -> Found '  num2str(sum(truthy)) '/200 true trips.'])

		driver_num = num2str(d);
		for t = 1:200
			fprintf(fid, '%s\n', [driver_num '_' num2str(t) ',' num2str(truthy(t))]);
		end
		

		%{
			Plot
		%}

		% plot
		% s = 6;
		% true_trips = setdiff(1:200,truthy);
		% view_trips(d, truthy(randperm(length(truthy),s)), true);  	% plot some false trips (Fig 1)
		% view_trips(d, true_trips(randperm(length(true_trips),s)), true);	% plot some true trips (Fig 2)
	end
end

toc(timestart)
fclose(fid);









