close all
clear all
format long

run setup_paths;

%{
	HOW TO RUN:
	(1) Add this directory and libraries directory to MATLAB path
	(2) Run predict_trips.m to predict on all extracted drivers
	matlab -nodisplay -nodesktop -nosplash < deep_learning/predict_trips.m
%}

%========================================================================
% INITIALISATION
%========================================================================

timestart = tic;

myCluster = parcluster;
delete(myCluster.Jobs);
myCluster = parcluster('local');
myCluster.NumWorkers = 23;
gcp = myCluster;


%========================================================================
% LOAD DATA
%========================================================================
datadir = 'deep_learning/data/';
featuredir = 'joes_features_csv/';

% if ~exist([datadir 'dfts.mat'])
% 	% D = zeros(2736,634);
% 	disp('Creating matrix of driver data ...');
% 	d = 1;
% 	for i = 1:3612 % 3612
% 		src = [featuredir num2str(i) '.csv'];
% 		if exist(src)

% 			DIDX(d) = i;
% 			D{d} = csvread(src,0,0);
% 			data = D{d};

% 			% normalise between 0 and 1 (for deep learning toolbox)
% 			for j = 1:size(data,2)
% 			    col = data(:,j);
% 			    mind = min(col);
% 			    maxd = max(col);
% 			    rng = (maxd - mind);
% 			    if rng ~= 0
% 			        data(:,j) = (col - mind) / rng;
% 			    else
% 			        data(:,j) = 0;
% 			    end
% 			end
% 			D{d} = data;

% 			d = d + 1;
% 		end
% 	end
% 	save([datadir 'dfts.mat'], 'D');
% 	save([datadir 'didx.mat'], 'DIDX');
% else
% 	D = load([datadir 'dfts.mat']);
% 	DIDX = load([datadir 'didx.mat']);
% 	DIDX = DIDX.DIDX;
% 	D = D.D;
% 	disp('Successfully loaded all driver data.');
% end



%========================================================================
% DEEP LEARNING
%========================================================================

% initialise parameters of dbn
opts.numepochs = 50;
opts.batchsize = 40;    % large batches are more strict
opts.momentum  = 0;
opts.alpha     = 1;

% apply deep learning
N = 2736;
P = zeros(N,200);
DIDX = zeros(3612,1);

% add zeros (y) for all drivers
% for i = 1:N
% 	D{i} = [D{i} zeros(size(D{i},1),1)];
% end

disp('Training...');
parfor i = 1:3612 % 3612
i
	src = [featuredir num2str(i) '.csv'];
	if exist(src)

		DIDX(i) = i;

		i

		D = csvread(src,0,0);
		data = D;

		% normalise between 0 and 1 (for deep learning toolbox)
		for j = 1:size(data,2)
		    col = data(:,j);
		    mind = min(col);
		    maxd = max(col);
		    rng = (maxd - mind);
		    if rng ~= 0
		        data(:,j) = (col - mind) / rng;
		    else
		        data(:,j) = 0;
		    end
		end
		D = data;

		D(:,end) = ones(size(D,1),1);

		r = 10;




		src = [featuredir num2str(r) '.csv'];
		while ~exist(src)
			src = [featuredir num2str(r) '.csv'];
		end

		K = csvread(src,0,0);
		data = K;

		% normalise between 0 and 1 (for deep learning toolbox)
		for j = 1:size(data,2)
		    col = data(:,j);
		    mind = min(col);
		    maxd = max(col);
		    rng = (maxd - mind);
		    if rng ~= 0
		        data(:,j) = (col - mind) / rng;
		    else
		        data(:,j) = 0;
		    end
		end
		K = data;

		% D = cell2mat(D');
		A = [D; K];







		train_x = A(:,1:end-1);
		train_y = A(:,end);

		% create and train a dbn
		dbn = {};
		dbn.sizes = [200 200 200];
		dbn = dbnsetup(dbn, train_x, opts);
		dbn = dbntrain(dbn, train_x, opts);

		% unfold dbn to nn
		nn = dbnunfoldtonn(dbn, 1);
		nn.activation_function = 'sigm';

		% train nn
		nn = nntrain(nn, train_x, train_y, opts);

		% predict
		prob = nnpredict(nn, D(:,1:end-1));
	    mind = min(prob);
	    maxd = max(prob);
	    rng = (maxd - mind);
	    if rng ~= 0
	        prob = (prob - mind) / rng;
	    else
	        prob = 0;
	    end

		% for t = 1:200
		% 	disp(['prob -> driver[' num2str(DIDX(d)) '], trip[' num2str(t) '] == ' num2str(prob(t))]);
		% end

		% sum(prob >= 0.5)

		P(i,:) = (prob >= 0.5);
		
	end
end















% parfor d = 1:N

% 	d

% 	% add ones (y) for the current driver
% 	X = D;
% 	X{d}(:,end) = ones(size(D{d},1),1);

% 	r = randi(N);
% 	while r == d
% 		r == randi(N);
% 	end

% 	% X = cell2mat(X');
% 	X = [X{d}; X{r}];

% 	train_x = X(:,1:end-1);
% 	train_y = X(:,end);

% 	% create and train a dbn
% 	dbn = {};
% 	dbn.sizes = [200 200 200 200];
% 	dbn = dbnsetup(dbn, train_x, opts);
% 	dbn = dbntrain(dbn, train_x, opts);

% 	% unfold dbn to nn
% 	nn = dbnunfoldtonn(dbn, 1);
% 	nn.activation_function = 'sigm';

% 	% train nn
% 	nn = nntrain(nn, train_x, train_y, opts);

% 	% predict
% 	prob = nnpredict(nn, D{d}(:,1:end-1));
%     mind = min(prob);
%     maxd = max(prob);
%     rng = (maxd - mind);
%     if rng ~= 0
%         prob = (prob - mind) / rng;
%     else
%         prob = 0;
%     end

% 	% for t = 1:200
% 	% 	disp(['prob -> driver[' num2str(DIDX(d)) '], trip[' num2str(t) '] == ' num2str(prob(t))]);
% 	% end

% 	P(d,:) = (prob >= 0.5);
% 	% sum(prob >= 0.5)
	
% end

fname = 'submission_file.csv';
fid = fopen(fname, 'w+');
fprintf(fid, '%s\n', 'driver_trip,prob');

for d = 1:3612
	if (DIDX(d) > 0)
		for t = 1:200
			fprintf(fid, '%s\n', [num2str(d) '_' num2str(t) ',' num2str(P(d,t))]);
		end
	end
end

toc(timestart)
fclose(fid);

exit;







