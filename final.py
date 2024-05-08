


"""
Name: Connor L'Heureux
CS230: Section 04
Data: London Pubs
URL: ADD LINK HERE

Description:

This program fist desiphers the specific types of establishments amoungst the dataset. In this case whether the pub is within an Inn, Hotel, Club, or is just a Pub. Using this data a pie chart is created based on selections made by the user. Alongwith this a bar chart totaling every establishment is made. After that a map is shown showing the single location chosen, a scatterplot is also made for all the multiple selections. FInally using a slider the user selects a postcode for the data to be displayed.
"""

import streamlit as st
import pandas as pd
from streamlit.logger import get_logger
import matplotlib.pyplot as plt
import pydeck as pdk

default_establishment_type = ["Pub", "Hotel", "Inn", "Club"] #these are the main establishment types within this pub data, had to be handfound.

default_local_authority = ["Oxford", "London", "Enfield"] #some defaults- just for the use of some of my runctions
def read_my_data(): #here this will read my data, and open it for the other functions thos os ised multiple times
    return pd.read_csv("open_pubs_10000_sample.csv").set_index("fsa_id")

# [DA1] Cleaning or manipulating data Remove rows with missing values in a specific column, this was my form of cleaning
def clean_data(data):
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
    data.dropna(subset=['postcode'], inplace=True)
    return data #cleaning the data by removing data that is missing a postcoed number, in this application all should have one b/c its location based

# [DA2] Sorting data in ascending or descending order HERE Sort data by postcode in ascending order
def sort_data(data):
    return data.sort_values('postcode', ascending=True)

# filter the data, use the variables that will be inputs in streamlit #this is [DA4]
def filter_data(sel_local_authority): #set default values here #CHANGE TO ONE IS NOT DEFUALT #this is PY[3]it is called multiple times
    df= read_my_data()
    df=df.loc[df['local_authority'].isin(sel_local_authority)] #filter here
    #edit this max easting
    return(df)

# Function to filter data based on establishment type #THIS IS MY [PY1] - two parameters, one has a default value
def filter_data_by_establishment(df, establishment_type="Inn"):
    filtered_df = df[df['name'].str.contains(establishment_type, case=False)] #here finding if the name of the location has pub, inn, hotel, this identifys more specifics
    return filtered_df #return the value

def filter_data_by_postcode(data, postcode): #here i will filter my data for the postcode
    postcode_filter = data[data['postcode'] == postcode]
    return postcode_filter

def find_location_frequency(df, sel_loc): #[DA7]#here use the data or df, then the sel loc is the multibox select
    filtered_data = df[df['local_authority'].isin(sel_loc)] #this will start the filtering in the df
    location_frequenchy = filtered_data['local_authority'].value_counts() #this will count the frequency at each location
    return location_frequenchy #return it

def create_location_frequency_bar_chart(location_frequency): #this is used to create my barchart

    plt.figure(figsize=(8, 6))  # sizing

    plt.title('Number of open spots at Locations') #my title
    plt.xlabel('Authority Location') #label here
    plt.xticks(rotation= 45) #this is for appearance
    plt.ylabel('Frequency') #label

    location_frequency.plot(kind='bar') #defines it as bar

    st.pyplot(plt)

def min_max_long_lat(data): #here this is for my min and max on my sliders for long and lat
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce') #coerce sets it to NaN so it will pass through
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    min_latitude = data['latitude'].min() #simple my math calculations
    min_longitude = data['longitude'].min()
    max_latitude = data['latitude'].max()
    max_longitude = data['longitude'].max()

    return min_latitude, max_latitude, min_longitude, max_longitude #return all the variables here for further use


def pie_chart(data): #create a pi chart using the df #referenced the video on brightspace for this
    count_esta = data['name'].str.split().str[-1].str.strip().value_counts() #count the frequency of the selected establishment, these are inn, pub, bar, club...
    count_esta = count_esta[count_esta.index.isin(default_establishment_type)] #it ill count it here if correct

    chart, axis = plt.subplots() #start the pie chart here
    axis.set_title('Pie chart of % of Establishment Types in locations')
    axis.pie(count_esta, labels=count_esta.index, autopct='%1.2f%%') #the index is the names of the types of establishments here #round to 2 decimals
    axis.axis('equal') #this makes the plot a circle for the pie chart so it looks smooth
    axis.set_title('Establishment Types')

    st.pyplot(chart)



def make_map(df): #referenced the video for this, also made some changes myself
    # Filter the DataFrame to include only the relevant columns
    df_map = df[['name', 'latitude', 'longitude']]

    # Convert latitude and longitude columns to numeric, dropping rows with missing values #clean data here also
    df_map['latitude'] = pd.to_numeric(df_map['latitude'], errors='coerce')
    df_map['longitude'] = pd.to_numeric(df_map['longitude'], errors='coerce')
    df_map = df_map.dropna(subset=['latitude', 'longitude'])

    view_state = pdk.ViewState(latitude=df_map['latitude'].mean(),longitude=df_map['longitude'].mean(),zoom=12) #referenced from video

    layer = pdk.Layer(type='ScatterplotLayer',data=df_map,get_position='[longitude, latitude]',get_radius=100,get_fill_color=[255, 0, 0],  # Red color for markers
    ) #referenced from video


    map = pdk.Deck(tooltip={"html": "<b>{name}</b>", "style": {"color": "white", "backgroundColor": "darkblue"}}, layers=[layer],
        initial_view_state=view_state,
    ) #referenced from video

    return map

