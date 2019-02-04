#import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from sge_tools import sge_qacct_parse

df = sge_qacct_parse("qacct_output.txt")

df['wait_time'] = df['qsub_time'] - df['start_time']

plt.scatter(df['slots'].values,df['ru_wallclock'].values)
plt.show()

df.plot.scatter(x='slots', y='maxvmem')
plt.show()
