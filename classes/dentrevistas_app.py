import streamlit as st
import base64
import pandas as pd

from classes.DatabaseManager import DatabaseManager
from classes.Student import Student


class StudentInfoApp:
    """
    Constructs a Student Information Application.
    """
    def __init__(self, fileID, sheet_name, token_name):
        """
        Initializes the StudentInfoApp with a database URL.

        :param fileID: ID of the file in the database.
        :type fileID: str.
        :param sheet_name: Name of the sheet in the database.
        :type sheet_name: str.
        :param token_name: Name of the token for authentication.
        :type token_name: str.
        """
        self.db_manager = DatabaseManager(fileID)
        self.sheet_name = sheet_name
        self.token_name = token_name
        self.save = False

        if 'df_cloud' not in st.session_state:
            st.session_state.df_cloud, st.session_state.dftoken = self.db_manager.request_database(self.sheet_name, self.token_name)
        if 'df' not in st.session_state:
            st.session_state.df = None
        if 'update_values' not in st.session_state:  
            st.session_state.update_values = {}  
        if 'log' not in st.session_state:  
            st.session_state.log = {} 

        self.student = Student(st.session_state.df_cloud)
        self.widget_id = (id for id in range(1, 100))

    def head(self):
        """
        Displays the header and the logo of the application
        """
        st.set_page_config(page_title="Opção 3", page_icon="3️⃣")
        
        with open('./utils/front.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        try:
            with open('./utils/logo_jr.png', 'rb') as logo_file:
                logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
                st.markdown(f'<p align="center"><img src="data:image/png;base64,{logo_base64}" width="500"></p>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Logo file not found")
        st.markdown("<h1 style='text-align: center; font-size: 38px;'>Formulário de atualização de informações<br>Fundação Potência</h1>", unsafe_allow_html=True)

        st.markdown("<p style='text-align: center;'>>>> Aplicativo desenvolvido para atualização de informações de medalhistas olímpicos <<<</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 30px;'>✅ Opção 3 - Banco de dados: Entrevistas</h1>", unsafe_allow_html=True)
        st.markdown(""" <div style="text-align: center; font-size: 20px;"> Nessa página, é possível adicionar/alterar informações referentes às entrevistas no banco de dados adicionando um arquivo excel com as informações no mesmo padrão do arquivo excel de entrevistas original</div>""", unsafe_allow_html=True)

    def set_save_state(self):
        """
        Toggles the save state of the application.
        """
        self.save =  not self.save

    def get_save_state(self):
        """
        Returns the save state of the application.

        :return: Save state.
        :rtype: bool.
        """
        return self.save
    
    def update_db(self):
        """
        Updates the database of the application.
        """
        st.session_state.df_cloud, st.session_state.dftoken = self.db_manager.request_database(self.sheet_name, self.token_name)

    def run(self):
        """
        Runs the application.
        """
        st.markdown("<h1 style='text-align: center; font-size: 30px;'><br>🌐 Atualização de informações 🌐</h1>", unsafe_allow_html=True)

        with st.form("input_user"):
            st.markdown(""" <div style="font-size: 20px;"> 1️⃣ <strong> Digite o nome completo do(a) aluno(a):</div>""", unsafe_allow_html=True)

            uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
            st.form_submit_button('continuar')
            try:
                tabela = pd.read_excel(uploaded_file)

                if st.session_state.df == None:
                    st.session_state.df = tabela
            except:
                pass
        try:
            if tabela is not None:
                st.success(f"###### os nomes das colunas foram encontradas no database! \nclique em cotinuar novamente")

                intersection_names = pd.DataFrame({'Nome': list(set(self.student.get_rows(tabela)['Nome'].dropna()) & set(tabela['Nome'].dropna()))})
                if not intersection_names.empty:
                    st.markdown('Os seguintes nomes estão duplicados: ')
                    st.dataframe(intersection_names)
                    st.markdown('As informações repetidas do primeiro serão sobrepostas com as do segundo')
                merged_df = pd.concat([self.student.get_rows(tabela), tabela]).drop_duplicates('Nome', keep='last')
                merged_df = merged_df.sort_values(by='IDPessoa')
                merged_df = merged_df.reset_index(drop=True)
                merged_df = merged_df.dropna(subset=['Nome'])
                st.markdown('os 10 ultimos elementos da database ficarão assim: ')
                st.dataframe(merged_df.tail(10))
                st.markdown('Verifique se não há nada fora do padrão, numero errado de intervalos, letras maiúsculas, colunas com nomes errado, colunas que deveriam ter o mesmo nome, etc...')
                if st.button('Salvar'):
                    st.session_state.df = merged_df
                    self.db_manager.save_db(st.session_state.df)
                    self.set_save_state()
                elif st.button('Cancelar'):
                    st.session_state.clear()  # Limpa a sessão
                    st.experimental_rerun()  
        except:
            pass

