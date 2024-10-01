import pandas as pd

def sample_excel_to_csv(excel_file, sheet_name, csv_file):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    sampled_df = df.iloc[::10]

    sampled_df.to_csv(csv_file, index=False)

if __name__ == "__main__":
    excel_file = 'data.xlsx' 
    sheet_name = 'Groundwaterlevelnew_Daily'     
    csv_file = 'dwlr_data.csv'

    sample_excel_to_csv(excel_file, sheet_name, csv_file)
    print(f'Sampled values saved to {csv_file}')
