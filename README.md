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


# Google Drive authentication instruction

## Step 1: Create a project in Google Cloud

1. Go to https://console.cloud.google.com
2. Create a new project
3. Choose you project
## Step 2: Enable Google Drive API
1. In the API & Service section, select Library
2. Find Google Drive API and enable it for your project
   (Enabling can take up to 5 minutes)
## Step 3: Configure OAuth consent screen
1. In the API & Service section, select OAuth consent screen
2. And choose create External type 
3. Fill App name, supported email and developer contact email addresses (everything else optional)
4. You can skip scopes tab
5. In tab test users add user email
6. Choose Back to Dashboard

## Step 4: Create Credentials
1. In the API & Service section, select Credentials
2. Click Create credentials and select OAuth Client ID
3. Choose Web application, named it.
4. In Authorized JavaScript origins add URI to "http://localhost:8080"
5. In Authorized redirect URIs add URI to "http://localhost:8080/" (last slash is IMPORTANT)
6. Then create credential and download json file
7. Rename the file to "client_secrets.json" and place it in your working directory.

