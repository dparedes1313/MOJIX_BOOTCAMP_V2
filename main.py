import streamlit as st
import pandas as pd
import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns

# st.title("CSV READER")
# file = st.file_uploader("Upload a CSV", type="csv")
# if file:
#     df = pd.read_csv(file)
#     st.dataframe(df)
#     st.markdown("---")
#     fig1 = plt.figure(figsize-(10,4))
#     sns.countplot(x='Pclass', data=df)
#     st.pyplot(fig1)
    
#     fig2 = plt.figure(figsize-(10,4))
#     sns.boxplot('Pclass', y='Age', data=df)
#     st.pyplot(fig2)
    

st.title('Comparison Between Countries on Covid-19 Evolution')
st.write('This is a web app that allows you to compare covid-19 evolution between countries.')
st.write('Enjoy!')


st.write("Data in the following link! ;) [link](https://ourworldindata.org/epi-curve-covid-19)")

covid = pd.read_csv("owid-covid-data.csv")
covid = covid[['location', 'iso_code', 'date', 'new_cases']]

covid.columns = ['Country', 'Code', 'Date', 'Confirmed']
st.write(covid)

country_options = covid['Country'].unique().tolist()
date_options = covid['Date'].unique().tolist()
date = st.selectbox('Which date would you like to explore?', date_options, 100)
country = st.multiselect("Which country would you like to compare?", country_options, ['Bolivia', 'Chile', 'Peru'])

covid = covid[covid['Country'].isin(country)]

st.write("Click Play!")

fig2 = px.bar(covid, x='Country', y='Confirmed', color='Country', range_y=[0,35000], 
                animation_frame='Date', animation_group='Country')

fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1
fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 1

fig2.update_layout(width=800)

st.write(fig2)
