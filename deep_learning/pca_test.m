close all
clear all

labels = {'time','avg\_speed','max\_speed','min\_speed','time\_fast', ...
    'time\_slow','percent\_fast','percent\_slow','stops','percent\_stop', ...
    'avg\_acc','max\_acc','min\_acc','avg\_dec','max\_dec','min\_dec'};

% get data

driver_num = 104;
src = ['feature_data/' num2str(driver_num) '.csv'];
raw_data = csvread(src,1,0);

% apply pca

[coeff,score,latent,tsquared,exp] = pca(raw_data);

% keep features that represent with >= 99% confidence

comps = cumsum(latent)./sum(latent);
ncomps = sum(comps <= 0.99);
coeff = coeff(:,1:ncomps);
cscore = zscore(raw_data) * coeff;

% plot
figure()
boxplot(raw_data, 'orientation', 'horizontal', 'labels', labels)
figure()
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',labels);