import sim650
"""
Simple Runner Application to show the minimal use of the sim650 classes.
"""

#file = "D:\\650\\fibonzu.650"
#file = "D:\\650\\chessboard.650"
#file = "D:\\650\\jd_division.650"
#file = "D:\\650\\fibonze.650"
file = "D:\\650\\fibonze_console_input.650"
#file = "D:\\650\\fibobmi.650"
#file = "D:\\650\\ma_divide.650"
#file = "D:\\650\\et_fibo.650"
#file = "D:\\650\\ma_infinite_loop.650"


x = sim650.sim650()
#x.checkSource(file)
x.loadSource(file)
#x.runWithTraces()
#x.run()

