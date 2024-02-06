# ORK RECAMP

## Overview

RECAMP (Record Examination and Comparison for Active Membership and dues Paid status) is a Python-based tool designed to facilitate the comparison of active and dues-paid members in the Amtgard LARP organization using the Online Record Keeper (ORK). The tool is intended for use by Monarchs or Prime Ministers of a kingdom, as the required information is only accessible to players in these positions.

## Prerequisites

- A computer running Linux, macOS, or Windows.
- Python 3.6+
- [Poetry](https://python-poetry.org/docs/) (Python packaging and dependency management - this isn't strictly necessary, but will help install dependencies if you don't know how to otherwise. The installation and usage sections will assume its useage.)
- Familiarity with using command-line interfaces and tools
- Access to an ORK account with Monarch or Prime Minister privileges

## Installation

Before running RECAMP, ensure that you have installed and correctly configured the Poetry package manager. Once Poetry is installed, follow these steps:

1. Clone the repository or download the source code to your local machine.
2. Navigate to the directory containing the `pyproject.toml` and `poetry.lock` files.
3. Run `poetry install` to install all dependencies in a virtual environment.

## Configuration

Before running the script, you will need to provide your ORK username and password. Replace `'your_username'` and `'your_password'` with your actual ORK credentials in recamp.py,

## Usage

To run RECAMP, navigate to the cloned repository and execute the script using the following command:

```bash
poetry run python recamp.py
```

## How It Works

RECAMP operates in several steps:

### 1. User Authentication

The script starts by attempting to log in to the ORK using the provided credentials. If the login is successful, the script proceeds; otherwise, it terminates with an error message.

### 2. Data Retrieval

The tool fetches two sets of data from the ORK:

- **Active Players**: A report of all active players in the kingdom.
- **Dues Paid Players**: A report of all players who have paid their dues in the kingdom.

### 3. Data Comparison

The script compares the two datasets to identify players who are both active and have paid their dues.

### 4. Detail Collection

For each matched player, the tool gathers additional details such as email, first name, and last name.

### 5. Progress Tracking

A progress bar is displayed in the console to provide feedback on the data collection process.

### 6. Output

The final data is saved to a CSV file named `eligible_voters_{timestamp}.csv`, where `{timestamp}` is the current date and time in the ISO 8601 format.

## Output Format

The CSV file contains the following columns:

- `ork_id`: The ORK ID of the player.
- `personaName`: The persona name of the player.
- `firstname`: The first name of the player.
- `lastname`: The last name of the player.
- `email`: The email address of the player.
- `ork_url`: The URL to the player's ORK profile.

## Notes

- The tool includes a custom login function and error handling to manage the connection to the ORK.
- It uses the `requests` library for HTTP requests and `BeautifulSoup` for parsing HTML content.
- The script includes a progress bar function for visual feedback during the data collection process.
- Right now this is currently hardcoded to function for the Kingdom of the Golden Plains, but in a future update, I will add a function that allows you to choose a kingdom. For now, you'll need to replace the 11 in 'Kingdom&id=11' with your kingdom's ID number.
- In addition to choosing a kingdom, I also plan to choose a park instead of an entire kingdom.
- The columns in the CSV file were chosen to work seamlessly with Golden Plains' online voting system - [LimeSurvey](https://www.limesurvey.org/).

## Contributing

Contributions to RECAMP are welcome. Please ensure that you test your changes thoroughly before submitting a pull request.

## License

RECAMP has been release under the [GPL-3.0](https://github.com/Hielyr/ork_recamp?tab=readme-ov-file#) license,

## Contact

For questions or issues regarding RECAMP, please open an issue on the GitHub repository.
