
import asyncio

from dataclasses import dataclass

import logging

import sys

from typing import Optional




from tenacity import retry, stop_after_attempt, wait_fixed

from ib_async import IB

from ib_async.contract import Option, Stock

from ib_async.objects import OptionChain


HOST: str = '127.0.0.1' if sys.platform == 'linux' else 'fuji.220122.xyz'
    
PORT: int = 4001

CLIENT_ID: int = 1



# target IB loggers to suppress non-critical error messages:
logging.getLogger("ib_async").setLevel(logging.CRITICAL)

logging.getLogger("ibapi").setLevel(logging.CRITICAL)


# order=True means that the object can be sorted, order by contract, then premium, oi, money
@dataclass(order=True)
class OptionPosition:
    localSymbol: str   # e.g. "NVDA 20280121C700", same .localSymbol property name as in Option class
    premium: float | None  # price per contract
    oi: float | None      # open interest
    money: float    # total money involved (your own meaning)
    option_key: Option    



async def get_expiries_and_strikes_async(symbol: str, ib: IB) -> tuple[list[str] | None, list[float] | None]:
    """
    INDEPENDENT

    USED BY: get_all_option_positions_async
    """

    handcrafted_stock: Stock = Stock(symbol, "SMART", "USD")

    qualified_stock_list = None

    qualified_stock_list: list[Stock] = await ib.qualifyContractsAsync(handcrafted_stock)

    if not qualified_stock_list or qualified_stock_list[0] is None:  # order is important
        return None, None
    
    qualified_stock: Stock = qualified_stock_list[0]
    
    params_list = None

    params_list: list[OptionChain] = await ib.reqSecDefOptParamsAsync(
        qualified_stock.symbol,   # same as symbol, e.g. "META"
        "",                  # futFopExchange (empty for stocks)
        qualified_stock.secType,  # "STK"
        qualified_stock.conId,
    )

    if not params_list:
        return None, None

    option_chain_expiries: set[str] = { x for param in params_list for x in param.expirations }

    sorted_expiries: list[str] = sorted(list(option_chain_expiries))

    option_chain_strikes: set[float] = { x for param in params_list for x in param.strikes }

    sorted_strikes: list[float] = sorted(list(option_chain_strikes))

    return sorted_expiries, sorted_strikes
    # END OF get_expiries_and_strikes_async()





class ContractNotFound(Exception):
    """More specific Exception"""
    pass

@retry(stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)     
async def get_single_qualified_option_async(option: Option, ib: IB) -> Option: 
    
    
    # If IB can’t find a matching contract, this will be [None]
    qualified_list = await ib.qualifyContractsAsync(option)

    if not qualified_list or qualified_list[0] is None:
        raise ContractNotFound()
    
    return qualified_list[0]
    # END OF get_single_qualified_option_async()




async def steward(coroutine_func, semaphore):
    """
    USED BY: get_all_money

    steward is a semaphore worker
    """
    async with semaphore:
        return await coroutine_func


async def ensure_connected(ib: IB, readonly: bool) -> None:
    """
    No default readonly value to force caller to supply a readonly value.
    """
    if ib.isConnected():
        return

    try:
        ib.disconnect()
        await asyncio.sleep(0.2)
    except:
        pass

    await ib.connectAsync(HOST, PORT, clientId=CLIENT_ID, timeout=10, readonly=readonly)
    print('DISCONNECT and CONNECT AGAIN IN ensure_connected')
    if readonly:
        
        ib.reqMarketDataType(3)

    




