import numpy as np
import allocation


TOP25_ROI = 0.7382243048475519

stock_return = TOP25_ROI #*deposit

return_vector = [1, 1.05, 1.042, 1.09, TOP25_ROI+ 1, 1.06]



# start balance as base (just 40% liquid)
# 2 BAR CHARTS, bar chart of entire salary deposited, bar chart of each bar * return vector