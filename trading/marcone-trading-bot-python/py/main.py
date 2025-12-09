import sys

sys.path.append(".")
import os
import asyncio
import websockets
from deriv_api import (
    DerivAPI,
    errors,
)
from dotenv import load_dotenv

load_dotenv()

market = "R_10"
stop = False
entry = initial_entry = 1
profit_loss = 0
odd_count = 0
even_count = 0
win_count = 0
loss_count = 0
ask_price = None
account = None
app_id = os.getenv("APP_ID")
api_token = os.getenv("DERIV_TOKEN")
martingale_entries = []

if len(api_token) == 0:
    sys.exit("The environment variable DERIV_TOKEN is not defined")


async def connect():
    url = f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    try:
        connection = await websockets.connect(url)
        return connection
    except Exception as e:
        print("Failed to connect:", e)
        return None


async def martingaleAlgorithm(status, entry, martingale_entries):
    if status == "won":
        martingale_entries = []
        return initial_entry
    if status == "lost":
        martingale_entries.append(entry)
        return sum(martingale_entries) + entry


async def main(
    ask_price,
    win_count,
    loss_count,
    profit_loss,
    stop,
    odd_count,
    even_count,
    entry,
    market,
):

    entry = initial_entry = float(input("Entry: "))
    number_of_repititions = int(input("Number of Repetitions: "))
    goal = int(input("Goal: "))
    stoploss = int(input("Stoploss: "))
    odd_count = 0
    previous_ask_price = None  # Add variable to store the previous price
    ask_price = None
    while True:
        connection = await connect()
        if connection is None:
            return

        api = DerivAPI(connection=connection)
        await api.authorize(api_token)

        while True:
            try:
                ticks = await api.ticks(market)
                account = await api.balance()
                ask_price = ticks.get("tick", {}).get("quote")
                break
            except errors.ResponseError as e:
                if "AlreadySubscribed" in str(e):
                    print(f"Already subscribed to {market}. Restarting connection.")
                    continue
                else:
                    print(f"Error getting ticks for {market}: {e}")
                    break

        last_digit = int(float(ask_price) * 1000) % 10

        # Check if the price is new by comparing with the previous one
        if ask_price == previous_ask_price:
            continue

        # Update the previous price
        previous_ask_price = ask_price
        print(previous_ask_price)

        if last_digit % 2 != 0:
            odd_count += 1
            even_count = 0
            print(f"{odd_count} consecutive odd digits")
        else:
            even_count += 1
            odd_count = 0
            print(f"{even_count} consecutive even digits")
        if odd_count >= number_of_repititions:
            odd_count = 0
            proposal = await api.proposal(
                {
                    "proposal": 1,
                    "amount": entry,
                    "basis": "stake",
                    "contract_type": "DIGITODD",
                    "currency": "USD",
                    "duration": 1,
                    "duration_unit": "t",
                    "symbol": market,
                }
            )
            proposal_id = proposal.get("proposal").get("id")
            buy = await api.buy({"buy": proposal_id, "price": entry})
            contract_id = buy.get("buy").get("contract_id")
            while True:
                poc = await api.proposal_open_contract(
                    {"proposal_open_contract": 1, "contract_id": contract_id}
                )
                status = poc.get("proposal_open_contract", {}).get("status", "")
                if status != "open":
                    break

            if status == "won" or profit_loss == stoploss:
                win_count += 1
                print("Successful operation (win)")
                profit = poc.get("proposal_open_contract", {}).get("profit", 0)
                print(f"Amount won: {profit}")
                profit_loss += float(profit)
                print(f"Current Profit {profit_loss}, Current Balance {account}")
                entry = await martingaleAlgorithm(status, entry, martingale_entries)

            elif status == "lost" or profit_loss == stoploss:
                loss_count += 1
                print("Operation with loss (loss)")
                loss = poc.get("proposal_open_contract", {}).get("profit", 0)
                print(f"Amount lost: {loss}")
                profit_loss += float(loss)
                print(f"Current Profit {profit_loss}, Current Balance {account}")
                entry = await martingaleAlgorithm(status, entry, martingale_entries)

        if even_count >= number_of_repititions:
            even_count = 0
            proposal = await api.proposal(
                {
                    "proposal": 1,
                    "amount": entry,
                    "basis": "stake",
                    "contract_type": "DIGITEVEN",
                    "currency": "USD",
                    "duration": 1,
                    "duration_unit": "t",
                    "symbol": market,
                }
            )
            proposal_id = proposal.get("proposal").get("id")
            buy = await api.buy({"buy": proposal_id, "price": entry})
            contract_id = buy.get("buy").get("contract_id")
            while True:
                poc = await api.proposal_open_contract(
                    {"proposal_open_contract": 1, "contract_id": contract_id}
                )
                status = poc.get("proposal_open_contract", {}).get("status", "")
                if status != "open":
                    break

            if status == "won" or profit_loss == stoploss:
                win_count += 1
                print("Successful operation (win)")
                profit = poc.get("proposal_open_contract", {}).get("profit", 0)
                print(f"Amount won: {profit}")
                profit_loss += float(profit)
                print(f"Current Profit {profit_loss}, Current Balance {account}")
                entry = await martingaleAlgorithm(status, entry, martingale_entries)

            elif status == "lost" or profit_loss == stoploss:
                loss_count += 1
                print("Failed operation (loss)")
                loss = poc.get("proposal_open_contract", {}).get("profit", 0)
                print(f"Amount lost: {loss}")
                profit_loss += float(loss)
                print(f"Current Profit {profit_loss}, Current Balance {account}")
                entry = await martingaleAlgorithm(status, entry, martingale_entries)

        if profit_loss >= goal or profit_loss <= -stoploss or stop:
            if profit_loss >= goal:
                print(f"goal Achieved {profit_loss}")
            elif profit_loss <= -stoploss:
                print(f"Stop Loss {profit_loss}")
            break
        # Resource cleanup
        await connection.close()


asyncio.run(
    main(
        ask_price,
        win_count,
        loss_count,
        profit_loss,
        stop,
        odd_count,
        even_count,
        entry,
        market,
    )
)
