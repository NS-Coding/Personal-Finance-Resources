# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from utils.config_manager import load_config, save_config, get_available_funds
from utils.allocation import get_allocations
from utils.rebalancing import calculate_rebalancing
import datetime
import yfinance as yf
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.context_processor
def inject_fund_info():
    fund_id = request.args.get('fund_id')
    available_funds = get_available_funds()
    fund_name = None
    if fund_id:
        try:
            config = load_config(fund_id)
            fund_name = config.get('fund_name', fund_id)
        except:
            fund_name = fund_id
    elif available_funds:
        fund_id = available_funds[0]['id']
        fund_name = available_funds[0]['name']
    return dict(fund_id=fund_id, fund_name=fund_name, available_funds=available_funds)

@app.route('/')
def home():
    fund_id = request.args.get('fund_id')
    available_funds = get_available_funds()
    if not available_funds:
        return redirect(url_for('edit_config'))
    if not fund_id:
        fund_id = available_funds[0]['id']
    try:
        config = load_config(fund_id)
        fund_name = config.get('fund_name', fund_id)
    except Exception as e:
        flash(f'Error loading configuration: {e}', 'danger')
        return redirect(url_for('edit_config'))

    return render_template('home.html', fund_name=fund_name, fund_id=fund_id, available_funds=available_funds)


@app.route('/edit_config', methods=['GET', 'POST'])
def edit_config():
    fund_id = request.args.get('fund_id')
    available_funds = get_available_funds()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Load':
            fund_id = request.form.get('fund_id')
            return redirect(url_for('edit_config', fund_id=fund_id))
        elif action == 'Create':
            new_fund_name = request.form.get('new_fund_name')
            if not new_fund_name:
                flash('Please enter a name for the new fund.', 'danger')
                return redirect(url_for('edit_config'))
            # Generate a unique fund ID
            fund_id = new_fund_name.replace(' ', '_')
            # Ensure the fund_id is unique
            existing_fund_ids = [fund['id'] for fund in available_funds]
            if fund_id in existing_fund_ids:
                flash(f'A fund with the name "{new_fund_name}" already exists. Please choose a different name.', 'danger')
                return redirect(url_for('edit_config'))
            # Create a default configuration for the new fund
            config = {
                'fund_name': new_fund_name,
                'date_of_birth': 1990,
                'funds': {
                    'us_stock': [],
                    'intl_stock': [],
                    'us_bond': [],
                    'intl_bond': [],
                    'short_term_tips': []
                },
                'glide_path': []
            }
            save_config(config, fund_id)
            flash(f'New fund "{new_fund_name}" created successfully!', 'success')
            return redirect(url_for('edit_config', fund_id=fund_id))
        elif action == 'Save':
            try:
                fund_id = request.form.get('fund_id')
                config = load_config(fund_id)
                asset_class_names = {
                    'us_stock': 'United States Stock',
                    'intl_stock': 'International Stock',
                    'us_bond': 'United States Bond',
                    'intl_bond': 'International Bond',
                    'short_term_tips': 'Short-Term TIPS'
                }
                # Update date of birth
                date_of_birth = int(request.form['date_of_birth'])
                config['date_of_birth'] = date_of_birth

                # Update funds
                for asset_class in config['funds'].keys():
                    symbols = request.form.getlist(f'{asset_class}_symbol')
                    percentages = request.form.getlist(f'{asset_class}_percentage')
                    funds = []
                    total_percentage = 0
                    for symbol, percentage in zip(symbols, percentages):
                        if symbol.strip():
                            fund_percentage = float(percentage)
                            funds.append({'symbol': symbol.strip(), 'percentage': fund_percentage})
                            total_percentage += fund_percentage
                    if abs(total_percentage - 100) > 0.01:
                        flash(f'The total percentage for {asset_class_names[asset_class]} must equal 100%. Currently, it is {total_percentage}%.', 'danger')
                        return redirect(url_for('edit_config', fund_id=fund_id))
                    config['funds'][asset_class] = funds

                # Update glide path
                glide_path = []
                ages = request.form.getlist('age')
                us_stock = request.form.getlist('us_stock')
                intl_stock = request.form.getlist('intl_stock')
                us_bond = request.form.getlist('us_bond')
                intl_bond = request.form.getlist('intl_bond')
                short_term_tips = request.form.getlist('short_term_tips')
                for idx in range(len(ages)):
                    allocations = {
                        'us_stock': float(us_stock[idx]),
                        'intl_stock': float(intl_stock[idx]),
                        'us_bond': float(us_bond[idx]),
                        'intl_bond': float(intl_bond[idx]),
                        'short_term_tips': float(short_term_tips[idx])
                    }
                    total_alloc = sum(allocations.values())
                    if abs(total_alloc - 100) > 0.01:
                        flash(f'The total allocation percentages at age {ages[idx]} must equal 100%. Currently, it is {total_alloc}%.', 'danger')
                        return redirect(url_for('edit_config', fund_id=fund_id))
                    glide_path.append({
                        'age': int(ages[idx]),
                        'allocations': allocations
                    })
                config['glide_path'] = glide_path

                # Save updated config
                save_config(config, fund_id)
                flash('Configuration updated successfully!', 'success')
                return redirect(url_for('edit_config', fund_id=fund_id))
            except Exception as e:
                flash(f'Error updating configuration: {e}', 'danger')
                return redirect(url_for('edit_config', fund_id=fund_id))
    else:
        if fund_id:
            try:
                config = load_config(fund_id)
                asset_class_names = {
                    'us_stock': 'United States Stock',
                    'intl_stock': 'International Stock',
                    'us_bond': 'United States Bond',
                    'intl_bond': 'International Bond',
                    'short_term_tips': 'Short-Term TIPS'
                }
                return render_template('edit_config.html', config=config, asset_class_names=asset_class_names)
            except Exception as e:
                flash(f'Error loading configuration: {e}', 'danger')
                return redirect(url_for('edit_config'))
        else:
            # No fund selected, render the fund selection page
            return render_template('edit_config_select.html', available_funds=available_funds)
    return render_template('edit_config_select.html', available_funds=available_funds)