async def get_contract_oi_async(option: Option, ib: IB) -> OptionPosition | None:

    """
    DEPENDS:

    USED BY:
    """
    
    data_ready = asyncio.Event()
    
    def on_tick(ticker_obj):
        if option.right == 'C':
            condition_met = str(ticker_obj.close) != 'nan' and str(ticker_obj.callOpenInterest) != 'nan'
        else:
            condition_met = str(ticker_obj.close) != 'nan' and str(ticker_obj.putOpenInterest) != 'nan'
            
        if condition_met:
            data_ready.set()
    
    ticker = None
    
    try: 
            
        # Request market data including generic ticks
        # 100 = option volume, 101 = option open interest
        ticker = ib.reqMktData(option, genericTickList='100,101')    
        
        ticker.updateEvent += on_tick
        
        await asyncio.wait_for(data_ready.wait(), timeout=5)
        
    except:
        return None    
            
    finally:
        # Prefer two separate try blocks so one cleanup failure doesn’t skip the other.
        try:
            if ticker is not None:
                ticker.updateEvent -= on_tick
        except Exception:
            pass
        try:
            if ticker is not None:
                ib.cancelMktData(option)
        except Exception:
            pass




    premium: float | None = float(ticker.close) if ticker.close is not None else None

    if option.right == "C":
        oi: float | None = float(ticker.callOpenInterest) if ticker.callOpenInterest is not None else None
        
    elif option.right == "P":
        oi: float | None = float(ticker.putOpenInterest) if ticker.putOpenInterest is not None else None
    else:
        oi: float | None = None

    if premium is not None and oi is not None: 
        contract_money: float = round(oi * 100.0 * premium)

        position = OptionPosition(localSymbol=option.localSymbol, premium=premium, oi=oi, money=contract_money, option_key=option)

        print(position)

        return position
    else:
        return None
    # END OF get_contract_oi_async(option, ib)










async def gather_positions_async(call_options: list[Option], put_options: list[Option]) -> Any:
    """
    DEPENDS: 

    USED BY: 

    """

    working_calls: list[Option] = call_options.copy()

    working_puts: list[Option] = put_options.copy()

    print(f'INITIAL working_calls length: {len(working_calls)}')

    print(f'INITIAL working_puts length: {len(working_puts)}')

    finished_calls_dict: dict = {}
    
    finished_puts_dict: dict = {}

    sem_num = 25


    while working_calls:
        
        ib = IB()

        # clientId here must be differ from the clientID in main()    
        await ib.connectAsync(HOST, PORT, clientId=sem_num, timeout=10, readonly=True)

        ib.reqMarketDataType(3)   # 3 = delayed

        print(f'{sem_num=}')
        
        sem = asyncio.Semaphore(sem_num)    

        print(f'INITIAL working_calls length in the while loop: {len(working_calls)}')

        print(f'INITIAL finished calls in the while loop: {len(finished_calls_dict)}')

        call_option_tasks = [ get_contract_oi_async(option, ib) for option in working_calls ]
    
        call_wrapped = [ steward(coro, sem) for coro in call_option_tasks ]

        call_position_list: list[OptionPosition | None | Exception] = await asyncio.gather(*call_wrapped, return_exceptions=True)

        print(call_position_list)
        


        successful_call_positions: list[OptionPosition] = [ x for x in call_position_list if isinstance(x, OptionPosition) ]


        for position in successful_call_positions:
            finished_calls_dict[position.localSymbol] = position

        # filter working calls
        working_calls: list[Option] = [ x for x in working_calls if x.localSymbol not in finished_calls_dict.keys() ]
        
        print(f'\n\n\n\nEND LOOP successful positions:\n\n', len(successful_call_positions))

        print(f'\n\n\n\nEND LOOP working calls:\n\n', len(working_calls))

        ib.disconnect()

        if len(successful_call_positions) == 0:
            
            break


    print(f'working_calls length: {len(working_calls)}')

    print(f'finished_calls_dict length: {len(finished_calls_dict)}')



    sem_num = 25

    while working_puts:
        #await ensure_connected(ib, readonly=True)

        ib = IB()
        
        await ib.connectAsync(HOST, PORT, clientId=sem_num, timeout=10, readonly=True)

        ib.reqMarketDataType(3)

        print(f'{sem_num=}')
        
        sem = asyncio.Semaphore(sem_num)    
    
        print(f'INITIAL working_puts length in the while loop: {len(working_puts)}')

        put_option_tasks = [ get_contract_oi_async(option, ib) for option in working_puts ]
    
        put_wrapped = [ steward(coro, sem) for coro in put_option_tasks ]

        put_position_list: list[OptionPosition | None | Exception] = await asyncio.gather(*put_wrapped, return_exceptions=True)


        successful_put_positions: list[OptionPosition] = [ x for x in put_position_list if isinstance(x, OptionPosition) ]

        for position in successful_put_positions:
            finished_puts_dict[position.localSymbol] = position

        working_puts: list[Option] = [ x for x in working_puts if x.localSymbol not in finished_puts_dict.keys() ]
        
        print(f'\n\n\n\nEND LOOP successful positions:\n\n', len(successful_put_positions))

        print(f'\n\n\n\nEND LOOP working_puts:\n\n', len(working_puts))


        ib.disconnect()

        if len(successful_put_positions) == 0:
            break

        


    call_position_list = list(finished_calls_dict.values())
    
    put_option_list =  list(finished_puts_dict.values())

    return call_position_list, put_option_list 
    # END OF gather_positions_async(call_options, put_options)







