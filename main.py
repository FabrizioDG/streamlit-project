import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title = "My streamlit project",
    page_icon = "👺",
    layout = "wide"

)
datos = pd.read_csv("data/red_recarga_acceso_publico_2021.csv", sep=";")

col1, col2, col3 = st.columns([1,5,1])
with col2:
    st.image("https://es.web.img3.acsta.net/r_654_368/img/f7/e9/f7e9d8a138b31502ee19b7e09b747a94.jpg")
    st.markdown("<h1 style='text-align: center; color: black;'>Kimetsu no Yaiba</h1>", unsafe_allow_html=True)
    #st.title()

uploaded_file = st.sidebar.file_uploader("Upload your csv file", type=["csv"])
#OSS pandas funziona anche con un file direttamente e non con la string di dove sta il file
if uploaded_file is not None:
    try:
        datos = pd.read_csv(uploaded_file)
    except:
        st.write("error")

option = st.sidebar.selectbox("Select the view", ("Home", "Visualization", "Map", "Filters"))


st.sidebar.write(option)


#with st.sidebar:
#    option = st.selectbox("Select the view", ("Home", "Visualization", "Map"))
#    st.write(option)

if option=="Home":
    st.subheader("Home")

    with st.expander("App details - click to show"):
        st.write(""" This is an app to do many beutiful things""")


    #echo shows what you wrote in the code!
    with st.echo():
        #codigo para mostrar lista de numeros pares
        lista = list(range(10))
        even_list = [x for x in lista if x%2==0 and x!=0]
    st.write(even_list)
    st.write(datos)


elif option=="Map":
    st.subheader("Map")

    datos_mapa = datos[["longitud", "latidtud"]].rename({"longitud" : "lon", "latidtud" : "lat"}, axis=1)
    #datos_mapa.columns = ["lon", "lat"]
    st.map(datos_mapa)

elif option=="Visualization":
    st.subheader("Visualization")

    datos_bar = datos.groupby("DISTRITO")[["Nº CARGADORES"]].sum().reset_index()
    st.bar_chart(datos, x="DISTRITO", y="Nº CARGADORES")

elif option=="Filters":
    st.subheader("Filters")
    masks=[]
    st.sidebar.markdown(" Choose what filter you want to apply")
    filter1 = st.sidebar.checkbox("Distrito")
    filter2 = st.sidebar.checkbox("Operador")
    filter3 = st.sidebar.checkbox("Min/Max")
    zoom = 11

    if filter1:
        filters_distrito = st.sidebar.selectbox("Select the filter on 'distrito' ", list(datos["DISTRITO"].unique()))
        st.sidebar.write(filters_distrito)
        masks.append(datos["DISTRITO"]==filters_distrito)
        zoom = 13

    if filter2:
        filters_operator = st.sidebar.selectbox("Select the filter on 'operador' ", list(datos["OPERADOR"].unique()))
        st.sidebar.write(filters_operator)
        masks.append(datos["OPERADOR"] == filters_operator)

    if filter3:
        min_chargers = datos["Nº CARGADORES"].min()
        max_chargers = datos["Nº CARGADORES"].max()
        filter_minmax = st.sidebar.select_slider("Select the filter on 'distrito' ",  list(range(min_chargers, max_chargers+1)))
        masks.append(datos["Nº CARGADORES"]==filter_minmax)

    if len(masks)!=0:
        new_datos = datos[np.logical_and.reduce(masks)]
        st.write(new_datos)
        if len(new_datos)==0:
            st.warning('The DataFrame with these filters is empty!!', icon="⚠️")
            st.stop()
        if not filter1:
            with col2:
                df = datos.groupby("DISTRITO")[["OPERADOR"]].count().reset_index()
                fig, ax = plt.subplots()
                ax.bar(df["DISTRITO"], df["OPERADOR"])
                plt.xticks(rotation=90)
                st.pyplot(fig)
        if not filter2:
            with col2:
                df = datos.groupby("OPERADOR")[["DISTRITO"]].count().reset_index()
                fig, ax = plt.subplots()
                ax.bar(df["OPERADOR"], df["DISTRITO"])
                plt.xticks(rotation=90)
                st.pyplot(fig)
        datos_mapa = new_datos[["longitud", "latidtud"]].rename({"longitud" : "lon", "latidtud" : "lat"}, axis=1)
        st.map(datos_mapa, zoom)

