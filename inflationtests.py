#3qzKshxVDHS9sL7vkphZ
import nasdaqdatalink
import quandl

# Get inflation data from Quandl
quandl.ApiConfig.api_key = "3qzKshxVDHS9sL7vkphZ"
data = quandl.get("RATEINF/CPI_USA", start_date="2021-12-31", end_date="2023-03-28")

# Calculate inflation rate
inflation_rate = (data.iloc[-1]['Value'] - data.iloc[0]['Value']) / data.iloc[0]['Value']

# Calculate the value of 500 dollars in December 2022 versus the value of 500 dollars now
value_in_december_2022 = 500 / data.iloc[0]['Value']
value_now = value_in_december_2022 * data.iloc[-1]['Value']

amount_now = 500 * inflation_rate
amount_after_conv = 500-amount_now

# Print results
print(f"The inflation rate from December 2022 to February 2023 is {inflation_rate:.2%}")
print(f"The value of 500 dollars in December 2021 is {value_in_december_2022:.2f} CPI-adjusted dollars")
print(f"The value of 500 dollars now (April 2023) is {value_now:.2f} CPI-adjusted dollars")
print(f"The value of 500 dollars in Dec22 is now worth (April 2023) {amount_after_conv:.2f}")
