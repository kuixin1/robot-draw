import os
import DobotDllType as dType

# 接收一个txt文件名，逐行读取内容
def read_points_from_txt(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            coords = [float(x) for x in line.split(',')]
            points.append(coords)
    return points

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    dType.SetQueuedCmdClear(api)
    dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    # 获取所有txt文件
    txt_dir = 'output_strokes'
    txt_files = [os.path.join(txt_dir, f) for f in os.listdir(txt_dir) if f.endswith('.txt')]


    for txt_file in txt_files:
        points = read_points_from_txt(txt_file)
        if not points:               # 文件可能为空
            continue
        print(f"Drawing {txt_file} ...")

        # ------------- 第 1 步：空移到起点（z=60）-------------
        first_x, first_y, _ = points[0]
        lastIndex = dType.SetPTPCmd(api,
                                    dType.PTPMode.PTPMOVJXYZMode,
                                    first_x, first_y, 60, 0, isQueued=1)[0]

        # ------------- 第 2 步：降到绘画高度 z=50 -------------
        lastIndex = dType.SetPTPCmd(api,
                                    dType.PTPMode.PTPMOVJXYZMode,
                                    first_x, first_y, 50, 0, isQueued=1)[0]

        # ------------- 第 3 步：正常画线 -----------------------------
        for x, y, z in points[1:]:          # 第 0 点已经处理过，跳过
            lastIndex = dType.SetPTPCmd(api,
                                        dType.PTPMode.PTPMOVJXYZMode,
                                        x, y, 50, 0, isQueued=1)[0]

        # ------------- 第 4 步：画完抬笔到 z=60（为下一条做准备）---
        last_x, last_y, _ = points[-1]
        lastIndex = dType.SetPTPCmd(api,
                                    dType.PTPMode.PTPMOVJXYZMode,
                                    last_x, last_y, 60, 0, isQueued=1)[0]
    

    dType.SetQueuedCmdStartExec(api)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
    dType.SetQueuedCmdStopExec(api)

dType.DisconnectDobot(api)