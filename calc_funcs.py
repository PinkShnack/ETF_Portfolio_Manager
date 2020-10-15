
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob


def load_tickers(ticker_percent_dict):

    """
    Load the chosen tickers.

    Examples
    --------
    >>> from calc_funcs import load_tickers
    >>> ticker_percent_dict = {'SNAW': 25, 'AYEM': 25, 'DGTL': 25, 'IQQH': 25}
    >>> filenames = load_tickers(ticker_percent_dict)

    """
    if not isinstance(ticker_percent_dict, dict):
        raise ValueError("ticker_percent_dict must be a dictionary")

    fnames = glob("dummy_data/*.csv")
    desired_tickers = [i for i in ticker_percent_dict.keys()]

    fnames = glob("dummy_data/*.csv")
    filenames = []
    for f in fnames:
        for ticker in desired_tickers:
            if ticker in f:
                filenames.append(f)

    return filenames


# summarise = "Standort" or "Sektor"
def get_portfolio_info(summarise, ticker_name_dict, ticker_percent_dict,
                       figsize=(10, 16), save=False):
    """
    Get overall information about Sektor and Standort.

    Examples
    --------
    >>> from calc_funcs import get_portfolio_info
    >>> ticker_name_dict = {'AYEM': 'MSCI EM IMI ESG ETF',
    ... 					'DGTL': 'Digitalisation ETF',
    ... 					'IQQH': 'Global Clean Energy ETF',
    ...                     'SNAW': 'MSCI World ESG ETF',}
    >>> ticker_percent_dict = {'SNAW': 25, 'AYEM': 25, 'DGTL': 25, 'IQQH': 25}

    >>> get_portfolio_info("Sektor", ticker_name_dict, ticker_percent_dict)
    >>> get_portfolio_info("Standort", ticker_name_dict, ticker_percent_dict)

    """
    filenames = load_tickers(ticker_percent_dict=ticker_percent_dict)

    fontsize = 24
    print(f"\nOutputting {summarise} Information...")

    ticker_sektor_dict = {}
    for filename in filenames:
        ticker = filename[-17:-13]
        name = ticker_name_dict[ticker]
        file = pd.read_csv(filename, header=2, decimal=',')
        print(f"    {name}")
        sektor_df = file.groupby(
            [summarise], as_index=False).sum().sort_values(
                by='Gewichtung (%)', ascending=False, ignore_index=True)

        sektor_df.plot(x=summarise, y="Gewichtung (%)", kind="barh",
                       legend=False)
        plt.title(name)
        plt.tight_layout()
        if save:
            plt.savefig(f"{name}_{summarise}.png")

        percent_to_scale = ticker_percent_dict[ticker]/100
        sektor_df_rescaled = sektor_df.copy()
        sektor_df_rescaled["Gewichtung (%)"] = sektor_df_rescaled[
            "Gewichtung (%)"].mul(percent_to_scale)

        ticker_sektor_dict[ticker] = sektor_df_rescaled

    master_sektor_df = pd.DataFrame()
    for ticker in ticker_sektor_dict:
        # make a master_sektor df and groupby
        master_sektor_df = pd.concat(
            [master_sektor_df, ticker_sektor_dict[ticker]], ignore_index=True)

    master_sektor_df_grouped = master_sektor_df.groupby(
        [summarise], as_index=False).sum().sort_values(
            by='Gewichtung (%)', ascending=False, ignore_index=True)

    master_sektor_df_grouped['Gewichtung (%)'].sum()

    master_sektor_df_grouped.plot(x=summarise, y="Gewichtung (%)",
                                  kind="barh", legend=False, figsize=figsize)
    plt.title(f"Portfolio {summarise}", fontsize=fontsize+4)
    plt.xlabel("Percentage", fontsize=fontsize+4)
    plt.ylabel(summarise, fontsize=fontsize+4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    if save:
        plt.savefig(f"Portfolio {summarise}.png")

    if summarise == "Standort":
        master_sektor_df_grouped.drop([0], axis=0, inplace=True)
        master_sektor_df_grouped.plot(x=summarise, y="Gewichtung (%)",
                                      kind="barh", legend=False,
                                      figsize=figsize)
        plt.title(f"Portfolio {summarise} (America not incl.)",
                  fontsize=fontsize+4)
        plt.xlabel("Percentage", fontsize=fontsize+4)
        plt.ylabel(summarise, fontsize=fontsize+4)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.tight_layout()
        if save:
            plt.savefig(f"Portfolio {summarise} (America not incl.).png")


def get_individual_company_info(company_name, ticker_name_dict,
                                ticker_percent_dict,
                                figsize=(10, 16), save=False):

    """
    Get the weighting of an individual company.

    Examples
    --------
    >>> from calc_funcs import get_individual_company_info
    >>> ticker_name_dict = {'AYEM': 'MSCI EM IMI ESG ETF',
    ... 					'DGTL': 'Digitalisation ETF',
    ... 					'IQQH': 'Global Clean Energy ETF',
    ...                     'SNAW': 'MSCI World ESG ETF',}
    >>> ticker_percent_dict = {'SNAW': 25, 'AYEM': 25, 'DGTL': 25, 'IQQH': 25}
    >>> company_name = "Apple"
    >>> get_individual_company_info(company_name, ticker_name_dict,
    ...                             ticker_percent_dict)

    """
    filenames = load_tickers(ticker_percent_dict=ticker_percent_dict)

    print(f"\nOutputting {company_name} Information...")

    company_weighting_list = []
    for filename in filenames:
        ticker = filename[-17:-13]
        name = ticker_name_dict[ticker]
        file = pd.read_csv(filename, header=2, decimal=',')
        print(f"    {name}")
        # get company weight in each filename

        file.drop(file.tail(1).index, inplace=True)

        file.set_index("Name", inplace=True)
        full_name = []
        for index_name in file.index:
            if company_name.upper() in index_name.upper():
                full_name.append(index_name)

        if len(full_name) == 1:  # shouldn't do anything if it's not included!
            full_name = full_name[0]
            company_weight = file.at[full_name, "Gewichtung (%)"]
            percent_to_scale = ticker_percent_dict[ticker]/100
            company_weight_scaled = company_weight * percent_to_scale
            company_weighting_list.append(company_weight_scaled)
    overall_company_weight = sum(company_weighting_list)
    return overall_company_weight
