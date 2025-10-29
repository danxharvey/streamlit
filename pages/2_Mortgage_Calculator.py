import streamlit as st
import pandas as pd
import math

# Neuron 5 logo
st.logo('img/favicon.ico', size="large", link=None, icon_image=None)
st.image('img/bg_logo.png', width=400)  # width in pixels#

# Describe page
st.title(':blue[Mortgage Repayment Calculator]')
st.markdown('**Example of an interactive and dynamic front-end allowing user to calculate mortgage repayments.**')

# Gather user inputs
st.write('&nbsp;')
st.header('Loan Data', divider='red')
col1, col2 = st.columns(2)
home_value = col1.number_input('Home Value (£)', min_value=0, value=500000)
deposit = col1.number_input('Deposit (£)', min_value=0, value=50000)
interest_rate = col2.number_input('Interest Rate (%)', min_value=0.0, value=4.5)
loan_term = col2.number_input('Loan Term (Years)', min_value=1, value=25)

# Calculate the repayments
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
num_payments = loan_term * 12
monthly_payment = (
                    loan_amount
                    * (monthly_interest_rate * (1+monthly_interest_rate) ** num_payments)
                    / ((1 + monthly_interest_rate) ** num_payments-1)
                )

# Calculate repayments
total_payments = monthly_payment * num_payments
total_interest = total_payments - loan_amount

# Display the metrics
st.write('&nbsp;')
st.header('Repayment Analysis', divider='red')
col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Monthly Repayments', value=f'£{monthly_payment:,.2f}')
col2.metric(label='Total Mortgage Cost', value=f'£{total_payments:,.0f}')
col3.metric(label='Interest Repaid', value=f'£{total_interest:,.0f}')
col4.metric(label='Interest Component', value=f'{total_interest/loan_amount*100:,.0f}%')
 
# Create a dataframe with the monthly payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, num_payments+1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance = round(max(0, remaining_balance - principal_payment), 2)
    year = math.ceil(i/12) # Calculate the year of the loan
    schedule.append(
        [
            i, monthly_payment, principal_payment, interest_payment,
            remaining_balance, year
        ]
    )

df = pd.DataFrame(schedule,
                  columns=['Month', 'Payment', 'Principal', 'Interest',
                          'Remaining Balance', 'Year'],
                )

# Display dataframe as a chart
st.write('&nbsp;')
st.header('Repayment Schedule', divider='red')
payments_df = df[['Year', 'Remaining Balance']].groupby('Year').min()
st.line_chart(payments_df, y_label='Value (£)', x_label='Loan Year')