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

## Getting data from FRED ##

@st.cache
def load_data():
   # Markets
    marketsdf = web.DataReader(
        ['SP500','NASDAQ100', 'VIXCLS', 'CBBTCUSD', 'DGS10', 'DGS30', 'BOGZ1FL663067003Q'], 'fred', startdate)
    marketsdf  = marketsdf.interpolate(method='linear')
    marketsdf['Date'] = marketsdf.index

    # Money Supply
    moneysupplydf  = web.DataReader(
        ['WM1NS', 'WM2NS', 'BOGMBASE', 'M2V', 'TLAACBW027SBOG', 'CASACBW027SBOG', 'USGSEC', 'MABMM301USM189S', 'TOTBKCR', 'TOTALSL'], 'fred', startdate)
    moneysupplydf  = moneysupplydf.interpolate(method='linear')

    # Federal Finance
    federalfinancedf = web.DataReader(
        ['FGRECPT','W006RC1Q027SBEA','FYFRGDA188S','FGEXPND','A091RC1Q027SBEA','GFDEBTN','FDHBFRBN','FYGFDPUN','FDHBFIN'], 'fred', startdate)

    # Commodity
    commoditydf = web.DataReader(
        ['GOLDPMGBD228NLBM','SLVPRUSD','MHHNGSP','DCOILWTICO','PCOALAUUSDM','PURANUSDM','PIORECRUSDM','PALUMUSDM','PNICKUSDM','PCOPPUSDM',
         'PMAIZMTUSDM','PWHEAMTUSDM','PPOILUSDM','PSOYBUSDM'], 'fred', startdate)
    commoditydf  = commoditydf.interpolate(method='linear')
    commoditydf['Copper/Gold Ratio'] = commoditydf['PCOPPUSDM'] / commoditydf['GOLDPMGBD228NLBM']
    # PPI
    ppidf = web.DataReader(
        ['PPIACO','WPU101', 'WPUSI012011','WPS0811', 'WPU083', 'PCU325211325211', 'PCU33443344', 'PCU325325'], 'fred', startdate)
    
    # Economic Performance
    economicperformdf = web.DataReader(
        ['GDP', 'GDPC1', 'ASTDSL', 'MEDCPIM158SFRBCLE','CORESTICKM159SFRBATL', 'UNRATE', 'U6RATE', 'PSAVERT', 'CES0500000003', 'CES0500000011', 'TCU',
         'RRVRUSQ156N', 'RHVRUSQ156N', 'TOTBUSSMSA', 'BUSINV', 'ISRATIO', 'DGORDER', 'AMDMVS'], 'fred', startdate)
    economicperformdf  = economicperformdf.interpolate(method='linear')
    economicperformdf['Date'] = economicperformdf.index
    
    return marketsdf, moneysupplydf, federalfinancedf, commoditydf, ppidf, economicperformdf 


marketsdf, moneysupplydf, federalfinancedf, commoditydf, ppidf, economicperformdf  = load_data()


## Multiline Viz ##

def multiline_viz(df,*arg):
 # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Date'], empty='none')
    
    
    base = alt.Chart(df).transform_fold(
        [*arg],
    ).mark_line().encode(
        x='Date:T',
        y='value:Q',
        tooltip = [
            alt.Tooltip('Date:T'),
            alt.Tooltip('value:Q'),
            ],
        color='key:N'
    )
    
        # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df).mark_point().encode(
        x='Date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = base.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = base.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='Date:T',
    ).transform_filter(
        nearest
    )
    
    # Put the five layers into a chart and bind the data
    base2 = alt.layer(
        base, selectors, points, rules, text
    ).properties(
        width=600, height=300
    )

    
    return st.altair_chart(base2)


## Page Selection ##

