import requests
from bs4 import BeautifulSoup
import zipfile
import io
import re
import pandas as pd

def get_fama_french_5_factor_url():
    """
    Scrapes Kenneth French's data library page to locate the URL for the Fama–French 5 Factor daily data.
    
    Returns:
        str: The full URL to the zip file containing the daily data.
    """
    base_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/"
    library_url = base_url + "data_library.html"
    response = requests.get(library_url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve the data library page from Kenneth French's website.")
    
    soup = BeautifulSoup(response.content, "html.parser")
    target_url = None
    # Look for an <a> tag whose href likely points to the 5 Factor daily data zip file.
    for a in soup.find_all("a", href=True):
        href = a['href']
        # Check for keywords indicating the daily data file.
        if "5_Factors" in href and "daily" in href.lower() and href.endswith(".zip"):
            target_url = base_url + href if not href.startswith("http") else href
            break
    if target_url is None:
        raise Exception("Unable to locate the Fama–French 5 Factor daily data file link on the page.")
    return target_url

def download_fama_french_5_factors(start_date='1990-01-01'):
    """
    Downloads and processes the historical daily Fama–French 5 Factor data from Kenneth French's website.
    
    This file does not have a labeled header row. Instead, every valid data row starts with an 8-digit date.
    We assume that the file’s columns appear in the following order:
    
      1. Date (YYYYMMDD)
      2. Mkt-RF (market premium; we rename this to "MKT")
      3. SMB
      4. HML
      5. RMW
      6. CMA
      7. RF (the risk-free rate)
    
    Factor values (columns 2–6) and RF (column 7) are originally in percentages. Here, we convert them 
    to decimals. For portfolio construction, we later use only the five factor columns (dropping RF).
    
    Args:
        start_date (str): Only data on or after this date (YYYY-MM-DD) will be returned.
    
    Returns:
        DataFrame: A pandas DataFrame indexed by date with columns:
                   ['MKT', 'SMB', 'HML', 'RMW', 'CMA', 'RF']
    """
    url = get_fama_french_5_factor_url()
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download the Fama–French 5 Factor data from the URL.")
    
    # Open the ZIP file from the downloaded bytes.
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Look for any file ending with .txt in the ZIP archive.
        filename = next((name for name in z.namelist() if name.endswith(".txt")), None)
        if filename is None:
            raise Exception("No .txt file found in the downloaded zip archive.")
        with z.open(filename) as f:
            all_lines = f.read().decode('latin-1').splitlines()
    
    # Use a regular expression to select lines that begin with an 8-digit number.
    date_regex = re.compile(r"^\d{8}")
    data_lines = [line for line in all_lines if date_regex.match(line.strip())]
    if not data_lines:
        raise Exception("No data lines were found that match the expected date format.")
    
    # Join the selected lines; these lines contain our data rows.
    data_str = "\n".join(data_lines)
    
    # Manually specify the column names.
    # Note: The file has 7 columns: Date, Mkt-RF, SMB, HML, RMW, CMA, RF.
    col_names = ["Date", "Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]
    df = pd.read_csv(io.StringIO(data_str), 
                     delim_whitespace=True, 
                     header=None, 
                     names=col_names)
    
    # Robustness: keep only rows where the Date column appears to be an 8-digit number.
    df = df[df["Date"].astype(str).str.len() == 8]
    
    # Convert the Date column to datetime objects and set it as the index.
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
    df.set_index("Date", inplace=True)
    
    # Rename "Mkt-RF" to "MKT" for clarity and retain the other columns.
    rename_map = {
        "Mkt-RF": "MKT",
        "SMB": "SMB",
        "HML": "HML",
        "RMW": "RMW",
        "CMA": "CMA",
        "RF": "RF"
    }

    df.drop(columns="RF", inplace=True)
    
    # Convert the factor columns from percentages to decimals.
    # Note: You may consider dropping "RF" later if it's not needed in portfolio construction.
    df = df.astype(float) / 100.0
    df.rename(columns=rename_map, inplace=True)
    
    # Filter for data on or after the specified start_date.
    factors = df[df.index >= pd.to_datetime(start_date)]
    
    return factors

if __name__ == "__main__":
    factors = download_fama_french_5_factors()
    print(factors.head())