from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName('fruits liked').getOrCreate()

data = [('P1','Apple'),('P1','Banana'),('P1','Mango'),('P3','Banana'),('P3','Apple'),('P2','Apple'),('P2','Mango')]

df = spark.createDataFrame(data, ['persons','fruits'])
df.show()

allowed_fruits = ['Apple', 'Banana']

invalid_persons = df.filter(~col('fruits').isin(allowed_fruits)).select('persons').distinct()

valid_persons_df = df.filter(col('fruits').isin(allowed_fruits)).select('persons').distinct()

result_df = valid_persons_df.subtract(invalid_persons)
result_df.show()