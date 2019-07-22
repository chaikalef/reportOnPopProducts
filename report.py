from pandas import DataFrame, Timestamp, read_csv, to_datetime
from pandas.tseries.offsets import DateOffset

# Params
# Paths
ordersPath = 'orders.csv'
ordersLinesPath = 'orders_lines.csv'
resPath = 'res.csv'

# Column names
dateTimeColName = 'DateTime'
prodIdColName = 'ProductId'
priceColName = 'Price'
orderIdColName = 'OrderId'
newColumns = [
    'prodFreq',
    'profitPerProd',
    'meanCheck'
]
# Date offsets
yearsOffset = 0
monthsOffset = 1
daysOffset = 0

# Calc offset date and time
dateTimeThreshold = Timestamp.now() - DateOffset(
    years=yearsOffset,
    months=monthsOffset,
    days=daysOffset
)

# Read CSV
orders = read_csv(ordersPath)
ordersLines = read_csv(ordersLinesPath)
print('\nOrders shape: ')
print(orders.shape)
print('\nOrders_lines shape: ')
print(ordersLines.shape)

# Create Primary Key
PK = set(orders.columns).intersection(set(ordersLines.columns))
print('\nPrimary key: ')
print(PK)

# Create table with new orders and delete dataTime col
orders = orders[
    to_datetime(orders[dateTimeColName]) >= dateTimeThreshold
][
    set(orders.columns) - {dateTimeColName}
]
print('\nOrders: ')
print(orders)

# Create inner joined table with all columns
newProds = ordersLines.merge(
    orders,
    how='inner',
    on=list(PK)
)
print('\nJoined table: ')
print(newProds)

# Create sort table (ProductId, Frequency)
popProds = newProds[prodIdColName].value_counts().rename_axis(
    prodIdColName).reset_index(name=newColumns[0])
print('\nFrequency per product: ')
print(popProds)

# Create profit per product
profitPerProd = newProds.groupby(prodIdColName)[priceColName].sum(
).rename_axis(prodIdColName).reset_index(name=newColumns[1])
print('\nProfit per product: ')
print(profitPerProd)

# Add profit to popProds table
popProds = popProds.merge(
    profitPerProd,
    how='inner',
    on=prodIdColName
)
print('\nFrequency per product and profit per product: ')
print(popProds)

# Create profit per order (check per customer)
profitPerOrder = newProds.groupby(orderIdColName)[priceColName].sum(
).rename_axis(orderIdColName).reset_index(name='check')
print('\nProfit per order: ')
print(profitPerOrder)

# Add empty new column
popProds[newColumns[2]] = None
print('\nFrequency per product, profit per product and empty column: ')
print(popProds)

for prodId in popProds[prodIdColName]:
    print('\n\nProduct Id: ' + str(prodId))

    # Find orders which contain product with prodId
    ordersWithProdId = newProds[
        newProds[prodIdColName] == prodId
    ][orderIdColName].tolist()
    print('Orders which contain product ' + str(prodId) + ': ')
    print(ordersWithProdId)

    # Filter profit per order (check per customer) by containing of product
    # with prodId
    profitPerOrderWithProdId = profitPerOrder[
        profitPerOrder[orderIdColName].isin(ordersWithProdId)
    ]
    print('Filtered profit per order: ')
    print(profitPerOrderWithProdId)

    # Calc mean profit per order (mean check per customer) which contain
    # product with prodId
    meanProfitPerOrderWithProdId = profitPerOrderWithProdId['check'].mean()
    print('Mean profit per order: ' + str(meanProfitPerOrderWithProdId))

    # Add mean profit per order (mean check per customer) to popProds table
    indexOfCurProdIdInPopProds = popProds.index[popProds[prodIdColName] == prodId][0]
    popProds.loc[
        indexOfCurProdIdInPopProds, newColumns[2]
    ] = meanProfitPerOrderWithProdId


print('\n\nFrequency per product, profit per product and mean check: ')
print(popProds)
popProds.to_csv(
    path_or_buf=resPath,
    index=False
)
