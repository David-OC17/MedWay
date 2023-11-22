# import matplotlib.pyplot as plt

# # Assuming states is a dictionary with batchNum: value
# states = {
#     'Batch1': True,
#     'Batch2': False,
#     'Batch3': True,
#     'Batch4': False,
# }

# # Create a list of rows for the table
# table_rows = [['Batch Number', 'State']]

# for batch_num, value in states.items():
#     table_rows.append([batch_num, str(value)])

# # Create a figure and axes
# fig, ax = plt.subplots()

# # Hide axes
# ax.axis('off')

# # Create a table
# table = ax.table(cellText=table_rows, loc='center', colWidths=[0.2, 0.2])

# # Customize the table appearance (optional)
# table.auto_set_font_size(False)
# table.set_fontsize(10)
# table.scale(1.2, 1.2)

# # Save the figure as an image (e.g., PNG)
# plt.savefig('table_image.png', bbox_inches='tight', pad_inches=0.1)
# plt.show()

import plotly.graph_objects as go
import plotly.io as pio

fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ])

# Save the figure as a PNG file
pio.write_image(fig, 'table_image.png')
