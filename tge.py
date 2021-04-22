import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime as dt
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
from comm_data import *



img_logo = Image.open('hedcor-logo.png')
st.sidebar.image(img_logo, width=200)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{style.css}" rel="stylesheet">',
                unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(
        f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

st.markdown("## Turbine-Generator Efficiency")
    
with st.beta_expander("Upload Data"):
    file = st.file_uploader("Choose CSV file", type="csv")


def main():
    
  
    dashboard_view()

  
@st.cache
def load_data():
    if file is not None:
        data = pd.read_csv(file)
        def dtm(x): return dt.strptime(str(x), '%d/%m/%Y %H:%M')

        # data['Date'] = pd.to_datetime(data['Date'])
        data["DateTime"] = data["DateTime"].apply(dtm)
        return data


def get_selected_data(dt, plant, unit):

    df = dt[(dt["Plant"] == plant)
            & (dt["Unit"] == unit)]

    data = df[(df['Efficiency'] > 0)].reset_index(drop=True)

    return data


def scatterplot_efficiency_date(dt):

    dt['DateTime'] = pd.to_datetime(dt['DateTime'])

    dt = dt.sort_values(by=['DateTime'])

    dt = dt[["DateTime", "Efficiency", "Period"]].reset_index(drop=True)

    dt = dt[(dt['Efficiency'] > 0)]

    fig = px.scatter(dt,
                     x="DateTime",
                     y="Efficiency",
                     color="Period"
                     )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Turbine-Generator Efficiency",
        width=912
    )

    st.write(fig)


def scatterplot_discharge_power(dt):

    dt['DateTime'] = pd.to_datetime(dt['DateTime'])

    dt = dt.sort_values(by=['DateTime'])

    dt = dt[["Discharge", "Power Output", "Month", "Efficiency"]
            ].reset_index(drop=True)

    dt = dt[(dt['Efficiency'] > 0)]
    
    fig = go.Figure()
    
    fig = px.scatter(dt,
                     x="Power Output",
                     y="Discharge",
                     color="Month"
                     )
    
    fig.update_layout(
        xaxis_title="Power Output",
        yaxis_title="Discharge",
        width=912
    )

    st.write(fig)


def scatterplot_efficiency_power(dt, com, eff):

    dt['DateTime'] = pd.to_datetime(dt['DateTime'])

    dt = dt.sort_values(by=['DateTime'])
    
    dt = dt[["Discharge", "Power Output", "Month", "Efficiency"]
            ].reset_index(drop=True)

    dt = dt[(dt['Efficiency'] > 0)]

    dt_com = com
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
                     x=dt["Power Output"],
                     y=dt["Efficiency"],
                     name="Actual Data",
                     mode='markers',
                     marker_color='lightskyblue',
                     marker_size=8,
                     marker_line_width=1
                     ))
    
    
    fig.add_trace(go.Scatter(
                     x=dt_com["Power Output"],
                     y=dt_com[eff],
                     name="Commission Data",
                     mode='markers',
                     marker_symbol='x-dot',
                     marker_color='rgba(152, 0, 0, .8)',
                     marker_size=10,
                     marker_line_width=2
                     ))
    
    fig.update_traces(mode='markers')
    fig.update_layout(xaxis_title="Power Output",
                      yaxis_zeroline=False, xaxis_zeroline=False,
                      width=912
                  
    )

    st.write(fig)


def pairplot(dt):
    dt = dt[["Discharge", "Velocity", "Pressure Head",
             "Net Head", "Theoretical Power", "Power Output", "Efficiency", "Period"]].reset_index(drop=True)
    fig = sns.pairplot(dt, hue="Period")
    st.pyplot(fig)


def heatmap(dt):
    dt = dt[["Discharge", "Velocity", "Pressure Head",
             "Net Head", "Theoretical Power", "Power Output", "Efficiency"]].reset_index(drop=True)

    corr = dt.corr()

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots()

    cmap = sns.diverging_palette(230, 10, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap,  center=0, annot=True,
                square=False, linewidths=.5, cbar_kws={"shrink": .5})

    st.write(fig)


def dashboard_view():

    st.sidebar.markdown('#### Filter Data')
    if file is not None:
        
        data = load_data()

        PLANT = data['Plant'].unique()
        UNIT = data['Unit'].unique()

        PLANT_SELECTED = st.sidebar.selectbox('Select plant', PLANT)
        UNIT_SELECTED = st.sidebar.selectbox('Select Unit', UNIT)
        
         
        if UNIT_SELECTED == "Unit 1":    
          unt = df_comm_unit_1
          unt = df_comm_unit_1[(df_comm_unit_1["Plant"]== PLANT_SELECTED)]
        else:
          unt = df_comm_unit_2
          unt = df_comm_unit_2[(df_comm_unit_1["Plant"]== PLANT_SELECTED)]
        
        dt = get_selected_data(data, PLANT_SELECTED, UNIT_SELECTED)

        st.markdown('### Efficiency and Power Output')
        option_eff = st.selectbox('Select Type of Efficiency',('Turbine Guaranted Eff.', 'Generator Guaranted Eff.', 'Overall Eff.'))
        scatterplot_efficiency_power(dt, unt, option_eff)
        
        st.markdown('### Discharge and Power Output')
        scatterplot_discharge_power(dt)
        
        st.markdown('### Hourly Efficiency')
        scatterplot_efficiency_date(dt)

        # st.markdown('### Pair Plot')
        # pairplot(dt)

        # st.markdown('### Correlation Plot')
        # heatmap(dt)

        st.markdown('### Raw data')
        st.dataframe(dt)
        
        st.markdown('### Tubine - Generator Commissioning Result')
        st.dataframe(unt)
 


if __name__ == "__main__":
    main()
