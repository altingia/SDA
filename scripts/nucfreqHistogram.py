#!/bin/env python
import numpy as np
import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import matplotlib.ticker.FuncFormatter
from sklearn.mixture import GaussianMixture
import argparse 


parser = argparse.ArgumentParser()
parser.add_argument("nucfreq", help="assembly.consensus.nucfreq")
args = parser.parse_args()

nucfreq=args.nucfreq


colnames = ["contig", "pos", "A", "C", "G", "T", "deletion", "insertion"]

f = open(nucfreq)
first  = []
second = []
truepos= []
for line in f:
    line = line.split()
    truepos.append(int(line[1]))
    bases = []
    for basepair in line[2:6]:
        bases.append(int(basepair))
    bases = sorted(bases, reverse=True)
    first.append(bases[0])
    second.append(bases[1])
pos = np.array( range(0,len(second)) ) 
second = np.array(second)
first = np.array(first)
truepos = np.array(truepos)
print(len(second), len(first + second))
second = second[ (first+second) < 140 ]; 
#second = np.random.choice(second, size=500000)
print(len(second))

#plt.rc('font', family='serif')
fig = plt.figure()


print(second)
# the histogram of the data
plt.hist(second, bins=(second.max()-1))

plt.xlabel('Depth')
plt.ylabel('Probability')
plt.axis([10, 120, 0, len(second)/200 ])

plt.savefig('nucfreqHistogram.png')

exit()
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)





prime, = plt.plot(truepos, first, 'o', color="black", markeredgewidth=0.0, markersize=3, label = "most frequent base pair")
sec, = plt.plot(truepos, second,'o', color="red",   markeredgewidth=0.0, markersize=3, label = "second most frequent base pair")
ax.set_xlabel('BP Position')
ax.set_ylabel('Depth')

ylabels = [format(label, ',.0f') for label in ax.get_yticks()]
xlabels = [format(label, ',.0f') for label in ax.get_xticks()]
ax.set_yticklabels(ylabels)
ax.set_xticklabels(xlabels)

# Hide the right and top spines
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
# Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.legend()

plt.savefig('threshold.png')

exit(0)
# after this stuff is gmm stuff that did not work

#second[second > 300 ] = 15
gmm = GaussianMixture(n_components=2, covariance_type="diag", tol=0.001, weights_init= [.5,.5])
gmm = gmm.fit(X=np.expand_dims(second, 1))

varrs = gmm.covariances_
stds = np.sqrt(varrs)
mean = max(gmm.means_)[0]
sd = max(stds)[0]

print("mean: {} std: {} weights {}".format(mean, sd, gmm.weights_))

# but if there is a duplicaiton or something the number of errors doubles because errors from
# both regiosn map there. So I have to make the threshold much higher
minCoverage = (sd  + mean)  
numAbove = sum(second > minCoverage)
print("Threshhold: {} \t Number of points above threshhold: {}".format(minCoverage, numAbove))


# reset stuff 
psvs = second[second > minCoverage]
psvPos = pos[second > minCoverage]
noise = second[second <= minCoverage]
noisePos = pos[second <= minCoverage]


psvGmm = GaussianMixture(n_components=1, covariance_type="diag", tol=0.001)
psvGmm = psvGmm.fit(X=np.expand_dims(psvs, 1))
varrs = psvGmm.covariances_
stds = np.sqrt(varrs)
mean = max(psvGmm.means_)[0]
sd = max(stds)[0]
# if I look at things 5 or more std distributions away I should only have a .0001  error rate 
maxCoverage = mean + sd * 5 
print("mean: {} std: {}".format(mean, sd))


plt.plot(noisePos, noise, 'ro')
plt.plot(psvPos, psvs, 'go')
plt.plot(pos, first, 'bo')
plt.axhline(y=minCoverage, color='g', linestyle='--')
plt.axhline(y=maxCoverage, color='g', linestyle='--')

#plt.show()
plt.savefig('threshold.png')


minCoverage = int(minCoverage)
maxCoverage = int(maxCoverage)
maxFile = open(autoMax, "w+")
minFile = open(autoMin, "w+")
maxFile.write(str(maxCoverage) + "\n" )
minFile.write(str(minCoverage) + "\n" )

print("min/maxCoverage: {}/{}".format((minCoverage), (maxCoverage)))
print( "PLEASE LOOK AT threshold.png TO CONFIRM AUTO THRESHOLDS" )


