%% train dbn on some trip features for a driver

driver_num = 100;
trip_num = 1;
raw_data = csvread(['feature_data/' num2str(driver_num) '.csv'], 1, 0);

% normalise between 0 and 1
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

dbn.sizes = [25];
opts.numepochs =   1;
opts.batchsize = 20;
opts.momentum  =   0;
opts.alpha     =   1;
dbn = dbnsetup(dbn, train_x, opts);
dbn = dbntrain(dbn, train_x, opts);

%unfold dbn to nn
nn = dbnunfoldtonn(dbn, 1);
nn.activation_function = 'sigm';

% get test driver's trips
test_driver = 109;
test_data = csvread(['feature_data/' num2str(test_driver) '.csv'], 1, 0);

%train nn
nn = nntrain(nn, train_x, ones(length(train_x), 1), opts);

% nnpredict(nn, train_x)
nnpredict(nn, test_data);







