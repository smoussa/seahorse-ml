%% FEATURES:
% [ driver, time, avg_speed, max_speed, min_speed, time_fast,
% time_slow, percent_fast, percent_slow, stops, percent_stop, avg_acc,
% max_acc, min_acc, avg_dec, max_dec, min_dec ]

header = ['time,avg_speed,max_speed,min_speed,time_fast,' ...
    'time_slow,percent_fast,percent_slow,stops,percent_stop,' ...
    'avg_acc,max_acc,min_acc,avg_dec,max_dec,min_dec'];

for d = 100:110
    
    fname = ['feature_data/' num2str(d) '.csv'];
    fid = fopen(fname, 'w+');
    fprintf(fid, '%s\n', header);
    fclose(fid);
    
    for t = 1:200
        extract_trip(fname, d,t);
    end
end