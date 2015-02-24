%% load single driver and trip for visualisation
driver_num = 111;
trip_num = 5;
data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);

%% average speed (including stationary periods) and maximum speed
% minimum speed = 0?

time = length(data);
distance = 0;
max_diff = 0;

for i = 2:time
    diff = sqrt(sum((data(i,:) - data(i-1,:)) .^ 2));    
    if (diff > max_diff)
        max_diff = diff;
    end
    distance = distance + diff;
end

% m/s to mph
m = 2.2369362920544;
avg_speed = (distance/time) / m
max_speed = max_diff / m

