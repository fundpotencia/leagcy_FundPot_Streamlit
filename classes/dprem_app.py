import streamlit as st
import base64

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

        if 'df' not in st.session_state:
            st.session_state.df, st.session_state.dftoken = self.db_manager.request_database(self.sheet_name, self.token_name)
        if 'update_values' not in st.session_state:  
            st.session_state.update_values = {}  
        if 'log' not in st.session_state:  
            st.session_state.log = {} 

        self.student = Student(st.session_state.df)
        self.widget_id = (id for id in range(1, 100))

    def head(self):
        """
        Displays the header and the logo of the application
        """
        st.set_page_config(page_title="Opção 2", page_icon="2️⃣")
        
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
        st.markdown("<h1 style='text-align: center; font-size: 30px;'>✅ Opção 2 - Banco de dados: Premiações</h1>", unsafe_allow_html=True)
        st.markdown(""" <div style="text-align: center; font-size: 20px;"> Nessa página, é possível editar o banco de dados referente à algumas informações sobre os alunos e suas participações nas olimpíadas como por exemplo: <strong> escola, cidade, estado, medalha, série, ano, gênero... </div>""", unsafe_allow_html=True)        

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
        st.session_state.df, st.session_state.dftoken = self.db_manager.request_database(self.sheet_name, self.token_name)

    def run(self):
        """
        Runs the application.
        """
        st.markdown("<h1 style='text-align: center; font-size: 30px;'><br>🌐 Atualização de informações 🌐</h1>", unsafe_allow_html=True)

        with st.form("input_user"):
            st.markdown(""" <div style="font-size: 20px;"> 1️⃣ <strong> Digite o nome completo do(a) aluno(a):</div>""", unsafe_allow_html=True)        

            name = st.text_input(" ").upper()
            st.form_submit_button("Buscar")
            
        if self.student.check_student(name):
            st.session_state.student_name = name  
            st.success(f"###### {name} encontrado(a) no database!")
            
            st.subheader("📝 Atualização de dados")
            st.markdown(f""" <div style="font-size: 18px; color: black;"> <strong>{name} encontrado(a) com as seguintes informações:</div>""", unsafe_allow_html=True)
            student_rows = self.student.get_student_rows(name).copy()
            student_rows = student_rows.set_index('Nome')
            st.dataframe(student_rows)    

            st.session_state.df = self.student.update_df(name)
            st.markdown(f""" <div style="font-size: 18px; color: black;"> <strong>Informações de {name} atualizadas:</div>""", unsafe_allow_html=True)
            student_rows = self.student.get_student_rows(name).copy()
            student_rows = student_rows.set_index('Nome')
            st.dataframe(student_rows)    

                
            if st.button('Salvar', key=next(self.widget_id)):
                self.db_manager.save_db(st.session_state.df, st.session_state.dftoken)
                self.set_save_state()
                
        else: 
            st.error("Aluno(a) não encontrado(a) no database!")