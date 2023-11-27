import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff



st.set_page_config(layout="wide", initial_sidebar_state='collapsed') # установка широкого расположения объектов


# Add histogram data
# x1 = np.random.randn(200) - 2
# x2 = np.random.randn(200)
# x3 = np.random.randn(200) + 2

# # Group data together
# hist_data = [x1, x2, x3]

# group_labels = ['Group 1', 'Group 2', 'Group 3']

# fig = ff.create_distplot(
#         hist_data, group_labels, bin_size=[.1, .25, .5])

# # Plot!
# st.plotly_chart(fig, use_container_width=True)



# medal_type = st.selectbox('Medal Type', [0, 1, 2])
    
# fig_2 = px.pie(hist_data, values=medal_type, names=2,
#                 title=f'number of {medal_type} medals',
#                 height=300, width=200)
# fig_2.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
# st.plotly_chart(fig_2, use_container_width=True)


df = pd.read_csv(r'J:\Самописное\Personal_projects\Obligations parser\Obligations_data_parsed_863_09.11.2023.csv').drop('Unnamed: 0', axis=1)

# df = px.data.tips()
fig = px.pie(df, names='Рейтинг', color='Ссылка', )
fig.show()