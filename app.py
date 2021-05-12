import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date
from pandas_datareader import data as web




st.title("Economic Monitor Web App")

menu = ["Equity Markets & US Treasury Bonds & Bitcoin", "Federal Finance", "Commodities", "Economic Performance", "About"]
    
st.sidebar.header("Choose from")
choice = st.sidebar.selectbox("Menu",menu)
    
st.sidebar.header("Select Date")
#st.sidebar.subheader('Financials')
startdate = st.sidebar.date_input('Start Date', date(2019, 1, 1))
enddate = st.sidebar.date_input('End Date')

if choice == "Equity Markets & US Treasury Bonds & Bitcoin":
    st.subheader("Equity Markets & US Treasury Bonds & Bitcoin")

    # Ticker
    tickersp500 = 'SP500' # S&P 500

    # User pandas_reader.data.DataReader to load the desired data.
    sp500df = web.DataReader(tickersp500, 'fred', startdate)['SP500']

    # Visualization
    st.write('S&P 500')
    st.line_chart(sp500df)

    # Nasdaq100
    nasdaq100df = web.DataReader('NASDAQ100', 'fred', startdate)['NASDAQ100']

    # Visualization
    st.write('NASDAQ100')
    st.line_chart(nasdaq100df)

    # Volatility Index
    vixdf = web.DataReader('VIXCLS', 'fred', startdate)['VIXCLS']

    st.write('Volatility Index: VIX')
    st.line_chart(vixdf)

    # Coinbase Bitcoin 
    bitcoindf = web.DataReader('CBBTCUSD', 'fred', startdate)['CBBTCUSD']

    st.write('Bitcoin [$US]')
    st.line_chart(bitcoindf)

    # US 10-year Treasury Rate
    treasury10y = web.DataReader('DGS10', 'fred', startdate)['DGS10']

    st.write('US 10-year Treasury Rate [%]')
    st.line_chart(treasury10y)

    # US 10-Year Treasury Inflation-Indexed Security, Constant Maturity 
    treasuryinflation10y = web.DataReader('DFII10', 'fred', startdate)['DFII10']

    st.write('US 10-Year Treasury Inflation-Indexed Security [%]')
    st.line_chart(treasuryinflation10y)

    # US 30-year Treasury Rate
    treasury30y = web.DataReader('DGS30', 'fred', startdate)['DGS30']

    st.write('US 30-year Treasury [%]')
    st.line_chart(treasury30y)

    # BTC vs. Gold/Silver vs. S&P500/Nasdaq vs. 10/30y-Treasury
    st.write('Corr BTC / S&P500&Nasdaq / US10&30y-Treasury')
    data = sp500df.to_frame().join([bitcoindf,nasdaq100df,treasury10y,treasury30y], how='outer')
    data['Year'] = data.index
    # Coorelation S&P500/Nasdaq vs. 10/30y-Treasury
    st.write(data.corr())

    st.subheader("Money Supply")

    # US M1 Money Stock 
    m1df = web.DataReader('WM1NS', 'fred', startdate)['WM1NS']

    st.write('US M1 Money Stock')
    st.line_chart(m1df)

    # US M2 Money Stock 
    m2df = web.DataReader('WM2NS', 'fred', startdate)['WM2NS']

    st.write('US M2 Money Stock')
    st.line_chart(m2df)

    # US Velocity of M2 Money Stock 
    m2vdf = web.DataReader('M2V', 'fred', startdate)['M2V']

    st.write('US Velocity of M2 Money Stock')
    st.line_chart(m2vdf)

    # US M3 Money Stock
    m3df = web.DataReader('MABMM301USM189S', 'fred', startdate)['MABMM301USM189S']

    st.write('US M3 Money Stock')
    st.line_chart(m3df)    

    # Bank Credit All Commercial Banks US
    bankcreditdf = web.DataReader('TOTBKCR', 'fred', startdate)['TOTBKCR']

    st.write('Bank Credit All Commercial Banks US [Billions of $US]')
    st.line_chart(bankcreditdf)   

    # Total Consumer Credit Owned and Securitized, Outstanding
    consumercreditdf = web.DataReader('TOTALSL', 'fred', startdate)['TOTALSL']

    st.write('Total Consumer Credit Owned and Securitized, Outstanding [Billions of $US]')
    st.line_chart(consumercreditdf)   

