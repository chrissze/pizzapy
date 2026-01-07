

from typing import Dict, List, Union


Contract = Dict[str, Union[float, int, str]]  # type alias

# the drop 1 month is not suitable for FX Futures
fut_dict: Dict[str, Contract] = {
    'ZB': {'exchange': 'CBOT'
           , 'lot': 1000.0
           , 'url': 'https://www.cmegroup.com/trading/interest-rates/us-treasury/30-year-us-treasury-bond'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_us_treasury_bonds_combined_total_reportable_long_positions'
           , 'type': 'treasury'
           , 'name1': 'Treasury Bonds (CBT)'
           , 'name2': 'Treasury Bonds (CBT)'
           , 'monthdrop': 0},
    'ZN': {'exchange': 'CBOT'
           , 'lot': 1000.0
           , 'url': 'https://www.cmegroup.com/trading/interest-rates/us-treasury/10-year-us-treasury-note'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_us_10year_treasury_notes_futures_open_interest'
           , 'type': 'treasury'
           , 'name1': 'Treasury Notes (CBT)'
           , 'name2': 'Treasury Notes (CBT)'
           , 'monthdrop': 0},
    'ZF': {'exchange': 'CBOT'
           , 'lot': 1000.0
           , 'url': 'https://www.cmegroup.com/trading/interest-rates/us-treasury/5-year-us-treasury-note'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_us_5year_treasury_notes_futures_open_interest'
           , 'type': 'treasury'
           , 'name1': '5 Yr. Treasury Notes (CBT)'
           , 'name2': '5 Yr. Treasury Notes (CBT)'
           , 'monthdrop': 0},
    'ZT': {'exchange': 'CBOT'
           , 'lot': 2000.0
           , 'url': 'https://www.cmegroup.com/trading/interest-rates/us-treasury/2-year-us-treasury-note'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_us_2year_treasury_notes_futures_open_interest'
           , 'type': 'treasury'
           , 'name1': '2 Yr. Treasury Notes (CBT)'
           , 'name2': '2 Yr. Treasury Notes (CBT)'
           , 'monthdrop': 0},
    'GE': {'exchange': 'CME'
           , 'lot': 2500.0
           , 'url': 'https://www.cmegroup.com/trading/interest-rates/stir/eurodollar'
           , 'ycharts': 'https://ycharts.com/indicators/cme_3month_eurodollar_futures_open_interest'
           , 'type': 'treasury'
           , 'name1': 'Eurodollar (CME)'
           , 'name2': 'Eurodollar (CME)'
           , 'monthdrop': 0},
    'ZC': {'exchange': 'CBOT'
           , 'lot': 50.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/corn'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_corn_futures_open_interest_ct'
           , 'xls': 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=csv&reportType=P&productId=300'
           , 'type': 'agricultural'
           , 'name1': 'Corn (CBT)'
           , 'name2': 'Corn (CBT)'
           , 'monthdrop': 0},
    'ZL': {'exchange': 'CBOT'
           , 'lot': 600.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean-oil'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_soybean_oil_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Soybean Oil (CBT)'
           , 'name2': 'Soybean Oil (CBT)'
           , 'monthdrop': 0},  # cents
    'ZM': {'exchange': 'CBOT'
           , 'lot': 100.0
           ,  'url': 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean-meal'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_soybean_meal_combined_open_interest'
           , 'type': 'agricultural'
           , 'name1': 'Soybean Meal (CBT)'
           , 'name2': 'Soybean Meal (CBT)'
           , 'monthdrop': 0},  # dollar per ton
    'ZS': {'exchange': 'CBOT'
           , 'lot': 50.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_soybeans_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Soybeans (CBT)'
           , 'name2': 'Soybeans (CBT)'
           , 'monthdrop': 0},
    'ZW': {'exchange': 'CBOT'
           , 'lot': 50.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/grain-and-oilseed/wheat'
           , 'ycharts': 'https://ycharts.com/indicators/cbot_soybean_oil_futures_open_interest_ct' # substitute
           , 'type': 'agricultural'
           , 'name1': 'Wheat (CBT)'
           , 'name2': 'Wheat (CBT)'
           , 'monthdrop': 0}, # cents
    'LE': {'exchange': 'CME'
           , 'lot': 400.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/livestock/live-cattle'
           , 'ycharts': 'https://ycharts.com/indicators/cme_live_cattle_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Cattle-Live (CME)'
           , 'name2': 'Cattle-Live (CME)'
           , 'monthdrop': 0},  # cents
    'GF': {'exchange': 'CME'
           , 'lot': 500.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/livestock/feeder-cattle'
           , 'ycharts': 'https://ycharts.com/indicators/cme_feeder_cattle_futures_open_interest'
           , 'type': 'agricultural'
           , 'name1': 'Cattle-Feeder (CME)'
           , 'name2': 'Cattle-Feeder (CME)'
           , 'monthdrop': 0},  # cents
    'HE': {'exchange': 'CME'
           , 'lot': 400.00
           , 'url': 'https://www.cmegroup.com/trading/agricultural/livestock/lean-hogs'
           , 'ycharts': 'https://ycharts.com/indicators/cme_lean_hogs_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Hogs-Lean (CME)'
           , 'name2': '"Hogs-Lean (CME)'
           , 'monthdrop': 0},  # cents
    'CC': {'exchange': 'ICE'
           , 'lot': 10.0
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_cocoa_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Cocoa (ICE-US)'
           , 'name2': 'Cocoa (NYBOT)'
           , 'monthdrop': 0},
    'CT': {'exchange': 'ICE'
           , 'lot': 500.00
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_cotton_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Cotton (ICE-US)'
           , 'name2': 'Cotton (NYBOT)'
           , 'monthdrop': 0},
    'KC': {'exchange': 'ICE'
           , 'lot': 375.00
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_coffee_c_futures_open_interest'
           , 'type': 'agricultural'
           , 'name1': 'Coffee (ICE-US)'
           , 'name2': 'Coffee (NYBOT)'
           , 'monthdrop': 0},
    'OJ': {'exchange': 'ICE'
           , 'lot': 150.00
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_frozen_concentrated_orange_juice_futures_open_interest'
           , 'type': 'agricultural'
           , 'name1': 'Orange Juice (ICE-US)'
           , 'name2': 'Orange Juice (NYBOT)'
           , 'monthdrop': 0},
    'SB': {'exchange': 'ICE'
           , 'lot': 1120.00
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_sugar_futures_open_interest_ct'
           , 'type': 'agricultural'
           , 'name1': 'Sugar-World (ICE-US)'
           , 'name2': 'Sugar-World (NYBOT)'
           , 'monthdrop': 0},
    'YM': {'exchange': 'CBOT'
           , 'lot': 5.0
           , 'url': 'https://www.cmegroup.com/trading/equity-index/us-index/e-mini-dow'
           , 'ycharts': 'https://ycharts.com/indicators/cme_mini_nasdaq_100_stock_index_futures_open_interest' # substitute
           , 'type': 'index'
           , 'name1': 'Mini DJ Industrial Average (CBT)'
           , 'name2': 'Mini DJ Industrial Average (CBT)'
           , 'monthdrop': 0},  # dollar per ton
    'ES': {'exchange': 'CME'
           , 'lot': 50.0
           , 'url': 'https://www.cmegroup.com/trading/equity-index/us-index/e-mini-sandp500'
           , 'ycharts': 'https://ycharts.com/indicators/cme_mini_nasdaq_100_stock_index_futures_open_interest'  # substitute
           , 'type': 'index'
           , 'name1': 'Mini S '
           , 'name2': 'Mini S '
           , 'monthdrop': 0},  # '&' has weird encoding in html source code
    'NQ': {'exchange': 'CME'
           , 'lot': 20.0
           , 'url': 'https://www.cmegroup.com/trading/equity-index/us-index/e-mini-nasdaq-100'
           , 'ycharts': 'https://ycharts.com/indicators/cme_mini_nasdaq_100_stock_index_futures_open_interest'
           , 'type': 'index'
           , 'name1': 'Mini Nasdaq 100 (CME)'
           , 'name2': 'Mini Nasdaq 100 (CME)'
           , 'monthdrop': 0},
    'DX': {'exchange': 'NYBOT'
           , 'lot': 1000.0
           , 'url': ''
           , 'ycharts': 'https://ycharts.com/indicators/ice_us_dollar_index_futures_open_interest'
           , 'type': 'currency'
           , 'name1': 'U.S. Dollar Index'
           , 'name2': '"U.S. Dollar Index'
           , 'monthdrop': 0},  # for DX 20080924
    '6A': {'exchange': 'CME'
           , 'lot': 100000.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/australian-dollar'
           , 'ycharts': 'https://ycharts.com/indicators/cme_new_zealand_dollar_futures_open_interest' # substitute
           , 'type': 'currency'
           , 'name1': 'Australian Dollar (CME)'
           , 'name2': 'Australian Dollar (CME)'
           , 'monthdrop': 0},
    '6B': {'exchange': 'CME'
           , 'lot': 62500.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/british-pound_quotes'
           , 'ycharts': 'https://ycharts.com/indicators/cme_british_pound_sterling_futures_open_interest'
           , 'type': 'currency'
           , 'name1': 'British Pound (CME)'
           , 'name2': 'British Pound (CME)'
           , 'monthdrop': 0},
    '6C': {'exchange': 'CME'
           , 'lot': 100000.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/canadian-dollar'
           , 'ycharts': 'https://ycharts.com/indicators/cme_new_zealand_dollar_futures_open_interest' # substitute
           , 'type': 'currency'
           , 'name1': 'Canadian Dollar (CME)'
           , 'name2': 'Canadian Dollar (CME)'
           , 'monthdrop': 0},
    '6E': {'exchange': 'CME'
           , 'lot': 125000.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/euro-fx'
           , 'ycharts': 'https://ycharts.com/indicators/cme_euro_fx_futures_open_interest'
           , 'type': 'currency'
           , 'name1': 'Euro (CME)'
           , 'name2': 'Euro (CME)'
           , 'monthdrop': 0},
    '6J': {'exchange': 'CME'
           , 'lot': 12500000.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/japanese-yen'
           , 'ycharts': 'https://ycharts.com/indicators/cme_japanese_yen_futures_open_interest'
           , 'type': 'currency'
           , 'name1': 'Japanese Yen (CME)'
           , 'name2': 'Japanese Yen (CME)'
           , 'monthdrop': 0},
    '6S': {'exchange': 'CME'
           , 'lot': 125000.0
           , 'url': 'https://www.cmegroup.com/trading/fx/g10/swiss-franc'
           , 'ycharts': 'https://ycharts.com/indicators/cme_swiss_franc_futures_dealer_long_positions'
           , 'type': 'currency'
           , 'name1': 'Swiss Franc (CME)'
           , 'name2': 'Swiss Franc (CME)'
           , 'monthdrop': 0},
    'GC': {'exchange': 'NYMEX'
           , 'lot': 100.0
           , 'url': 'https://www.cmegroup.com/trading/metals/precious/gold'
           , 'ycharts': 'https://ycharts.com/indicators/comex_gold_futures_open_interest'
           , 'cmeid': '437'
           , 'type': 'metal'
           , 'name1': 'Gold (CMX)'
           , 'name2': 'Gold (CMX)'
           , 'monthdrop': 0},
    'SI': {'exchange': 'NYMEX'
           , 'lot': 5000.0
           , 'url': 'https://www.cmegroup.com/trading/metals/precious/silver'
           , 'ycharts': 'https://ycharts.com/indicators/comex_silver_futures_open_interest'
           , 'type': 'metal'
           , 'name1': 'Silver (CMX)'
           , 'name2': 'Silver (CMX)'
           , 'monthdrop': 0},  # some dollar some cents
    'HG': {'exchange': 'NYMEX'
           , 'lot': 25000.0
           , 'url': 'https://www.cmegroup.com/trading/metals/base/copper'
           , 'ycharts': 'https://ycharts.com/indicators/comex_grade_1_copper_futures_open_interest'
           , 'type': 'metal'
           , 'name1': 'Copper-High (CMX)'
           , 'name2': 'Copper-High (CMX)'
           , 'monthdrop': 0},  # some dollar some cents
    'PA': {'exchange': 'NYMEX'
           , 'lot': 100.0
           , 'url': 'https://www.cmegroup.com/trading/metals/precious/palladium'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_palladium_futures_open_interest'
           , 'type': 'metal'
           , 'name1': 'Palladium (NYM)'
           , 'name2': 'Palladium (NYM)'
           , 'monthdrop': 0},
    'PL': {'exchange': 'NYMEX'
           , 'lot': 50.0
           , 'url': 'https://www.cmegroup.com/trading/metals/precious/platinum'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_platinum_futures_open_interest_ct'
           , 'type': 'metal'
           , 'name1': 'Platinum (NYM)'
           , 'name2': 'Platinum (NYM)'
           , 'monthdrop': 0},
    'CL': {'exchange': 'NYMEX'
           , 'lot': 1000.0
           , 'url': 'https://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_light_sweet_crude_oil_futures_open_interest'
           , 'type': 'energy'
           , 'name1': 'Crude Oil , Light Sweet (NYM)'
           , 'name2': 'Crude Oil , Light Sweet (NYM)'
           , 'monthdrop': 1},  # cme_id: '425'
    'HO': {'exchange': 'NYMEX'
           , 'lot': 42000.0
           , 'url': 'https://www.cmegroup.com/trading/energy/refined-products/heating-oil'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_natural_gas_futures_open_interest_ct' # substitute
           , 'type': 'energy'
           , 'name1': 'NY Harbor ULSD (NYM)'
           , 'name2': 'Heating Oil No. 2 (NYM)'
           , 'monthdrop': 0},
    'NG': {'exchange': 'NYMEX'
           , 'lot': 10000.0
           , 'url': 'https://www.cmegroup.com/trading/energy/natural-gas/natural-gas'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_natural_gas_futures_open_interest_ct'
           , 'type': 'energy'
           , 'name1': 'Natural Gas (NYM)'
           , 'name2': 'Natural Gas (NYM)'
           , 'monthdrop': 0},
    'RB': {'exchange': 'NYMEX'
           , 'lot': 42000.0
           , 'url': 'https://www.cmegroup.com/trading/energy/refined-products/rbob-gasoline'
           , 'ycharts': 'https://ycharts.com/indicators/nymex_natural_gas_futures_open_interest_ct' # substitute
           , 'type': 'energy'
           , 'name1': 'Gasoline-NY RBOB (NYM)'
           , 'name2': 'Gasoline-NY RBOB (NYM)'
           , 'monthdrop': 0}}    # 'Brent Crude (ICE) 'Brent Crude (ICE-EU)


all_fut: List[str] = sorted(list(fut_dict.keys()))


def getfutures(typestr: str) -> List[str]:
    if typestr == 'allfutures':
        all_future_contracts: List[str] = [(k + ' - ' + v.get('name1')) for k, v in fut_dict.items()]
        return sorted(all_future_contracts)
    else:
        filtered: List[str] = [(k + ' - ' + v.get('name1')) for k, v in fut_dict.items() if v.get('type') == typestr]
        return sorted(filtered)


def getfutcode(typestr: str) -> List[str]:
    if typestr == 'allfutures':
        return all_fut
    else:
        filtered: List[str] = [k for k, v in fut_dict.items() if v.get('type') == typestr]
        return filtered


fut_type_list: List[str] = ['allfutures', 'agricultural', 'currency', 'energy'
                            , 'index', 'metal', 'treasury']



if __name__ == '__main__':
    print('aaa')

