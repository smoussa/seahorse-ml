function view_trips(driver_num, trips, highlight)

	% highlight interesting areas
	figure()

	if highlight
		for t = 1:numel(trips)
			trip = trips(t);

			[data, fast, slow, stationary] = extract_features(driver_num, trip);

			subplot(ceil(length(trips)/2), 2, t);
			hold on;
			plot(data(:,1), data(:,2))
			title(['Driver ' num2str(driver_num) ' ~ Trip ' num2str(trip)]);
			xlabel('X');
			ylabel('Y');

			% highlight significant speeds (or slow speeds) on trip path
			plot(data(fast,1), data(fast,2), 'o');
			plot(data(slow,1), data(slow,2), 'o');
			plot(data(stationary,1), data(stationary,2), 'ko');
			hold off;
		end

		% plot speed and acceleration over time
		% figure()
		% plot(speed);
		% hold on;
		% plot(grad);
		% hold off;
	else
		for t = 1:numel(trips)
			trip = trips(t);

			[data, fast, slow, stationary] = extract_features(driver_num, trip);

			subplot(ceil(length(trips)/2), 2, t);
			plot(data(:,1), data(:,2))
			hold on
			title(['Driver ' num2str(driver_num) ' ~ Trip ' num2str(trip)]);
			xlabel('X');
			ylabel('Y');
			hold off;
		end
	end
end