elif choice == "Federal Finance":
    st.subheader('Federal Finance')

    # Federal Receipts 
    federalreceiptsdf = web.DataReader('FGRECPT', 'fred', startdate)['FGRECPT']

    st.write('US Federal Receipts [Millions of $US]')
    st.line_chart(federalreceiptsdf) 

    # Federal government current tax receipts
    federaltaxreceiptsdf = web.DataReader('W006RC1Q027SBEA', 'fred', startdate)['W006RC1Q027SBEA']

    st.write('US Federal government current tax receipts [Billions of $US]')
    st.line_chart(federaltaxreceiptsdf)

    # Federal Receipts as Percent of Gross Domestic Product 
    federalreceiptsofgdpdf = web.DataReader('FYFRGDA188S', 'fred', startdate)['FYFRGDA188S']

    st.write('US Federal Receipts as Percent of Gross Domestic Product [% of GDP]')
    st.line_chart(federalreceiptsofgdpdf)  

    # Federal Government: Current Expenditures
    federalexpendpdf = web.DataReader('FGEXPND', 'fred', startdate)['FGEXPND']

    st.write('US Federal Government: Current Expenditures [Billions of $US]')
    st.line_chart(federalexpendpdf)  

    # Federal government current expenditures: Interest payments 
    federalinterestpaymentdf = web.DataReader('A091RC1Q027SBEA', 'fred', startdate)['A091RC1Q027SBEA']

    st.write('US Federal government current expenditures: Interest payments [Billions of $US]')
    st.line_chart(federalinterestpaymentdf)

    # Federal Debt: Total Public Debt
    federaldebtdf = web.DataReader('GFDEBTN', 'fred', startdate)['GFDEBTN']

    st.write('US Federal Debt: Total Public Debt [Millions of $US]')
    st.line_chart(federaldebtdf)

    # Federal Debt Held by Federal Reserve Banks 
    federaldebtbyfeddf = web.DataReader('FDHBFRBN', 'fred', startdate)['FDHBFRBN']

    st.write('US Federal Debt Held by Federal Reserve Banks [Billions of $US]')
    st.line_chart(federaldebtbyfeddf)

    # Federal Debt Held by the Public 
    federaldebtbypublicdf = web.DataReader('FYGFDPUN', 'fred', startdate)['FYGFDPUN']

    st.write('US Federal Debt Held by the Public [Millions of $US]')
    st.line_chart(federaldebtbypublicdf)

    # Federal Debt Held by Foreign and International Investors
    federaldebtbyforeigndf = web.DataReader('FDHBFIN', 'fred', startdate)['FDHBFIN']

    st.write('US Federal Debt Held by Foreign and International Investors [Billions of $US]')
    st.line_chart(federaldebtbyforeigndf)

    # Federal Debt: Total Public Debt as Percent of Gross Domestic Product 
    federaldebtofgdpdf = web.DataReader('GFDEGDQ188S', 'fred', startdate)['GFDEGDQ188S']

    st.write('US Federal Debt: Total Public Debt as Percent of Gross Domestic Product [% of GDP]')
    st.line_chart(federaldebtofgdpdf)


