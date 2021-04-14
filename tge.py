import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime as dt
import seaborn as sns


st.sidebar.markdown("## HEDCOR")
file = st.sidebar.file_uploader("Choose CSV file", type="csv")


def main():
    st.markdown("## Turbine-Generator Efficiency")

    option = st.sidebar.selectbox(
        "Option", ('Dashboard', 'Individual Test'))

    if option == 'Dashboard':
        dashboard_view()

    if option == 'Individual Test':
        st.title(option)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(
        f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')


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
        width=900
    )

    st.write(fig)


def scatterplot_discharge_power(dt):

    dt['DateTime'] = pd.to_datetime(dt['DateTime'])

    dt = dt.sort_values(by=['DateTime'])

    dt = dt[["Discharge", "Power Output", "Month", "Efficiency"]
            ].reset_index(drop=True)

    dt = dt[(dt['Efficiency'] > 0)]

    fig = px.scatter(dt,
                     x="Power Output",
                     y="Discharge",
                     color="Month"
                     )
    fig.update_layout(
        xaxis_title="Power Output",
        yaxis_title="Discharge",
        width=900
    )

    st.write(fig)


def scatterplot_efficiency_power(dt):

    dt['DateTime'] = pd.to_datetime(dt['DateTime'])

    dt = dt.sort_values(by=['DateTime'])

    dt = dt[["Discharge", "Power Output", "Month", "Efficiency"]
            ].reset_index(drop=True)

    dt = dt[(dt['Efficiency'] > 0)]

    fig = px.scatter(dt,
                     x="Power Output",
                     y="Efficiency",
                     color="Month"
                     )
    fig.update_layout(
        xaxis_title="Power Output",
        yaxis_title="Efficiency",
        width=900
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

    st.sidebar.markdown('#### Filter data')
    if file is not None:
        data = load_data()

        PLANT = data['Plant'].unique()
        UNIT = data['Unit'].unique()

        PLANT_SELECTED = st.sidebar.selectbox('Select plant', PLANT)
        UNIT_SELECTED = st.sidebar.selectbox('Select Unit', UNIT)

        dt = get_selected_data(data, PLANT_SELECTED, UNIT_SELECTED)

        st.markdown('### Hourly Efficiency')
        scatterplot_efficiency_date(dt)

        st.markdown('### Discharge and Power Output')
        scatterplot_discharge_power(dt)

        st.markdown('### Efficiency and Power Output')
        scatterplot_efficiency_power(dt)

        st.markdown('### Pair Plot')
        pairplot(dt)

        st.markdown('### Correlation Plot')
        heatmap(dt)

        st.markdown('### Raw data')
        st.dataframe(dt)


if __name__ == "__main__":
    main()
