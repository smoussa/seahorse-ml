%% load single driver and trip for visualisation
driver_num = 100;
trip_num = 11;
data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);

%% extract features

time = length(data);
distance = 0;
stops = 0;

D = zeros(time, 1);
for i = 2:time
    D(i-1) = sqrt(sum((data(i,:) - data(i-1,:)) .^ 2));
end

% m/s to mph
m = 2.2369362920544;
speed = D ./ m;

% speed
avg_speed = mean(speed);
max_speed = max(D);
min_speed = min(D);

% periods of very fast or very slow
fast_spd_th = 20;
slow_spd_th = 4;
fast = D > fast_spd_th;
slow = D < slow_spd_th;
time_speeding = sum(fast);
time_slowly = sum(slow);
percent_fast = time_speeding / time;
percent_slow = time_slowly / time;

% stationary periods
stationary = stops; %/ 3600 % in hrs
percent_stationary = stops / time; %*100%

% acceleration
grad = gradient(speed);
acc = (grad > 0) .* grad;
max_acc = max(acc);
min_acc = min(acc);
avg_acc = mean(acc);

% deceleration
dec = abs((grad < 0) .* grad);
max_dec = max(dec);
min_dec = min(dec);
avg_dec = mean(dec);

%% plot graphs

% plot speed and acceleration over time
plot(speed);
hold on;
plot(grad);
hold off;

% plot trip path
figure
plot(data(:,1), data(:,2))
hold on
title(['Driver ' num2str(driver_num) ' ~ Trip ' num2str(trip_num)]);
xlabel('X');
ylabel('Y');

% highlight significant speeds (or slow speeds) on trip path
plot(data(fast,1), data(fast,2), 'o');
plot(data(slow,1), data(slow,2), 'o');

hold off;
















