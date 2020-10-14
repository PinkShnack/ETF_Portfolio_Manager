
import os
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

# open a file,
# make the top row the row titles

testing = False
if testing:
        
    file = pd.read_csv('SXRQ_holdings.csv', header=2, decimal=',')
    file.head()
    sektor_df = file.groupby([summarise]).sum().sort_values(
        by='Gewichtung (%)',ascending=False)
    sektor_df

ticker_name_dict = {
    'AYEM': 'MSCI EM IMI ESG ETF',
    'DGTL': 'Digitalisation ETF',
    'IQQH': 'Global Clean Energy ETF',
    'IS3S': 'MSCI World Value Factor',
    'IUSN': 'MSCI World Small Cap ETF',
    'SNAW': 'MSCI World ESG ETF',
    'SXRQ': 'Euro Gov Bond ETF 7-10yrs'}

ticker_percent_dict = {
    'AYEM': 10,
    'DGTL': 5,
    'IQQH': 5,
    'IS3S': 5,
    'IUSN': 10,
    'SNAW': 60,
    'SXRQ': 5}

fontsize = 24

summarise = "Standort"

filenames = glob("*.csv")

def get_portfolio_info(summarise):

	ticker_sektor_dict = {}
	for filename in filenames:
	    ticker = filename[0:4]
	    name = ticker_name_dict[ticker]
	    file = pd.read_csv(filename, header=2, decimal=',')
	    print(f"    {name}")
	    sektor_df = file.groupby([summarise], as_index=False).sum().sort_values(
	        by='Gewichtung (%)',ascending=False, ignore_index=True)

	    sektor_df.plot(x=summarise, y="Gewichtung (%)",kind="barh", legend=False)
	    plt.title(name)
	    plt.tight_layout()
	    plt.savefig(f"{name}_{summarise}.png")

	    percent_to_scale = ticker_percent_dict[ticker]/100
	    sektor_df_rescaled = sektor_df.copy()
	    sektor_df_rescaled["Gewichtung (%)"] = sektor_df_rescaled[
	        "Gewichtung (%)"].mul(percent_to_scale)
	    
	    ticker_sektor_dict[ticker] = sektor_df_rescaled



	sektor_df_rescaled.columns

	master_sektor_df = pd.DataFrame()
	for ticker in ticker_sektor_dict:
	    # make a master_sektor df and groupby
	    master_sektor_df = pd.concat([master_sektor_df, ticker_sektor_dict[ticker]],
	        ignore_index=True)

	master_sektor_df_grouped = master_sektor_df.groupby([summarise], as_index=False).sum().sort_values(
	        by='Gewichtung (%)',ascending=False, ignore_index=True)


	master_sektor_df_grouped['Gewichtung (%)'].sum()

	master_sektor_df_grouped.plot(x=summarise, y="Gewichtung (%)",
		kind="barh", legend=False, figsize=(16,16))
	plt.title(f"Portfolio {summarise} (no bond incl.)",
		fontsize=fontsize+4)
	plt.xlabel("Percentage", fontsize=fontsize+4)
	plt.ylabel(summarise, fontsize=fontsize+4)
	plt.xticks(fontsize=fontsize)
	plt.yticks(fontsize=fontsize)
	plt.tight_layout()
	plt.savefig(f"Portfolio {summarise}.png")

	if summarise == "Standort":
		master_sektor_df_grouped.drop([0], axis=0,
			inplace=True)
		master_sektor_df_grouped.plot(x=summarise, y="Gewichtung (%)",
			kind="barh", legend=False, figsize=(16,16))
		plt.title(f"Portfolio {summarise}",
			fontsize=fontsize+4)
		plt.xlabel("Percentage", fontsize=fontsize+4)
		plt.ylabel(summarise, fontsize=fontsize+4)
		plt.xticks(fontsize=fontsize)
		plt.yticks(fontsize=fontsize)
		plt.tight_layout()
		plt.savefig(f"Portfolio {summarise} (America not incl.).png")


if __name__ == "__main__":
	print("\nOutputting Sektor Information...")
	get_portfolio_info(summarise="Sektor")
	print("\nOutputting Standort Information...")
	get_portfolio_info(summarise="Standort")
	print("\nLook in your folder to see the figures!")
