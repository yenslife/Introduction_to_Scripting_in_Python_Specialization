import matplotlib.pyplot as plt

import pygal

bar = pygal.Bar()(1, 3, 3, 7)(1, 6, 6, 4)
bar.render_in_browser()
bar.render_to_file('test.sgv')

