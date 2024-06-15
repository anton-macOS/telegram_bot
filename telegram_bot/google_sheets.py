import os
import logging
import gspread
from dotenv import load_dotenv

load_dotenv()
CURATOR_TABLE_TEMPLATE_ID = os.getenv('CURATOR_TABLE_TEMPLATE_ID')
service_account = os.getenv('FILE_PATH')
GOOGLE_SHEET_MAIL = os.getenv('GOOGLE_SHEET_MAIL')


class GoogleSheet:
    spreadsheets_list = []

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

    def share_sheet(self, sheet, mail):
        try:
            spreadsheet = self.gc.open_by_url(sheet)
            logging.info('Таблица открыта')
            spreadsheet.share(mail, perm_type='user', role='writer')
            logging.info('Дан доступ')
        except gspread.SpreadsheetNotFound:
            logging.info('Таблица не найдена')

    def copy_curator_template(self, mail, full_name):
        try:
            template = self.gc.open_by_key(CURATOR_TABLE_TEMPLATE_ID)
            template.share(mail, perm_type='user', role='reader', notify=False)
            logging.info('Пользователю добавлен в доступ')
            spreadsheet = self.gc.copy(CURATOR_TABLE_TEMPLATE_ID, title=f'База Студентов - {full_name}')
            self.spreadsheets_list.append(spreadsheet.id)
            new_spreadsheet = self.gc.open_by_key(spreadsheet.id)
            permissions = template.list_permissions()
            print(permissions)
            for perm in permissions:
                if perm['role'] != 'owner':
                    if 'emailAddress' in perm:
                        new_spreadsheet.share(perm['emailAddress'], perm_type=perm['type'], role='writer')

            for sheet_id in self.spreadsheets_list[:-1]:
                sheet = self.gc.open_by_key(sheet_id)
                sheet.share(mail, perm_type='user', role='writer', notify=False)
                logging.info('В предыдущую добален доступ')

        except Exception as e:
            logging.info(f'Ошибка - {e}')

    def remove_permission(self, tab, mail):
        try:
            spreadsheet = self.gc.open_by_url(tab)
            logging.info('Таблица открыта')
            spreadsheet.remove_permissions(mail)
            logging.info('Доступ закрыт')
        except gspread.SpreadsheetNotFound:
            logging.info('Проблемы')
