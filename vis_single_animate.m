
% load single driver and trip for visualisation
driver_num = 100;
trip_num = 65;
data = csvread(['sample_data/' num2str(driver_num) ...
    '/' num2str(trip_num) '.csv'], 1, 0);
for i=1:length(data)-1
	plot(data(i:i+1,1), data(i:i+1,2),'r')
	hold on
	pause(0.1)
end
% plot(smooth(data(:,1), 'rloess'), smooth(data(:,2), 'rloess'))
title(['Driver ' num2str(driver_num) ' ~ Trip ' num2str(trip_num)]);
xlabel('X');
ylabel('Y');
hold off;