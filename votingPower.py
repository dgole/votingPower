import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import sys
sys.path.append('./python/')
import stateData as sd
import tools
###############################################################################
usMap      = tools.USmap()
popDensity = sd.popDensity

# choose a color for each state based on population density
colors = {}
cmap   = plt.cm.hot_r
vmin   = 0
vmax   = 450
norm   = Normalize(vmin=vmin, vmax=vmax)
for stateName in usMap.stateNames:
    if stateName in popDensity.keys():
        pop = popDensity[stateName]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[stateName] = cmap(np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
usMap.ax_c = usMap.fig.add_axes([0.9, 0.1, 0.03, 0.8])
usMap.cb   = ColorbarBase(usMap.ax_c,cmap=cmap,norm=norm,orientation='vertical',
                                  label=r'[population per $\mathregular{km^2}$]')

usMap.colorStates(colors)

usMap.ax.set_title('United States Population Density by State')

plt.savefig('./plots/votingPower.png', bbox_inches='tight', dpi=600)