async def get_all_option_positions_async(symbol:str, ib: IB) -> tuple[list, list]:
    """
    DEPENDS: gather_positions_async, runner

    USED BY: main
    """
    

    try:
        #await ensure_connected(ib, readonly=True)

        expiries, strikes = await get_expiries_and_strikes_async(symbol, ib)

        # LIMTED expirations during development
        #expiries = [x for x in expiries if x.startswith('20251219') ]

    except Exception as e:
        print(f"Got error when retriving expiries and strikes {e}")

    sem = asyncio.Semaphore(20)    

    all_qualified_calls = []

    all_qualified_puts = []

    all_call_positions = []

    all_put_positions = []
    
    for expiry in expiries:
        

        handcrafted_call_options: list[Option] = [Option(symbol=symbol, lastTradeDateOrContractMonth=expiry, strike=strike, right='C', exchange='SMART') for strike in strikes ]

        call_option_tasks = [ get_single_qualified_option_async(option, ib) for option in handcrafted_call_options ]


        call_wrapped = [steward(coro, sem) for coro in call_option_tasks]

        call_option_list: list[Optional[Option]] = await asyncio.gather(*call_wrapped, return_exceptions=True)

        qualified_call_options_this_expiry: list[Option] = [x for x in call_option_list if isinstance(x, Option) ]

        all_qualified_calls += qualified_call_options_this_expiry



        handcrafted_put_options: list[Option] = [Option(symbol=symbol, lastTradeDateOrContractMonth=expiry, strike=strike, right='P', exchange='SMART') for strike in strikes ]

        put_option_tasks = [ get_single_qualified_option_async(option, ib) for option in handcrafted_put_options]

        put_wrapped = [steward(coro, sem) for coro in put_option_tasks]
    
        put_option_list: list[Optional[Option]] = await asyncio.gather(*put_wrapped, return_exceptions=True)

        qualified_put_options_this_expiry: list[Option] = [x for x in put_option_list if isinstance(x, Option) ]

        all_qualified_puts += qualified_put_options_this_expiry



        try:
            call_positions_this_expiry, put_positions_this_expiry = await gather_positions_async(qualified_call_options_this_expiry, qualified_put_options_this_expiry)

            all_call_positions += call_positions_this_expiry

            all_put_positions += put_positions_this_expiry

        except Exception as e:
            print(f'gather error: {e} ')

    return all_call_positions, all_put_positions 
    # END OF get_all_option_positions_async()








    

    
async def get_option_ratio_async(symbol: str, ib: IB) -> tuple[float, float, float, float]:

    """
    
    DEPENDS: 

    """
  
    
    call_positions, put_positions = await get_all_option_positions_async(symbol, ib)

    # PROGRAM WILL WAIT HERE UNTILL get_all_option_contracts_async DONE.

    call_money = sum([ x.money for x in call_positions ])

    put_money = sum([ x.money for x in put_positions ])


    call_oi = sum([ x.oi for x in call_positions ])

    put_oi = sum([ x.oi for x in put_positions ])


    print(f'total call positions length: {len(call_positions)}')

    print(f'total put positions length: {len(put_positions)}')


    return call_money, put_money, call_oi, put_oi
    # END OF get_option_ratio_async(symbol, ib)





async def main() -> None:

    """
    
    DEPENDS: 

    """
    

    SYMBOL: str = 'AMC'

    ib_client = IB()
    
    await ib_client.connectAsync(HOST, PORT, clientId=CLIENT_ID, timeout=10, readonly=True)

    ib_client.reqMarketDataType(3)   # 3 = delayed


    try:
        call_money, put_money, call_oi, put_oi = await get_option_ratio_async(SYMBOL, ib_client)


        print(f'{call_money=}')
        print(f'{put_money=}')
        print(f'{call_oi=}')
        print(f'{put_oi=}')

    except Exception as e:

        print(f"Got error {e}")

    ib_client.disconnect()

    # END OF main()




    
if __name__ == "__main__":
    asyncio.run(main())
