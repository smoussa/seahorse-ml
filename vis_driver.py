import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

driver_num = 100
source_dir = 'drivers/{0}/'.format(driver_num)
num_trips = 200


cm = plt.get_cmap('Accent')
cNorm  = colors.Normalize(vmin=1, vmax=num_trips)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

for t in range(1,num_trips+1):
    T = np.genfromtxt(source_dir+str(t)+'.csv', skip_header=1, delimiter=",")
    colorVal = scalarMap.to_rgba(t)
    plt.plot(T[:,0], T[:,1], color=colorVal)

plt.title('Trips of Driver '+str(driver_num))
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig("test.eps",format='eps')
