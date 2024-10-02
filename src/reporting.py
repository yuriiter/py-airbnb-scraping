import pandas as pd
import json
import os

def append_to_reports_csv(args):
    """Append CLI parameters to reports.csv."""
    report_file = 'generated/reports.csv'
    new_data = {
        'query': args.query,
        'adults': args.adults,
        'checkin': args.checkin,
        'checkout': args.checkout,
        'price_min': args.price_min,
        'price_max': args.price_max,
        'output': args.output
    }
    
    if os.path.isfile(report_file):
        df = pd.read_csv(report_file)
        df = df.append(new_data, ignore_index=True)
    else:
        df = pd.DataFrame([new_data])
    
    df.to_csv(report_file, index=False)
    print('Saved query report to reports.csv')

def save_search_results(listings, output_file):
    if output_file.endswith('.csv'):
        pd.DataFrame(listings).to_csv(output_file, index=False, encoding='utf-8')
    elif output_file.endswith('.json'):
        with open(output_file, "w") as f:
            json.dump(listings, f, indent=2, separators=(',', ': '))
    print(f"Saved to {output_file}")
