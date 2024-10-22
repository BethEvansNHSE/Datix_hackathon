import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Title and description
st.title("Incident Data Visualisation Report")
st.markdown("""
This report provides various visualisations to explore the Datix data, including heatmaps and scatterplot matrices.
Use the tabs below to navigate between different visualisations.


## Data Summary
The dataset used includes details about incidents, their categories, the date & time they were reported, and the harm level.

""")


#Load in data
raw_datix_df = pd.read_csv(r"../data/1924_Total.csv")
divisions_list = raw_datix_df["Division"].drop_duplicates().sort_values().tolist()
specialities_list = raw_datix_df["Speciality"].drop_duplicates().sort_values().tolist()
# select division
divisions = st.container()
all_divisions = st.checkbox("Select all", value=True, key=1)

if all_divisions:
    selected_divisions = divisions.multiselect(
        "Select division(s)",
        raw_datix_df["Division"].drop_duplicates().sort_values().tolist(),
        raw_datix_df["Division"].drop_duplicates().sort_values().tolist()
    )
else:
    selected_divisions = divisions.multiselect(
        "Select division(s)",
        raw_datix_df["Division"].drop_duplicates().sort_values().tolist()
    )

# filter on division
edited_df = raw_datix_df[raw_datix_df["Division"].isin(selected_divisions)]

# select specialty
specialities = st.container()
all_specialties = st.checkbox("Select all", value=True, key=2)

if all_specialties:
    selected_specialties = st.multiselect(
        "Select specialty(s)",
        edited_df["Speciality"].drop_duplicates().sort_values().tolist(),
        edited_df["Speciality"].drop_duplicates().sort_values().tolist()
    )
else:
    selected_specialties = st.multiselect(
        "Select specialty(s)",
        edited_df["Speciality"].drop_duplicates().sort_values().tolist()
    )

# filter on specialties
edited_df = raw_datix_df[raw_datix_df["Speciality"].isin(selected_specialties)]

# datix_df = raw_datix_df.copy()
datix_df = edited_df.copy()

# Get drop the non-time formats, thanks stack overflow!
datix_df['Time of Incident'] = pd.to_datetime(datix_df['Time of Incident'], errors='coerce')

datix_df = datix_df.dropna(subset=['Time of Incident'])

# get hour time rounded
datix_df['Time Rounded'] = datix_df['Time of Incident'].dt.round('H')

# Create hour of day column
datix_df['Hour of Day'] = datix_df['Time of Incident'].dt.hour

# make sure that incident date is a date format
datix_df['Incident Date'] = pd.to_datetime(datix_df['Incident Date'], format='%d/%m/%Y')

# Day of the week (Monday = 0, Sunday = 6)
datix_df['Day of Week'] = datix_df['Incident Date'].dt.day_name()

# Create tabs - ?
tab1, tab2, tab3, tab4 = st.tabs(["Incident Count by Hour", "Incident Count by Day", "Interactive Heatmap", "Static Heatmap"])

# Tab 1:
with tab1:
    st.subheader('Incident Distribution by Hour')
    st.markdown("""
    This visualisation shows the distribution of incidents by the hour of the day.
    The incidents have been rounded to the nearest hour to provide an overview of how often incidents are reported at different times.
    """)
    
    # Group hour
    incident_by_hour = datix_df.groupby(datix_df['Time Rounded'].dt.hour).size()
    
    # Plot using Plotly (interactive)
    fig = px.bar(incident_by_hour, 
                 x=incident_by_hour.index, 
                 y=incident_by_hour.values, 
                 labels={'x': 'Hour of the Day', 'y': 'Number of Incidents'},
                 title='Incident Distribution by Rounded Hour')
    
    st.plotly_chart(fig)

# Tab 2: 
with tab2:
    st.subheader('Incident Count by Day of the Week')
    st.markdown("""
    This visualisation presents the number of incidents occurring on each day of the week. 
    It provides insights into whether certain days are more prone to incidents than others.
    """)
    
    incidents_by_day = datix_df['Day of Week'].value_counts()
    fig2 = px.bar(incidents_by_day,
                x=incidents_by_day.index, 
                y=incidents_by_day.values,
                labels={'x': 'Day of the Week', 'y': 'Number of Incidents'},
                title='Incident Count by Day of the Week')
    st.plotly_chart(fig2)
    
    # plt.figure(figsize=(10, 6))
    # incidents_by_day.plot(kind='bar', color='skyblue')
    # plt.title('Incident Count by Day of the Week')
    # plt.xlabel('Day of the Week')
    # plt.ylabel('Number of Incidents')
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # st.pyplot(plt)

# Tab 3: Interactive Heatmap - Enhanced Scatter plot maybe look into? Try to find old Rcode using Corr?
with tab3:
    st.subheader('Interactive Incident Density Heatmap')
    st.markdown("""
    This interactive heatmap illustrates the density of incidents based on the hour of the day and the day of the week.
    Use this visualisation to explore how incidents are distributed across different time periods.
    """)

    heatmap_data = datix_df.pivot_table(index='Day of Week', columns='Hour of Day', aggfunc='size', fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(day_order)

    heatmap_data_long = heatmap_data.reset_index().melt(id_vars='Day of Week', var_name='Hour of Day', value_name='Incident Count')

    fig = px.imshow(
        heatmap_data, 
        labels={'x': 'Hour of the Day', 'y': 'Day of the Week', 'color': 'Incident Count'},
        x=heatmap_data.columns, 
        y=heatmap_data.index,
        color_continuous_scale='YlGnBu'
    )

    fig.update_layout(
        title='Incident Density by Hour of the Day and Day of the Week',
        xaxis_title='Hour of the Day',
        yaxis_title='Day of the Week'
    )
    
    st.plotly_chart(fig)

# Tab 4:
with tab4:
    st.subheader('Static Incident Density Heatmap')
    st.markdown("""
    This static heatmap provides an alternative view of incident density by hour of the day and day of the week. 
    It offers a clear, non-interactive view of how incidents vary over time.
    """)

    heatmap_data = datix_df.pivot_table(index='Day of Week', columns='Hour of Day', aggfunc='size', fill_value=0)
    heatmap_data = heatmap_data.reindex(day_order)

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5, annot=True, fmt='g')  # 'fmt="g"' ensures no scientific notation
    plt.title('Incident Density by Hour of the Day and Day of the Week')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.tight_layout()
    
    st.pyplot(plt)