elif choice == "Commodities":

    st.subheader('Precious Metals')

    # Gold Fixing Price 10:30 A.M. (London time) in London Bullion Market
    goldpricedf = web.DataReader('GOLDPMGBD228NLBM', 'fred', startdate)['GOLDPMGBD228NLBM']

    st.write('Gold Fixing Price ($US per Troy Ounce) - 10:30 A.M. Londin time')
    st.line_chart(goldpricedf)

    # Silver Fixing Price 12:00 noon (London time) in London Bullion Market
    silverdf = web.DataReader('SLVPRUSD', 'fred', startdate)['SLVPRUSD']

    st.write('Silver Fixing Price ($US per Troy Ounce) - 12:00 noon London time')
    st.line_chart(silverdf)

    st.subheader("Energy")

    # Henry Hub Natural Gas Spot Price 
    gasdf = web.DataReader('MHHNGSP', 'fred', startdate)['MHHNGSP']

    st.write('Henry Hub Natural Gas Spot Price ($US per Million BTU)')
    st.line_chart(gasdf)

    # West Texas Intermediate Oil Price (WTI)
    oilpricedf = web.DataReader('DCOILWTICO','fred', startdate)

    st.write('Oil Price [$US per Barrel] - WTI')
    st.line_chart(oilpricedf)

    # Global price of Coal, Australia 
    coaldf = web.DataReader('PCOALAUUSDM','fred', startdate)

    st.write('Global price of Coal [$US per Metric Ton]')
    st.line_chart(coaldf)

    # Global price of Uranium 
    uraniumdf = web.DataReader('PURANUSDM','fred', startdate)

    st.write('Global price of Uranium [$US per Pound]')
    st.line_chart(uraniumdf)


    st.subheader("Industry Metals")

    # Global price of Iron Ore
    ironoredf = web.DataReader('PIORECRUSDM', 'fred', startdate)['PIORECRUSDM']

    st.write('Global price of Iron Ore [$US per Metric Ton]')
    st.line_chart(ironoredf)

    # Global price of Aluminum 
    aluminumdf = web.DataReader('PALUMUSDM', 'fred', startdate)['PALUMUSDM']

    st.write('Global price of Aluminum [$US per Metric Ton]')
    st.line_chart(aluminumdf)

    # Global price of Nickel 
    nickeldf = web.DataReader('PNICKUSDM', 'fred', startdate)['PNICKUSDM']

    st.write('Global price of Nickel [$US Dollars per Metric Ton]')
    st.line_chart(nickeldf)

    # Global price of Copper 
    copperdf = web.DataReader('PCOPPUSDM', 'fred', startdate)['PCOPPUSDM']

    st.write('Global price of Copper [$US per Metric Ton]')
    st.line_chart(copperdf)

    # Copper/Gold
    coppergold = copperdf.to_frame().join(goldpricedf, how='outer')
    # Interpolate with a linear method to fill out the gab in the graph
    coppergold  = coppergold .interpolate(method='linear')
    coppergold['Date'] = coppergold.index 
    coppergold['coppergold'] = coppergold['PCOPPUSDM'] / coppergold['GOLDPMGBD228NLBM']

    st.write('Copper/Gold Ratio ')
    st.line_chart(coppergold['coppergold'])


    st.subheader("Agriculture")

    # Global price of Corn 
    corndf = web.DataReader('PMAIZMTUSDM', 'fred', startdate)['PMAIZMTUSDM']

    st.write('Global price of Corn [$US per Metric Ton]')
    st.line_chart(corndf)

    # Global price of Wheat
    wheatdf = web.DataReader('PWHEAMTUSDM', 'fred', startdate)

    st.write('Global price of Wheat [$US per Metric Ton]')
    st.line_chart(wheatdf)

    # Global price of Palm Oil 
    palmoildf = web.DataReader('PPOILUSDM', 'fred', startdate)

    st.write('Global price of Palm Oil [$US per Metric Ton]')
    st.line_chart(palmoildf)

    # Global price of Soybeans 
    soybeansdf = web.DataReader('PSOYBUSDM', 'fred', startdate)

    st.write('Global price of Soybeans [$US per Metric Ton]')
    st.line_chart(soybeansdf)

    st.subheader("Producer Price Index")
    st.write("(Index 1982 = 100)")

    # Producer Price Index by Commodity: All Commodities
    ppidf = web.DataReader('PPIACO', 'fred', startdate)

    st.write('Producer Price Index by Commodity: All Commodities')
    st.line_chart(ppidf)   

    # Producer Price Index by Commodity: Metals and Metal Products: Iron and Steel
    ppimetaldf = web.DataReader('WPU101', 'fred', startdate)

    st.write('Producer Price Index by Commodity: Metals and Metal Products: Iron and Steel')
    st.line_chart(ppimetaldf)

    # Producer Price Index by Commodity: Special Indexes: Construction Materials
    ppiconstructionpdf = web.DataReader('WPUSI012011', 'fred', startdate)

    st.write('Producer Price Index by Commodity: Special Indexes: Construction Materials')
    st.line_chart(ppiconstructionpdf)

    # Producer Price Index by Commodity: Lumber and Wood Products: Softwood Lumber 
    ppisoftwoodlumberdf = web.DataReader('WPS0811', 'fred', startdate)

    st.write('Producer Price Index by Commodity: Lumber and Wood Products: Softwood Lumber')
    st.line_chart(ppisoftwoodlumberdf)

    # Producer Price Index by Commodity: Lumber and Wood Products: Plywood
    ppiwoodlumberdf = web.DataReader('WPU083', 'fred', startdate)

    st.write('Producer Price Index by Commodity: Lumber and Wood Products: Plywood')
    st.line_chart(ppiwoodlumberdf)

    # Producer Price Index by Industry: Plastics Material and Resins Manufacturing
    ppiplasticdf = web.DataReader('PCU325211325211', 'fred', startdate)

    st.write('Producer Price Index by Industry: Plastics Material and Resins Manufacturing')
    st.line_chart(ppiplasticdf)

    # Producer Price Index by Industry: Semiconductor and Other Electronic Component Manufacturing
    ppisemidf = web.DataReader('PCU33443344', 'fred', startdate)

    st.write('Producer Price Index by Industry: Semiconductor and Other Electronic Component Manufacturing')
    st.line_chart(ppisemidf)

    # Producer Price Index by Industry: Chemical Manufacturing
    ppichemdf = web.DataReader('PCU325325', 'fred', startdate)

    st.write('Producer Price Index by Industry: Chemical Manufacturing')
    st.line_chart(ppichemdf)


    # US Median Consumer Price Index(CPI)
    cpidf = web.DataReader('MEDCPIM158SFRBCLE', 'fred', startdate)

    st.write('Median CPI')
    st.line_chart(cpidf)

