import os
import logging
from dotenv import load_dotenv
load_dotenv()

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

file_path = os.path.abspath(__file__)
cur_directory = os.path.dirname(file_path)
client_secrets = os.path.join(cur_directory, 'client_secrets.json')
folder_id = os.getenv('FOLDER_ID')


class GoogleDriveLoad:
    def __init__(self):
        self.drive = None
        self.connect()

    def connect(self):
        try:
            gauth = GoogleAuth()
            gauth.LoadClientConfigFile(client_secrets)
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
            logging.info('Подключение к диску успешно!')
        except Exception as e:
            logging.info(f'Что-то пошло не так!: {e}')
            self.drive = None

    def download_photo(self, file_name, local_photo):
        if self.drive is None:
            logging.info('Проблемы с подключением к Google Drive')
        try:
            photo_drive = self.drive.CreateFile({'title': f"{file_name}_ТЛ_",
                                                 'parents': [{'id': folder_id}]})
            photo_drive.SetContentFile(local_photo)
            photo_drive.Upload()
            photo_drive.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            })
            file_link = photo_drive['alternateLink']
            logging.info(f'Файл - {file_name} успешно загружен')
            return file_link

        except Exception as e:
            logging.info(f'Ошибка загрузки файла: {e}')


