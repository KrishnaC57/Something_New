from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, lit

spark = SparkSession.builder.appName("practice").getOrCreate()
sc = spark.sparkContext

lis = [(1, 2), (1, 3), (2, 4), (5, 1), (5, 3), (11, 7), (12, 8), (13, 5), (13, 10), (14, 12), (14, 3), (15, 14), (15, 13)]
schema = ['user_id','follower_id']

df = spark.createDataFrame(lis,schema)
df.show()

userCount = df.select(col('user_id').alias('users')).union(df.select(col('follower_id').alias('users'))).distinct()
userCount.show()

followerCount = df.groupBy('user_id').agg(count('follower_id').alias('followers'))
followerCount.show()

total_users = userCount.count()
print(total_users)

result = followerCount.withColumn('followers_percentage', (col('followers')*100)/ lit(total_users) )

result.show()
