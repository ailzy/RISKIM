
from talibutil import *
import pandas as pd

talib_list = TechnicalFactors.get_factors_names()

version = '0.0.1'
id_prefix = '001'
factors_num = len(talib_list)

factor_name_list = \
list(zip(['%s-%.3d' % (id_prefix, i) for i in range(factors_num)],
         talib_list, 
         [version for i in range(factors_num)]))

pdf = pd.DataFrame(factor_name_list, columns=['factor_id', 'factor_name', 'version'])

pdf.to_csv('techname.csv')
