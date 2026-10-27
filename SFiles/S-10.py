from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, collect_set, when, array_contains
spark = SparkSession.builder.appName('BasketTransform').getOrCreate()

data = [('A', 'Apple,Mango,Orange'),('B', 'Apple'),('C', 'Guava,Cherry'),('D', 'Mango,Cherry,Orange')]
schema = ['person','Basket']

df = spark.createDataFrame(data, schema)
df.show()

df = df.withColumn('BasketArr', split(col('Basket'),','))
df.show(truncate = False)

fruits_df = df.select(explode(col("BasketArr")).alias("Fruit")).distinct()

fruits = [row["Fruit"] for row in fruits_df.collect()]
print(fruits)

for fruit in fruits:
    df = df.withColumn(fruit, when(array_contains(col("BasketArr"), fruit), "Yes").otherwise("No"))

df_final = df.select(["Person"] + fruits)    # df.drop('Basket','basketArr')
df_final.show()
