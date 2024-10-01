# utils/config_manager.py

import json
import os

def load_config(fund_id):
    config_path = os.path.join('funds', f'{fund_id}.json')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file for fund '{fund_id}' not found.")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def save_config(config, fund_id):
    os.makedirs('funds', exist_ok=True)
    config_path = os.path.join('funds', f'{fund_id}.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def get_available_funds():
    funds = []
    if not os.path.exists('funds'):
        return funds
    for filename in os.listdir('funds'):
        if filename.endswith('.json'):
            fund_id = filename[:-5]  # Remove '.json' extension
            try:
                config = load_config(fund_id)
                fund_name = config.get('fund_name', fund_id)
                funds.append({'id': fund_id, 'name': fund_name})
            except Exception as e:
                continue  # Skip if there's an error loading the config
    return funds