def make_scatterplot(df):
    df_map = df[['name', 'latitude', 'longitude', 'postcode']].copy()
    df_map['latitude'] = pd.to_numeric(df_map['latitude'], errors='coerce') #clean the data here, g
    df_map['longitude'] = pd.to_numeric(df_map['longitude'], errors='coerce') #clean the data here
    df_map = df_map.dropna(subset=['latitude', 'longitude']) #cleans the data further for use

    plt.figure(figsize=(10, 6)) #sizing for the chart
    plt.scatter(df_map['longitude'], df_map['latitude'], alpha=0.5) #identify that its a scatterplot, then alter it for the long and lat
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Scatter Plot of Postcodes') #^^^ titles
    plt.grid(True) #allow it to work
    st.pyplot(plt)


def all_local_authority(): #[py4] #referenced the video for this but adjusted code for my data
    df = read_my_data()
    lst = []
    for ind, row in df.iterrows(): #this allows it to be added #[DA8]
        if row['local_authority'] not in lst:
            lst.append(row['local_authority'])
    return lst #this will give me a list of all my local)authority names, I further use this in the multi select box

def all_postcodes():
    df = read_my_data()
    return df['postcode'].unique().tolist() #make a list of all postcodes


def display_postcode_data(data, postcode):
    data = filter_data_by_postcode(data, postcode) #filter the data first
    st.markdown(f"**Below is the specific data for the postcode selected {postcode}:**")
    st.table(data.sort_values('postcode', ascending=True)) #this will sore the items in ascending order

def main():
    data= clean_data(read_my_data())
    st.write("<h1 style='font-family: Arial, sans-serif; color: blue;'>Data Visualization with Python</h1>", unsafe_allow_html=True) #using html allowing to change font and color
    st.image('pub.jpg', caption='Here is a typical London Pub', use_column_width=True)
    st.markdown("<h3 style='text-align: center;'>Welcome to this London Open Pubs data. Open the sidebar to begin your customization</h3>", unsafe_allow_html=True) #this is using HTML 5 to center, I took CS213 - last semester and found that I can apply it to python streamlit.
    #Above are my headings and images

#BELOW IS SIDEBAR
    st.sidebar.markdown("<span style= 'color:red'>Please choose options on all of these to filter each section of data.</span>", unsafe_allow_html=True)
    st.sidebar.image('maplondon.jpg', caption='Map of London', use_column_width=True)
    st.write("")#format
    chosen_authorities = st.sidebar.multiselect("Select muliple local authoritys, for a pie chart that will display establishment percentages: ", all_local_authority()) #this is my [ST 1]
    st.write("")  # format
    st.write("")  # format
    local_authority = st.sidebar.selectbox("Select a local authority type for the map: ", all_local_authority()) #this is my [ST2]
    st.write("")  # format
    st.write("")  # format
    postcodes = all_postcodes()
    choice_postcode = st.sidebar.select_slider("Slide to select a postcode all of the other information that goes with the postcode will be displayed", options=postcodes)

    data_scatter = filter_data(chosen_authorities)

#BELOW will begin my charting codes,
    st.write("")  # format
    st.write("<span style= 'color:blue'>Below is a pie chart showing the distribution of establishment types in the multi-select box of local authorities:</span>", unsafe_allow_html=True)
    st.write("") #format
    filtered_data_local_authority = data[data['local_authority'].isin(chosen_authorities)] #validate this data here



    pie_chart(filtered_data_local_authority) #[VIZ 1] #function to output


    st.write("")  # format
    st.markdown("**Below is a barchart of number of open places in each selected location!**")
    location_frequency = find_location_frequency(data, chosen_authorities)
    if location_frequency.empty: #did an if statement here, to validate a selection
        st.write(f"<span style='color:red'>There is no data selected for this chart, please select the data in the SideBar!</span>", unsafe_allow_html=True)

    else:
        create_location_frequency_bar_chart(location_frequency) #[VIZ4]


    filtered_data_single_authority = filter_data([local_authority])
    st.write("")  # format
    st.write("")#format
    st.markdown("**A map is shown below, this map uses the location chosen in the select box.**")
    map = make_map(filtered_data_single_authority) #[VIZ2]
    st.write(f"Map of open locations in {local_authority}") #use f-string to display the titles, it will adjust based on selection
    st.pydeck_chart(map)
    st.write("")#format
    st.write("")#format
    st.write("")#format
    st.markdown("**Below is a scatterplot showing the longitude and latitude of each open place. The points are each place in each location selected that is open**")
    make_scatterplot(data_scatter) #[VIZ3] #use function



    display_postcode_data(data, choice_postcode) #Made another visual, to explain data more to the user

if __name__ == '__main__':
    main()
LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
