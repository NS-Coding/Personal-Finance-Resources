# utils/rebalancing.py

from utils.config_manager import load_config
from utils.allocation import get_allocations
import datetime

def calculate_rebalancing(current_holdings, amount_to_invest, config=None):
    if config is None:
        config = load_config()
    # Calculate age based on current year and date of birth
    current_year = datetime.datetime.now().year
    date_of_birth = config.get('date_of_birth', 0)
    age = current_year - date_of_birth
    desired_allocations = get_allocations(age, config)
    funds = config['funds']
    # Sum current holdings
    total_current_value = sum(current_holdings.values()) + amount_to_invest
    desired_holdings = {}
    for asset_class in desired_allocations:
        allocation_percentage = desired_allocations[asset_class] / 100
        desired_value = total_current_value * allocation_percentage
        fund_list = funds.get(asset_class, [])
        if not fund_list:
            continue
        for fund_info in fund_list:
            fund_symbol = fund_info['symbol']
            fund_percentage = fund_info['percentage'] / 100
            fund_desired_value = desired_value * fund_percentage
            desired_holdings[fund_symbol] = fund_desired_value
    # Calculate how much to buy of each fund
    amounts_needed = {}
    total_needed = 0
    for fund in desired_holdings:
        current_value = current_holdings.get(fund, 0)
        target_value = desired_holdings[fund]
        amount_needed = target_value - current_value
        if amount_needed > 0:
            amounts_needed[fund] = amount_needed
            total_needed += amount_needed
        else:
            amounts_needed[fund] = 0
    # Adjust amounts to invest based on available amount_to_invest
    amounts_to_invest_per_fund = {}
    if total_needed > 0:
        for fund, amount_needed in amounts_needed.items():
            proportion = amount_needed / total_needed
            amount_to_invest_in_fund = amount_to_invest * proportion
            amounts_to_invest_per_fund[fund] = amount_to_invest_in_fund
    else:
        # Portfolio is already balanced
        for fund in desired_holdings:
            amounts_to_invest_per_fund[fund] = 0
    return amounts_to_invest_per_fund, amounts_needed, age
