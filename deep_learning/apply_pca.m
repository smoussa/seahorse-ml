function [data] = apply_pca(raw)

	[coeff,score,latent,tsquared,exp] = pca(raw);

	comps = cumsum(latent)./sum(latent);
	ncomps = sum(comps <= 0.99);
	coeff = coeff(:,1:ncomps);
	data = zscore(raw) * coeff;

	% plot
	% if plot == true

	% 	labels = {'time','avg_speed','max_speed','min_speed','time_fast', ...
	%     'time_slow','percent_fast','percent_slow','stops','percent_stop', ...
	%     'avg_acc','max_acc','min_acc','avg_dec','max_dec','min_dec'};

	% 	figure()
	% 	boxplot(raw, 'orientation', 'horizontal', 'labels', labels)
	% 	figure()
	% 	biplot(coeff(:,1:2),'scores', score(:,1:2), 'varlabels',labels);
	% end

	% find extremes
	% if extremes == true
	% 	[st2,index] = sort(tsquared,'descend'); % sort in descending order
	% 	extreme = index(1);
	% end
end