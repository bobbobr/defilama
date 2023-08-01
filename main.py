import pandas as pd
import requests
import json
from datetime import datetime
import time
import math
import streamlit as st

#baseUrl = 'https://api.llama.fi'
baseUrl = "https://yields.llama.fi"

# protocols endpoint
#protocols = requests.get(baseUrl + '/protocols')
protocols = requests.get(baseUrl +'/pools')

protocolData = pd.DataFrame.from_dict(protocols.json()["data"])
protocolDatast = protocolData.loc[(protocolData['stablecoin'] == True) & (protocolData['tvlUsd'] >= 500000)]
protocolDatast.sort_values(by=['apyPct7D'],ascending=False)

st.title('DeFi Lama analysis')
show_data = st.expander("Посмотреть данные")

with show_data:
    st.write(protocolDatast.head(20))
st.caption('Write smth')
sel = st.selectbox("Параметр", protocolDatast.columns)
st.write(protocolDatast.sort_values(by=sel, ascending=False))

st.caption('Then we can check by specific pool and date')

find = st.selectbox("Symbols", protocolDatast.symbol)

pool = protocolDatast.loc[protocolDatast['symbol'] == find]

st.write(pool)
# Выбор значения из столбца "project"
find2 = st.selectbox("Project", pool['project'])

# Фильтрация строк по выбранному значению из столбца "project"
pool2 = pool.loc[pool['project'] == find2]
st.write(pool2)

# Выбор значения из столбца "chain"
find3 = st.selectbox("Chain", pool2['chain'])

# Фильтрация строк по выбранному значению из столбца "chain"
pool3 = pool2.loc[pool2['chain'] == find3, 'pool']

st.write("Соответствующее значение из столбца 'pool':", pool3.values[0] if not pool3.empty else "Значение не найдено")

baseUrl2 = "https://yields.llama.fi/chart/"


df = requests.get(baseUrl2 +pool3.values[0])
da = pd.DataFrame.from_dict(df.json()["data"])
st.write(da)


start_date = st.date_input("Select start date")
end_date = st.date_input("Select end date")

# Convert the selected dates to strings in the format "YYYY-MM-DD" for filtering
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")


# Filter the DataFrame based on the selected time range
filtered_data = da[(da["timestamp"] >= start_date_str) & (da["timestamp"] <= end_date_str)]


fi = st.selectbox("Параметр", da.columns[1:])
if not filtered_data[fi].notna().any():

    st.write("No data available for the selected time range.")

else:
    # Calculate the change in the second column over the selected time range
    change_in_second_column =  filtered_data[fi].iloc[-1] / filtered_data[fi].iloc[0] - 1

    # Display the filtered data and the calculated change
    st.write("Filtered Data for the selected time range:")
    st.write(filtered_data)



    change_in_second_column_rounded = round(change_in_second_column*100, 2)
    st.write(f"Change in {fi} over the selected time range: {change_in_second_column_rounded:.2f}%")


