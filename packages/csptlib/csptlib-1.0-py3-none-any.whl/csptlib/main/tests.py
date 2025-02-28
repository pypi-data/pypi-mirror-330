from transplotlib import *

if __name__ == '__main__':
    print('used for test transplotlib')
    tra = SignalPlanPlot()  # 实例化
    tra.gw_speed = 50  # 绿波速度
    tra.phase_inbound = ['lead', 'lag']  # 设置相序
    tra.phase_outbound = ['lag', 'lag']
    # 设置信号机个数，周期，相位差
    tra.controllers_num, tra.cycle, tra.offset = 2, [148, 148], [0, 96]
    tra.inter_location_inbound = [154, 1271]  # 上行交叉口进口道停止线位置
    tra.inter_location_outbound = [202, 1347]  # 下行交叉口进口道停止线位置
    # 设置配时方案
    tra.ari_signal_plan_ring1 = {'yr1': [3, 2], 'green1': [29, 43],
                                 'yr2': [2, 2], 'green2': [39, 37], 'red': [75, 64]}
    tra.ari_signal_plan_ring2 = {'yr1': [3, 2], 'green1': [43, 39],
                                 'yr2': [2, 2], 'green2': [25, 41], 'red': [75, 64]}
    tra.plot_signal_plan(band_text=(True, 1800))  # 绘制配时图
    transplt.show()
