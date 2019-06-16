# Ordering Automation

My lab job is to order things. This involves taking information from a Google Sheet to an online ordering form. I've finally decided to automate this process.

## Getting Started

If you also want to automate your ordering download the `automate.py` script. Also, contact me for an example of both the `config.py` file and the Google Sheet being used as the formats for both of these are hard-coded in.

### Prerequisites

**Python packages:**
- `pandas`
- `selenium`
- `gspread`
- `oauth2client`

Use pip or conda to install any of these
```python
pip install pandas selenium gspread oauth2client
conda install pandas selenium gspread oauth2client
```

**Other things:**
- Google Chrome webdriver
  - Get it here
  - You'll also have to point to it's location in the config file

### Installing

Currently this is a one-off script. To use download it and run it like this:

`python automate.py`

Hopefully, I'll package it up nicer in the future :)

## Authors

* **Jeremy Anderson** - *Initial work* - [Biophyser](https://github.com/biophyser)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
