from bokeh.models import ColumnDataSource, FactorRange
from bokeh.transform import factor_cmap, dodge
from bokeh import palettes
from matplotlib import font_manager
from matplotlib import pyplot as plt
import time
import json
import requests
import pandas as pd
from math import pi
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.sampledata.commits import data
from bokeh.transform import jitter
from random import randrange


url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time()*1000)
json_data = json.loads(requests.get(url).json()['data'])

for key in json_data.keys():
    print('-- - -- '*20)
    print(key, json_data[key])
    print('-- - -- '*20)
    if isinstance(json_data[key], list):
        for t in range(len(json_data[key])):
            print(json_data[key][t])
    elif isinstance(json_data[key], dict):
        for s in json_data[key].keys():
            print(s, json_data[key][s])
    else:
        pass


writer = pd.ExcelWriter(r'output.xlsx')

def wto_excel(data, sheet_name):
    pd.DataFrame(data).to_excel(writer, sheet_name)


def inp_excel(pic, sheet_name):
    writer.insert_image(pic, sheet_name)


def ChinaDayList():
    print('-- -- '*10, 'China_Day_List ', '-- -- '*10)
    print(json_data['chinaDayList'])
    Data = pd.DataFrame(json_data['chinaDayList'])
    wto_excel(Data, 'hinaDayList')
    print(Data)
    date = list(Data['date'])
    confirm = list(Data['confirm'])
    suspect = list(Data['suspect'])
    dead = list(Data['dead'])
    heal = list(Data['heal'])
    deadRate = list(Data['deadRate'])
    healRate = list(Data['healRate'])
    return date, confirm, suspect, dead, heal, deadRate, healRate


def catch_country_data():
    today_country = []
    print('-- -- '*10, 'catch_country_data ', '-- -- '*10)
    Data = json_data['areaTree']
    print(Data, '\n'*2)
    for t in range(len(Data)):
        print('-- -- '*10, Data[t]['name'], '-- -- '*10)
        for key in Data[t].keys():
            print(key, Data[t][key])
            if key == 'total':
                dic = Data[t]['total']
                dic['name'] = Data[t]['name']
                today_country.append(dic)
    data = pd.DataFrame(today_country)
    print(data)
    wto_excel(data, 'today_country')

    print('--- - --- '*10)

    drop_list = ['suspect', 'dead', 'showRate', 'showHeal']
    data_n = data

    for t in drop_list:
        data_n = data_n.drop(t, axis=1)

    i = 0

    for t in data_n['healRate']:
        t = float(t)
        if t < 10.0 or t > 90.0:
            data_n = data_n.drop(i)
        i += 1

    j = 0
    for t in data_n['confirm']:
        t = int(t)
        if t > 90:
            data_n = data_n.drop(j)
        j += 1
    print(data_n)
    confirm = list(data_n['confirm'])
    healRate = list(data_n['healRate'])
    name = list(data_n['name'])
    heal = list(data_n['heal'])
    deadRate = list(data_n['deadRate'])
    return confirm, healRate, name, heal, deadRate


def catch_province_data():
    total_porvince = []
    print('-- -- '*10, 'catch_province_data ', '-- -- '*10)
    Data = json_data['areaTree'][0]['children']
    print(Data, '/n'*2)
    print('-- -- '*10, 'get_data_structure ', '-- -- '*10)
    for t in range(len(Data)):
        print('-- -- '*10, Data[t]['name'], '-- -- '*10)
        for key in Data[t].keys():
            print(key, Data[t][key])
            if key == 'total':
                dic = Data[t]['total']
                dic['name'] = Data[t]['name']
                total_porvince.append(dic)
            if key == 'children':
                for s in range(len(Data[t]['children'])):
                    print(Data[t]['children'][s])
    data = pd.DataFrame(total_porvince)
    print(data)
    wto_excel(data, 'provinces_total')
    print('--- - --- '*10)

    confirm = list(data['confirm'])
    suspect = list(data['suspect'])
    dead = list(data['dead'])
    heal = list(data['heal'])
    name = list(data['name'])
    return confirm, suspect, dead, heal, name



def catch_city_data(provice):
    total_city = []
    print('-- -- '*10, 'catch_city_data ', '-- -- '*10)
    Data = json_data['areaTree'][0]['children']
    print(Data, '/n'*2)
    print('-- -- '*10, 'get_data_structure ', '-- -- '*10)
    for t in range(len(Data)):
        print('- '*10, Data[t]['name'], '- -'*10)
        if Data[t]['name'] == provice:
            for key in Data[t].keys():
                print(key, Data[t][key])
                if key == 'children':
                    for s in range(len(Data[t]['children'])):
                        print(Data[t]['children'][s])
                        for k in Data[t]['children'][s].keys():
                            print(k, Data[t]['children'][s][k])
                            if k == 'total':
                                dic = Data[t]['children'][s]['total']
                                dic['name'] = Data[t]['children'][s]['name']
                                total_city.append(dic)

    data = pd.DataFrame(total_city)
    print(data)
    wto_excel(data, 'provinces_total')
    print('--- - --- '*10)

    confirm = list(data['confirm'])
    suspect = list(data['suspect'])
    dead = list(data['dead'])
    heal = list(data['heal'])
    name = list(data['name'])
    return confirm, suspect, dead, heal, name




