# SSA Stock Analysis 📊

SSA Stock Analysis is a very basic interactive Streamlit application designed for analyzing investment returns in stocks, focusing on indices without considering dividends. It allows you to calculate and visualize the return on investment (ROI) for different investment strategies, such as Lump Sum and Dollar Cost Averaging, over a defined investment horizon.

The application is available here

## Features

- **Stock Selection:** Choose from a list of popular stocks or use a search bar to select any other stock available on Yahoo Finance.
- **ROI Calculation:** Compute the annualized ROI for Lump Sum and Dollar Cost Averaging strategies over a specified investment horizon.
- **Data Visualization:** Display charts showing the evolution of stock prices and volatility. Compare ROI distributions using boxplots and violin plots.
- **Investment Customization:** Set the investment amount, investment frequency, investment horizon, as well as the start and end dates for the historical data analysis.

## Live Demo

Check out the live demo of the application [here](https://ssa-stockanalysis.streamlit.app).

## Installation

1. **Clone the repository:**
   ```bash
   git clone <REPOSITORY-URL>
   cd <DIRECTORY-NAME>
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate  # For Windows
   ```
3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## Usage

1. Access the application via the Streamlit interface.
2. Select a stock from the available list in the sidebar or use the search bar to select another stock.
3. Define your investment properties (amount, frequency, horizon, dates).
4. Visualize the results in the form of graphs and key metrics.
5. Compare the performance of the two investment strategies over the selected period.

## Project Structure

* main.py: The main script containing the Streamlit code for the application.
* investmentStrategies.py: Module containing the calculation functions for the different investment strategies.
* requirements.txt: List of Python dependencies needed to run the application.
* README.md: This file, explaining how to use and install the application.


## Authors

Slim Saanouni - For any inquiries, feel free to [contact me](mailto:saanouni.slim@gmail.com).

## License

This project is licensed under the MIT License.

