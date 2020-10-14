
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

# summarise = "Standort" or "Sektor"
def get_portfolio_info(summarise, ticker_name_dict, ticker_percent_dict,
                       figsize=(10,16), save=False):
    """

    Examples
    --------
    >>> from calc_funcs import get_portfolio_info
    >>> ticker_name_dict = {'AYEM': 'MSCI EM IMI ESG ETF',
    ... 					'DGTL': 'Digitalisation ETF',
    ... 					'IQQH': 'Global Clean Energy ETF'}
    >>> ticker_percent_dict = {'AYEM': 50, 'DGTL': 25, 'IQQH': 25}

    >>> get_portfolio_info("Sektor", ticker_name_dict, ticker_percent_dict)
    >>> get_portfolio_info("Standort", ticker_name_dict, ticker_percent_dict)


    """
    filenames = glob("dummy_data/*.csv")


    fontsize = 24
    print(f"\nOutputting {summarise} Information...")

    ticker_sektor_dict = {}
    for filename in filenames:
        ticker = filename[-17:-13]
        name = ticker_name_dict[ticker]
        file = pd.read_csv(filename, header=2, decimal=',')
        print(f"    {name}")
        sektor_df = file.groupby([summarise], as_index=False).sum().sort_values(
            by='Gewichtung (%)',ascending=False, ignore_index=True)

        sektor_df.plot(x=summarise, y="Gewichtung (%)",kind="barh", legend=False)
        plt.title(name)
        plt.tight_layout()
        if save:
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
        kind="barh", legend=False, figsize=figsize)
    plt.title(f"Portfolio {summarise})",
        fontsize=fontsize+4)
    plt.xlabel("Percentage", fontsize=fontsize+4)
    plt.ylabel(summarise, fontsize=fontsize+4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    if save:
        plt.savefig(f"Portfolio {summarise}.png")

    if summarise == "Standort":
        master_sektor_df_grouped.drop([0], axis=0,
            inplace=True)
        master_sektor_df_grouped.plot(x=summarise, y="Gewichtung (%)",
            kind="barh", legend=False, figsize=figsize)
        plt.title(f"Portfolio {summarise} (America not incl.)",
            fontsize=fontsize+4)
        plt.xlabel("Percentage", fontsize=fontsize+4)
        plt.ylabel(summarise, fontsize=fontsize+4)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.tight_layout()
        if save:
            plt.savefig(f"Portfolio {summarise} (America not incl.).png")