if choice == "Equity Markets & US Treasury Bonds & Bitcoin":
    st.subheader("Equity Markets & US Treasury Bonds & Bitcoin")
    
    # S&P500
    st.write('S&P 500')
    st.line_chart(marketsdf['SP500'])

    # Nasdaq100
    st.write('NASDAQ100')
    st.line_chart(marketsdf['NASDAQ100'])

    # Coinbase Bitcoin 
    st.write('Bitcoin [$US]')
    st.line_chart(marketsdf['CBBTCUSD'])

    # SP500/Bitcoin
    st.write('SP500/Bitcoin Ratio')
    st.line_chart(marketsdf['SP500'] / marketsdf['CBBTCUSD'])
    
    # US 10/30-year Treasury Rate
    st.write('US 10/30-year Treasury Rate [%]')
    multiline_viz(marketsdf, 'DGS10', 'DGS30')
    
    # BTC vs. Gold/Silver vs. S&P500/Nasdaq vs. 10/30y-Treasury
    st.write('Corr BTC / S&P500&Nasdaq / US10&30y-Treasury')
    st.write(marketsdf[marketsdf.columns.drop(['BOGZ1FL663067003Q', 'VIXCLS'])].corr())
    
    # Volatility Index
    st.write('Volatility Index: VIX')
    st.line_chart(marketsdf['VIXCLS'])
    
    # Security Brokers and Dealers; Margin Accounts at Brokers and Dealers; Asset, Level 
    st.write('Security Brokers and Dealers; Margin Accounts at Brokers and Dealers [Millions of $US]')
    st.line_chart(marketsdf['BOGZ1FL663067003Q'])

    st.subheader("Money Supply")
        
    # US Monetary Base; Total 
    st.write('US Monetary Base [Millions of $US]')
    st.line_chart(moneysupplydf['BOGMBASE']) 
    
    # US M1 Money Stock 
    st.write('US M1 Money Stock')
    st.line_chart(moneysupplydf['WM1NS'])

    # US M2 Money Stock 
    st.write('US M2 Money Stock')
    st.line_chart(moneysupplydf['WM2NS'])   

    # US Velocity of M2 Money Stock 
    st.write('US Velocity of M2 Money Stock')
    st.line_chart(moneysupplydf['M2V'])
    
    # Total Assets, All Commercial Banks 
    st.write('Total Assets, All US Commercial Banks [Billions of $US]')
    st.line_chart(moneysupplydf['TLAACBW027SBOG'])

    # Cash Assets, All Commercial Banks 
    st.write('Cash Assets, All US Commercial Banks [Billions of $US]')
    st.line_chart(moneysupplydf['CASACBW027SBOG'])
    
    # Treasury and Agency Securities, All Commercial Banks   
    st.write('Treasury and Agency Securities, All US Commercial Banks [Billions of $US]')
    st.line_chart(moneysupplydf['USGSEC'])
    
    # Commercial Banks Treasury and Agency Securities/Total Assets Ratio
 
    st.write('US Commercial Banks Treasury and Agency Securities/Total Assets Ratio')
    st.line_chart(moneysupplydf['USGSEC']/moneysupplydf['TLAACBW027SBOG'])
    
    # Cash Assets/Total Assets Ratio
 
    st.write('US Commercial Banks Cash Assets/Total Assets Ratio')
    st.line_chart(moneysupplydf['CASACBW027SBOG']/moneysupplydf['TLAACBW027SBOG'])

    # Bank Credit All US Commercial Banks
    st.write('Bank Credit All US Commercial Banks [Billions of $US]')
    st.line_chart(moneysupplydf['TOTBKCR'])   

    # Total US Consumer Credit Owned and Securitized, Outstanding
    st.write('Total US Consumer Credit Owned and Securitized, Outstanding [Billions of $US]')
    st.line_chart(moneysupplydf['TOTALSL'])   

elif choice == "Federal Finance":
    st.subheader('Federal Finance')

    # Federal Receipts 
    st.write('US Federal Receipts [Millions of $US]')
    st.line_chart(federalfinancedf['FGRECPT']) 

    # Federal government current tax receipts
    st.write('US Federal government current tax receipts [Billions of $US]')
    st.line_chart(federalfinancedf['W006RC1Q027SBEA'])

    # Federal Government: Current Expenditures
    st.write('US Federal Government: Current Expenditures [Billions of $US]')
    st.line_chart(federalfinancedf['FGEXPND'])  

    # Federal Debt: Total Public Debt
    st.write('US Federal Debt: Total Public Debt [Millions of $US]')
    st.line_chart(federalfinancedf['GFDEBTN'])
    
    # Federal government current expenditures: Interest payments 
    st.write('US Federal government current expenditures: Interest payments [Billions of $US]')
    st.line_chart(federalfinancedf['A091RC1Q027SBEA'])

    # Federal Debt Held by Federal Reserve Banks 
    st.write('US Federal Debt Held by Federal Reserve Banks [Billions of $US]')
    st.line_chart(federalfinancedf['FDHBFRBN'])

    # Federal Debt Held by the Public 
    st.write('US Federal Debt Held by the Public [Millions of $US]')
    st.line_chart(federalfinancedf['FYGFDPUN'])

    # Federal Debt Held by Foreign and International Investors
    st.write('US Federal Debt Held by Foreign and International Investors [Billions of $US]')
    st.line_chart(federalfinancedf['FDHBFIN'])


