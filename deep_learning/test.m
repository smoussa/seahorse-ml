close all
clear all

%% things to try
%{
    - dbn with multiple hidden layers and different sizes
    - apply pca, take first few that provide 95% confidence
    - train dbn with these features
%}

%% normalise data

header = {'time','avg\_speed','max\_speed','min\_speed','time\_fast', ...
    'time\_slow','percent\_fast','percent\_slow','stops','percent\_stop', ...
    'avg\_acc','max\_acc','min\_acc','avg\_dec','max\_dec','min\_dec'};

driver_num = 105;
trip_num = 1;
src = ['feature_data/' num2str(driver_num) '.csv'];
raw_data = csvread(src,1,0);

% normalise between 0 and 1 (for deep learning toolbox)
data = double(raw_data);
for i = 1:size(data,2)
    col = data(:,i);
    mind = min(col);
    maxd = max(col);
    rng = (maxd - mind);
    if rng ~= 0
        data(:,i) = (col - mind) / rng;
    else
        data(:,i) = 0;
    end
end
train_x = data;


%% apply pca

[pc,score,latent,tsquared,exp] = pca(zscore(data));

% keep features that represent with < 99% confidence
comps = cumsum(latent)./sum(latent);
ncomps = sum(comps < 0.99);

% [st2,index] = sort(tsquared,'descend'); % sort in descending order
% extreme = index(1);
% [index ]

[spc, si] = sort(var(pc)', 'descend'); % SELECTION ISSUE!!
topcomps = si(1:ncomps);

[V D] = eig(cov(zscore(data)));

% biplot(pc(:,1:3),'Scores',score(:,1:3),'VarLabels',header);
% biplot(pc(topcomps,1:2),'Scores',score(topcomps,1:2),'VarLabels', ...
%     header(topcomps));

train_x = train_x(:,topcomps);


%% train dbn on some trip features for a driver

% create and train a dbn
dbn.sizes = [3 2];
opts.numepochs = 1;
opts.batchsize = 20;
opts.momentum  = 0;
opts.alpha     = 1;
dbn = dbnsetup(dbn, train_x, opts);
dbn = dbntrain(dbn, train_x, opts);

%unfold dbn to nn
nn = dbnunfoldtonn(dbn, 1);
nn.activation_function = 'sigm';

%train nn
nn = nntrain(nn, train_x, ones(length(train_x), 1), opts);

% nnpredict(nn, train_x)
probs = zeros(200,10);
classes = zeros(200,10);
for i = 1:10
    [probs(:,i), classes(:,i)] = nnpredict(nn, train_x);
end

mean(probs,2)
plot(mean(probs,2), 'o')





%% test with other drivers

% get test driver's trips
% test_driver = 109;
% test_x = csvread(['feature_data/' num2str(test_driver) '.csv'], 1, 0);









