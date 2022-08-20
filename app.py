import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title="Inventory Discrepancy", page_icon=":bar_chart:", layout="wide")


df = pd.read_csv('inventory_discrepancy_cleaned.csv', index_col=0)



st.sidebar.header("You can filter here:")

Category = st.sidebar.multiselect("Select the product category:",
                                   options= df['Retail_Product_Level1Name'].unique(),
                                   default= df['Retail_Product_Level1Name'].unique())


df_selection = df.query("Retail_Product_Level1Name == @Category")

st.dataframe(df_selection)

### Main Page

st.title(":bar_chart: Inventory Discrepancy")
st.markdown("##")

### TOP

total_unders = int(df_selection['unders'].sum())
average_unders = round(df_selection['unders'].mean(), 1)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Total Unders")
    st.subheader(f"{total_unders}")
with right_column:
    st.subheader("Average Unders")
    st.subheader(f"{average_unders}")

st.markdown("---")

### BAR CHARTS
unders_by_category = (df_selection.groupby(by=['Retail_Product_Level1Name']).sum()[['unders']].sort_values('unders'))

fig_category = px.bar(unders_by_category, x=unders_by_category.index, y='unders', 
                            title='Total unders per category', template = 'plotly_white',
                            color_discrete_sequence=["#0083b8"] * len(unders_by_category))

fig_category.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))



unders_by_product_name = df_selection.groupby(by=['Retail_Product_Name']).sum()[['unders']].nlargest(30, ['unders']).sort_values('unders', ascending=True)

fig_product_name = px.bar(unders_by_product_name, x='unders', y=unders_by_product_name.index, 
                            orientation='h', title='Top 30 Products', template = 'plotly_white',
                            color_discrete_sequence=["#0083b8"] * len(unders_by_category))

fig_product_name.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_category, use_container_width=True)
right_column.plotly_chart(fig_product_name, use_container_width=True)


# HIDE STREAMLIT STYLE
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
