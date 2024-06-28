from datetime import datetime
import re
from db.session import get_db
from crud.admin import admin_crud

# regex
CHECK_FULL_NAME = re.compile(r'^[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+\s[А-ЯЁЄІЇҐ][а-яёєіїґ]+$')
CHECK_PHONE = re.compile(r'^(\+?\d{12}|\d{10})$')
CHECK_DATE = re.compile(r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$')
CHECK_MAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
CHECK_CARD = re.compile(r'^\d{16}$')
CHECK_TRC = re.compile(r'^T[a-zA-Z0-9]{33}$')
CHECK_TG_ACCOUNT = re.compile(r'^@')


# The function formats the date string into YYYY-MM-DD format for writing to the database
def parse_date(date):
    date_form = datetime.strptime(date, '%d.%m.%Y')
    return date_form.strftime('%Y-%m-%d')


# Function for searching admin id by username
async def find_admin_id(username):
    with get_db() as db:
        return admin_crud.get_field_by_username(db=db, username=username, field='id')
