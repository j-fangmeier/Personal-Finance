# Personal-Finance

Personal Finance Analysis

The goal of this project was to use the personal finance website Mint to customize a graphical interface of how I was spending my money.  This project utilizes a Mint api to login to the Mint website automatically.  Once in Mint a csv needs to be created and placed in a directory.  Then the Pandas library is utilized to create a data frame, clean the data, and filter out unnecessary columns.

After Pandas is used to clean the data, Matplotlib is used to create a horizontal bar chart organized by the category and sorted by the amount.  A heatmap is then generated using the Calmaps library which will visualize which days had the highest spending.