elif choice == "Commodities":

    st.subheader('Precious Metals')
 
    # Gold Fixing Price 10:30 A.M. (London time) in London Bullion Market    
    st.write('Gold Fixing Price ($US per Troy Ounce) - 10:30 A.M. Londin time')
    st.line_chart(commoditydf['GOLDPMGBD228NLBM'])
    
    # Silver Fixing Price 12:00 noon (London time) in London Bullion Market
    st.write('Silver Fixing Price ($US per Troy Ounce) - 12:00 noon London time')
    st.line_chart(commoditydf['SLVPRUSD'])
    
    st.subheader("Energy")

    # Henry Hub Natural Gas Spot Price 
    st.write('Henry Hub Natural Gas Spot Price ($US per Million BTU)')
    st.line_chart(commoditydf['MHHNGSP'])

    # West Texas Intermediate Oil Price (WTI)
    st.write('Oil Price [$US per Barrel] - WTI')
    st.line_chart(commoditydf['DCOILWTICO'])

    # Global price of Coal, Australia 
    st.write('Global price of Coal [$US per Metric Ton]')
    st.line_chart(commoditydf['PCOALAUUSDM'])

    # Global price of Uranium 
    st.write('Global price of Uranium [$US per Pound]')
    st.line_chart(commoditydf['PURANUSDM'])

    st.subheader("Industry Metals")

    # Global price of Iron Ore
    st.write('Global price of Iron Ore [$US per Metric Ton]')
    st.line_chart(commoditydf['PIORECRUSDM'])

    # Global price of Aluminum 
    st.write('Global price of Aluminum [$US per Metric Ton]')
    st.line_chart(commoditydf['PALUMUSDM'])

    # Global price of Nickel 
    st.write('Global price of Nickel [$US Dollars per Metric Ton]')
    st.line_chart(commoditydf['PNICKUSDM'])

    # Global price of Copper 
    st.write('Global price of Copper [$US per Metric Ton]')
    st.line_chart(commoditydf['PCOPPUSDM'])

    # Copper/Gold
    st.write('Copper/Gold Ratio')
    st.line_chart(commoditydf['Copper/Gold Ratio'])
    
    st.subheader("Agriculture")

    # Global price of Corn 
    st.write('Global price of Corn [$US per Metric Ton]')
    st.line_chart(commoditydf['PMAIZMTUSDM'])
                  
    # Global price of Wheat
    st.write('Global price of Wheat [$US per Metric Ton]')
    st.line_chart(commoditydf['PWHEAMTUSDM'])

    # Global price of Palm Oil 
    st.write('Global price of Palm Oil [$US per Metric Ton]')
    st.line_chart(commoditydf['PPOILUSDM'])

    # Global price of Soybeans 
    st.write('Global price of Soybeans [$US per Metric Ton]')
    st.line_chart(commoditydf['PSOYBUSDM'])

    st.subheader("Producer Price Index")
    st.write("(Index 1982 = 100)")
    
    # Producer Price Index by Commodity: All Commodities
    st.write('Producer Price Index by Commodity: All Commodities')
    st.line_chart(ppidf['PPIACO'])   

    # Producer Price Index by Commodity: Metals and Metal Products: Iron and Steel
    st.write('Producer Price Index by Commodity: Metals and Metal Products: Iron and Steel')
    st.line_chart(ppidf['WPU101'])

    # Producer Price Index by Commodity: Special Indexes: Construction Materials
    st.write('Producer Price Index by Commodity: Special Indexes: Construction Materials')
    st.line_chart(ppidf['WPUSI012011'])

    # Producer Price Index by Commodity: Lumber and Wood Products: Softwood Lumber 
    st.write('Producer Price Index by Commodity: Lumber and Wood Products: Softwood Lumber')
    st.line_chart(ppidf['WPS0811'])

    # Producer Price Index by Commodity: Lumber and Wood Products: Plywood
    st.write('Producer Price Index by Commodity: Lumber and Wood Products: Plywood')
    st.line_chart(ppidf['WPU083'])

    # Producer Price Index by Industry: Plastics Material and Resins Manufacturing
    st.write('Producer Price Index by Industry: Plastics Material and Resins Manufacturing')
    st.line_chart(ppidf['PCU325211325211'])

    # Producer Price Index by Industry: Semiconductor and Other Electronic Component Manufacturing
    st.write('Producer Price Index by Industry: Semiconductor and Other Electronic Component Manufacturing')
    st.line_chart(ppidf['PCU33443344'])

    # Producer Price Index by Industry: Chemical Manufacturing
    st.write('Producer Price Index by Industry: Chemical Manufacturing')
    st.line_chart(ppidf['PCU325325'])
    

