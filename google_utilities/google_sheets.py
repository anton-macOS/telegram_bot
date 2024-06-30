import os
import gspread
from dotenv import load_dotenv
from telegram_bot.logger_setup import logger

load_dotenv()
ADMIN_MAIL = os.getenv('ADMIN_MAIL')
CURATOR_TABLE_TEMPLATE_ID = os.getenv('CURATOR_TABLE_TEMPLATE_ID')
file_path = os.path.abspath(__file__)
cur_directory = os.path.dirname(file_path)
service_account = os.path.join(cur_directory, 'service_account.json')




class GoogleSheet:
    spreadsheets_list = []

    def __init__(self):
        self.gc = None
        self.connect()

    def connect(self):
        try:
            self.gc = gspread.service_account(service_account)
            logger.info('Подключение успешно')
        except Exception as e:
            logger.info(f'Что-то пошло не так - {e}')
            self.gc = None

    def share_sheet(self, sheet, mail):
        try:
            spreadsheet = self.gc.open_by_url(sheet)
            logger.info('Таблица открыта')
            spreadsheet.share(mail, perm_type='user', role='writer')
            logger.info('Дан доступ')
        except gspread.SpreadsheetNotFound:
            logger.info('Таблица не найдена')

    def copy_curator_template(self, mail, full_name):
        try:
            template = self.gc.open_by_key(CURATOR_TABLE_TEMPLATE_ID)
            template.share(mail, perm_type='user', role='reader', notify=True)
            logger.info('Пользователю добавлен в доступ')
            spreadsheet = self.gc.copy(CURATOR_TABLE_TEMPLATE_ID, title=f'База Студентов - {full_name}')
            self.spreadsheets_list.append(spreadsheet.id)
            new_spreadsheet = self.gc.open_by_key(spreadsheet.id)
            new_spreadsheet.share(ADMIN_MAIL, perm_type='user', role='writer', notify=False)
            permissions = template.list_permissions()
            for perm in permissions:
                if perm['role'] != 'owner':
                    if 'emailAddress' in perm:
                        new_spreadsheet.share(perm['emailAddress'], perm_type=perm['type'], role='writer')

            for sheet_id in self.spreadsheets_list[:-1]:
                sheet = self.gc.open_by_key(sheet_id)
                sheet.share(mail, perm_type='user', role='writer', notify=False)
                logger.info('В предыдущую добален доступ')
            logger.info('Шаблон таблицы куратора создан')
        except Exception as e:
            logger.info(f'Ошибка - {e}')

    def remove_permission(self, tab, mail):
        try:
            spreadsheet = self.gc.open_by_url(tab)
            logger.info('Таблица открыта')
            spreadsheet.remove_permissions(mail)
            logger.info('Доступ закрыт')
        except gspread.SpreadsheetNotFound:
            logger.info('Проблемы')


google_sheet = GoogleSheet()
