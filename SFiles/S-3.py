from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName('fruits liked').getOrCreate()

data =[('111',),('222',),('*',),('333',),('444',),('???',)]

df = spark.createDataFrame(data,['value'])
df.show()

res = df.filter(f.col('value').rlike('^[0-9]+$'))
res.show()
