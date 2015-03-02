
% load single driver and trip for visualisation
driver_num = 100;
trip_num = 65;
data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);

plot(data(:,1), data(:,2))
hold on
% plot(smooth(data(:,1), 'rloess'), smooth(data(:,2), 'rloess'))
title(['Driver ' num2str(driver_num) ' ~ Trip ' num2str(trip_num)]);
xlabel('X');
ylabel('Y');
hold off;