function [extremes] = build_dbn(driver_num, dbn, opts)

	% fetch driver data
	src = ['./feature_data/' num2str(driver_num) '.csv']
	raw = csvread(src,1,0);
	n = length(raw);

	% apply pca
	data = apply_pca(raw);
	% data = raw;

	% normalise between 0 and 1 (for deep learning toolbox)
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

	% create and train a dbn
	dbn = dbnsetup(dbn, train_x, opts);
	dbn = dbntrain(dbn, train_x, opts);

	% unfold dbn to nn
	nn = dbnunfoldtonn(dbn, 1);
	nn.activation_function = 'sigm';

	% train nn
	nn = nntrain(nn, train_x, ones(length(train_x), 1), opts);

	% predict
	probs = nnpredict(nn, train_x);
	norm_trips = abs((probs - mean(probs)) / std(probs));
	num_extremes = length(find(norm_trips > 1))
	extremes = find(norm_trips > 1)

end