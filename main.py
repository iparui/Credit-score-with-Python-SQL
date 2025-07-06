


# Import pandas package
import pandas as pd
# Input dummy data
input_data = {
    'user_name': ['Jai12', 'Princi45', 'Gaurav6', 'Anuja120'],
    # Data for credit score calculation
    'on_time_payments': [28, 24, 19, 30],
    'total_payments': [30, 26, 22, 30],

    'credit_used': [3000, 1500, 1000, 0],
    'credit_limit': [10000, 5000, 4000, 1000],

    'oldest_account_years': [5, 3, 2, 8],

    'has_credit_card': [1, 1, 1, 0],
    'has_loan': [0, 1, 1, 1],
    'has_mortgage': [0, 0, 0, 1],

    'num_inquiries': [2, 1, 3, 0]
}
# Make a data frame out of the dummy data
df = pd.DataFrame(input_data)
#print(df)
pd.options.display.max_columns = None
print(df.head())
# Add more coloumns for calculating credit score
df["payment_history"] = (df["on_time_payments"] / df["total_payments"]) * 100
df["credit_utilization"] = (df["credit_used"] / df["credit_limit"]) * 100
df["credit_utilization_score"] = (100 - df["credit_utilization"]).clip(lower=0)
max_reference_age = 10
df["credit_history_length"] = (df["oldest_account_years"] / max_reference_age) * 100
df["credit_history_length"] = df["credit_history_length"].clip(upper=100)
def get_credit_mix_score(row):
    types = [row["has_credit_card"], row["has_loan"], row["has_mortgage"]]
    num_types = sum(types)
    return {0: 0, 1: 50, 2: 75, 3: 100}.get(num_types, 0)
df["credit_mix_score"] = df.apply(get_credit_mix_score, axis=1)
df["new_credit"] = (100 - df["num_inquiries"] * 15).clip(lower=0)

# Final raw score (weighted sum)
df["raw_score"] = (
    df["payment_history"] * 0.35 +
    df["credit_utilization_score"] * 0.30 +
    df["credit_history_length"] * 0.15 +
    df["credit_mix_score"] * 0.10 +
    df["new_credit"] * 0.10
)

# Scale to 300–850 range
df["credit_score"] = 300 + (df["raw_score"] / 100) * 550
df["credit_score"] = df["credit_score"].round()

# Show final output
print(df[["user_name", "credit_score"]])
#connect to sql
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              host='127.0.0.1',
                              database='credit_score')
print("Database Connected")

#Opening table
mycursor = cnx.cursor()
mycursor.execute("SELECT COUNT(*) AS column_count FROM information_schema.COLUMNS WHERE table_name = 'credit_score_table_output';")
coloumn_count_result=mycursor.fetchone()
print(f"Column count: {coloumn_count_result[0]}")
mycursor.execute("SELECT COUNT(*) AS row_count FROM credit_score_table_output")
row_count_result=mycursor.fetchone()
print(f"Row count: {row_count_result[0]}")

alter_table_sql = """
ALTER TABLE credit_score_table_output
ADD COLUMN credit_score INT,
ADD COLUMN on_time_payments INT,
ADD COLUMN total_payments INT,
ADD COLUMN credit_used INT,
ADD COLUMN credit_limit INT,
ADD COLUMN oldest_account_years INT,
ADD COLUMN has_credit_card TINYINT,
ADD COLUMN has_loan TINYINT,
ADD COLUMN has_mortgage TINYINT,
ADD COLUMN num_inquiries INT;
"""

mycursor.execute(alter_table_sql)

mycursor.execute("SELECT COUNT(*) AS column_count FROM information_schema.COLUMNS WHERE table_name = 'credit_score_table_output';")
coloumn_count_result=mycursor.fetchone()
print(f"Column count after altering: {coloumn_count_result[0]}")
# Make a function to add dataframe from Python to mysql database
def add_df_to_sql(df, mycursor, cnx):
    sql = "INSERT INTO credit_score_table_output (user_name, credit_score, on_time_payments, total_payments, credit_used, credit_limit, oldest_account_years, has_credit_card, has_loan, has_mortgage, num_inquiries) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # Loop over DataFrame rows
    for index, row in df.iterrows():
        val = (row['user_name'], row['credit_score'], row['on_time_payments'], row['total_payments'], row['credit_used'], row['credit_limit'], row['oldest_account_years'], row['has_credit_card'], row['has_loan'], row['has_mortgage'], row['num_inquiries'])
        mycursor.execute(sql, val)

    # Commit the transaction
    cnx.commit()
    print(f"{len(df)} record(s) inserted.")
add_df_to_sql(df, mycursor, cnx)
#Check if the row count after adding data to data base
mycursor.execute("SELECT COUNT(*) AS row_count FROM credit_score_table_output")
row_count_result=mycursor.fetchone()
print(f"Row count after: {row_count_result[0]}")



cnx.close()

