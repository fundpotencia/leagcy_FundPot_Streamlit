import os
import streamlit as st
import base64


def head():
    """
    Displays the header and the logo of the application
    """
    st.set_page_config(page_title="Home", page_icon="🌍")
    with open('./utils/front.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    try:
        with open('./utils/logo_jr.png', 'rb') as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
            st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Logo file not found")
    st.markdown("<h1 style='text-align: center; font-size: 38px;'>Central de atualização de informações<br>Fundação Potência</h1>", unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>", unsafe_allow_html=True)
    st.markdown(""" <div style="text-align: center; font-size: 21px; margin: 20px;"> <strong> Seja bem vindo à central de atualização de informações do database da Fundação Potência! 
                    Para atualizar os datasets, clique em um dos botões abaixo. Você será redirecionado para a página de atualização correspondente. <br>
                    <br></div>""", unsafe_allow_html=True)


def redirect():
    """
    Redirects the user to the desired page
    """
    col1, col2, col3 = st.columns(3)  # Adiciona uma terceira coluna

    # Coluna 1
    link1 = '''<p style="text-align: center;">
                <a href="https://itajrfundpot-dalunos.streamlit.app/" target="_blank">
                <input type="button" value="👨‍🎓 Opção 1" style="margin-top: 20px; border-radius: 10px; padding: 10px 20px; border: none; color: black; background-color: rgba(255, 255, 255, 0.7);">
                </a>
                </p>'''
    col1.markdown(link1, unsafe_allow_html=True)

    col1.markdown(""" <div style="text-align: center; font-size: 30px; word-wrap: break-word;"> <strong>👨‍🎓 Dataset de Alunos </div>""", unsafe_allow_html=True)

    col1.markdown(""" <div style="text-align: center; font-size: 23px; word-wrap: break-word;"> Nessa página, é possível editar o banco de dados referente à 
                algumas informações pessoais dos alunos como por exemplo: <strong> gênero, 
                LinkedIn, biografia do LinkedIn... </div>""", unsafe_allow_html=True)

    # Coluna 2
    link2 = '''<p style="text-align: center;">
                <a href="https://itajrfundpot-dpremiacoes.streamlit.app/" target="_blank">
                <input type="button" value="🥇 Opção 2" style="margin-top: 20px; border-radius: 10px; padding: 10px 20px; border: none; color: black; background-color: rgba(255, 255, 255, 0.7);">
                </a>
                </p>'''
    col2.markdown(link2, unsafe_allow_html=True)

    col2.markdown(""" <div style="text-align: center; font-size: 30px; word-wrap: break-word;"> <strong>🥇 Dataset de Olimpíadas </div>""", unsafe_allow_html=True)

    col2.markdown(""" <div style="text-align: center; font-size: 23px; word-wrap: break-word;"> Nessa página, é possível editar o banco de dados referente 
                        à algumas informações sobre os alunos e suas participações nas olimpíadas como por exemplo: <strong> escola, cidade, estado, 
                        medalha, série, ano... </div>""", unsafe_allow_html=True)

    # Coluna 3
    link3 = '''<p style="text-align: center;">
                <a href="https://itajrfundpot-dentrevistas.streamlit.app/" target="_blank">
                <input type="button" value="🎙️ Opção 3" style="margin-top: 20px; border-radius: 10px; padding: 10px 20px; border: none; color: black; background-color: rgba(255, 255, 255, 0.7);">
                </a>
                </p>'''
    col3.markdown(link3, unsafe_allow_html=True)

    col3.markdown(""" <div style="text-align: center; font-size: 30px; word-wrap: break-word;"> <strong>🎙️ Dataset de Entrevistas </div>""", unsafe_allow_html=True)

    col3.markdown(""" <div style="text-align: center; font-size: 23px; word-wrap: break-word;"> Nessa página, é possível editar o banco de dados referente 
                        às entrevistas dos alunos, incluindo informações como: <strong> entrevistador, data da entrevista, tópicos abordados... </div>""", unsafe_allow_html=True)

head()
redirect()


