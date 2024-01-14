
# Psyche-Scan

this project is a web based solution for calculating mental health analysis for a user.

In this competative world it is necessary to look upon your mental health.

## Features

- User friendly interface
- Data Manupilation using CSV and Python
- **Algorithmic Processing:** An in-house algorithm processes sentiment scores and PPG form responses to generate individual and overall mental health scores.
- **Visualization:** Results are presented through a user-friendly interface, including pie charts for tweets, PPG responses, and overall mental health.
- **Resource Provision:** Additional resources, such as general suggestions, remedies (primarily yoga), and contact details of mental health professionals, are provided.

## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
- Database: MongoDB

## Installation

For running this project you need to have following python libraries installed in your machine

- Pandas
- vader
- Flask
- MongoDB 

### Installation of Flask
```bash
  pip install Flask
```

### Installation of Pymongo
```bash
  pip install pymongo
```

### Installation of vader
```bash
  pip install nltk
```
then create python file and write the following contents
```bash
  import nltk
  nltk.download('vader_lexicon')
```
and run the file then your vader_lexicon will be downloaded and you can delete the file afterwards

### Installation of MongoDB
- Download MongoDB: 
    - Visit the official MongoDB download page: MongoDB Download Center 
    - Choose the version suitable for your Windows OS (e.g., Windows Server 2019, Windows 10 64-bit), and click "Download."

- Install MongoDB:
    - Run the downloaded installer (.msi file).
- You can also download Compass for GUI version

## Running

Now after cloning the repository go to your text editor and run app.py file then go to 

http://127.0.0.1:8000

and then you will be able to run it.

This project is licensed under the MIT License.
