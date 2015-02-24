%% load single driver and trip for visualisation
driver_num = 100;
trip_num = 5;
data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);

%% speed and time features
% (1) average speed (including stationary periods)
% (2) maximum speed
% (3) minimum speed always 0?
% (4) total time spent stationary
% (5) average time spent stationary

time = length(data);
distance = 0;
max_diff = 0;
min_diff = Inf;
stops = 0;

for i = 2:time
    diff = sqrt(sum((data(i,:) - data(i-1,:)) .^ 2));
    distance = distance + diff;
    
    if (diff > max_diff)
        max_diff = diff;
    end
    if (diff < min_diff)
        min_diff = diff;
    end
    if (diff == 0) % stationary
        stops = stops + 1;
    end
end

% m/s to mph
m = 2.2369362920544;

avg_speed = (distance/time) / m;
max_speed = max_diff / m;
min_speed = min_diff / m;

stationary = stops %/ 3600 % in hrs
percent_stationary = stops / time
















