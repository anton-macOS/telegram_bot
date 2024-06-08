import logging
import gspread


class GoogleSheet:
    def __init__(self, file_path):
        self.gc = None
        self.file_path = file_path
        self.connect()

    def connect(self):
        try:
            self.gc = gspread.service_account(self.file_path)
            logging.info('Подключение успешно')
        except Exception as e:
            logging.info(f'Что-то пошло не так - {e}')
            self.gc = None

    def share_sheet(self, tab, mail):
        try:
            spreadsheet = self.gc.open_by_url(tab)
            logging.info('Таблица открыта')
            spreadsheet.share(mail, perm_type='user', role='writer')
            logging.info('Дан доступ')
        except gspread.SpreadsheetNotFound:
            logging.info('Таблица не найдена')

    def remove_permission(self, tab, mail):
        try:
            spreadsheet = self.gc.open_by_url(tab)
            logging.info('Таблица открыта')
            spreadsheet.remove_permissions(mail)
            logging.info('Доступ закрыт')
        except gspread.SpreadsheetNotFound:
            logging.info('Проблемы')
