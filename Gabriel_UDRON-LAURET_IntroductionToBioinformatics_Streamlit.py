import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(layout="wide")

df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/6adb6deb-da00-4843-8990-18b83f76b4a7', sep=';')

df_clean = df.drop(['patho_niv2', 'patho_niv3', 'dep_niv_2', 'montant_moy', 'niveau_prioritaire','tri', 'type_somme','ntop', 'n_recourant_au_poste'], axis=1)

df_clean2 = df.drop(['patho_niv2', 'patho_niv3', 'montant_moy', 'niveau_prioritaire','tri', 'type_somme','ntop'], axis=1)

df_group2 = df_clean2.groupby(['annee','patho_niv1','dep_niv_1', 'dep_niv_2']).sum().reset_index()

df_group = df_clean.groupby(['annee','patho_niv1','dep_niv_1']).sum().reset_index()



def dfyearpatho(annee, patho):
  temp = df_group[df_group['annee']==annee]
  temp = temp[temp['patho_niv1']==patho]
  return temp

def plotyearpatho(annee, patho):
  temp = dfyearpatho(annee, patho)
  fig = temp.plot(kind='bar', x='dep_niv_1', y='montant')
  return fig

def pieyearpatho(annee, patho):
  temp = dfyearpatho(annee, patho)
  x = temp['montant']
  fig = plt.pie(x, labels = temp['dep_niv_1']);
  return fig

def plotcomp(listy, patho):
  listy.sort()
  for i in range(len(listy)):
    x = dfyearpatho(listy[i], patho)
    x = x.sort_values(by = 'dep_niv_1')
    montant = x['montant'].to_numpy()
    if i == 0:
      values = montant
    else: 
      values = np.vstack((values, montant))
  groups = x['dep_niv_1']
  fig, ax = plt.subplots()
  ax.tick_params(labelrotation=45)
  for i in range(values.shape[0]):
    ax.bar(groups, values[i], bottom = np.sum(values[:i], axis = 0), label = listy[i])
  ax.legend()

def liststat(listy, patho):
  listy.sort()
  dftemp = dfyearpatho(listy[0], patho)
  groups = dftemp['dep_niv_1'].tolist()
  for j in range(len(groups)):
    st.write("\n")
    st.markdown("##### " + groups[j] + " :")
    for i in range(len(listy)):
      dftemp = dfyearpatho(listy[i], patho)
      value = "{:,}".format(int(dftemp[dftemp['dep_niv_1'] == groups[j]]['montant']))
      st.markdown("###### " + str(listy[i]) + " : " + str(value) + "€")

def totalstat(listy, patho):
  listy.sort()
  dftemp = dfyearpatho(listy[0], patho)
  groups = dftemp['dep_niv_1'].tolist()
  toto = []
  toto2 = []
  for i in range(len(listy)):
    total = 0
    #st.write("\n")
    #st.markdown("##### Total on " + str(listy[i]) + " :")
    for j in range(len(groups)):
      dftemp = dfyearpatho(listy[i], patho)
      value = int(dftemp[dftemp['dep_niv_1'] == groups[j]]['montant'])
      total = total + value
    toto2.append(total)
    total = "{:,}".format(total)
    toto.append(total)
    st.markdown("###### " + str(listy[i]) + " : " + total + "€")
  return toto2

def dfyearpatho2(annee, patho):
  temp = df_group2[df_group2['annee']==annee]
  temp = temp[temp['patho_niv1']==patho]
  return temp

def pieindetail(annee, patho, depone):
  temptest = dfyearpatho2(annee, patho)
  temp = temptest[temptest['dep_niv_1']==depone]
  x = temp['montant']
  fig = plt.pie(x, labels = temp['dep_niv_2']);
  return fig


def mainpage():
  st.title('Welcome to my Bioinformatics Project')
  st.markdown("### What is about ?")
  st.markdown("##### This project is about doing graph and statistics about how many euros spend in each pathology and where it go")
  st.markdown("### Here's the dataset that we will use to see where the money is going")
  st.markdown("##### You can download the complete dataset [here](https://www.data.gouv.fr/fr/datasets/r/6adb6deb-da00-4843-8990-18b83f76b4a7)")
  st.write(df_group)

