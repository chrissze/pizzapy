r"""

    
"""

# STANDARD LIBRARIES

from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime
from io import StringIO
from os.path import basename
from os import environ
from pathlib import Path
from re import search, sub
from subprocess import run
from sys import argv, platform
from typing import List, Optional
from urllib.parse import urlparse


# THIRD PARTY LIBRARIES
from bs4 import BeautifulSoup, ResultSet

from pandas import DataFrame, ExcelWriter, isna, read_html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tenacity import retry, RetryError, stop_after_attempt
from webdriver_manager.chrome import ChromeDriverManager





WP_URL: str = 'https://bet.hkjc.com/ch/racing/wp'

BASE_DIR: Path = Path.cwd().resolve()

PROGRAM: str = basename(argv[0])

HKJC_ENV: Optional[str] = environ.get('HKJC')

NEW_HKJC_ENV: Optional[str] = None  # Will be set if a new HKJC URL is detected at detect_url()

RETRY_TIMES: int = 10


def valid_race(race_str) -> int:
    """
    INDEPENDENT

    USED BY: parse_args
    """
    race = int(race_str)
    if 1 <= race <= 12:
        return race
    else:
        raise ArgumentTypeError(f"Race number must be between 1 and 12. \nYour input: {race_str}")




def valid_url(url_str: str) -> str:
    parsed = urlparse(url_str)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return url_str
    else:
        raise ArgumentTypeError(f"Invalid URL: {url_str}")





def parse_args() -> tuple[Optional[int], bool]:
    """
    DEPENDS: PROGRAM, valid_race

    USED BY: write_excel(due to OPEN_EXCEL, RACE_NUM)
    """
    parser = ArgumentParser(
        description="Parse race arguments",
        usage=f"\n {PROGRAM} <URL>\n {PROGRAM} <race_num> -o \n {PROGRAM} \n {PROGRAM} -o \n {PROGRAM} 3 \n {PROGRAM} 3 -o \n"
    )
    
    parser.add_argument(
        'positional',
        nargs='*',
        help="Race number and optional URL"
    )

    parser.add_argument(
        'race_number',
        nargs='?',
        type=valid_race,
        default=None,
        help="Race number (1-12). Default is current race."
    )

    parser.add_argument(
        'url',
        nargs='?',
        type=valid_url,
        default=None,
        help="Race URL (e.g., https://bet.hkjc.com/...)"
    )

    parser.add_argument(
        '-o',
        '--open',
        action='store_true',
        help="open Excel file"
    )

    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="open in debug mode"
    )

    args = parser.parse_args()

    input_num = None
    input_url = None

    if len(args.positional) == 1:
        try:
            input_num = valid_race(args.positional[0])
        except:
            input_url = valid_url(args.positional[0])

    if len(args.positional) == 2:
        try:
            input_num = valid_race(args.positional[0])
            input_url = valid_url(args.positional[1])
        except:
            input_url = valid_url(args.positional[0])
            input_num = valid_race(args.positional[1])
    
    open_excel: bool = args.open
    debug_mode: bool = args.debug
    return input_num, input_url, open_excel, debug_mode


INPUT_NUM, INPUT_URL, OPEN_EXCEL, DEBUG = parse_args()

    

def inject_to_terminal(var_name, var_value):
    """
    INDEPENDENT
    USED BY: main
    """
    applescript = f'''
    tell application "Terminal"
        do script "export {var_name}='{var_value}'" in window 1
        activate
    end tell
    '''
    run(['osascript', '-e', applescript], check=True)




def set_excel_window_size():
    """
    INDEPENDENT
    USED BY: main
    """
    applescript = '''
    tell application "Microsoft Excel"
        activate
        set bounds of front window to {100, 100, 600, 600}
    end tell
    '''
    run(['osascript', '-e', applescript], check=True)



def replace_race_num(url: str, race_num=None) -> str:
    """
    INDEPENDENT
    
    USED BY: write_excel
    """
    url = url.rstrip('/')  # Remove trailing slash
    if race_num is None:
        return url

    return sub(r'(\/)(\d+)$', rf'\g<1>{race_num}', url)




# Function to get the final redirected URL
def get_redirect_url_html(url, get_source=False) -> tuple[str, str]:
    """
        INDEPENDENT

        USED BY: detect_url, getting_hkjc_url_html

        RETURNS: redirect_url, html_text

        
        --incognito flag ensures the browser starts with a new isolated session, discarding any previous cache/cookies.

        
        This works:
            WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
    
        This does NOT works:
            WebDriverWait(browser, 15).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        Wait for the page to fully load, adjust WebDriverWait timeout as needed, 
        adjust it to larger value will not prolong the process

    """
    print('    .')

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--enable-javascript")
    options.add_argument("--headless=new")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Recommended for running as root
    options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
    options.add_argument("--incognito")  # Start in incognito mode to disable cache

    service=Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(
        options=options, 
        service=service
    )

    html_text = ""
    browser.get(url)

    if get_source:
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        
        # html_text should be placed before redirect_url to load the whole page
        html_text: str = browser.page_source
        
    redirect_url: str = browser.current_url

    browser.quit()
    return redirect_url, html_text