elif choice == "Economic Performance":
    st.subheader("Economic Performance")

    # US Gross Domestic Product (GDP)
    gdp = web.DataReader('GDP', 'fred', startdate)

    st.write('US GDP')
    st.line_chart(gdp)

    # US Real GDP
    realgdp = web.DataReader('GDPC1', 'fred', startdate)

    st.write('US Real GDP')
    st.line_chart(realgdp)

    st.subheader("Labor Market")

    # US Unemployment Rate
    unemploymentdf = web.DataReader('UNRATE', 'fred', startdate)

    st.write('US Unemployment Rate')
    st.line_chart(unemploymentdf)

    # US Unemployment Rate (U-6)
    unemploymentu6df = web.DataReader('U6RATE', 'fred', startdate)

    st.write('US Unemployment Rate(U-6)')
    st.line_chart(unemploymentu6df)

    # US Personal Savings Rate
    personalsavingratetdf = web.DataReader('PSAVERT', 'fred', startdate)

    st.write('US Personal Saving Rate')
    st.line_chart(personalsavingratetdf)

    # US Average Hourly Earnings of All Employees, Total Private 
    hourlyearningsdf = web.DataReader('CES0500000003', 'fred', startdate)

    st.write('US Average Hourly Earnings of All Employees [$US]')
    st.line_chart(hourlyearningsdf)

    # US Average Weekly Earnings of All Employees, Total Private
    weeklyearningsdf = web.DataReader('CES0500000011', 'fred', startdate)

    st.write('US Average Weekly Earnings of All Employees [$US]')
    st.line_chart(weeklyearningsdf)

    # US Manufacturing Sector: Labor Productivity 
    laborproductivitydf = web.DataReader('MPU9900063', 'fred', startdate)

    st.write('US Labor Productivity - Manufacturing Sector [% YoY]')
    st.line_chart(laborproductivitydf)

    # Private Business Sector: Labor Productivity 
    laborproductivityprivatdf = web.DataReader('MPU4900063', 'fred', startdate)

    st.write('US Labor Productivity - Private Business Sector [% YoY]')
    st.line_chart(laborproductivityprivatdf)

    st.subheader("Business Activity")

    # Capacity Utilization: Total Index 
    capacityutildf = web.DataReader('TCU', 'fred', startdate)

    st.write('US Capacity Utilization [% of Capacity]')
    st.line_chart(capacityutildf)

    # New Privately-Owned Housing Units Started 
    privatehousingunitsgdf = web.DataReader('HOUST', 'fred', startdate)

    st.write('US New Privately-Owned Housing Units Started [Thousands of Units]')
    st.line_chart(privatehousingunitsgdf)

    # New Privately-Owned Housing Units Under Construction  
    privatehousingunitsconstgdf = web.DataReader('UNDCONTSA', 'fred', startdate)

    st.write('US New Privately-Owned Housing Units Under Construction [Thousands of Units]')
    st.line_chart(privatehousingunitsconstgdf)                                          

    # Rental Vacancy Rate for the United States  
    rentalvacancydf = web.DataReader('RRVRUSQ156N', 'fred', startdate)

    st.write('US Rental Vacancy Rate [%]')
    st.line_chart(rentalvacancydf)

    # Homeowner Vacancy Rate for the United States
    homeownervacancydf = web.DataReader('RHVRUSQ156N', 'fred', startdate)

    st.write('US Homeowner Vacancy Rate [%]')
    st.line_chart(homeownervacancydf)        

    # Total Business Sales 
    businesssalesdf = web.DataReader('TOTBUSSMSA', 'fred', startdate)

    st.write('US Total Business Sales [Millions of $US]')
    st.line_chart(businesssalesdf)            

    #  Total Business Inventories
    businessinventoriesdf = web.DataReader('BUSINV', 'fred', startdate)

    st.write('US Total Business Inventories [Millions of $US]')
    st.line_chart(businessinventoriesdf)

    # Total Business: Inventories to Sales Ratio
    inventoriestosalesratiodf = web.DataReader('ISRATIO', 'fred', startdate)

    st.write('US Total Business: Inventories to Sales Ratio')
    st.line_chart(inventoriestosalesratiodf)     

    # Manufacturers New Orders: Durable Goods
    manufacnewordersdf = web.DataReader('DGORDER', 'fred', startdate)

    st.write('US Manufacturers New Orders: Durable Goods [Millions of $US]')
    st.line_chart(manufacnewordersdf)   

    # Manufacturers' Value of Shipments: Durable Goods 
    manufacnewshipdf = web.DataReader('AMDMVS', 'fred', startdate)

    st.write('US Manufacturers Value of Shipments: Durable Goods  [Millions of $US]')
    st.line_chart(manufacnewshipdf)   


elif choice == "About":
    st.subheader("About Economic Monitor Web App")
    st.info("Built with Streamlit by [Lifelonglearner](https://www.lifelonglearner.de/)")
    st.text("LifelongLearner")
