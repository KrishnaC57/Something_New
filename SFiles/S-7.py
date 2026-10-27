from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, sum, avg
from pyspark.sql.window import Window

Spark = SparkSession.builder.appName('Tickets').getOrCreate()

data = [('TKT-1001', 'Alex Johnson', 'Resolved', 2.5),
    ('TKT-1002', 'Priya Sharma', 'In Progress', 4.0),
    ('TKT-1003', 'Alex Johnson', 'Closed', 1.5),
    ('TKT-1004', 'Michael Chen', 'Open', 0.0),
    ('TKT-1005', 'Priya Sharma', 'Resolved', 6.0),
    ('TKT-1006', 'Michael Chen', 'Pending', 3.5),
    ('TKT-1007', 'Alex Johnson', 'Closed', 2.0),
    ('TKT-1008', 'Sarah Williams', 'In Progress', 5.0),
    ('TKT-1009', 'Priya Sharma', 'Resolved', 7.5),
    ('TKT-1010', 'Sarah Williams', 'Open', 0.0),
    ('TKT-1011', 'Michael Chen', 'Resolved', 4.5),
    ('TKT-1012', 'Alex Johnson', 'In Progress', 3.0)]

columns = ['TicketID', 'AssignedTo','Status','ResolutionHours']

df = Spark.createDataFrame(data, columns)
df.show()

procdf = df.groupBy('AssignedTo')\
            .agg(
                count("*").alias("TotalTickets"),
                sum(when(col('Status') == "Closed", 1).otherwise(0)).alias("ClosedTickets"),
                avg(when(col('Status') == "Closed",col('ResolutionHours'))).alias("AvgResolutionHours")
            )\
            .fillna(0)\
            .filter(col('TotalTickets') >2)
procdf.show()
