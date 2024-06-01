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