import pandas as pd
import numpy as np
from datetime import datetime, timezone


def import_data(csv_file):
    '''
    filter solscan data to include only enteries where user Transfered SOL
    '''
    df = pd.read_csv(csv_file)
    df_new = pd.DataFrame(df)
    df_filtered = df[(df['Action'] == 'TRANSFER') & (df['TokenAddress'] == 'SOL')]
    # print(df_filtered)
    return df_filtered

def add_date_col(df):
    '''
    function to create new col to represent Time in a more regular format
    '''
    df['Real_Time'] = df['Time'].apply(lambda x: datetime.fromtimestamp(x, tz=timezone.utc))
    # print(df)
    return df

def recieved_sol(df,wallet):
    ##keep all the wallet that recieved at .2 solana from somewhere
    filtered_df = df[(df['To'] == wallet) & (df['Amount'] > 200000000)]
    ##Print all the different wallets from the "From" col
    from_list = filtered_df['From'].tolist()
    unique_reciever_from_list = list(set(from_list))
    print("list of wallets that recieved sol: " , unique_reciever_from_list)
    return unique_reciever_from_list

def sent_sol(df,wallet):
    filtered_df = df[(df["From"] == wallet) & (df['Amount'] > 200000000)]
    from_list = filtered_df['To'].tolist()
    unique_sender_from_list = list(set(from_list))
    print("list of wallets that sent sol: " , unique_sender_from_list)
    return unique_sender_from_list

def compare_wallets(received_list, sent_list):
    # Convert lists to sets for easier comparison
    received_set = set(received_list)
    sent_set = set(sent_list)

    # Find common wallets
    common_wallets = received_set.intersection(sent_set)

    # Find unique wallets to each list
    unique_to_received = received_set - sent_set
    unique_to_sent = sent_set - received_set

    # Print results
    # common wallets are most likely the same owner as the owner of "wallet"
    print("Common wallets that both sent and received SOL:", common_wallets)
    print("Wallets that received SOL but did not send SOL:", unique_to_received)
    print("Wallets that sent SOL but did not receive SOL:", unique_to_sent)

    # Return results
    return {
        'common': list(common_wallets),
        'unique_to_received': list(unique_to_received),
        'unique_to_sent': list(unique_to_sent)
    }



def main():
    wallet = 'inputwallet'
    csv_file = "solscanTransfer.csv"
    filtered_df = import_data(csv_file)
    dated_df = add_date_col(filtered_df)
    received_list = recieved_sol(dated_df,wallet)
    sent_list = sent_sol(dated_df,wallet)
    compare_wallets(received_list, sent_list)


if __name__ == "__main__":
    main()



# --------------------------------------------------------------------------------------------------
'''
Equivalent SQL queries to the functions above, replace "inputwallet" with wallet address
'''

# -- Create a filtered view to include only entries where the user transferred SOL
# CREATE VIEW filtered_solscan AS
# SELECT *
# FROM solscan_transfers
# WHERE Action = 'TRANSFER' AND TokenAddress = 'SOL';

# -- Add a readable date format column to the filtered data
# ALTER TABLE filtered_solscan
# ADD COLUMN Real_Time TIMESTAMPTZ;

# UPDATE filtered_solscan
# SET Real_Time = to_timestamp(Time);

# -- List unique wallets that received more than 0.2 SOL
# CREATE VIEW received_wallets AS
# SELECT DISTINCT "From" AS Wallet
# FROM filtered_solscan
# WHERE "To" = 'inputwallet'
#   AND Amount > 200000000;

# -- List unique wallets that sent more than 0.2 SOL
# CREATE VIEW sent_wallets AS
# SELECT DISTINCT "To" AS Wallet
# FROM filtered_solscan
# WHERE "From" = 'inputwallet'
#   AND Amount > 200000000;

# -- Common wallets that both sent and received SOL
# SELECT Wallet
# FROM received_wallets
# INTERSECT
# SELECT Wallet
# FROM sent_wallets;

# -- Wallets that received SOL but did not send SOL
# SELECT Wallet
# FROM received_wallets
# EXCEPT
# SELECT Wallet
# FROM sent_wallets;

# -- Wallets that sent SOL but did not receive SOL
# SELECT Wallet
# FROM sent_wallets
# EXCEPT
# SELECT Wallet
# FROM received_wallets;
