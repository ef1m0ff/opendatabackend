# Open Data Challenge - Telegram Event Management System  

This repository contains the codebase for the **Open Data Challenge** hackathon project. The goal of this project is to create a seamless event management system leveraging Telegram as a platform for communication and integration with a backend service for storing and retrieving event data.  

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Future Improvements](#future-improvements)

---

## Overview
This system automates the process of creating, retrieving, and managing events shared on Telegram channels or chats. It uses NLP to extract event details and stores them in a backend system, allowing for quick event dissemination and user interaction. The backend also manages user-event relationships and supports a real-time WebSocket connection for updates.

---

## Features
1. **Telegram Integration**:  
   Automatically listens for new Telegram messages, extracts event data using NLP, and processes it.  
2. **Event Parsing**:  
   Extracts event details such as date, time, location, and description from text messages.  
3. **Real-Time Backend**:  
   A FastAPI-based backend for storing events, user data, and managing interactions through APIs and WebSockets.  
4. **Data Cleaning**:  
   Utilizes advanced text preprocessing to filter out noise and ensure consistent data formats.  
5. **Strapi Integration**:  
   Events and user data are synced with a Strapi-based CMS for centralized management.  
6. **WebSocket Updates**:  
   Maintains real-time connections to update the user interface with live data.  

---

## Architecture

1. **Telegram Bot**:  
   The bot listens to incoming messages and triggers an event handler for message parsing.  
2. **FastAPI Backend**:  
   Handles user management, event storage, and real-time WebSocket updates.  
3. **NLP Utilities**:  
   Processes raw message text to extract structured event data.  
4. **Strapi CMS**:  
   Provides a central location to manage event data, including user-event relationships.  

---

## Getting Started  

### Prerequisites
- Python 3.8+  
- Node.js and npm (for Strapi setup)  
- Telegram API credentials (API ID, API HASH, and Bot Token)  
- `.env` file with the following keys:  
  ```plaintext
  API_ID=your_telegram_api_id
  API_HASH=your_telegram_api_hash
  PHONE=your_telegram_phone_number
  STRAPI_BASE_URL=your_strapi_base_url
  ```

### Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/open-data-challenge.git
   cd open-data-challenge
   ```
2. Install Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file as described in [Prerequisites](#prerequisites).  
4. Start the Telegram client:  
   ```bash
   python main.py
   ```
5. Set up and run the FastAPI server:  
   ```bash
   cd server
   uvicorn server:app --reload --host 127.0.0.1 --port 8020
   ```
6. (Optional) Install and set up Strapi for managing backend data.

---

## Usage

1. **Telegram Client**:  
   - The bot listens to messages and extracts event data.  
   - Parsed data is sent to the FastAPI backend for processing and storage.  

2. **FastAPI Backend**:  
   - Exposes API endpoints for managing users and events.  
   - Supports WebSocket connections for real-time updates.  

3. **Processing Pipeline**:  
   - Incoming Telegram messages are cleaned, parsed, and transformed into structured JSON data.  

---

## Technologies Used
- **Python**: Core programming language for the Telegram bot and FastAPI backend.  
- **FastAPI**: Web framework for API and WebSocket functionality.  
- **httpx**: Asynchronous HTTP client for API requests.  
- **Telethon**: Telegram client library for handling incoming messages.  
- **Strapi**: Headless CMS for managing event and user data.  
- **NLP Tools**: `cleantext` for text preprocessing.  

---

## Folder Structure

```plaintext
.
├── main.py                 # Telegram bot client
├── process_raw_data.py     # Data cleaning and NLP utilities
├── server.py               # FastAPI backend server
├── utils/                  # Shared utility functions
├── data/                   # Input and output files (e.g., parsed messages)
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

---

## Future Improvements
1. **Enhanced NLP**:  
   Improve event data extraction using machine learning models.  
2. **User-Friendly Interface**:  
   Develop a web-based frontend for managing events and user interactions.  
3. **Analytics Dashboard**:  
   Provide insights on events and user engagement.  
4. **Localization**:  
   Support multiple languages for better accessibility.  