elif choice == "Economic Performance":
    st.subheader("Economic Performance")

    # US Gross Domestic Product (GDP)
    st.write('US GDP')
    st.line_chart(economicperformdf['GDP'])

    # US Real GDP
    st.write('US Real GDP')
    st.line_chart(economicperformdf['GDPC1'])
    
    # US All Sectors; Total Debt Securities; Liability, Level 
    st.write('US All Sectors; Total Debt Securities; Liability,')
    st.line_chart(economicperformdf['ASTDSL'])
    
    # US All Sectors; Total Debt Securities / GDP Ratio
    st.write('US All Sectors; Total Debt Securities / GDP Ratio')
    st.line_chart((economicperformdf['ASTDSL']/1000)/economicperformdf['GDP'])
    
    # US All Sectors; Total Debt Securities / M2 Ratio
    st.write('US All Sectors; Total Debt Securities / M2 Ratio')
    st.line_chart(((economicperformdf['ASTDSL']/1000)/moneysupplydf['WM2NS']).interpolate(method='linear'))
    
    # US Median Consumer Price Index(CPI)
    st.write('Median CPI')
    st.line_chart(economicperformdf['MEDCPIM158SFRBCLE'])
    
    # Sticky Price Consumer Price Index less Food and Energy
    st.write('Core CPI (less Food&Energy)')
    st.line_chart(economicperformdf['CORESTICKM159SFRBATL'])
    
    st.subheader("Labor Market")

    # US Unemployment Rate (U3&U6)
    st.write('US Unemployment Rate (U3&U6)')
    multiline_viz(economicperformdf, 'UNRATE', 'U6RATE')
    
    # US Personal Savings Rate
    st.write('US Personal Saving Rate')
    st.line_chart(economicperformdf['PSAVERT'])

    # US Average Hourly Earnings of All Employees, Total Private
    st.write('US Average Hourly Earnings of All Employees [$US]')
    st.line_chart(economicperformdf['CES0500000003'])
    
    # US Average Weekly Earnings of All Employees, Total Private
    st.write('US Average Weekly Earnings of All Employees [$US]')
    st.line_chart(economicperformdf['CES0500000011'])

    st.subheader("Business Activity")

    # Capacity Utilization: Total Index 
    st.write('US Capacity Utilization [% of Capacity]')
    st.line_chart(economicperformdf['TCU'])                                         

    # Rental Vacancy Rate for the United States  
    st.write('US Rental Vacancy Rate [%]')
    st.line_chart(economicperformdf['RRVRUSQ156N'])

    # Homeowner Vacancy Rate for the United States
    st.write('US Homeowner Vacancy Rate [%]')
    st.line_chart(economicperformdf['RHVRUSQ156N'])        

    # Total Business Sales 
    st.write('US Total Business Sales [Millions of $US]')
    st.line_chart(economicperformdf['TOTBUSSMSA'])            

    # Total Business Inventories
    st.write('US Total Business Inventories [Millions of $US]')
    st.line_chart(economicperformdf['BUSINV'])

    # Total Business: Inventories to Sales Ratio
    st.write('US Total Business: Inventories to Sales Ratio')
    st.line_chart(economicperformdf['ISRATIO'])     

    # Manufacturers New Orders: Durable Goods
    st.write('US Manufacturers New Orders: Durable Goods [Millions of $US]')
    st.line_chart(economicperformdf['DGORDER'])   

    # Manufacturers' Value of Shipments: Durable Goods 
    st.write('US Manufacturers Value of Shipments: Durable Goods  [Millions of $US]')
    st.line_chart(economicperformdf['AMDMVS'])   


elif choice == "About":
    st.info("Built with Streamlit by [Lifelonglearner](https://www.lifelonglearner.de/)")
    st.text("LifelongLearner")
