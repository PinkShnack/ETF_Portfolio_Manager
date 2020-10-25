'''

1. get data about all iShares ETFs from 
    "https://www.ishares.com/uk/individual/en/products/etf-investments"
    - done
1a. create dict with ISIN and ticker - done

2. grab the links in that website/xml doc and extract together with the data these:
    code-number, etf-ticker, DONT NEED NAME can use * inplace of it
    Create dicts of these with ticker as key
    - done
2a. Need to parse the html to get the code-names from the tickers!
    - done

3. Create function that downloads the ticker data using the above info.
3a. Create the link string for pandas to download using the ticker and codenumber
3b. Have the download function return the df from the downloaded csv file
    using the link string
3b. 

4. Create portfolio class.
    Plan this.

'''