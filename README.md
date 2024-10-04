# Personal Finance Resources

The Personal Finance Resources Repository is a Flask web application that helps users manage their investment portfolios efficiently. It allows users to configure funds, set up glide paths, rebalance portfolios, and visualize asset allocations over time.

## Table of Contents

- [Investment Fund Manager](#investment-fund-manager)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
  - [Usage](#usage)
    - [Home Page](#home-page)
      - [Sections Overview](#sections-overview)
      - [Getting Started](#getting-started-1)
    - [Rebalance](#rebalance)
    - [Allocation Plot](#allocation-plot)
    - [Fund Performance](#fund-performance)
    - [Edit Config](#edit-config)
    - [Create Fund](#create-fund)
  - [Developer Guide](#developer-guide)
    - [Project Structure](#project-structure)
    - [Key Components](#key-components)
    - [Code Functionality](#code-functionality)
      - [Configuration Management](#configuration-management)
      - [Glide Path and Allocations](#glide-path-and-allocations)
      - [Rebalancing Logic](#rebalancing-logic)
      - [Fund Performance Data](#fund-performance-data)
      - [Templates and Static Files](#templates-and-static-files)
  - [Contributing](#contributing)
  - [License](#license)
  - [Additional Notes](#additional-notes)
  - [FAQ](#faq)
    - [How do I add a new fund?](#how-do-i-add-a-new-fund)
    - [How can I modify an existing fund?](#how-can-i-modify-an-existing-fund)
    - [The charts are not displaying correctly. What can I do?](#the-charts-are-not-displaying-correctly-what-can-i-do)
    - [How do I generate a `requirements.txt` file from my virtual environment?](#how-do-i-generate-a-requirementstxt-file-from-my-virtual-environment)
  - [Contact](#contact)
  - [End Notes](#end-notes)

---

## Features

- **Portfolio Rebalancing**: Calculate investment amounts to rebalance your portfolio based on your age and target allocations.
- **Glide Path Configuration**: Define how your asset allocation changes over time.
- **Fund Performance Tracking**: View current and historical performance metrics for your funds.
- **Interactive Charts**: Visualize asset allocation over time and fund performance using interactive charts.
- **Customizable Funds**: Add, remove, and configure funds and asset classes according to your investment strategy.

---

## Getting Started

### Prerequisites

- **Python 3.7 or higher**
- **Git** (optional, for cloning the repository)
- **Virtual Environment** (recommended)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/investment-fund-manager.git
   cd investment-fund-manager
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Set the Flask App Environment Variable**

   - On macOS/Linux:

     ```bash
     export FLASK_APP=app.py
     ```

   - On Windows (Command Prompt):

     ```bash
     set FLASK_APP=app.py
     ```

2. **Run the Application**

   ```bash
   flask run
   ```

3. **Access the Application**

   Open your web browser and navigate to `http://localhost:5000`.

---

## Usage

### Home Page

The home page provides an overview of the application and instructions on how to use each section. Start by selecting an existing fund from the dropdown menu or creating a new one.

#### Sections Overview

- **Rebalance**: Calculate how to allocate new investments to maintain your target asset allocation.
- **Allocation Plot**: Visualize your asset allocation over time based on your glide path.
- **Fund Performance**: View current and historical performance metrics for your funds.
- **Edit Config**: Customize your investment strategy, including funds and glide paths.
- **Create Fund**: Set up a new investment fund with its own configuration.

#### Getting Started

To begin, select an existing fund from the dropdown menu or create a new one. Navigate through the sections using the navigation bar at the top.

### Rebalance

Use this section to calculate how to allocate new investments to maintain your target asset allocation.

- **Steps**:
  1. Enter the amount you wish to invest.
  2. Provide your current holdings for each fund.
  3. The application will suggest investment amounts for each fund to rebalance your portfolio.

### Allocation Plot

Visualize how your asset allocation changes over time based on your configured glide path.

- **Features**:
  - View a line chart showing the percentage allocation to each asset class over your investing lifetime.
  - The chart is interactive and adjusts to screen size for optimal viewing.

### Fund Performance

View detailed performance metrics for your funds.

- **Features**:
  - See current prices, daily changes, and historical returns.
  - Select individual funds to view their historical performance charts.
  - Charts are interactive and allow for time frame adjustments.

### Edit Config

Customize your investment strategy.

- **Features**:
  - **Date of Birth**: Set your date of birth to calculate age-based allocations.
  - **Funds Configuration**:
    - Add or remove funds for each asset class.
    - Set target percentages for each fund.
    - Ensure that percentages within an asset class sum to 100%.
  - **Glide Path Configuration**:
    - Define how your asset allocations change at different ages.
    - Add or remove glide path entries.
    - Drag and drop entries to reorder them.
    - Ensure that allocations at each age sum to 100%.

### Create Fund

Use this section to set up a new investment fund.

- **Steps**:
  1. Enter a unique fund name.
  2. Configure funds for each asset class and set their target percentages.
  3. Define your glide path by specifying allocations at different ages.
  4. Save the configuration to create the new fund.

---

## Developer Guide

### Project Structure

```
investment-fund-manager/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── funds/
│   └── [Fund Configuration Files].json
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── plot.html
│   ├── rebalance.html
│   ├── fund_performance.html
│   └── edit_config.html
├── static/
│   └── [Static Files]
├── utils/
│   ├── __init__.py
│   ├── allocation.py
│   ├── config_manager.py
│   └── rebalancing.py
```

### Key Components

- **app.py**: The main Flask application file containing route definitions and application logic.
- **templates/**: Contains all HTML templates rendered by Flask, using Jinja2 templating.
- **funds/**: Stores fund configuration files in JSON format.
- **utils/**: Contains utility modules for allocation calculations, configuration management, and rebalancing logic.

### Code Functionality

#### Configuration Management

- **Module**: `utils/config_manager.py`
- **Purpose**: Handles loading and saving fund configurations.
- **Functions**:
  - `load_config(fund_id)`: Loads a fund's configuration from a JSON file.
  - `save_config(fund_id, config)`: Saves a fund's configuration to a JSON file.
  - `get_available_funds()`: Returns a list of available fund configurations.

#### Glide Path and Allocations

- **Module**: `utils/allocation.py`
- **Purpose**: Calculates asset allocations based on age and glide path.
- **Functions**:
  - `get_allocations(age, config)`: Returns the interpolated asset allocation for a given age.

#### Rebalancing Logic

- **Module**: `utils/rebalancing.py`
- **Purpose**: Calculates how to allocate new investments to rebalance the portfolio.
- **Functions**:
  - `calculate_rebalancing(...)`: Computes the investment amounts needed for rebalancing.

#### Fund Performance Data

- **Data Retrieval**: Uses the `yfinance` library to fetch current and historical fund data.
- **Templates**: Data is displayed in `fund_performance.html`.
- **Charts**: Utilizes Chart.js for interactive charts.

#### Templates and Static Files

- **Templates**: HTML files using Jinja2 templating, located in the `templates/` directory.
- **Static Files**: CSS, JavaScript, and image files located in the `static/` directory.


---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add new feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

---

## License

This project is licensed under the MIT License.

---

## Additional Notes

- **Dependencies**:

  - **Flask**: Web framework used for the application.
  - **yfinance**: Library to fetch financial data.
  - **pandas**: Data analysis and manipulation tool.
  - **Chart.js**: JavaScript library for creating charts, included via CDN in templates.
  - **Bootstrap**: Used for responsive design and styling, included via CDN.

- **Virtual Environment**

  - Using a virtual environment is recommended to manage dependencies and avoid conflicts.
  - The `.gitignore` file is configured to exclude virtual environment directories.


## FAQ

### How do I add a new fund?

- Navigate to the **Create Fund** section.
- Enter the fund name and configure the funds and glide path.
- Save the configuration to start using the new fund.

### How can I modify an existing fund?

- Go to the **Edit Config** section.
- Select the fund you wish to modify.
- Make the necessary changes and save the configuration.

### The charts are not displaying correctly. What can I do?

- Ensure that you have a stable internet connection, as Chart.js is included via CDN.
- Check the browser console for any errors.
- Verify that your fund configurations and glide paths are correctly set up.

### How do I generate a `requirements.txt` file from my virtual environment?

- **Activate Your Virtual Environment**:

  - On Windows:

    ```bash
    venv\Scripts\activate
    ```

  - On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

---

## Contact

For any questions or support, please contact:

- **GitHub**: [ThePhiRatio](https://github.com/ThePhiRatio)

---

## End Notes

Thank you for using the Personal Finance Resources Repository! We hope this application helps you achieve your investment goals. If you have any feedback or suggestions, please don't hesitate to reach out.
