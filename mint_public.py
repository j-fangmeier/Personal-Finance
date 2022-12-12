import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import calmap
import mintapi


#Launch and Login to Mint to download transaction data
mint = mintapi.Mint(
    'Username',  # Email used to log in to Mint
    'Password',  # Your password used to log in to mint
    # Optional parameters
    mfa_method='sms',  # See MFA Methods section
                       # Can be 'sms' (default), 'email', or 'soft-token'.
                       # if mintapi detects an MFA request, it will trigger the requested method
                       # and prompt on the command line.
    mfa_input_callback=None,  # see MFA Methods section
                              # can be used with any mfa_method
                              # A callback accepting a single argument (the prompt)
                              # which returns the user-inputted 2FA code. By default
                              # the default Python `input` function is used.
    mfa_token=None,   # see MFA Methods section
                      # used with mfa_method='soft-token'
                      # the token that is used to generate the totp
    intuit_account=None, # account name when multiple accounts are registered with this email.
    headless=False,  # Whether the chromedriver should work without opening a
                     # visible window (useful for server-side deployments)
                         # None will use the default account.
    session_path=None, # Directory that the Chrome persistent session will be written/read from.
                       # To avoid the 2FA code being asked for multiple times, you can either set
                       # this parameter or log in by hand in Chrome under the same user this runs
                       # as.
    imap_account=None, # account name used to log in to your IMAP server
    imap_password=None, # account password used to log in to your IMAP server
    imap_server=None,  # IMAP server host name
    imap_folder='INBOX',  # IMAP folder that receives MFA email
    wait_for_sync=False,  # do not wait for accounts to sync
    wait_for_sync_timeout=300,  # number of seconds to wait for sync
    fail_if_stale=True, # True will raise an exception if Mint is unable to refresh your data.
	use_chromedriver_on_path=False,  # True will use a system provided chromedriver binary that
	                                 # is on the PATH (instead of downloading the latest version)
    driver=None        # pre-configured driver. If None, Mint will initialize the WebDriver.
  )

#Place CSV in below location
df = pd.read_csv('Transactions.csv File Location')

#Prompt for date and year transaction data is wanted from
Year = input("What year do you want transaction data starting from?(YYYY) ")
Month = input("What month do you want transaction data starting from?(MM) ")

mint.close()
#Drop unwanted columns and filter data
df1 = df.drop(columns=['Notes','Labels','Original Description'])

df1['Date'] = pd.to_datetime(df1['Date'], format = '%m/%d/%Y')

filtered_df1 = df1.loc[(df1['Date'] >= f'{Year}-{Month}-01')]

filtered_df1 = filtered_df1.loc[(filtered_df1['Transaction Type'] == 'debit')]

filtered_df1 = filtered_df1.loc[(filtered_df1['Category'] != 'Credit Card Payment')]

filtered_df1 = filtered_df1.loc[(filtered_df1['Category'] != 'Transfer')]

filtered_df1 = filtered_df1.loc[(filtered_df1['Category'] != 'Mortgage & Rent')]

filtered_df1 = filtered_df1.loc[(filtered_df1['Category'] != 'Auto Payment')]

#Plot data on horizontal bar chart
plt.figure(figsize=(10,15))

filtered_df1.groupby('Category')[['Amount']].sum().sort_values('Amount',ascending=True).plot.barh()

plt.xlabel('Amount($)', size = 15)
plt.ylabel('Categories', size=15)
plt.title('Total Spending Per Category', size=20)

plt.show()

#Plot data using calmap
date_df = filtered_df1.set_index('Date')
purchases = pd.Series(date_df.Amount)

plt.figure(figsize=(16,8))
calmap.yearplot(data=purchases, year = 2022)
plt.show()