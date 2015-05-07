
% load single driver and visualise their trips
driver_num = 100;
source_dir = ['sample_data/' num2str(driver_num) '/'];
num_trips = 200;

for t = 1:num_trips
    T = csvread([source_dir num2str(t) '.csv'], 1, 0);
    plot(T(:,1), T(:,2),'LineSmoothing','on');
    hold on;
end

title(['Trips of Driver ' num2str(driver_num)]);
xlabel('X');
ylabel('Y');
