# cannedtuna.py

# market indices for backtesting
djia = [
    "MMM", "AXP", "AMGN", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT",
    "NKE", "PG", "CRM", "TRV", "UNH", "VZ", "V", "WBA", "WMT", "DIS"
]
nasdaq_100 = [
    "AAPL", "MSFT", "AMZN", "GOOG", "GOOGL", "META", "NVDA", "TSLA", "PEP", "AVGO",
    "COST", "CSCO", "ADBE", "TXN", "CMCSA", "NFLX", "AMD", "QCOM", "INTC", "HON",
    "AMGN", "INTU", "SBUX", "AMAT", "MDLZ", "ISRG", "BKNG", "ADI", "LRCX", "MU",
    "GILD", "ADP", "FISV", "ATVI", "CSX", "MRVL", "KLAC", "PANW", "ADSK", "VRTX",
    "MELI", "REGN", "KDP", "SNPS", "NXPI", "CTAS", "FTNT", "MNST", "IDXX", "LULU",
    "ASML", "EXC", "ORLY", "TEAM", "CDNS", "MAR", "AEP", "MCHP", "ODFL", "PAYX",
    "CTSH", "PCAR", "XEL", "FAST", "DLTR", "BIIB", "WBD", "ANSS", "EA", "ROST",
    "VRSK", "SPLK", "SGEN", "AZN", "ALGN", "CHTR", "KHC", "EBAY", "WBA", "BKR",
    "CEG", "DDOG", "ZS", "MRNA", "ABNB", "LCID", "DOCU", "CRWD", "PDD", "ZM",
    "OKTA", "VRSN", "SIRI", "CPRT", "NTES", "JD", "BIDU", "MTCH", "CTRP", "EXPE"
]
s_and_p_500 = [
    "AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "GOOGL", "META", "TSLA", "BRK.B", "AVGO", 
    "WMT", "LLY", "JPM", "V", "UNH", "ORCL", "XOM", "MA", "COST", "HD", 
    "PG", "NFLX", "BAC", "JNJ", "CRM", "ABBV", "CVX", "TMUS", "KO", "MRK", 
    "WFC", "CSCO", "ADBE", "NOW", "AMD", "BX", "ACN", "PEP", "IBM", "MCD", 
    "LIN", "AXP", "DIS", "MS", "PM", "ABT", "TMO", "GS", "ISRG", "CAT", 
    "GE", "INTU", "VZ", "QCOM", "TXN", "BKNG", "T", "DHR", "CMCSA", "PLTR", 
    "BLK", "SPGI", "RTX", "NEE", "PGR", "LOW", "SCHW", "AMGN", "HON", "ETN", 
    "SYK", "PFE", "UNP", "AMAT", "TJX", "KKR", "UBER", "C", "COP", "ANET", 
    "BSX", "PANW", "ADP", "LMT", "DE", "BMY", "VRTX", "BA", "NKE", "GILD", 
    "FI", "CB", "SBUX", "MMC", "MU", "UPS", "MDT", "PLD", "ADI", "AMT", 
    "LRCX", "SHW", "MO", "GEV", "SO", "EQIX", "TT", "ELV", "CTAS", "WM", 
    "CRWD", "ICE", "CI", "INTC", "APH", "PH", "PYPL", "MCO", "CMG", "CME", 
    "DUK", "DELL", "KLAC", "ABNB", "MDLZ", "CDNS", "PNC", "MSI", "REGN", "WELL", 
    "AON", "USB", "ITW", "MAR", "HCA", "CEG", "SNPS", "ZTS", "CL", "MCK", 
    "EMR", "GD", "FTNT", "EOG", "TDG", "MMM", "APD", "CVS", "ORLY", "COF", 
    "ECL", "NOC", "WMB", "SPG", "FDX", "RCL", "RSG", "CSX", "AJG", "CARR", 
    "ADSK", "DLR", "CHTR", "OKE", "BDX", "TFC", "HLT", "KMI", "PCAR", "FCX", 
    "AFL", "ROP", "TRV", "NSC", "CPRT", "MET", "SLB", "BK", "TGT", "GM", 
    "PSA", "GWW", "FICO", "SRE", "URI", "NXPI", "JCI", "AMP", "VST", "ALL", 
    "AZO", "PSX", "AXON", "ROST", "CMI", "AEP", "MNST", "DHI", "PAYX", "FANG", 
    "PWR", "O", "HWM", "MPC", "D", "MSCI", "AIG", "COR", "FAST", "NDAQ", 
    "NEM", "KMB", "FIS", "TEL", "PEG", "OXY", "PRU", "LHX", "CCI", "AME", 
    "LEN", "KDP", "DFS", "HES", "KVUE", "KR", "PCG", "STZ", "EA", "ODFL", 
    "TRGP", "EW", "GLW", "LULU", "DAL", "VLO", "BKR", "CTVA", "GRMN", "IR", 
    "F", "CBRE", "VRSK", "XEL", "SYY", "CTSH", "IT", "OTIS", "A", "LVS", 
    "YUM", "EXC", "VMC", "KHC", "GEHC", "ACGL", "GIS", "IQV", "EXR", "MLM", 
    "WAB", "HSY", "MTB", "HIG", "RMD", "IDXX", "HPQ", "IRM", "CCL", "NUE", 
    "DD", "HUM", "RJF", "UAL", "ROK", "ED", "TTWO", "VICI", "WTW", "ETR", 
    "EIX", "EFX", "AVB", "FITB", "BRO", "CSGP", "MCHP", "LYV", "TPL", "WEC", 
    "DXCM", "XYL", "DECK", "EBAY", "TSCO", "ANSS", "CAH", "DOW", "GPN", "KEYS", 
    "GDDY", "CNC", "PPG", "STT", "EQR", "SW", "HPE", "EL", "ON", "MPWR", 
    "K", "TROW", "DOV", "BR", "FTV", "NVR", "TYL", "CHD", "EQT", "HAL", 
    "MTD", "VTR", "PHM", "WBD", "NTAP", "SYF", "VLTO", "AWK", "HBAN", "CPAY", 
    "DTE", "PPL", "LYB", "HUBB", "ADM", "WDC", "AEE", "CINF", "EXPE", "WRB", 
    "PTC", "SMCI", "RF", "FE", "SBAC", "CDW", "ROL", "DVN", "BIIB", "WST", 
    "IFF", "TSN", "WAT", "ES", "WY", "ATO", "TDY", "ERIE", "LDOS", "CBOE", 
    "NTRS", "PKG", "ZBH", "STE", "BF.B", "FOXA", "FSLR", "STLD", "CLX", "MKC", 
    "LUV", "ZBRA", "CNP", "STX", "FOX", "INVH", "CFG", "COO", "NRG", "BLDR", 
    "CMS", "OMC", "DRI", "ESS", "IP", "LH", "BBY", "GEN", "PFG", "MAA", 
    "SNA", "CTRA", "PODD", "L", "KEY", "TER", "ULTA", "ARE", "TRMB", "JBHT", 
    "FDS", "VRSN", "HRL", "PNR", "DGX", "HOLX", "DG", "NI", "MAS", "NWS", 
    "GPC", "IEX", "MOH", "BALL", "J", "ALGN", "KIM", "EXPD", "NWSA", "UDR", 
    "MRNA", "AVY", "BAX", "EG", "DPZ", "LNT", "DLTR", "CF", "TXT", "VTRS", 
    "DOC", "JBL", "FFIV", "TPR", "AMCR", "AKAM", "EVRG", "NDSN", "RL", "INCY", 
    "POOL", "RVTY", "BXP", "SWKS", "EPAM", "REG", "APTV", "CAG", "DVA", "CPT", 
    "HST", "KMX", "SWK", "PAYC", "UHS", "CPB", "JKHY", "TAP", "CHRW", "SJM", 
    "ALLE", "JNPR", "DAY", "NCLH", "BG", "SOLV", "ALB", "EMN", "TECH", "BEN", 
    "AIZ", "CTLT", "LW", "IPG", "MGM", "GNRC", "PNW", "AOS", "LKQ", "WYNN", 
    "CRL", "FRT", "ENPH", "AES", "HAS", "MKTX", "HSIC", "GL", "TFX", "MHK", 
    "MTCH", "MOS", "APA", "CZR", "IVZ", "CE", "BWA", "HII", "WBA", "PARA", 
    "FMC", "QRVO", "AMTM"
]

nyse_fang = [
    "META", "AAPL", "AMZN", "NFLX", "GOOGL", "MSFT", "NVDA", "TSLA", "AMD", "SNOW"
]
russel_2000 = []
