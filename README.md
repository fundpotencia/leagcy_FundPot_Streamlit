# FundPot_Streamlit
 
# Streamlit Apps to Update Datasets

Welcome to the Streamlit App for updating datasets. This repository contains a Streamlit application designed to manage and update various datasets stored on Google Drive. It also includes a mechanism to handle authentication if the Google Drive API token expires.

## Table of Contents

- [Overview](#overview)
- [Files](#files)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Pages](#pages)

## Overview

This Streamlit application allows users to:
- View a home page.
- Update three different datasets.
- Handle authentication for Google Drive API if the token has expired.

## Files

The repository consists of five main files, each representing a page of the Streamlit app:

1. **🏠_Home.py**: Home page
2. **dAlunos_op1.py**: Page to update the `dAlunos` dataset
3. **dPrem_op2.py**: Page to update the `dPremiacoes` dataset
4. **dEntrevistas_op3.py**: Page to update the `dEntrevistas` dataset
5. **redirect.py**: Page to update the Google Drive API token

Additionally, the repository includes:

- **classes**: Contains the basic structure of the Streamlit app.
- **updateDB**: Manages the app to Google Drive integration through the Google Drive API.
- **updateToken**: Handles the Google Drive API token update process.
- **utils**: Includes other utilities such as background images and logos.
- **requirements.txt**: Lists the libraries needed to run the app.

## Installation

To run this app locally, you need to have Python and Streamlit installed. You can install the required libraries using the following command:

```sh
pip install -r requirements.txt
```

## Running the App

To run the app locally, use the following command in your terminal:

```sh
streamlit run <app_name>.py
```

Replace <app_name> with the name of the page file you want to run. For example, to run the home page, use:

```sh
streamlit run 🏠_Home.py
```

## Pages

- **🏠_Home.py**: This is the main landing page of the app.
- **dAlunos_op1.py**: Use this page to update the dAlunos dataset.
- **dPrem_op2.py**: Use this page to update the dPremiacoes dataset.
- **dEntrevistas_op3.py**: Use this page to update the dEntrevistas dataset.
- **redirect.py**: If your Google Drive API token has expired, use this page to update the token.


Feel free to explore and update the datasets as needed. For any issues or contributions, please open an issue or submit a pull request. Enjoy using the app!