def extracting_iso_date(url) -> Optional[str]:

    """
        INDEPENDENT

        USED BY: getting_hkjc_url_html, detect_url

        https://bet.hkjc.com/ch/racing/wp/2025-03-02/ST/1  -> 2025-03-02
        https://bet.hkjc.com/ch/racing/wp/2025-03-02/ST/1/ -> 2025-03-02
        https://bet.hkjc.com/ch/racing/wp/2025-03-02/ST    -> 2025-03-02
        https://bet.hkjc.com/ch/racing/wp/2025-03-02/ST/   -> 2025-03-02
    """
    # Regex to match 4-digit year, 2-digit month, and 2-digit day
    pattern = r"\b(\d{4}-\d{2}-\d{2})\b"
    match = search(pattern, url)
    if match:
        return match.group(1)
    return None




def extracting_race_num(url) -> Optional[int]:
    """
    INDEPENDENT

    USED BY: getting_hkjc_url_html, detect_url
    
    RETURNS:
        Optional[int]: The extracted race number as an integer, or None if not found.

    def test():
        
        print(extracting_race_num('https://bet.hkjc.com/ch/racing/wp/2025-03-02/ST/1'))
        # 1

        print(extracting_race_num('bet.hkjc.com/ch/racing/wp/2025-03-02/ST/3/'))
        # 3
        
        print(extracting_race_num('http://bet.hkjc.com/ch/racing/wp/2025-03-02/HV/11'))
        #11
        
        print(extracting_race_num('https://bet.hkjc.com/ch/racing/wp/2025-03-02/HV/9/'))
        # 9
            
        print(extracting_race_num('https://bet.hkjc.com/ch/racing/wp/2025-03-02/S1/4'))
        # 4
    """
    pattern = r'/[A-Z]+\d*/(\d+)/?$'
    match = search(pattern, url)
    if match:
        return int(match.group(1))
    return None




def determine_hkjc_env_injection() -> Optional[str]:
    """
    DEPENDS: extracting_race_num, extracting_iso_date

    USED BY: main

    # If RACE_URL is input on command, it will trigger NEW_HKJC_ENV being injected to terminal.
    """
        
    if INPUT_URL:
        race_number_result: Optional[int] = extracting_race_num(INPUT_URL)
        date_result: Optional[str] = extracting_iso_date(INPUT_URL)
    else:
        race_number_result: Optional[int] = None
        date_result: Optional[str] = None
    
    if race_number_result and date_result:
        global NEW_HKJC_ENV
        NEW_HKJC_ENV = INPUT_URL
        return INPUT_URL
    else:
        return None
        
    





def get_df(html_text: str) -> DataFrame:
    """
    INDEPENDENT

    USED BY: getting_hkjc_url_html

    The races folder can be either ST and HV, while ST is compatible to both.

        https://bet.hkjc.com/ch/racing/wp/{wed_iso}/ST/1

        https://bet.hkjc.com/ch/racing/wp/{wed_iso}/HV/1
    """
    
    soup: BeautifulSoup = BeautifulSoup(html_text, 'html.parser')
    soup_tables: ResultSet = soup.find_all('table')

    dfs: List[DataFrame] = read_html(StringIO(html_text), header=None) if soup_tables else []
    
    if dfs:
        df = dfs[0]
        odds = df.iloc[2, -3]

        if isna(odds):
            if DEBUG:
                print("No odds")
            raise ValueError(f"NaN detected in odds.")
        print(df)
        return df
    else:
        return None
    





@retry(stop=stop_after_attempt(RETRY_TIMES)) 
def detect_url() -> str:
    """
    DEPENDS: get_redirect_url_html, extracting_iso_date, extracting_race_num, RETRY_TIMES, WP_URL

    USED BY: write_excel

    if hkjc long url is detected successfully, this function will modify global variable NEW_HKJC_ENV, 
    which will be used to inject HKJC env to the terminal at the end of the program.

    """
    
    hkjc_redirect_url, _ = get_redirect_url_html(WP_URL, get_source=False)

    url_iso_date: Optional[str] = extracting_iso_date(hkjc_redirect_url)
    if url_iso_date is None:
        msg: str = 'URL iso date missing'
        if DEBUG:
            print(msg)
        raise Exception(msg)
    
    url_race_num: Optional[int] = extracting_race_num(hkjc_redirect_url)
    if url_race_num is None:
        msg: str = 'URL race number missing'
        if DEBUG:
            print(msg)
        raise Exception(msg)

    global NEW_HKJC_ENV
    NEW_HKJC_ENV = hkjc_redirect_url
    return hkjc_redirect_url




