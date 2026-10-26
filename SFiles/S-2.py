from pyspark.sql import SparkSession
from pyspark.sql.functions import lead, col
from pyspark.sql.window import Window

spark = SparkSession.builder.appName('fruits liked').getOrCreate()

data = [('18-11-2022','apple',10),
('18-11-2022','oranges',8),
('19-11-2022','apple',5),
('19-11-2022','oranges',5),
('20-11-2022','apple',7),
('20-11-2022','oranges',10)]

schema = ['sale_date', 'fruit', 'num_sold']

df = spark.createDataFrame(data, schema)
df.show()
window = Window.partitionBy('sale_date').orderBy('sale_date')

res = df.withColumn('sold1', lead('num_sold').over(window))\
        .withColumn('diff', col('num_sold') - col('sold1'))\
        .select('sale_date','diff')\
        .filter(col('diff').isNotNull())
res.show()