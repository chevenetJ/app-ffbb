import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_helper.tools import init_data, result_player, data_wikipedia, trace_data
from PIL import Image
from io import BytesIO
from datetime import datetime as dt

st.set_page_config(page_title="Projet FFBB", initial_sidebar_state="collapsed")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#st.session_state

pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score, pd_matchs_players_noScore = init_data()

# Barre de recherche (dépend de la recherche avancée)
def store():
    if not ('rch' not in st.session_state) :
        if st.session_state['rch'] != '':
            st.session_state['rch'] = st.session_state['rch']
        else :
            del st.session_state['rch'] 
    filter = """"""
    if not ('years' not in st.session_state) :
        if st.session_state['years'] != (1926, 2023):
            st.session_state['years'] = st.session_state['years']
            filter += "Année >= " + str(st.session_state['years'][0]) + " & Année <= " + str(st.session_state['years'][1])
        else :
            del st.session_state['years']
    if not ('tm' not in st.session_state) :
        if st.session_state['tm'] != []:        
            st.session_state['tm'] = st.session_state['tm']
            if len(filter) > 0 :
                filter += ' & '
            for type in st.session_state['tm']:
                if type != st.session_state['tm'][0]:
                    filter += ' & '
                filter += 'Genre == "' + type + '"'
        else :
            del st.session_state['tm']
    if not ('adv' not in st.session_state) :
        if st.session_state['adv'] != []:        
            st.session_state['adv'] = st.session_state['adv']
            if len(filter) > 0 :
                filter += ' & '
            for advs in st.session_state['adv']:
                if advs != st.session_state['adv'][0]:
                    filter += ' & '
                filter += "Adversaire == '" + advs + "'"
        else :
            del st.session_state['adv']
    if not ('place' not in st.session_state) :
        if st.session_state['place'] != []:        
            st.session_state['place'] = st.session_state['place']
            if len(filter) > 0 :
                filter += ' & '
            for places in st.session_state['place']:
                if places != st.session_state['place'][0]:
                    filter += ' & '
                filter += "Lieu == '" + places + "'"
        else :
            del st.session_state['place']
        
    #st.write((filter))
    #[filter]
    #st.write(len(filter))

    if len(filter)>0:
        L = list(pd_matchs.query(filter)["index"])
        id_filter = "id_match in ("
        for id in L :
            id_filter += "'"+id+"', "
        id_filter += ")"
        L_jr = list(pd_matchs_players.query(id_filter).Nom.unique())
    else :
        L_jr =  list(pd_players.JOUEUR.values)
            
    
    rch = st.selectbox("Recherche", options = [''] + L_jr, help="Cherchez un joueur de l'équipe de France de Basket", key='rch')#, placeholder = "Chercher un joueur")
    return rch

def reset_filter():
    if not ('rch' not in st.session_state) :
        if st.session_state['rch'] != '':
            st.session_state['rch'] = st.session_state['rch']
        else :
            del st.session_state['rch'] 
    if not ('years' not in st.session_state) :
        del st.session_state['years']
    if not ('tm' not in st.session_state) :
        del st.session_state['tm']
    if not ('adv' not in st.session_state) :
        del st.session_state['adv']
    if not ('place' not in st.session_state) :
        del st.session_state['place']   

rch = store()

