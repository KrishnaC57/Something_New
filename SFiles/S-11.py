from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, sum, avg
from pyspark.sql.window import Window

Spark = SparkSession.builder.appName('Tickets').getOrCreate()

data1 = [(1, 'John'),(2, 'Mary'),(3, 'David'),(4, 'Sarah'),(5, 'Robert')]
columns1 = ['CustomerID', 'CustName']

Customers = Spark.createDataFrame(data1, columns1)
Customers.show()

data2 = [(101, 1),(102, 1),(103, 2),(104, 3),(105, 3),(106, 3),(107, 5)]
columns2 = ['OrderID', 'CustomerID']

Orders = Spark.createDataFrame(data2, columns2)
Orders.show()

procdf = Customers.join(Orders, on = "CustomerID", how ="inner")\
                    .groupBy('CustomerID','CustName')\
                    .agg(count("*").alias("TotalOrders"))
procdf.show()
result = procdf.withColumn('CustomerType', when(col("TotalOrders").between(2,5),"Regular Customer")\
                            .when(col("TotalOrders") == 1,"New Customer")\
                            .when(col("TotalOrders") > 5,"VIP Customer"))
result.show()
