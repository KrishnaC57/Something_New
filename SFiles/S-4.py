from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, desc
from pyspark.sql.window import Window

spark = SparkSession.builder.appName('z sql 4').getOrCreate()

data = [('ram', 20, 'Finance',50000),
('Sudeep', 25, 'Sales',30000),
('Suresh', 22, 'Finance',50000),
('Pradeep', 28, 'Finance',20000),
('Iqbal', 22, 'Sales',20000)]

schema = ['Name','Age', 'Department','salary']

df = spark.createDataFrame(data,schema)
df.show()

columns_format = ['Department','Name','Age','salary','avg_sal']

windowSpec = Window.partitionBy('Department')
res = df.withColumn('avg_sal' ,avg('salary').over(windowSpec))\
        .orderBy('Department',desc('Age'))\
        .select(columns_format)
res.show()
