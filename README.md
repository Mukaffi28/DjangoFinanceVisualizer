# Django CRUD Web App with SQL Server Integration
Greetings to this Django web application repository, where you can explore CRUD operations seamlessly integrated with SQL Server and experience interactive chart visualization. Feel free to visit the website at https://mukaffi28.pythonanywhere.com/.

## Task 1

Django JSON Visualization Web App! This web application is designed to display visual representations of data provided in a JSON format. You can access the app at either [https://mukaffi28.pythonanywhere.com/home/](https://mukaffi28.pythonanywhere.com/home/) or [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/).

## Features

- **Data Model**: The application utilizes a model named `jsonModel` to structure and manage the JSON data.

- **Visualization**: Upon accessing the home page, the `home` function in `views.py` processes the JSON data and renders visual representations for an enhanced user experience.

## Task 2

## Overview

Django CRUD Application for Stock Management! This web application allows users to perform CRUD operations (Create, Read, Update, Delete) on stock data. You can access the app at [https://mukaffi28.pythonanywhere.com/](https://mukaffi28.pythonanywhere.com/).

## Features

- **Model:**
  The application uses a model named `Stock` to manage and store stock data efficiently.

- **CRUD Functionality:**
  Users can perform Create, Read, Update, and Delete operations on stock data.

- **Search Capability:**
  The application provides search functionality, enabling users to search through all the stored data easily.

## How to Use

1. **Access the Web App:**

   Visit [https://mukaffi28.pythonanywhere.com/](https://mukaffi28.pythonanywhere.com/) to interact with the CRUD functionalities.

2. **Perform CRUD Operations:**

   - **Create:** Add new stock entries by using the provided form.
   
   - **Read:** View the existing stock data on the main page.
   
   - **Update:** Edit stock details through the update functionality.
   
   - **Delete:** Remove stock entries as needed.

3. **Search Data:**

   Use the search feature to find specific stock information quickly.

## Task 3

## Overview

Welcome to the Financial Data Visualization App! This application provides a comprehensive view of financial market data through multi-axis charts and pie charts. Users can explore Close price, Open price, and Volume trends, along with a candlestick chart specific to the chosen trade_code. Additionally, three pie charts offer insights into the top 10 trade codes based on different criteria. You can access the app at [https://mukaffi28.pythonanywhere.com/stock-chart/](https://mukaffi28.pythonanywhere.com/stock-chart/) or through the 'Visualization' button in the navigation bar.

## Features

- **Multi-Axis Chart:**
 The application incorporates a multi-axis chart displaying Close price, Open price, and Volume trends for a comprehensive overview of market data.

- **Candlestick Chart:**
  Users can choose a specific trade_code to view a detailed candlestick chart, offering insights into Open, Close, High, and Low prices.

- **Pie Charts:**
  - **Top 10 Trade Codes with Highest Trading Volumes:**
    Visual representation of the top 10 trade codes with the highest trading volumes.

  - **Top 10 Trade Codes by Opening Prices:**
    Pie chart illustrating the top 10 trade codes based on opening prices.

  - **Top 10 Trade Codes by Closing Prices:**
    Visualization of the top 10 trade codes based on closing prices.

## How to Use

1. **Access the Web App:**

   Visit [https://mukaffi28.pythonanywhere.com/stock-chart/](https://mukaffi28.pythonanywhere.com/stock-chart/) to explore the financial data visualization.

2. **Multi-Axis Chart:**

   - Observe trends in Close price, Open price, and Volume on the multi-axis chart.

3. **Candlestick Chart:**

   - Choose a specific trade_code to view detailed information in the candlestick chart.

4. **Pie Charts:**

   - Explore the top 10 trade codes with the highest trading volumes.
   - Analyze the top 10 trade codes based on opening prices.
   - Understand the top 10 trade codes based on closing prices.

## Learning Journey Summary

## Django Framework:

- Explored the intricacies of Django's structure, gaining proficiency in models, views, templates, and forms.
  
- Successfully set up and configured Django projects, laying the foundation for effective web development.

## SQL Server Integration:

- Embraced the migration process from a JSON model to an SQL model in Django, enhancing data management capabilities.
  
- Learned the art of connecting Django to an SQL Server, enabling seamless CRUD operations for efficient data handling.

## Data Visualization:

- Implemented visually appealing table visualization using Django templates, enhancing the presentation of data.
  
- Mastered the creation of line and bar charts with Chart.js, providing dynamic and engaging data representation.

- Developed a multi-axis chart, integrating dropdowns for dynamic data changes and a richer user experience.

## Deployment:

- Successfully deployed a Django application on a cloud hosting service, gaining practical insights into the deployment process.

## Challenges Faced

Throughout the project development, I navigated several challenges that enriched my learning experience:

## Loading Data to JSON:

- Encountered issues where some volume column entries were in string format instead of decimal, necessitating conversion for accurate representation.

## Data Formatting:

- Addressed challenges posed by data entries containing commas (e.g., "22,200"), requiring removal or conversion to ensure proper formatting and consistency across the dataset.

## Deployment:

- Overcome deployment challenges by meticulously configuring the environment, ensuring a smooth transition, and verifying that the application runs seamlessly on the chosen hosting service.


