# Hangman Web App

Welcome to the Hangman Web App repository! This project is a web-based word guessing game where players attempt to guess a hidden word letter by letter. The backend of the app is built using FastAPI and uses a PostgreSQL database, while the frontend is built with Flask.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Play the classic Hangman word guessing game online.
- Interactive frontend built using Flask.
- Backend API developed using FastAPI.
- Utilizes a PostgreSQL database to store game data.

## Getting Started

### Prerequisites

Before you begin, make sure you have the following software installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/LaimonasAR/HangMan.git
   
2. Navigate to the repository directory:
   ```bash
   cd HangMan
   
3. Build and start the application using Docker Compose:
   ```bash
   docker-compose up -d --build
This command will build and start the backend and frontend services.

### Usage
Access the Hangman web app by opening your web browser and navigating to `http://localhost:5000`.

Start playing the Hangman game by guessing letters and completing the hidden word.

### Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
   

### License
This project is licensed under the MIT License.
