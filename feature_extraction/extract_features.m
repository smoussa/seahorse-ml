function [data, fast, slow, stationary] = extract_features(driver_num, trip_num)

	data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);


	%% extract features

	time = length(data);

	D = zeros(time, 1);
	for i = 2:time
	    D(i-1) = sqrt(sum((data(i,:) - data(i-1,:)) .^ 2));
	end

	% m/s to mph
	% m = 2.2369362920544;
	% speed = D ./ m
	speed = D;

	% speed
	avg_speed = mean(speed);
	max_speed = max(speed);
	min_speed = min(speed);

	% periods of very fast or very slow
	fast_spd_th = 25;
	slow_spd_th = 4;
	fast = D > fast_spd_th;
	slow = D < slow_spd_th;
	time_fast = sum(fast);
	time_slow = sum(slow);
	percent_fast = time_fast / time;
	percent_slow = time_slow / time;

	% stationary periods
	stationary = D < 0.5;
	stops = sum(stationary); %/ 3600 % in hrs
	percent_stop = stops / time; %*100%

	% acceleration
	grad = gradient(speed);
	acc = abs((grad > 0) .* grad);
	max_acc = max(acc);
	min_acc = min(acc);
	avg_acc = mean(acc);

	% deceleration
	dec = abs((grad < 0) .* grad);
	max_dec = max(dec);
	min_dec = min(dec);
	avg_dec = mean(dec);

end