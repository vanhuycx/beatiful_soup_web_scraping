import pandas as pd

df = pd.read_csv('Customer.csv')

print(df[(df['Payment Method']=='cash')])

# print(df)


# df = pd.DataFrame({"a": [1, 2, 3, 4]}, index=['A', 'b', 'C', 'd'])
# print(df.sort_index())