@app.route('/rebalance', methods=['GET', 'POST'])
def rebalance():
    fund_id = request.args.get('fund_id')
    if not fund_id:
        available_funds = get_available_funds()
        if available_funds:
            fund_id = available_funds[0]['id']
        else:
            flash('No funds available. Please create a fund first.', 'danger')
            return redirect(url_for('edit_config'))
    try:
        config = load_config(fund_id)
        fund_name = config.get('fund_name', fund_id)
    except Exception as e:
        flash(f'Error loading configuration: {e}', 'danger')
        return redirect(url_for('edit_config'))

    fund_list = []
    for funds in config['funds'].values():
        for fund_info in funds:
            fund_list.append(fund_info['symbol'])
    if request.method == 'POST':
        try:
            amount_to_invest = float(request.form['amount_to_invest'])
            current_holdings_input = request.form.get('current_holdings', {})
            current_holdings = {}
            for fund in fund_list:
                value = request.form.get(f"current_holdings[{fund}]")
                if value is not None:
                    current_holdings[fund] = float(value)
                else:
                    current_holdings[fund] = 0.0
            amounts_to_invest, amounts_needed, age = calculate_rebalancing(current_holdings, amount_to_invest, config)
            return render_template('rebalance.html', amounts=amounts_to_invest, amounts_needed=amounts_needed, age=age, fund_name=fund_name, fund_id=fund_id)
        except Exception as e:
            flash(f'Error in rebalancing: {e}', 'danger')
            return redirect(url_for('rebalance', fund_id=fund_id))
    return render_template('rebalance.html', amounts=None, fund_list=fund_list, fund_name=fund_name, fund_id=fund_id)

