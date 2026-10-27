from pyspark.sql import SparkSession
from pyspark.sql.functions import col,desc
from pyspark.sql.window import Window

spark = SparkSession.builder.appName('z sql 5').getOrCreate()

data = [('Brazil', 10000),('India', 15000),('US', 20000),('UK', 12000),('Europe', 12000)]

schema = ['country','population']

df = spark.createDataFrame(data,schema)
df.show()

ind_df = df.filter(col('country') == 'India')

highest_pop = df.filter(col('country') != 'India').orderBy(desc('population')).limit(1)

lowest_pop = df.filter(col('country') != 'India').orderBy('population').limit(1)

res = ind_df.union(highest_pop).union(lowest_pop)
res.show()
