
def update_single_st_core() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            guru_upsert_1s(s)
            zacks_upsert_1s(s)
            option_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def update_single_st_gu() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            guru_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def update_single_st_za() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            zacks_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def update_single_st_op() -> None:
    while True:
        symbol: str = input('Which stock do you want to update (input 0 to quit) ?')
        s = symbol.upper()
        if s == '0':
            break
        elif s in all_stocks:
            option_upsert_1s(s)
        else:
            print('you have entered an invalid symbol')


def op_nasdaq(s: str, d: DictProxy={}) -> Tuple[Optional[float], Optional[float]]:
    lower_code = s.lower()
    pool = Pool(os.cpu_count())
    option_url: str = f"https://www.nasdaq.com/symbol/{lower_code}/option-chain?dateindex=-1"
    print(option_url)
    try:
        option_r: Response = requests.get(option_url)
        bad_status: bool = option_r.status_code != 200

        option_soup: BeautifulSoup = BeautifulSoup(option_r.text, 'html.parser')
        option_soup_items: ResultSet = [] if bad_status else option_soup.find('div', id='OptionsChain-dates')
        option_soup_tags = [] if not option_soup_items else option_soup_items.find_all('a')

        main_urls = [] if not option_soup_tags else [x['href'] for x in option_soup_tags[0:-1]]


        result1 = pool.map(op_calc, main_urls)
        callm1 = sum(cm for cm, _, _ in result1)
        putm1 = sum(pm for _, pm, _ in result1)
        page_urls = list(chain.from_iterable(urls for _, _, urls in result1))

        result2 = pool.map(op_calc, page_urls)
        callm2 = sum(cm for cm, _, _ in result2)
        putm2 = sum(pm for _, pm, _ in result2)

        #print(callm1, putm1, page_urls)
        #print(callm2, putm2)

        callmoney = (callm1 + callm2) * 100.0
        putmoney = (putm1 + putm2) * 100.0

        if all([callmoney, putmoney]):
            d['callmoney'] = round(callmoney, 0)
            d['putmoney'] = round(putmoney, 0)

        return callmoney, putmoney

    except requests.exceptions.RequestException as e:
        print('opt RequestException: ', e)
        return None, None
    except Exception as e2:
        print('opt Exception e2: ', e2)
        return None, None
    finally:  # To make sure processes are closed in the end, even if errors happen
        pool.close()
        


def op_calc(page: str) -> Tuple[float, float, List[str]]:
    try:
        page_r: Response = requests.get(page)
        bad_status: bool = page_r.status_code != 200
        page_dfs: List[DataFrame] = [] if bad_status else pd.read_html(page_r.text, header=0)

        df = pd.DataFrame() if len(page_dfs) < 3 else page_dfs[2]
        cm, pm, page_urls = 0.0, 0.0, []
        if len(df.columns) == 16:
            df.columns = ['Calls', 'CallLast', 'CallChg', 'CallBid', 'CallAsk', 'CallVol', 'CallOI', 'Root', 'Strike',
                          'Puts', 'PutLast', 'PutChg', 'PutBid', 'PutAsk', 'PutVol', 'PutOI']
            df.CallLast = [float0(x) for x in df.CallLast]
            df.CallOI = [float0(x) for x in df.CallOI]
            df.CallVol = df.CallLast * df.CallOI

            df.PutLast = [float0(x) for x in df.PutLast]
            df.PutOI = [float0(x) for x in df.PutOI]
            df.PutVol = df.PutLast * df.PutOI

            cm: float = df.CallVol.sum()
            pm: float = df.PutVol.sum()


        if 'page=' not in page:
            page_soup: BeautifulSoup = BeautifulSoup(page_r.text, 'html.parser')
            page_soup_items: ResultSet = [] if bad_status else page_soup.find('div', id='pagerContainer')
            page_soup_tags = [] if not page_soup_items else page_soup_items.find_all('a')
            page_urls = [] if not page_soup_tags else list(set([x['href'] for x in page_soup_tags]))

        return cm, pm, page_urls

    except requests.exceptions.RequestException as e:
        print('opt calc RequestException: ', e)
        return 0.0, 0.0, []
    except Exception as e2:
        print('opt calc Exception e2: ', e2)
        return 0.0, 0.0, []