def draw_preday_confirm_suspect(date, confirm, suspect):
    print('-- -- '*10, 'drawing picture of confirm and suspect', '-- -- '*10)

    '''设置字体'''
    my_font = font_manager.FontProperties('Microsoft YaHei', size=14)

    '''设置字体'''
    plt.figure(figsize=(12, 8))

    '''绘制图表'''
    plt.plot(date, confirm, label='确诊人数')
    plt.plot(date, suspect, label='疑似人数')
    plt.scatter(date, confirm)
    plt.scatter(date, suspect)

    '''设置X轴刻度'''
    x = date
    xtick_lables = date
    plt.xticks(x, xtick_lables, rotation=45)

    '''添加描述信息'''
    plt.xlabel('日期', fontproperties=my_font)
    plt.ylabel('人数', fontproperties=my_font)
    plt.title('2019-nCoV 每日累计确诊和疑似人数趋势图', fontproperties=my_font)

    '''显示辅助网格'''
    plt.grid(alpha=0.4)

    '''添加图例'''
    plt.legend(prop=my_font)
    plt.savefig('2019-nCov每日累计确诊和疑似人数趋势图.png')
    plt.show()

    '''存入excel'''


def draw_preday_dead_heal(date, dead, heal):
    print('-- -- ' * 10, 'drawing picture of dead and heal', '-- -- ' * 10)
    my_font = font_manager.FontProperties('Microsoft YaHei', size=14)
    plt.figure(figsize=(12, 8))
    plt.plot(date, dead, label='死亡人数')
    plt.plot(date, heal, label='治愈人数')
    plt.scatter(date, dead)
    plt.scatter(date, heal)
    x = date
    xtick_labels = date
    plt.xticks(x, xtick_labels, rotation=45)
    plt.xlabel("日期", fontproperties=my_font)
    plt.ylabel("人数", fontproperties=my_font)
    plt.title("2019-nCoV每日死亡和治愈人数趋势图", fontproperties=my_font)

    plt.grid(alpha=0.4)
    plt.legend(prop=my_font)
    plt.savefig('./2019-nCoV每日死亡和治愈人数趋势图.png')
    plt.show()


def draw_perday_deadRate_healRate(date, deadRate, healRate):
    print('-- -- ' * 10, 'drawing picture of deadRate and healRate', '-- -- ' * 10)
    print('dead_rate', deadRate)
    print('heal_rate', healRate)

    deadrate = []
    healrate = []
    deadRate_data = []
    healRate_data = []
    for i in range(len(deadRate)):
        deadrate.append(int(float(deadRate[i]) + 2))
        deadRate_data.append(float(deadRate[i]))
    print('{} : {}'.format('deadRate_max', max(deadrate)))
    for i in range(len(healRate)):
        healrate.append(int(float(healRate[i]) + 2))
        healRate_data.append(float(healRate[i]))
    print('{} : {}'.format('healRate_max', max(healrate)))
    if max(deadrate) > max(healrate):
        mx = max(deadrate)
    else:
        mx = max(healrate)

    my_font = font_manager.FontProperties('Microsoft YaHei', size=14)
    plt.figure(figsize=(12, 8))

    plt.plot(date, deadRate_data, label='死亡率')
    plt.plot(date, healRate_data, label='治愈率')
    plt.scatter(date, deadRate_data)
    plt.scatter(date, healRate_data)

    x = date
    xtick_labels = date
    plt.xticks(x, xtick_labels, rotation=45)
    y = [i for i in range(mx)]
    ytick_labels = ["{}%".format(i) for i in range(mx)]
    plt.yticks(y, ytick_labels)

    plt.xlabel("日期", fontproperties=my_font)
    plt.ylabel("百分比", fontproperties=my_font)
    plt.title("2019-nCoV每日死亡率和治愈率对比趋势图", fontproperties=my_font)
    plt.grid(alpha=0.4)
    plt.legend(prop=my_font)
    plt.savefig('./2019-nCoV每日治愈率和死亡率对比趋势图.png')
    plt.show()


