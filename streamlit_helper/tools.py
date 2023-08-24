import pandas as pd
import streamlit as st
import wikipediaapi
from bs4 import BeautifulSoup as bs
import requests
import plotly.express as px

def init_data():
    pd_matchs = pd.read_csv("./data/matchs.csv", index_col=0)
    pd_players = pd.read_csv("./data/players.csv", index_col=0)
    pd_matchs_players = pd.read_csv("./data/matchs_players.csv", index_col=0)

    pd_matchs_players_score = pd_matchs_players.query("Points != 'NPJ' & Points != 'ND'").copy()
    pd_matchs_players_score.Points = pd.to_numeric(pd_matchs_players_score.Points)
    pd_matchs_players_noScore = pd_matchs_players.query("Points == 'NPJ' | Points == 'ND'").copy()

    return pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score, pd_matchs_players_noScore

def result_player(rch, pd_matchs, pd_players, pd_matchs_players, pd_matchs_players_score):
    sel = rch
    p = pd_players.query("JOUEUR == '"+sel+"'")
    mp = pd_matchs_players.query("Nom == '"+sel+"'")  #mp_i = mp.id_match
    mp = pd.merge(mp, pd_matchs, left_on = ['id_match'], right_on = ['index'], how="left").copy()
    r_mp = pd_matchs_players_score.query("Nom == '"+sel+"'")#r_mp_i = r_mp.id_match
    r_mp = pd.merge(r_mp, pd_matchs, left_on = ['id_match'], right_on = ['index'], how="left").copy()
    #m = pd_matchs.loc[mp['index']]
    #r_m = pd_matchs.loc[r_mp['index']]

    ss = r_mp.Victoire.count()
    pts = p.POINTS
    win = r_mp.query('Victoire == True').Victoire.count()
    max = r_mp.Points.max()
    wmoy = round(100 * win / ss, 1)
    pmoy = round(pts / ss, 1)

    return mp, r_mp, pts, max, pmoy, ss, win, wmoy

def data_wikipedia(rch):
    wiki_wiki = wikipediaapi.Wikipedia('Projet FFBB (jules.chevenet@gmail.com)', 'fr')
    sels = rch.split()
    sel_f = sels[0]
    for nom in sels[1:]:
        sel_f += " " + nom[0] + nom[1:].lower()
    page_py = wiki_wiki.page(sel_f)
    if page_py.exists():
        title = page_py.title
        summary = page_py.summary
        url_wiki = page_py.fullurl
        response = requests.get(url_wiki)
        html = response.content
        soup = bs(html, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = []
        for img_tag in img_tags:
            if 'src' in img_tag.attrs:
                img_url = img_tag['src']
                image_urls.append(img_url)
            #print(len(image_urls))
        i_url = "https:" + image_urls[4]
        return True, title, summary, url_wiki, i_url
    return False, None, None, None, None

def trace_data(r_mp, abs, ord):
    y = 'Points'
    hover_data = ['Genre','Infos', 'Adversaire', "Victoire"]
    labels = dict(Genre='Type de match', count="Nombre de match", max='Max points', avg='Moyenne points')

    if abs == 'Type de match':
        x = 'Genre'
        color = 'Année'
    elif abs == 'Année':
        x = abs
        color = "Genre"
    else :
        x = abs
        color = None

    if ord == 'Points':
        return px.bar(r_mp, x= x, y=y, color=color, labels=labels, hover_data = hover_data)
    elif ord == "Nombre de match":
        histfunc = 'count'
    elif ord == "Max points":
        histfunc = 'max'
    elif ord == "Moyenne points":
        histfunc = 'avg'
    
    return px.histogram(r_mp, x=x, y=y, color=color, histfunc=histfunc, labels=labels)

