import numpy as np
import pandas as pd
import os
import warnings
import matplotlib.dates as mdates
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from datetime import datetime
import pandas.api.types as ptypes


# 将一列数据归一化
# 例如：将取值区间从[-30,40]中间的一列数等比例的缩放到[0,1]之间
# 输入为一个series对象（dataframe中的一行或一列），必须是数据列
def scale_series(series):
    try:
        max_value = series.max()
        min_value = series.min()
        des_series = (series - min_value) / (max_value - min_value)
        return des_series

    except Exception as e:
        print(f"An error occurred in function scale_series(): {e}")

def list_Excel_sheetNames(file_path):

    # 检测文件路径是否存在
    if not os.path.exists(file_path):
        warnings.warn(f"File path '{file_path}' does not exist.")
        exit(1)

    try:
        excel_file = pd.ExcelFile(file_path)

        # 获取表格的名称列表
        sheet_names = excel_file.sheet_names
        return sheet_names

    except Exception as e:
        print(f"An error occurred in function list_Excel_sheetNames(): {e}")


def list_matplotlib_support_font():
    # 查询当前系统所有字体
    from matplotlib.font_manager import FontManager
    import subprocess

    mpl_fonts = set(f.name for f in FontManager().ttflist)

    print('all font list get from matplotlib.font_manager:')
    for f in sorted(mpl_fonts):
        print('\t' + f)


# 副坐标轴坐标向主坐标轴坐标的转换函数
def twin_axes_to_main_axes(ax1, ax2, x, y_twin):
    if ax1 is None or ax2 is None:
        warnings.warn(f"函数twin_axes_to_main_axes中的输入坐标轴参数为空.")
        exit(1)

    # 创建坐标转换对象
    trans_main = ax1.transData
    trans_twin = ax2.transData
    # 使用副轴的坐标值和 ax2.transData 进行转换
    x_main = trans_twin.transform((x, y_twin))
    return trans_main.inverted().transform(x_main)       


# 主坐标轴坐标向副坐标轴坐标的转换函数
def main_axes_to_twin_axes(ax1, ax2, x, y_main):
    if ax1 is None or ax2 is None:
        warnings.warn(f"函数main_axes_to_twin_axes中的输入坐标轴参数为空.")
        exit(1)

    if isinstance(x, datetime):
        x_cursor = mdates.date2num(x)
    else:
        x_cursor=x

    # 获取共享x轴的坐标转换对象
    trans = ax1.transData + ax2.transData.inverted()
    twin_x,twin_y= trans.transform((x_cursor,y_main))
    return twin_x,twin_y



# 将副座标轴上的df数据点坐标对应到主坐标轴上
def transfer_dftwin_to_dfmain(ax1, ax2, dataframe):
    desdf = dataframe

    if ax1 is None or ax2 is None:
        warnings.warn(f"函数transfer_dftwin_to_dfmain中的输入坐标轴参数为空.")
        exit(1)

    # 遍历并修改每个元素值
    for index, row in desdf.iterrows():
        # 遍历每行的元素
        for column in desdf.columns:
            # 获取元素的当前值
            current_value = desdf.at[index, column]

            # 将副坐标上的df数据转换为主坐标轴上的对应值
            if isinstance(index, datetime):
                x_twin = mdates.date2num(index)
            else:
                x_twin=index

            x_main, y_main = twin_axes_to_main_axes(ax1, ax2, x_twin, current_value)

            # 将新值赋回 DataFrame
            desdf.at[index, column] = y_main

    return desdf


# 计算当前数据集上的数据最大差异
def cal_max_data_range(cur_df):
    if cur_df.empty:
        warnings.warn(f"函数cal_max_data_range中的输入dataframe为空.")
        exit(1)

    diff = 0
    try:
        for column in cur_df.columns:
            is_all_nan=cur_df[column].isna().all()
            if not is_all_nan: #排除全为nan的列
                max_value=max([x for x in cur_df[column].tolist() if not np.isnan(x)])  #排除掉列中nan的项
                min_value = min([x for x in cur_df[column].tolist() if not np.isnan(x)])
                cur_diff = max_value-min_value
                if cur_diff > diff:
                    diff = cur_diff

        return diff
    except Exception as e:
        print(f"An error occurred in function cal_max_data_range(): {e}")
    

# 找到绘制出的图标数据中与当前鼠标位置最邻近的点
# 当前鼠标点坐标与绘制出的dataframe折线图要同在一个坐标轴下（同是主轴，或同是副轴）
# x轴必须是日期类型
def find_nearest_datapoint(dataframe,cursor_x,cursor_y):
    if dataframe.empty:
        warnings.warn(f"函数find_nearest_datapoint中的输入dataframe为空.")
        exit(1)
    
    #计算当前dataframe的x轴，y轴的数据取值范围，为后续计算悬停位置离哪个数据点最近提供支持
    x=dataframe.index
    max_x_diff = mdates.date2num(max(x)) - mdates.date2num(min(x))
    max_y_diff= cal_max_data_range(dataframe)
    ratio=max_y_diff/max_x_diff  #用于将x，y轴的数据大小拉到同一个量级
    max_diff=math.sqrt(max_x_diff ** 2 + max_y_diff ** 2)

    # 计算nearest_x
    #先确定离当前鼠标点最近点的x坐标
    min_distances = []
    min_distance = None
    for column in dataframe.columns:
        y = dataframe[column].tolist()
        #cur_line = [(mdates.date2num(x[i]) - x_val) ** 2 + (y[i] - y_val) ** 2 for i in range(len(x))]
        #计算当前曲线上与鼠标最接近的点
        cur_line=[]
        for i in range(len(x)):
            if not math.isnan(y[i]): #为数字
                diff_y= y[i] - cursor_y
                #将过大的y轴数据减小，以便不会影响测量精度
                if ratio > 2:
                    diff_y=diff_y/ratio
                cur_distance=math.sqrt((mdates.date2num(x[i]) - cursor_x) ** 2 + diff_y ** 2)
                cur_line.append(cur_distance)
            else:
                cur_line.append(max_diff)
        if(len(cur_line)>0): #若此曲线在当前时间区间内无数据，则不能计入
            cur_min = min(cur_line)
            # 记录距离鼠标位置最近的那条线的各点到鼠标点距离
            if min_distance == None or cur_min < min_distance:
                min_distance = cur_min
                min_distances = cur_line

    if min_distance==None:
        warnings.warn(f"函数find_nearest_datapoint计算的当前dataframe{dataframe}没有任何数据，导致程序运行错误")
        exit(1)

    nearest_index = min_distances.index(min_distance)
    nearest_x=x[nearest_index]

    # 计算nearest_y
    #根据已经确定的离当前鼠标点最近点的x坐标，逐一计算dataframe中的每条线的y坐标，找到离当前鼠标点y坐标最近的那条线

    nearest_y = None
    min_diff = None
    for column in dataframe.columns:
        cur_y = dataframe[column][nearest_index]
        if not math.isnan(cur_y):  # 过滤掉数据的列
            cur_diff = abs(cur_y - cursor_y)
            if nearest_y == None or cur_diff < min_diff:
                nearest_y = cur_y
                min_diff = cur_diff


    if nearest_y is None:
        warnings.warn(f"函数find_nearest_datapoint计算的当前dataframe无法计算出nearest_y，因为此dataframe没有任何数字型数据，导致程序运行错误")
        exit(1)

    return nearest_x, nearest_y