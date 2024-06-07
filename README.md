# Onboarding Bot

Onboarding Bot is a Telegram bot designed to facilitate the onboarding process for new curators and admins. This bot collects user information, stores it in a PostgreSQL database, and allows admins to manage the onboarding stages.

## Table of Contents


## Features

- Registration of new curators with detailed information
- Management of onboarding stages
- Admin panel for managing curators
- Storage of user data in a PostgreSQL database

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/anton-macOS/telegram_bot.git
    cd telegram_bot
    ```

2. Install Poetry, if not already installed:

    ```sh
    pip install poetry
    ```

3. Install dependencies:

    ```sh
    poetry install
    ```
## Configuration

1. Copy the `.env.example` file to `.env`:

    ```sh
    cp .env.example .env
    ```
   
# Google Sheets Instruction

## Step 1: Enable Google Sheets API
1. In the API & Service section, select Library
2. Find Google Sheets API and enable it for your project (Enabling can take up to 5 minutes)
## Step 2: Create Credentials
1. In the API & Service section, select Credentials
2. Click Create credentials and select Service Account
3. Enter name and push Done
4. After in section Service Accounts in right top corner push - Manage service accounts
5. Then push action and manage key near your created credential
6. Push  add key and create json file
7. Rename the file to "service_account.json" and place it in your working directory.
## Step 3: Path settings
1. In env -> variable "FILE_PATH" enter local file path to the "service_account.json"
## VERY IMPORTANT
Very important! Go to your spreadsheet and share it with a client_email from service_account.json. 
If you don’t do this, you’ll get a gspread.exceptions.SpreadsheetNotFound
