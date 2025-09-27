# PARKING-MANAGEMENT
A simple Python &amp; MySQL based parking management system. Track vehicle entries/exits, calculate parking fees, and manage parking slots efficiently through a command-line interface.

# One_Parking

## Description
One_Parking is a simple command-line parking management system built with Python and MySQL. It helps manage vehicle check-ins and check-outs while automatically calculating parking fees based on the duration of parking. The system maintains logs and allows querying individual vehicle information.

## Features
- Vehicle Entry (Check-In) with timestamp recording
- Vehicle Exit (Check-Out) with automatic fee calculation
- View details of a particular vehicle by number plate
- Maintain daily and historical parking logs
- Tracks available parking slots dynamically
- Simple command-line interface for easy usage
- MySQL database integration

## Prerequisites
- Python 3.13.5
- MySQL Server installed and running
- Python package: `mysql-connector-python`

Install dependencies via pip:
```bash
pip install mysql-connector-python
```
## Setup Instructions

1. **Clone or download the repository**

   ```bash
   https://github.com/Tushar-KL/PARKING-MANAGEMENT.git
   ```
   ```bash
   cd One_Parking
   ```
2. Ensure MySQL Server is installed and running on your machine
3. Create the database in MySQL
Log into your MySQL console and run:
   ```sql
    CREATE DATABASE PARKING;
   ```
4. Place all Python files (main.py, interface.py, database.py) inside the One_Parking folder
5. Run the program
    ```bash
   python interface.py
    ```
6. When prompted, enter your MySQL password to connect to the database

## Usage
After launching interface.py, use the command-line menu to:
- Register vehicle entries (check-ins)
- Register vehicle exits (check-outs)
- Query information about specific vehicles
- Track available parking slots
- Exit the program safely
