#from __future__ import (absolute_import, division, print_function)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib import colors
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import sys
sys.path.append('./python/')
import stateData as sd
import tools
###############################################################################
fig, ax = plt.subplots()

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# Mercator projection, for Alaska and Hawaii
m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,
            projection='merc',lat_ts=20)  # do not change these numbers

#%% ---------   draw state boundaries  ----------------------------------------
## data from U.S Census Bureau
## http://www.census.gov/geo/www/cob/st2000.html
shp_info = m.readshapefile('./shapeData/st99_d00','states',drawbounds=True,
                           linewidth=0.45,color='gray')
shp_info_ = m_.readshapefile('./shapeData/st99_d00','states',drawbounds=False)


#%% -------- choose a color for each state based on population density. -------

title='EC Votes per Million People'
plotName = 'EC'
def getPlotVal(name):
    return sd.ec[name] / (sd.pop[name]/1.e6)
vmin = 1.; vmax = 6. # set range.
norm = colors.LogNorm(vmin=vmin, vmax=vmax)
cmap = plt.cm.inferno

'''
title='House Votes per Million People'
plotName = 'House'
def getPlotVal(name):
    return sd.house[name] / (sd.pop[name]/1.e6)
vmin = 1; vmax = 2 # set range.
cmap = plt.cm.inferno
norm = colors.Normalize(vmin=vmin, vmax=vmax)
'''
'''
title='Senate Votes per Million People'
plotName = 'Senate'
def getPlotVal(name):
    return 2.0 / (sd.pop[name]/1.e6)
vmin = 5.e-2; vmax = 4.e0 # set range.
cmap = plt.cm.inferno
norm = colors.LogNorm(vmin=vmin, vmax=vmax)
'''

colors={}
statenames=[]
for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        plotVal = getPlotVal(statename)
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = cmap((plotVal-vmin)/(vmax-vmin))[:3]
    statenames.append(statename)

#%% ---------  cycle through state names, color each one.  --------------------
for nshape,seg in enumerate(m.states):
    # skip DC and Puerto Rico.
    if statenames[nshape] not in ['Puerto Rico', 'District of Columbia']:
        color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)

AREA_1      = 0.005  # exclude small Hawaiian islands that are smaller than AREA_1
AREA_2      = AREA_1 * 30.0  # exclude Alaskan islands that are smaller than AREA_2
AK_SCALE    = 0.19  # scale down Alaska to show as a map inset
HI_OFFSET_X = -1900000  # X coordinate offset amount to move Hawaii "beneath" Texas
HI_OFFSET_Y = 250000    # similar to above: Y offset for Hawaii
AK_OFFSET_X = -250000   # X offset for Alaska (These four values are obtained
AK_OFFSET_Y = -750000   # via manual trial and error, thus changing them is not recommended.)

for nshape, shapedict in enumerate(m_.states_info):  # plot Alaska and Hawaii as map insets
    if shapedict['NAME'] in ['Alaska', 'Hawaii']:
        seg = m_.states[int(shapedict['SHAPENUM'] - 1)]
        if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > AREA_1:
            seg = [(x + HI_OFFSET_X, y + HI_OFFSET_Y) for x, y in seg]
            color = rgb2hex(colors[statenames[nshape]])
        elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > AREA_2:
            seg = [(x*AK_SCALE + AK_OFFSET_X, y*AK_SCALE + AK_OFFSET_Y)\
                   for x, y in seg]
            color = rgb2hex(colors[statenames[nshape]])
        poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
        ax.add_patch(poly)

ax.set_title(title)

#%% ---------  Plot bounding boxes for Alaska and Hawaii insets  --------------
light_gray = [0.8]*3  # define light gray color RGB
x1,y1 = m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
x2,y2 = m_([-180,-180,-177],[26,23,20])  # these numbers are fine-tuned manually
m_.plot(x1,y1,color=light_gray,linewidth=0.8)  # do not change them drastically
m_.plot(x2,y2,color=light_gray,linewidth=0.8)

#%% ---------   Show color bar  ---------------------------------------
ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
cb = ColorbarBase(ax_c,cmap=cmap,norm=norm,orientation='vertical')

plt.savefig('./plots/' + plotName + '.png', bbox_inches='tight', dpi=600)
