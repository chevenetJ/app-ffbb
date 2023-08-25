import streamlit as st
import requests
import streamlit.components.v1 as components
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.set_page_config(page_title="Projet FFBB", initial_sidebar_state="collapsed")

class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=300)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


pres = st.expander("Présentation du projet")
with pres :
    st.write("""### Objectifs
J'ai réalisé ce projet en vue la Coupe du Monde de Basket 2023, avec la volonté de promouvoir l'équipe de France.
J'ai depuis toujours été fasciné par le basket et les bleus m'ont fait vivre des émotions splendides dans la victoire comme dans la défaite.
Je pense que l'équipe de France a une histoire splendide et que trop peu de personnes en sont informées, mon but est donc d'aider à raconter cette histoire avec mes moyens.

### Autres réalisations
Dans cette optique, j'ai déjà produit des contenus associés à l'équipe de France. En premier lieu, j'ai entrepris une série de vidéo (inachevée) pour narrer les exploits du basket depuis les années 2000, puis j'ai ouvert un compte Twitter pour utiliser un format textuel, plus simple a réaliser.""")
    
    st.write('Playlist Youtube : ')

    st.markdown("""<iframe width="560" height="315" src="https://www.youtube.com/embed/_LelsH9W8Ko?si=uiLjIjxxjSoyU8rK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>""", unsafe_allow_html  = True)
    
    st.write('')
    st.write('Tweet EDF :')

    Tweet("https://twitter.com/sombrevech/status/1662408732569903105").component()

data = st.expander('Un projet Open Data')
with data:
    st.write("""### Trouver les données
Toutes les données des matchs proviennent du site de la FFBB, mais mes connaissances en Data Science m'ont permis de les exploiter d'une manière plus pertinente.
Elles sont disponibles pour tous sur le GitHub du projet et sont actualisées a chaque nouveau match de l'équipe de France.""")
    st.write('')
    url = "https://github.com/chevenetJ/app-ffbb/tree/main/data"
    st.markdown("lien vers les données : (%s)" % url)
    ##st.write("### Schémas de données")

cont = st.expander("Me contacter")
with cont :
    st.write("""### Participer au projet""")
    st.write("""Si vous souhaitez m'aider à perpétuer et améliorer le projet, c'est avec grand plaisir !
             Selon moi, toute personne peut apporter, par des compétences de programmation, de design ou par simple envie d'aider.
             N'hésitez pas à me contacter via Twitter ou par mail, j'an serai très heureux car ce projet me tient à coeur et je compte le pousser le plus loin possible""")
    st.write("""### Envoyer un mail""")
    txt = st.text_area('Contenu du mail : ', '''
    ''')
    subject = "Projet FFBB"
    body = txt
    sender_email = "jules.chevenet.pro@gmail.com"
    receiver_email = "jules.chevenet.pro@gmail.com"
    password = st.secrets["gmail_password"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    go = st.button("envoyer le mail")
    if go :
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        st.balloons()
    st.write("Ou envoyez un mail personnel à l'adresse jules.chevenet.pro@gmail.com")