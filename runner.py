import sim650
"""
Simple Runner Application to show the minimal use of the sim650 classes.
"""

#file = "sources/fibonze_console_input.650"
file = "sources/chessboard.650"

x = sim650.sim650()
#x.checkSource(file)
x.loadSource(file)
#x.runWithTraces()
#x.run()

