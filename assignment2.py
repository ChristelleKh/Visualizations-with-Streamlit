import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go
import streamlit as st

st.title('Educational Levels and Resources in Lebanon \:school::book:')

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image('C:/Users/User/Desktop/governorates-districts-of-lebanon.jpg')

@st.cache_data
def load_resources_data(nrows):
    df_edresources = pd.read_csv("https://linked.aub.edu.lb/pkgcube/data/766496d731ca34aa96a88c60f595617f_20240906_113458.csv", nrows=nrows)
    return df_edresources

@st.cache_data
def load_edlevel_data(nrows):
    df_edlevel = pd.read_csv("https://linked.aub.edu.lb/pkgcube/data/279c578864d266a6820b7739ab63c219_20240906_105551.csv", nrows=nrows)
    return df_edlevel

edleveldata_load_state = st.text('Loading educational level data...')
edleveldata = load_edlevel_data(10000)
edleveldata_load_state.text("Done! (using st.cache_data)")

resourcesdata_load_state = st.text('Loading educational resources data...')
resourcesdata = load_resources_data(10000)
resourcesdata_load_state.text("Done! (using st.cache_data)")


if st.checkbox('Show raw educational resources data'):
    st.subheader('Raw educational resources data')
    st.write(resourcesdata)

if st.checkbox('Show raw educational level data'):
    st.subheader('Raw educational level data')
    st.write(edleveldata)

#extract area from http link in refArea column in the dataframe df_edlevel and df_edresources
edleveldata['refArea'] = edleveldata['refArea'].apply(lambda x: x.split('/')[-1])
resourcesdata['refArea'] = resourcesdata['refArea'].apply(lambda x: x.split('/')[-1])

st.divider()
st.header('Data Analysis Graphs \:bar_chart:')
st.divider()

st.subheader('Distribution of Lebanese & Private Universities by area')
# Group by 'refArea' and sum the number of 'Lebanese university branches'
df_lebanese_universities = resourcesdata.groupby('refArea')['Nb of universities by type - Lebanese University branches'].sum().reset_index()

# Group by 'refArea' and sum the number of 'Private universities'
df_private_universities = resourcesdata.groupby('refArea')['Nb of universities by type - Private universities'].sum().reset_index()

# Create a histogram figure
fig = go.Figure()

if st.button('Show Lebanese University Branches Distribution'):

    # Add trace for Lebanese University branches
    fig.add_trace(go.Histogram(
        x=df_lebanese_universities['refArea'],
        y=df_lebanese_universities['Nb of universities by type - Lebanese University branches'],
        name='Lebanese University Branches',
        histfunc='sum', #how data is aggregated for each bin: adding values of the number of lebanese universities in each town
        marker_color='blue',
        opacity=0.7
    ))

    fig.update_layout(
        title='Distribution of Lebanese University Branches Across Areas',
        xaxis_title='Area',
        yaxis_title='Number of Lebanese University Branches',
        bargap=0.2,  # Gap between bars
        width=800,
        height=600
    )

if st.button('Show Private Universities Distribution'):
    # Add trace for Private universities
    fig.add_trace(go.Histogram(
        x=df_private_universities['refArea'],
        y=df_private_universities['Nb of universities by type - Private universities'],
        name='Private Universities',
        histfunc='sum',
        marker_color='orange',
        opacity=0.7 
    ))

    fig.update_layout(
        title='Distribution of Private Universities Across Areas',
        xaxis_title='Area',
        yaxis_title='Number of Private Universities',
        width=800,
        height=600
    )

if st.button('Show Both Universities Distribution'):
    # Add trace for Lebanese University branches
    fig.add_trace(go.Histogram(
        x=df_lebanese_universities['refArea'],
        y=df_lebanese_universities['Nb of universities by type - Lebanese University branches'],
        name='Lebanese University Branches',
        histfunc='sum', #how data is aggregated for each bin: adding values of the number of lebanese universities in each town
        marker_color='blue',
        opacity=0.7
    ))
    # Add trace for Private universities
    fig.add_trace(go.Histogram(
        x=df_private_universities['refArea'],
        y=df_private_universities['Nb of universities by type - Private universities'],
        name='Private Universities',
        histfunc='sum',
        marker_color='orange',
        opacity=0.7 
    ))
    # Update layout for better readability
    fig.update_layout(
        title='Distribution of Universities Across Areas',
        xaxis_title='Area',
        yaxis_title='Number of Universities',
        bargap=0.2,  # Gap between bars
        barmode='relative',  # to overlay both histograms
        width=800,
        height=600
    )

fig
st.markdown('''This histogram overlays the distribution of Lebanese University branches and private universities across the various areas in Lebanon.  
            It helps compare the availability of public versus private universities in different regions. The difference in numbers may reflect a disparity in access to public or private education.  
            It further highlights the areas with fewer or no public universities that should benefit from the expansion of public higher education facilities.
''')

st.divider()

st.subheader('Relationship between school dropout rates and illiteracy percentages across different towns')

options=['All']
for i in edleveldata['refArea']:
    options.append(i)

selectedarea= st.selectbox('Display by Area',options)
if (selectedarea=='All'):
    fig = px.scatter(edleveldata, 
                 x='PercentageofSchooldropout', 
                 y='PercentageofEducationlevelofresidents-illeterate', 
                 color='refArea',  # Color points by town for differentiation
                 hover_name = 'Town', # Get name of town when hovering the cursor over a point
                 title='Scatter Plot of School Dropout vs Illiteracy Percentage by Town',
                 labels= { 'PercentageofSchooldropout ': 'Percentage of School dropout', 
                            'PercentageofEducationlevelofresidents-illeterate':'Percentage of Illiteracy'})

    # Show the plot
    fig.update_layout(width=1000, height=600)
else:
    filtered_data = edleveldata[edleveldata['refArea'] == selectedarea]
    st.subheader(f'Percentage of Illiteracy vs School dropout in {selectedarea}')
    fig = px.scatter(filtered_data, 
                 x='PercentageofSchooldropout', 
                 y='PercentageofEducationlevelofresidents-illeterate', 
                 hover_name = 'Town', # Get name of town when hovering the cursor over a point
                 title='Scatter Plot of School Dropout vs Illiteracy Percentage by Town',
                 labels= { 'PercentageofSchooldropout ': 'Percentage of School dropout', 
                            'PercentageofEducationlevelofresidents-illeterate':'Percentage of Illiteracy'})

# Show the plot
    fig.update_layout(width=1000, height=600)

fig

st.markdown('''This scatter plot shows the relationship between school dropout rates and illiteracy percentages across different towns. Towns with lower percentage of school dropout have lower percentage of illiteracy, suggesting that dropping out of school might be contributing to illiteracy in those towns.  
            Educational authorities can maybe focus on retention programs to reduce school dropout in towns with high dropout rates to bring illiteracy rates down.   
            :blue-background[Note:] the color coding by area helps identify if certain regions are more affected than others.
''')