def moneypatho():
  st.sidebar.markdown("### Analysis of the money on different pathologies")

  patho = st.sidebar.selectbox("Select a pathology",df_group.patho_niv1.unique().tolist())
  date = st.sidebar.selectbox("Select a year", df_group.annee.unique().tolist())

  st.title("Analysis of the money on different pathologies")
  st.markdown("### Selected pathology : " + patho)

  dfyp = dfyearpatho(date,patho)
  dfyp

  row1, row2 = st.columns((1,1))
  with row1:
    plotyearpatho(date, patho)
    st.pyplot()
  with row2:
    pieyearpatho(date,patho)
    st.pyplot()
    st.markdown("#### Total money spent over the year on the selected pathology")
    totalstat([date], patho)
    

  if st.checkbox('See more details'):
    row5, row6 = st.columns((1,1))
    with row5:
      st.markdown("#### Dépenses")
      pieindetail(date, patho, 'Dépenses')
      st.pyplot()
    with row6:
      st.markdown("#### Hospitalisations (tous secteurs)")
      pieindetail(date, patho, 'Hospitalisations (tous secteurs)')
      st.pyplot()
    
    row7, row8 = st.columns((1,1))
    with row7:
      st.markdown("#### Prestations en espèces")
      pieindetail(date, patho, 'Prestations en espèces')
      st.pyplot()
    with row8:
      st.markdown("#### Soins de ville")
      pieindetail(date, patho, 'Soins de ville')
      st.pyplot()


def yearcomp():
  st.sidebar.markdown("### Select multiple years to do a comparaison on the current pathology")

  patho = st.sidebar.selectbox("Select a pathology",df_group.patho_niv1.unique().tolist())
  datecomp = st.sidebar.multiselect("Select multiple date to do a comparaison",df_group.annee.unique().tolist()) 

  st.title("Select multiple years to do a comparaison on the current pathology")

  if not datecomp:
    st.markdown("### You have to select multiple years on the sidebar to see some results")
  else:
    st.markdown("### Selected pathology : " + patho)
    row3, row4 = st.columns((1,1))
    with row3:
      st.pyplot(plotcomp(datecomp, patho))
      st.markdown("#### Total money spent over the years on the selected pathology")
      toto = totalstat(datecomp, patho)
      datecomp.sort()
      plt.plot(datecomp,toto)
      st.pyplot()
    with row4:
      liststat(datecomp,patho)
  
def pathocomp():
  st.sidebar.markdown("### Select multiple pathologies to do a comparaison on the current pathology")

  patho = st.sidebar.multiselect("Select two pathologies",df_group.patho_niv1.unique().tolist())
  datecomp = st.sidebar.multiselect("Select multiple years",df_group.annee.unique().tolist()) 

  st.title("Select multiple pathologies to do a comparaison on the current pathology")

  if not datecomp:
    st.markdown("### You have to select multiple years on the sidebar to see some results")
  elif not patho:
    st.markdown("### You have to select two pathologies on the sidebar to see some results")
  elif(len(patho)>2):
    st.markdown("##### Select only two pathologies at a time")
  elif len(patho) == 1 or len(datecomp) ==  1:
    st.markdown("##### You can't select only on option in the selectbox here")
  else:
    st.markdown("### Selected pathologies : " + patho[0] + ", " + patho[1])
    row3, row4 = st.columns((1,1))
    with row3:
      st.markdown("### " + patho[0])
      st.pyplot(plotcomp(datecomp, patho[0]))
      if st.checkbox("See more details"):
        liststat(datecomp,patho[0])
      st.markdown("#### Total money spent over the years on " + patho[0])
      tt1 = totalstat(datecomp, patho[0])
      datecomp.sort()
      plt.plot(datecomp,tt1)
      st.pyplot()
    with row4:
      st.markdown("### " + patho[1])
      st.pyplot(plotcomp(datecomp, patho[1]))
      if st.checkbox("See more detaiIs"):
        liststat(datecomp,patho[1])
      st.markdown("#### Total money spent over the years on " + patho[1])
      tt2 = totalstat(datecomp, patho[1])
      datecomp.sort()
      plt.plot(datecomp,tt2)
      st.pyplot()
    plt.plot(datecomp, tt1)
    plt.plot(datecomp, tt2)
    st.pyplot()
      
      

def whoami():
  st.title("Who am I ?")
  st.markdown("### Presentation of my profile")
  st.markdown("##### My name is Gabriel UDRON-LAURET, I was born on October 23, 2001, I live in the suburbs of Paris in the 92. I am currently in M2 in major Databases and Artificial Intelligence at EFREI")
  st.markdown("### Github")
  st.markdown("##### Here's the link of my [Github](https://github.com/Gabibul) where you can find most of my creations")
  st.markdown("### LinkedIn")
  st.markdown("##### If you have a job (well paid) for me you can contact me on my [LinkedIn](https://www.linkedin.com/in/gabriel-udron-lauret-4b74b3177/)")
  st.markdown("##### Or you can scan this QR code if you don't want to use the link")
  st.image('qrlinkedin.jpg')

page_names_to_funcs = {
    "Presentation of the project": mainpage,
    "Analysis of the money on different pathologies": moneypatho,
    "Comparaison of multiple years on the current pathology": yearcomp,
    "Comparaison of multiple pathologies on multiple years":pathocomp,
    "Who am I ?":whoami,
}

st.sidebar.title("Select what you want to see/do on this project")
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 