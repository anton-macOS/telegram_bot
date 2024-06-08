import logging

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveLoad:
    def __init__(self):
        self.drive = None
        self.connect()

    def connect(self):
        try:
            gauth = GoogleAuth()
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
            photo_drive = self.drive.CreateFile({'title': f"{file_name}_ТЛ_"})
            photo_drive.SetContentFile(local_photo)
            photo_drive.Upload()
            logging.info(f'Файл - {file_name} успешно загружен')
        except Exception as e:
            logging.info(f'Ошибка загрузки файла: {e}')
