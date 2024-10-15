import pandas as pd


# 算法的定义
def wind_power(wind_in, wind_rated, coe, data):
    res = pd.DataFrame()
    extents = [[0, wind_in]]
    L = [round(wind_in + 0.1 * i, 1) for i in range(10*(wind_rated-wind_in))]
    for i in L:
        extents.append([i, round(i + 0.1, 1)])
    extents.append([wind_rated, 100])
    limit = []
    for extent in extents:
        cond = (extent[0] <= data['WindSpeed']) & (data['WindSpeed'] < extent[1]) & (data['GridPower'] > 0)
        data_temp = data[cond]
        data_describe = data_temp['GridPower'].describe()
        q1 = data_describe.loc['25%']
        q3 = data_describe.loc['75%']
        iqr = q3 - q1
        result = [q1 - coe * iqr, q3 + coe * iqr]
        limit.append(result)
    limit = pd.DataFrame(limit)
    limit.columns = ['下限', '上限']
    limit['范围'] = [x for x in extents]
    return limit


def wind_power_res(lim, data):
    for i in range(len(lim)):
        a = (lim.iloc[i]['范围'][0] <= data['WindSpeed']) & (data['WindSpeed'] <= lim.iloc[i]['范围'][1])
        if a[0]:
            low_lim = lim.iloc[i]['下限']
            up_lim = lim.iloc[i]['上限']
            if (low_lim <= data['GridPower'][0]) & (data['GridPower'][0] <= up_lim):
                res = 1
            else:
                res = 0
    return res


def wind_power_logic(a, data):
    if a == 1:
        msg = '风机处于正常功率范围'
    elif data['WTState'][0] == 11:
        msg = 'SCADA降容'
    elif data['WTState'][0] == 12:
        msg = 'HMI降容'
    elif data['T_GBS_In_Visu'][0] > 80 or data['T_GBS_Out_Visu'][0] > 80:
        msg = '齿轮箱高温限功率状态'
    elif data['gConvCabinetTemp'][0] < -50:
        msg = '变频器低温限功率状态'
    elif data['T_GW_U1_Visu'][0] > 80 or data['T_GW_V1_Visu'][0] > 80 or data['T_GW_W1_Visu'][0] > 80:
        msg = '发电机高温限功率状态'
    else:
        msg = '未知原因限功率状态'
    return msg


# # 读取训练用数据
# train_data = pd.read_csv('C:/Users/Administrator/Desktop/TB-HIS/TB001_10s/风功率模型训练数据.csv', index_col=False)
# # 调用函数，获得阈值
# limit = wind_power(5, 11, 1.75, train_data)
# # 读取测试数据
# test_data = pd.read_csv('C:/Users/Administrator/Desktop/TB-HIS/TB001_10s/风功率模型测试数据.csv', index_col=False, encoding='gbk')
# # 输出功率判断结果,0则为降功率，1为正常
# wpr = wind_power_res(limit, test_data)
# wind_power_logic(wpr, test_data)