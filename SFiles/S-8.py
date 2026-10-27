from pyspark.sql import SparkSession
from pyspark.sql import functions as f
spark = SparkSession.builder.appName("JoinExample").getOrCreate()

data = [(1,1),(1,2),(1,3),(2,4),(2,5),(3,6),(3,4)]
df = spark.createDataFrame(data,['id','data'])
df.show()

result = df.groupBy("id").agg(f.collect_list('data').alias('data')).withColumn("data",f.concat_ws(', ',"data"))
result.show()
