# robot-draw

项目目标：根据一组给定的笔画图片，在dobot magician上作画出来

input: 输入一组连续作画的图像
output: 是我们通过input得到的单独的笔画

visual: 可视化文件夹
visual_input: 可视化我的输入图片
visual_output: 可视化我的输出图片
visual_output_strokes.py: 可视化我的输出坐标

采取的策略是插入节点，比如实际情况画出1cm的曲线，对应插入10个节点

extract_strokes: 通过连续的笔画图片提取笔画
main.py: 主程序

运行``` python main.py```

插入的节点示例：
19.62,12.75,50.00
19.62,12.88,50.00
19.62,13.00,50.00
19.62,13.12,50.00
19.50,13.25,50.00
19.50,13.38,50.00
19.50,13.50,50.00
......


![Dobot Magician 作画演示](docs/dobot.gif)