@app.route('/plot')
def plot():
    fund_id = request.args.get('fund_id')
    if not fund_id:
        available_funds = get_available_funds()
        if available_funds:
            fund_id = available_funds[0]['id']
        else:
            flash('No funds available. Please create a fund first.', 'danger')
            return redirect(url_for('edit_config'))
    try:
        config = load_config(fund_id)
        fund_name = config.get('fund_name', fund_id)
    except Exception as e:
        flash(f'Error loading configuration: {e}', 'danger')
        return redirect(url_for('edit_config'))

    if not config['glide_path']:
        flash('Glide path is empty. Please configure it first.', 'danger')
        return redirect(url_for('edit_config', fund_id=fund_id))

    # Sort glide path entries by age to ensure correct interpolation
    config['glide_path'] = sorted(config['glide_path'], key=lambda x: x['age'])

    ages = list(range(15, 96))  # Age range from 15 to 95
    allocation_keys = config['glide_path'][0]['allocations'].keys()
    allocations_over_age = {key: [] for key in allocation_keys}
    for age in ages:
        allocations = get_allocations(age, config)
        for key in allocations_over_age:
            allocations_over_age[key].append(allocations.get(key, 0))
    return render_template('plot.html', ages=ages, allocations_over_age=allocations_over_age, fund_name=fund_name, fund_id=fund_id)

@app.route('/fund_performance')
def fund_performance():
    fund_id = request.args.get('fund_id')
    if not fund_id:
        available_funds = get_available_funds()
        if available_funds:
            fund_id = available_funds[0]['id']
        else:
            flash('No funds available. Please create a fund first.', 'danger')
            return redirect(url_for('edit_config'))
    try:
        config = load_config(fund_id)
        fund_name = config.get('fund_name', fund_id)
    except Exception as e:
        flash(f'Error loading configuration: {e}', 'danger')
        return redirect(url_for('edit_config'))

    fund_symbols = []
    for funds in config['funds'].values():
        for fund_info in funds:
            fund_symbols.append(fund_info['symbol'])
    performance_data, historical_data = get_fund_performance(fund_symbols, config)
    return render_template('fund_performance.html', performance_data=performance_data, historical_data=historical_data, fund_symbols=fund_symbols, fund_name=fund_name, fund_id=fund_id)

