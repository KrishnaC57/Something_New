from pyspark.sql import SparkSession
from pyspark.sql.functions import col, month

# Initialize Spark session
spark = SparkSession.builder.appName("MobileDataAnalysis").getOrCreate()

# Sample data
data = [
    (12345, '9988445566', 'outgoing', '2022-01-23'),
    (67890, '8899445566', 'incoming', '2022-02-01'),
    (78915, '7799884455', 'outgoing', '2022-01-23'),
    (12345, '6698112244', 'outgoing', '2022-02-02'),
    (12345, '5598445566', 'incoming', '2022-01-24'),
    (12345, '1199885544', 'outgoing', '2022-02-05')
]

# Create DataFrame
columns = ["user_id", "mobile_number", "msg_type", "mob_date"]
df = spark.createDataFrame(data, columns)

# Convert mob_date to date type
df = df.withColumn("mob_date", col("mob_date").cast("date"))
df.show()

# Filter outgoing messages for January
jan_df = df.filter((col("msg_type") == "outgoing") & (month(col("mob_date")) == 1)) \
           .groupBy("user_id").count().withColumnRenamed("count", "jan_count")

# Filter outgoing messages for February
feb_df = df.filter((col("msg_type") == "outgoing") & (month(col("mob_date")) == 2)) \
           .groupBy("user_id").count().withColumnRenamed("count", "feb_count")

# Join and filter where February count > January count
result_df = feb_df.join(jan_df, "user_id") \
                  .filter(col("feb_count") > col("jan_count")) \
                  .select("user_id")

result_df.show()
