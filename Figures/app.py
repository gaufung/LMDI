import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
import matplotlib as mpl
from matplotlib import cm
import xlrd
from config import SHEET_INDEX, ROW_START, ROW_END, COLUMN_START, COLUMN_END,FILE_NAME
from model import Unit
plt.rcParams["font.family"] = "Calibri"
fp = FontProperties(family='Calibri')
font = findfont(fp)

#color handlermap
#cmap = plt.cm.jet
# extract all colors from the .jet map
# cmaplist = [cmap(i) for i in range(cmap.N)]
# # force the first color entry to be grey
# cmaplist[0] = (.5,.5,.5,1.0)
# # create the new map
# cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
# bounds = np.linspace(0,20,21)
# norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

class MplColorHelper:
    
  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
  def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)
col = MplColorHelper('rainbow',0,10)


class HandlerSquare(HandlerPatch):
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        center = xdescent + 0.5 * (width - height), ydescent
        p = mpatches.Rectangle(xy=center, width=height,
                               height=height, angle=0.0)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]  

def read_data():
    workbook = xlrd.open_workbook(FILE_NAME)
    sheet = workbook.sheets()[0]
    result = []
    yct = []
    for row_idx in range(ROW_START,ROW_END+1):
        row = sheet.row_values(row_idx)[COLUMN_START:COLUMN_END+1]
        result.append(Unit(row[0], float(row[1]), float(row[2]), col.get_rgb(float(row[1]))))
        yct.append(float(row[1]))
    for item in result:
        if '%.2f' % item.yct == '7.29':
            item._color=col.get_rgb(8.0)
        if '%.2f' % item.yct == '6.02':
            item._color=col.get_rgb(7.5)
        if '%.2f' % item.yct == '5.55':
            item._color=col.get_rgb(7)
        if '%.2f' % item.yct == '5.17':
            item._color=col.get_rgb(6.5)
        if '%.2f' % item.yct == '4.59':
            item._color=col.get_rgb(6)
        if '%.2f' % item.yct == '4.47':
            item._color=col.get_rgb(5.5)
        if '%.2f' % item.yct == '4.36':
                item._color=col.get_rgb(5)
        if '%.2f' % item.yct == '4.42':
            item._color=col.get_rgb(4.5)
    # yct = sorted(yct)
    # dic={}
    # for idx,value in enumerate(yct):
    #     dic[value]=idx
    # for item in result:
    #     item._color=col.get_rgb(dic[item.yct])
    return result

def _print(data):
    for item in data:
        print(item.name,item.yct,item.pei, item.color)

def _bottom(data, current_idx, is_yct=True):
    pass

def stack_values(data1, data2):
    result1 = [0.0]
    result2 = [0.0]
    for item1,item2 in zip(data1, data2):
        result1.append(result1[-1]+item1.yct)
        result2.append(result2[-1]+item2.pei)
    return result1, result2

def draw():
    row_data = read_data()
    data_by_yct = sorted(row_data, key=lambda unit: unit.yct, reverse=True)
    data_by_pei = sorted(row_data, key=lambda unit: unit.pei, reverse=True)
    stack1, stack2 = stack_values(data_by_yct, data_by_pei)
    index = 0.5
    bw = 0.5
    plt.figure(figsize=(7,9))
    plt.axis([0,3,-0.1,100])
    baritems= []
    labelitems= []
    for idx,item in enumerate(data_by_yct):
        baritems.append(plt.bar(index, np.array([item.yct]), bw, color=item.color, edgecolor='None',
                label=item.name, bottom=stack1[idx]))
        labelitems.append(item.name)
    for idx,item in enumerate(data_by_pei):
        plt.bar(index + 1, np.array([item.pei]), bw, color=item.color, edgecolor='None',
                bottom=stack2[idx])
    handlermap = {item[0]:HandlerSquare() for item in baritems}
    plt.legend([item[0] for item in baritems],labelitems,handler_map=handlermap,loc='right', ncol=1,fontsize=12, frameon=False)
    
    #add text
    for idx in range(0,30):
        if data_by_yct[idx].yct >= 3.33:
            plt.text(0.5, stack1[idx]+0.5*data_by_yct[idx].yct, '%.2f' % data_by_yct[idx].yct,ha='center',va='center')
    for idx in range(0,30):
        if data_by_pei[idx].pei >= 3.33:
            plt.text(1.5, stack2[idx]+0.5*data_by_pei[idx].pei, '%.2f' % data_by_pei[idx].pei,ha='center',va='center')
    
    #decorate
    x_ticks = [0.5, 1.5]
    x_label = [r"$D_{YCT}$", r"$D_{PEI}$"]

    y_ticks = np.arange(0,101,10)
    y_labels = np.array([str(item) for item in y_ticks])
    for y_value in y_ticks[1:]:
        plt.plot([0,0.25],[y_value,y_value],'k-',linewidth=0.5)
        plt.plot([0.75,1.25],[y_value,y_value],'k-',linewidth=0.5)
        plt.plot([1.75,2],[y_value,y_value],'k-',linewidth=0.5)
    plt.plot([0,2],[0,0],'k-',linewidth=1.0)
    plt.plot([2,2],[0,100],'k-',linewidth=0.5)
    plt.ylabel('Percentage (%)',fontproperties=fp, fontsize=15)
    plt.xticks(x_ticks, x_label, fontsize=12,fontproperties=fp)
    plt.yticks(y_ticks, y_labels,fontproperties=fp)
    gca = plt.gca()
    gca.xaxis.set_ticks_position('bottom')
    gca.yaxis.set_ticks_position('left')
    gca.yaxis.set_ticks_position('left')
    gca.spines['right'].set_color('none')
    gca.spines['top'].set_color('none')
    gca.spines['bottom'].set_color('none')
    #plt.show()
    plt.savefig('yct_and_pei_dpi_800.jpg',dpi=800)
if __name__ == '__main__':
    draw()