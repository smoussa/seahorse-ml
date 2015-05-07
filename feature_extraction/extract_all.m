%% FEATURES:
% [ driver, time, avg_speed, max_speed, min_speed, time_fast,
% time_slow, percent_fast, percent_slow, stops, percent_stop, avg_acc,
% max_acc, min_acc, avg_dec, max_dec, min_dec ]

header = ['time,avg_speed,max_speed,min_speed,time_fast,' ...
    'time_slow,percent_fast,percent_slow,stops,percent_stop,' ...
    'avg_acc,max_acc,min_acc,avg_dec,max_dec,min_dec'];

disp('Extracting all driver trips ...');

tstart = tic;
missing = 0;
parfor d = 1:3612
    
    srcpath =  ['drivers/' num2str(d)];
    if exist(srcpath)

        destpath = ['feature_data/' num2str(d) '.csv'];
        fid = fopen(destpath, 'w+');
    	fprintf(fid, '%s\n', header);
    	fclose(fid);

    	for t = 1:200
            extract_trip(destpath, d,t);
    	end

        disp(['Driver ' num2str(d) ' done.']);
    else
        disp(['driver ' num2str(d) ' does not exist']);
        missing = missing + 1;
    end
end

disp('Finished. Drivers and features extracted.');
disp([num2str(missing) ' driver(s) missing.']);
toc(tstart)