def draw_bar(confirm, healRate, name):
    print('-- -- ' * 10, 'drawing picture of bar v1', '-- -- ' * 10)

    '''解决中文显示的问题'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    '''输出文件'''
    output_file('2019-nCoV各国确诊和治愈率对比1.html')

    yr = ['confirm', 'healRate']
    data = {'country': name, 'confirm': confirm, 'healRate': healRate}
    source = ColumnDataSource(data=data)

    p = figure(x_range=name, y_range=(0, 90), plot_height=500,
               title='2019-nCoV各国确诊和治愈率对比1',
               toolbar_location=None, tools='')

    p.vbar(x=dodge('country', 0.0, range=p.x_range), top='confirm', width=0.2,
           source=source, color='#c9d9d3', legend_label='confirm')
    p.vbar(x=dodge('country', 0.25, range=p.x_range), top='healRate', width=0.2,
           source=source, color='#718dbf', legend_label='healRate')

    p.x_range.range_padding =0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    show(p)


def draw_preday_confirm(confirm, dead, heal, name):
    print('-- -- ' * 10, 'drawing preday confirm', '-- -- ' * 10)

    '''解决中文显示的问题'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    '''输出文件'''
    output_file('2019-nCoV各省生病人数.html')


    province = name
    province.pop(0)

    counts = []
    for i in range(len(confirm)):
        count = int(confirm[i]) - int(dead[i]) - int(heal[i])
        counts.append(count)
    counts.pop(0)
    ma = sorted(counts)
    ma = int(ma[-1] + 100)

    color = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f",
             "#9e0142", "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43",
             "#d73027", "#a50026", "#006837", "#1a9850", "#66bd63", "#a6d96a", "#d9ef8b", "#ffffbf", "#fee08b", "#fdae61",
             "#f46d43", "#d73027", "#a50026"]

    source = ColumnDataSource(data=dict(provinces=province, counts=counts, color=color))
    p = figure(x_range=province, y_range=(0, ma), plot_height=500, plot_width=2000,
               title='2019-nCoV各省生病人数',
               toolbar_location=None)
    p.vbar(x='provinces', top='counts', width=0.9, legend_field='provinces', color='color',
           source=source)
    p.xgrid.grid_line_color = None
    p.legend.orientation = 'horizontal'
    p.legend.location = 'top_center'

    show(p)

def draw_preday_country_confirm(confirm, dead, heal, name, province):

    print('-- -- ' * 10, 'drawing pre city confirm pie chart', '-- -- ' * 10)

    '''解决中文显示的问题'''
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    '''输出文件'''
    output_file('2019-nCoV各省生病人数.html')

    city = name
    counts = []
    for i in range(len(confirm)):
        count = int(confirm[i]) - int(dead[i]) - int(heal[i])
        counts.append(count)
    numb = len(city)

    dic_city = {}
    for i in range(numb):
        dic_city[city[i]] = counts[i]
    print(dic_city)


    colors = ["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4", "#e6f598", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d53e4f",
             "#9e0142", "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", "#fee090", "#fdae61", "#f46d43",
             "#d73027", "#a50026", "#006837", "#1a9850", "#66bd63", "#a6d96a", "#d9ef8b", "#ffffbf", "#fee08b", "#fdae61",
             "#f46d43", "#d73027", "#a50026"]

    color = []
    for i in range(numb):
        ranindex = randrange(0, len(colors))
        color.append(colors[ranindex])
        colors.pop(ranindex)
    print(color)


    data = pd.Series(dic_city).reset_index(name='value').rename(columns={'index': 'city'})
    data['angle'] = data['value']/data['value'].sum()*2*pi
    data['color'] = color

    p = figure(plot_height=500, title=province+'pre city pie chart', toolbar_location=None,
               tools='hover', tooltips='@city: @value', x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color='white', fill_color='color', legend_field='city',
            source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    show(p)




    pass

def main():
    global json_data
    global writer

    date, confirm, suspect, dead, heal, deadRate, healRate = ChinaDayList()
    draw_preday_confirm_suspect(date, confirm, suspect)
    
    draw_preday_dead_heal(date, dead, heal)
    draw_perday_deadRate_healRate(date, deadRate, healRate)
    confirm_prv, suspect_prv, dead_prv, heal_prv, name_prv = catch_province_data()
    draw_preday_confirm(confirm_prv, dead_prv, heal_prv, name_prv)
    '''
    confirm_cty, healRate_cty, name_cyt, heal_cyt, deadRate_cyt = catch_country_data()
    draw_bar(confirm_cty, healRate_cty, name_cyt)
    '''
    provinc = '江苏'
    confirm_city, suspect_city, dead_city, heal_city, name_city = catch_city_data(provinc)
    draw_preday_country_confirm(confirm_city, dead_city, heal_city, name_city, provinc)


    writer.save()


if __name__ == '__main__':
    main()