def get_fund_performance(fund_symbols, config):
    data = {}
    historical_data = {}
    # Calculate current age
    current_year = datetime.datetime.now().year
    date_of_birth = config.get('date_of_birth', 0)
    age = current_year - date_of_birth
    # Get current allocations
    current_allocations = get_allocations(age, config)
    # Build a mapping from fund symbol to allocation percentage
    fund_allocations = {}
    for asset_class, allocation_percentage in current_allocations.items():
        funds = config['funds'].get(asset_class, [])
        for fund_info in funds:
            symbol = fund_info['symbol']
            fund_percentage = fund_info['percentage']
            total_percentage = (allocation_percentage * fund_percentage) / 100
            fund_allocations[symbol] = total_percentage
    # Define periods
    periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    # Get historical data
    for symbol in fund_symbols:
        try:
            fund = yf.Ticker(symbol)
            hist = fund.history(period='max')
            if hist.empty:
                raise Exception(f"No historical data available for {symbol}")
            if 'Adj Close' in hist.columns:
                price_col = 'Adj Close'
            else:
                price_col = 'Close'
            hist = hist.reset_index().rename(columns={price_col: 'price', 'Date': 'date'})
            hist['date'] = hist['date'].dt.strftime('%Y-%m-%d')
            historical_data[symbol] = hist[['date', 'price']]
            if len(hist) >= 2:
                current_price = float(hist['price'].iloc[-1])
                previous_close = float(hist['price'].iloc[-2])
            else:
                current_price = float(hist['price'].iloc[-1])
                previous_close = current_price
            daily_change = current_price - previous_close
            daily_change_percent = (daily_change / previous_close) * 100 if previous_close else 0
            returns = {}
            for period in periods:
                hist_period = fund.history(period=period)
                if hist_period.empty or len(hist_period) < 2:
                    returns[period] = 'N/A'
                    continue
                if 'Adj Close' in hist_period.columns:
                    price_col_period = 'Adj Close'
                else:
                    price_col_period = 'Close'
                start_price = float(hist_period[price_col_period].iloc[0])
                end_price = float(hist_period[price_col_period].iloc[-1])
                period_return = ((end_price / start_price) - 1) * 100
                returns[period] = round(period_return, 2)
            allocation_percentage = fund_allocations.get(symbol, 0)
            data[symbol] = {
                'current_price': round(current_price, 2) if current_price else 'N/A',
                'daily_change': round(daily_change, 2) if daily_change else 'N/A',
                'daily_change_percent': round(daily_change_percent, 2) if daily_change_percent else 'N/A',
                'allocation_percentage': round(allocation_percentage, 2),
                'returns': returns
            }
        except Exception as e:
            data[symbol] = {
                'error': f"{e}"
            }
    # Calculate overall fund performance
    total_allocations = sum(fund_allocations.values())
    overall_returns = {}
    for period in periods:
        weighted_return = 0
        total_weight = 0
        for symbol in fund_symbols:
            fund_data = data.get(symbol)
            if fund_data and 'returns' in fund_data and fund_data['returns'].get(period) != 'N/A':
                allocation = fund_allocations.get(symbol, 0)
                fund_return = fund_data['returns'][period]
                weighted_return += (allocation / total_allocations) * fund_return
                total_weight += allocation / total_allocations
        if total_weight > 0:
            overall_returns[period] = round(weighted_return, 2)
        else:
            overall_returns[period] = 'N/A'
    data['Overall Portfolio'] = {
        'current_price': 'N/A',
        'daily_change': 'N/A',
        'daily_change_percent': 'N/A',
        'allocation_percentage': 100.0,
        'returns': overall_returns
    }
    # Calculate overall historical data
    overall_hist = None
    for symbol in fund_symbols:
        hist = historical_data.get(symbol)
        allocation = fund_allocations.get(symbol, 0) / 100
        if hist is not None:
            hist = pd.DataFrame(hist)
            hist['price'] = pd.to_numeric(hist['price'])
            hist['weighted_price'] = hist['price'] * allocation
            if overall_hist is None:
                overall_hist = hist[['date', 'weighted_price']].copy()
            else:
                overall_hist = pd.merge(overall_hist, hist[['date', 'weighted_price']], on='date', how='outer', suffixes=('', '_'+symbol))
                overall_hist.fillna(0, inplace=True)
                overall_hist['weighted_price'] = overall_hist['weighted_price'] + overall_hist['weighted_price_'+symbol]
                overall_hist.drop(columns=['weighted_price_'+symbol], inplace=True)
    if overall_hist is not None:
        overall_hist['date'] = pd.to_datetime(overall_hist['date'])
        overall_hist.sort_values('date', inplace=True)
        overall_hist = overall_hist.groupby('date').sum().reset_index()
        overall_hist['date'] = overall_hist['date'].dt.strftime('%Y-%m-%d')
        historical_data['Overall Portfolio'] = overall_hist[['date', 'weighted_price']].rename(columns={'weighted_price': 'price'}).to_dict(orient='records')
    # Convert individual fund historical data to list of dicts
    for symbol in fund_symbols:
        hist = historical_data.get(symbol)
        if hist is not None:
            hist = pd.DataFrame(hist)
            hist['date'] = pd.to_datetime(hist['date']).dt.strftime('%Y-%m-%d')
            historical_data[symbol] = hist.to_dict(orient='records')
    return data, historical_data

if __name__ == '__main__':
    app.run(debug=True)
