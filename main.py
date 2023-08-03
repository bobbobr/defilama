import pandas as pd
import requests
import streamlit as st
import json
import time


#baseUrl = 'https://api.llama.fi'
baseUrl = "https://yields.llama.fi"

# protocols endpoint
#protocols = requests.get(baseUrl + '/protocols')
protocols = requests.get(baseUrl +'/pools')

#stablecoin = st.checkbox('Only stablecoins')




protocolData = pd.DataFrame.from_dict(protocols.json()["data"])
protocolDatast = protocolData.loc[(protocolData['stablecoin'] == True)]

selected_chains = st.multiselect("Choose chain", protocolDatast.chain.unique())
all_chains = st.checkbox("Select all chains")


if all_chains:
    selected_chains = protocolDatast.chain.unique().tolist()

selected_projects = st.multiselect("Choose project", protocolDatast.project.unique())

all_projects = st.checkbox("Select all projects")


if all_projects:
    selected_projects = protocolDatast.project.unique().tolist()



protocolDatast = protocolDatast[protocolDatast['chain'].isin(selected_chains)]
protocolDatast = protocolDatast[protocolDatast['project'].isin(selected_projects)]
if (len(selected_chains) !=0) & (len(selected_projects) != 0):
    tv = st.number_input("Insert a TVL")
    #tv = st.slider("Choose minimum TVL", protocolDatast.sort_values(by=["tvlUsd"], ascending=False).tvlUsd.iloc[-1],protocolDatast.sort_values(by=["tvlUsd"], ascending=False).tvlUsd.iloc[0])
    protocolDatast = protocolDatast.loc[(protocolDatast['tvlUsd'] >= tv)]
    apy = st.slider("Choose minimum APY", protocolDatast.sort_values(by=["apy"], ascending=False).apy.iloc[-1],protocolDatast.sort_values(by=["apy"], ascending=False).apy.iloc[0])
    protocolDatast = protocolDatast.loc[(protocolDatast['apy'] >= apy)]
else:
    st.write("You should choose chains and projects")


st.title('DeFi Lama analysis')
show_data = st.expander("View Data")

with show_data:
    st.write(protocolDatast.head(20))

sel = st.selectbox("Options", protocolDatast.columns[3:])

def calculate_tvl(data, start, end):
    change_tvl = []
    for i in range(data.pool.shape[0]):
        baseUrl3 = "https://yields.llama.fi/chart/"
        df3 = requests.get(baseUrl3 + data.pool.iloc[i])
        try:
            df3.raise_for_status()  # Check for any request errors
            da = pd.DataFrame.from_dict(df3.json()["data"])
            if len(da) > (end - start):
                # Calculate the change in the second column over the selected time range
                change_in_second_column = da["tvlUsd"].iloc[end] / da["tvlUsd"].iloc[start] - 1
                change_tvl.append(round(change_in_second_column * 100, 2))
            else:
                change_tvl.append(0)
        except (requests.exceptions.HTTPError, json.JSONDecodeError) as e:
            st.write(f"Error: {e}")
            change_tvl.append(0)  # Append 0 in case of an error
        time.sleep(1)
    return change_tvl

#st.write(protocolDatast.sort_values(by=sel, ascending=False)["tvlPct"] == did)
#st.write(protocolDatast.sort_values(by=sel, ascending=False).insert(pd.DataFrame(calculate_tvl(protocolDatast.sort_values(by=sel, ascending=False), start_date_str, end_date_str), columns = ["tvlPct"])))

remember = protocolDatast.sort_values(by=sel, ascending=False)

remember["tvlPct1D"] = calculate_tvl(protocolDatast.sort_values(by=sel, ascending=False),0,1)
remember["tvlPct7D"] = calculate_tvl(protocolDatast.sort_values(by=sel, ascending=False),0,7)
remember["tvlPct30D"] = calculate_tvl(protocolDatast.sort_values(by=sel, ascending=False),0,30)


st.write(remember)

st.write(protocolDatast.sort_values(by=sel, ascending=False))


st.caption('Then we can check by specific pool and date')

#find = st.selectbox("Symbols", protocolDatast.symbol.unique())

#pool = protocolDatast.loc[protocolDatast['symbol'] == find]

#st.write(pool)


# Выбор значения из столбца "project"
#find2 = st.selectbox("Project", pool['project'].unique())

# Фильтрация строк по выбранному значению из столбца "project"
#pool2 = pool.loc[pool['project'] == find2]
#st.write(pool2)

# Выбор значения из столбца "chain"
#find3 = st.selectbox("Chain", pool2['chain'])

# Фильтрация строк по выбранному значению из столбца "chain"
#pool3 = pool2.loc[pool2['chain'] == find3, 'pool']

#st.write("Соответствующее значение из столбца 'pool':", pool3.values[0] if not pool3.empty else "Значение не найдено")

#baseUrl2 = "https://yields.llama.fi/chart/"


#df = requests.get(baseUrl2 + pool3.values[0])
#da = pd.DataFrame.from_dict(df.json()["data"])

#show_data2 = st.expander("View Data")

#with show_data2:
#    st.write(da.head(20))


start_date = st.date_input("Select start date")
end_date = st.date_input("Select end date")

# Convert the selected dates to strings in the format "YYYY-MM-DD" for filtering
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")


# Filter the DataFrame based on the selected time range
#filtered_data = da[(da["timestamp"] >= start_date_str) & (da["timestamp"] <= end_date_str)]


#fi = st.selectbox("Options", da.columns[1:])
#if not filtered_data[fi].notna().any():

#    st.write("No data available for the selected time range.")

#else:

    # Calculate the change in the second column over the selected time range
   # change_in_second_column =  filtered_data[fi].iloc[-1] / filtered_data[fi].iloc[0] - 1

    # Display the filtered data and the calculated change
   # st.write("Filtered Data for the selected time range:")
   # st.write(filtered_data)



   # change_in_second_column_rounded = round(change_in_second_column*100, 2)
    #st.write(f"Change in {fi} over the selected time range: {change_in_second_column_rounded:.2f}%")


selected_symbols2 = st.multiselect("Choose symbols", protocolDatast.symbol.unique())


new_pool = protocolDatast.loc[protocolDatast['symbol'].isin(selected_symbols2)]


selected_chains2 = st.multiselect("Choose chain", new_pool.chain.unique())

new_pool = new_pool.loc[new_pool['chain'].isin(selected_chains2)]

selected_projects2 = st.multiselect("Choose project", protocolDatast.project.unique())

new_pool = new_pool.loc[new_pool['project'].isin(selected_projects2)]

st.write(new_pool)


fi = st.selectbox("Optiosssns", new_pool.columns[3:7])


for i in range(new_pool.shape[0]):
        baseUrl3 = "https://yields.llama.fi/chart/"
        df3 = requests.get(baseUrl3 + new_pool.values[i][8])
        da = pd.DataFrame.from_dict(df3.json()["data"])
        filtered_data = da[(da["timestamp"] >= start_date_str) & (da["timestamp"] <= end_date_str)]

        if not filtered_data[fi].notna().any():
            st.write("No data available for the selected time range based on your option.")
            break
        else:

            # Calculate the change in the second column over the selected time range
            change_in_second_column = filtered_data[fi].iloc[-1] / filtered_data[fi].iloc[0] - 1



            change_in_second_column_rounded = round(change_in_second_column * 100, 2)
            #st.write(f"Change in {fi} over the selected time range is  {change_in_second_column_rounded:.2f}% for {new_pool.values[i][1]} {new_pool.values[i][0]} {new_pool.values[i][2]}")


