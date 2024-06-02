import asyncio
import warnings
import streamlit as st

from classes.dentrevistas_app import StudentInfoApp
from updateDB.main import run_updateDB
from updateDB.create_service import create_services


warnings.filterwarnings("ignore", category=UserWarning, message=".*Arrow table.*")

keys = {
    "folderID": st.secrets["dEntrevistas"]["folderID"],
    "fileID": st.secrets["dEntrevistas"]["fileID"],
    "filename": st.secrets["dEntrevistas"]["filename"],
    "sheet_name": st.secrets["dEntrevistas"]["sheet_name"],
    "token_name": st.secrets["dEntrevistas"]["token_sheet_name"]
}

app = StudentInfoApp(keys["fileID"], keys["sheet_name"], keys["token_name"])
app.head()
if all(asyncio.run(create_services())):
    app.run()


if app.get_save_state():
    st.info("Salvando... Esse processo pode demorar um pouco!")

    asyncio.run(run_updateDB(keys["folderID"], keys["fileID"], keys["filename"], keys["sheet_name"], keys["token_name"]))
    app.set_save_state()
    app.update_db()

    st.success("O Banco de dados foi salvo no drive com sucesso!")