@retry(stop=stop_after_attempt(RETRY_TIMES)) 
def getting_hkjc_url_html(url=None) -> tuple[str, DataFrame, Optional[str], Optional[int]]:
    """
    DEPENDS: get_redirect_url_html, extracting_iso_date, extracting_race_num, RETRY_TIMES, get_df

    USED BY: write_excel

    """
    processing_url = url if url else WP_URL
    
    hkjc_redirect_url, html_text = get_redirect_url_html(url=processing_url, get_source=True)

    url_iso_date: Optional[str] = extracting_iso_date(hkjc_redirect_url)
    if url_iso_date is None:
        msg: str = 'race iso date missing in the url'
        if DEBUG:
                print(msg)
        raise Exception(msg)
    
    url_race_num: Optional[int] = extracting_race_num(hkjc_redirect_url)
    if url_race_num is None:
        msg: str = 'Invalid race number in the url'
        if DEBUG:
            print(msg)
        raise Exception(msg)

    df: DataFrame = get_df(html_text)
    
    soup = BeautifulSoup(html_text, "html.parser")

    race_ids = [element["id"] for element in soup.find_all(id=True) if element["id"].startswith("raceno_")]

    if not race_ids:
        msg: str = 'race ids missing in the page source'
        if DEBUG:
            print(msg)
        raise Exception(msg)

    return hkjc_redirect_url, df, url_iso_date, url_race_num






def write_excel() -> None:
    """
    DEPENDS: BASE_DIR, RACE_NUM, OPEN_EXCEL, HKJC_ENV, detect_url, replace_race_num, getting_hkjc_url_html, parse_args(due to RACE_NUM, OPEN_EXCEL)

    USED BY: try_write_excel
    """

    if INPUT_NUM:
        if HKJC_ENV:
            redirect_url: str = HKJC_ENV
        else:
            print(f"DETECTING URL ")
            redirect_url: str = detect_url()
        revised_url = replace_race_num(url=redirect_url, race_num=INPUT_NUM)
        
        print(f"\nPROCESSING RACE #{INPUT_NUM} \n\n  {revised_url} \n")        
        print(f"  (start browser)")
        hkjc_redirect_url, df, iso_date, race_num = getting_hkjc_url_html(url=revised_url)
    else:
        processing_url = INPUT_URL if INPUT_URL else WP_URL
        print(f"\n\n\nPROCESSING CURRENT RACE FROM: \n\n  {processing_url}\n")
        print(f"  (start browser)")
        hkjc_redirect_url, df, iso_date, race_num = getting_hkjc_url_html(url=processing_url)

    print(f'\n\n\nFINAL URL: \n\n  {hkjc_redirect_url}\n')
    
    if df is not None:
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        rnum_folder: Path = BASE_DIR / f'R{race_num}'
        excel_file: Path = BASE_DIR / f'R{race_num}'/ f'race_{race_num}.xlsx'
        timed_excel_file: Path = BASE_DIR / f'R{race_num}'/ f'race_{race_num}_{now_str}.xlsx'
        
        Path(rnum_folder).mkdir(parents=True, exist_ok=True)
        
        with ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'race_{race_num}', index=False)
            print(f"SAVED TO:\n\n  {excel_file} \n")

        with ExcelWriter(timed_excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=f'race_{race_num}', index=False)
            print(f"  {timed_excel_file} \n")

        if OPEN_EXCEL:
            from os import system
            system(f'open {excel_file}')

    else:
        print(f"Empty data, no excel file creation.")




def try_write_excel() -> None:
    """
    DEPENDS: write_excel, RETRY_TIMES
    USED BY: main
    """
    try:
        write_excel()
    except RetryError as re:
        print(f'Retried {RETRY_TIMES} times but no data found, the program did not save files.')
    except Exception as e:
        print(f'Error: {e}')





def main() ->  None:
    """
    DEPENDS: try_write_excel, NEW_HKJC_ENV, inject_to_terminal, set_excel_window_size
    """

    print(f'\nH Program ver 3.26\n\n\n')
    print(f'USER INPUTS: \n')
    print(f'    {INPUT_NUM=} \n')
    print(f'    {INPUT_URL=} \n')
    print(f'    {OPEN_EXCEL=} \n')

    if INPUT_NUM and HKJC_ENV:
        print(f'\n\n\nDEFAULT URL FOR NUMBERED RACES: \n')
        print(f'    {HKJC_ENV=} \n\n\n')

    try_write_excel()

    determine_hkjc_env_injection()

    if OPEN_EXCEL and platform == 'darwin':
        try:
            set_excel_window_size()
        except Exception:
            pass

    
    if NEW_HKJC_ENV and platform == 'darwin':
        try:
            inject_to_terminal("HKJC", NEW_HKJC_ENV)
            print(f'\n\nHKJC_ENV IS UPDATED TO: \n\n    {NEW_HKJC_ENV} \n\n')
        except Exception:
            pass




if __name__ == '__main__':
    main()