# Barre de recherche avancée
rch_adv = st.expander("Recherche avancée")
with rch_adv:

    RA_c1, RA_c2 = st.columns([1,2])
    with RA_c1 :
        type = st.radio('Type de la recherche :', ['Année', 'Type de match', 'Adversaire',"Lieu"], help="Utilisez ce menu pour filtrer la liste des joueurs", disabled=False) 

    with RA_c2 :

        if type == 'Année' :
            years = st.slider('Année :',
                              pd_matchs.Année.unique().tolist()[0], 
                              pd_matchs.Année.unique().tolist()[-1], 
                              value=(pd_matchs.Année.unique().tolist()[0],pd_matchs.Année.unique().tolist()[-1]),
                              key="years")
            
        if type == "Type de match" :
            adv = st.multiselect(
                'Type de match',
                 pd_matchs.Genre.unique(),
                [], key = "tm")

        if type == "Adversaire" :
            adv = st.multiselect(
                'Adversaire',
                 pd_matchs.Adversaire.unique(),
                [], key = "adv")
            
        if type == "Lieu" :
            adv = st.multiselect(
                'Lieu',
                 pd_matchs.Lieu.unique(),
                [], key = "place")
            
        
    RAB_c1, RAB_c2 = st.columns([1,2])

    with RAB_c2 :
        RAC_c1, RAC_c2, RAC_c3, RAC_c4 = st.columns(4)

        if not ('years' not in st.session_state) :
            if st.session_state['years'] != (1926, 2023):
                with RAC_c1:
                    st.write('Année :',st.session_state["years"])
        if not ('tm' not in st.session_state) :
            if st.session_state['tm'] != []:
                with RAC_c2:
                    st.write("Type :", st.session_state["tm"])
        if not ('adv' not in st.session_state) :
            if st.session_state['adv'] != []:
                with RAC_c3:
                    st.write('Adversaire :', st.session_state["adv"])
        if not ('place' not in st.session_state) :
            if st.session_state['place'] != []:
                with RAC_c4:
                    st.write('Lieu :', st.session_state["place"])

    with RAB_c1 :
        st.write('Nombre de joueurs :')
        st.write(str())
        st.button('Effacer les filtres', on_click=reset_filter)

# Visualisation des data
viz = st.container()

with viz :

    if rch :
        mp, r_mp, pts, max, pmoy, ss, win, wmoy = result_player(rch, pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score)


        C1, e, C2 = st.columns([4, 1, 4])

        with C1 :
            is_wiki, title, summary, url_wiki, i_url = data_wikipedia(rch)

            if is_wiki:
                st.header(title, help = "Cette fonctionnalitée est encore en cours de développement et dépend de wikipédia, ce qui peut ammener des problèmes d'image ou de texte")
                st.image(i_url)
                st.caption(url_wiki)
                st.text_area('Résumé :', summary, height = 250)

            else :
                st.header(rch)
                st.write("")
                st.write("")
                st.warning('Pas de page wikipédia trouvée / existante pour ce joueur')


        with C2 :

            st.write("")

            c1, c2 = st.columns(2)
            with c1 :
                st.subheader("Premier match :")
                st.write(mp.Date.min())#,"%d-%m-%Y"
                st.write("")
                st.write("")
                st.metric('Matchs joués', ss)
                st.metric('Matchs gagnés', win)
                st.metric('% Victoire', wmoy)
            with c2 :
                st.subheader("Dernier match :")
                st.write(mp.Date.max())#, "%d-%m-%Y"
                st.write("")
                st.write("")
                st.metric('Points marqués', pts)
                st.metric('Meilleure performance', max)
                st.metric('Moyenne points', pmoy)

        CD1, CD2 = st.columns([1,3])

        with CD1:
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            ord = st.radio("Axe des ordonnée : ", ["Points", "Nombre de match", 'Max points', 'Moyenne points'])

            st.write("")
            st.write("")

            abs = st.radio('Axe des abscisse : ', ['Année', 'Type de match', 'Adversaire',"Compétition"])


        with CD2:
            fig = trace_data(r_mp, abs, ord)
            st.plotly_chart(fig)

        match_details = st.expander('Détail matchs')
        with match_details :
            st.write(mp[["Infos",'Genre','Adversaire', 'Victoire', "Score vainqueur", "Score perdant", "Points", 'Club']])

        #st.scatter()
        #st.write(pd_players.query("JOUEUR == '"+joueur+"'"))
        #pd_rch = pd.merge(pd_matchs_players.query("Nom == '"+sel+"'"), pd_matchs.loc[mp_i], left_on = ['id_match'], right_on = ['Index']).copy()

        #st.write(pd_rch[["Infos",'Genre','Adversaire', 'Victoire', "Score vainqueur", "Score perdant", "Points", 'Club']])
        #st.bar_chart(r_mp,x = 'Année',y = "Points")
        
