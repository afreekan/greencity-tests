# GreenCity UI Automation Tests

This repository contains automated UI tests for the GreenCity Events page, built using Python, Selenium WebDriver and Allure for reporting. The project strictly follows the Page Object Model (POM) and Component-based architecture.

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Chrome Browser
- Allure Commandline (requires Java)

#### Installing Allure on Windows:
You can quickly install Allure using Scoop:
```powershell
scoop install allure
```
Or download the zip from the [latest Allure Release](https://github.com/allure-framework/allure2/releases), extract it, and add the `bin` directory to your system `PATH`.

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Tests
To execute the test suite and gather Allure data:
```bash
pytest tests/test_events_page.py --alluredir=allure-results
```

### 4. Viewing the Report
Generate and open the interactive Allure report:
```bash
allure serve allure-results
```

## Author
Ostrovoi Illia
