import streamlit as st


class Student:
    """
    Constructs a Student class.
    """
    def __init__(self, df):
        """
        Initializes the Student with a DataFrame.

        :param df: DataFrame containing student data.
        :type df: pandas.DataFrame.
        """
        self.df = df

    def check_student(self, student_name):
        """
        Checks if a student exists in the DataFrame.

        :param student_name: Name of the student.
        :type student_name: str.
        :return: True if student exists, False otherwise.
        :rtype: bool.
        """
        if student_name in self.df['Nome'].values:
            return True
        else:
            return False

    def update_df(self, student_name):
        """
        Updates the DataFrame with new student information.

        :param student_name: Name of the student.
        :type student_name: str.
        :return: Updated DataFrame.
        :rtype: pandas.DataFrame.
        """
        columns_to_drop = ['Nome', 'Escola_Original', 'IDAluno', 'IndicePrivilegio', 'Olimpíada', 'IndiceDesempenho']
        columns_to_drop = [col for col in columns_to_drop if col in self.df.columns]
        if self.check_student(student_name):
            with st.form(key='update_form'):
                st.markdown(""" <div style="font-size: 20px;"><strong>2️⃣ Selecione a coluna para editar:</strong></div>""", unsafe_allow_html=True)
                column = st.selectbox(" ", self.df.drop(columns=columns_to_drop).columns)
                
                st.markdown(f""" <div style="font-size: 20px;"> <strong>3️⃣ Insira o novo valor:</strong></div>""", unsafe_allow_html=True)
                new_value = st.text_input(" ")
                
                submit_button = st.form_submit_button(label='Atualizar aluno')

                if submit_button and new_value:
                    if column and new_value:
                        self.df.loc[self.df['Nome'] == student_name, column] = new_value
                        st.session_state.update_values[column] = new_value  
                        st.success(f"As informações do aluno {student_name} foram atualizadas com sucesso!")
        else:
            st.error(f"O aluno {student_name} não foi encontrado no database.")
        return self.df

    def get_student_rows(self, student_name):
        """
        Retrieves rows of a specific student from the DataFrame.

        :param student_name: Name of the student.
        :type student_name: str.
        :return: Rows of the student if exists, None otherwise.
        :rtype: pandas.DataFrame or None.
        """
        if self.check_student(student_name):
            columns_to_drop = ['Escola_Original', 'IDAluno', 'IndicePrivilegio', 'IndiceDesempenho']
            columns_to_drop = [col for col in columns_to_drop if col in self.df.columns]

            student_rows = self.df.drop(columns=columns_to_drop)[self.df['Nome'] == student_name]
            return student_rows
        else:
            return None
        
    def check_table(self, table):
        """
        Checks if the columns of the given table are a subset of the columns in the DataFrame.

        :param table: The table whose columns are to be checked.
        :type table: pandas.DataFrame
        :return: True if all columns of the given table are present in the DataFrame, False otherwise.
        :rtype: bool
        """
        return set(table.columns).issubset(set(self.df.columns))


    def get_rows(self, tabela):
        """
        Retrieves rows from the DataFrame, dropping specific columns if they exist, 
        provided the columns of the given table are a subset of the DataFrame's columns.

        :param table: The table whose columns are to be checked before fetching rows from the DataFrame.
        :type table: pandas.DataFrame
        :return: The DataFrame with specific columns dropped if the check is successful, or None if the check fails.
        :rtype: pandas.DataFrame or None
        """
        if self.check_table(tabela):
            columns_to_drop = ['Escola_Original', 'IDAluno', 'IndicePrivilegio', 'IndiceDesempenho'] #decidir de alguma coluna sera dropada
            columns_to_drop = [col for col in columns_to_drop if col in self.df.columns]

            rows = self.df.drop(columns=columns_to_drop)
            return rows
        else:
            return None