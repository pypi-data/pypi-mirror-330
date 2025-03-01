import time

import pandas as pd
import xtquant.xtdata

code = 'SH,SZ'
code_list = code.split(",")
start = time.time()
data = xtquant.xtdata.get_full_tick(code_list)
end = time.time()
print(f"耗时: {end - start:.4f} 秒")
df = pd.DataFrame(data)
print(df['600600.SH'])
