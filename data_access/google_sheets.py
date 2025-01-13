import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from config.settings import CREDENTIALS_FILE, SHEET_ID, RANGE_NAME
# Импорт настроек из config/settings.py

# Объемы доступа
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# Описание прав доступа


def authenticate_google_sheets():
    """
    Авторизация через OAuth 2.0 и создание клиента для работы
    с Google Sheets API
    """
    creds = None

    # Проверяем, если токен уже сохранен
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Если нет токена или он невалиден, авторизуем пользователя
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохраняем токен для последующих запусков
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Создаем сервис для работы с Google Sheets API
    service = build('sheets', 'v4', credentials=creds)
    return service


def get_sheet_data():
    """Получаем данные из Google Sheets"""
    service = authenticate_google_sheets()
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SHEET_ID, range=RANGE_NAME
        ).execute()
    values = result.get('values', [])
    print(values)
