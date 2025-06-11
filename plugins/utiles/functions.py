#from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import PyPDFLoader

from langchain.chains import RetrievalQA

import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SimpleAgent():
    def __init__(self,
                 source_model='ollama',
                 model="llama3.2:1b",
                 chroma_db="./chroma_db",
                 path_directory = r'C:\Users\Quera\Desktop\Airflow-Server-main\files',
                 api_key= 'YOUR_API_KEY'):

        self.path_directory = path_directory
        self.chroma_db = chroma_db

        if source_model=='ollama':self.llm = Ollama(model=model)
        #elif source_model=='mistralai': self.llm = ChatMistralAI(model=model)
        else:self.llm = ChatOpenAI(model="gpt-4.1", openai_api_key=api_key)

    def check_file(self):
        list_files = os.listdir(self.path_directory)
        if len(list_files) > 0 : return list_files[0]
        else:raise Exception("No files in directory")

    def read_file(self, ti):
        file_name = ti.xcom_pull('task_check_file', key='return_value')
        pdf = PyPDFLoader(self.path_directory + '/' + file_name).load()
        return pdf[0].dict()['page_content'] + pdf[1].dict()['page_content']


    def chat_completion(self, ti):
        meassages = [
            {"role": "system", "content": "Tu es un assistant qui fait la synthèse d'un document PDF en 3 phrase max"},
            {"role": "user", "content": ti.xcom_pull('task_read_file', key='return_value')}
        ]
        return str(self.llm.invoke(meassages).content)
    
    def send_email_smtp(self, ti):
        smtp_host = "smtp.gmail.com"
        smtp_port = 587
        username = "duranty.kevin@gmail.com"
        password = "bfeqmskzptuekopp"
        to_email = "kevin.duranty@quera.fr"

        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = to_email
        msg["Subject"] = "Airflow Notification"

        html = f"<p>{ti.xcom_pull('task_llm', key='return_value')}</p>"
        msg.attach(MIMEText(html, "html"))
        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(username, password)
                server.sendmail(username, to_email, msg.as_string())
                print("✅ Email envoyé avec succès !")
        except Exception as e:
            print("❌ Erreur lors de l'envoi de l'email :", e)
            raise
            


n = 42

