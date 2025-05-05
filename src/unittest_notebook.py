# Databricks notebook source
# COMMAND ----------

# MAGIC %md
# MAGIC # Unit Tests for Databricks Asset Bundles
# MAGIC 
# MAGIC This notebook runs unit tests for the Databricks Asset Bundles project directly in the Databricks workspace.

# COMMAND ----------

# MAGIC %pip install pytest pytest-html

# COMMAND ----------

import os
import sys
import pytest
import unittest
import datetime
import json
from pyspark.sql import SparkSession

# COMMAND ----------

# Define the test directory path
test_dir = "/tmp/unittest"
os.makedirs(test_dir, exist_ok=True)

# Create a test file
test_file_path = os.path.join(test_dir, "test_main.py")

# COMMAND ----------

# Create the test file content
test_content = """
import unittest
import sys
import os

# Assuming the bundlesDevOpsDemo package is already installed in the cluster
try:
    from bundlesDevOpsDemo import main
    HAS_MODULE = True
except ImportError:
    HAS_MODULE = False

class TestMain(unittest.TestCase):
    def test_module_exists(self):
        """Test if the module exists"""
        self.assertTrue(HAS_MODULE, "bundlesDevOpsDemo module should exist")
        
    @unittest.skipIf(not HAS_MODULE, "Module not available")
    def test_get_taxis_function_exists(self):
        """Test if get_taxis function exists"""
        self.assertTrue(hasattr(main, 'get_taxis'), "get_taxis function should exist")
        
    @unittest.skipIf(not HAS_MODULE, "Module not available")
    def test_get_spark_function_exists(self):
        """Test if get_spark function exists"""
        self.assertTrue(hasattr(main, 'get_spark'), "get_spark function should exist")
    
    @unittest.skipIf(not HAS_MODULE, "Module not available")
    def test_get_taxis_returns_dataframe(self):
        """Test if get_taxis returns a DataFrame"""
        from pyspark.sql import SparkSession, DataFrame
        spark = SparkSession.builder.getOrCreate()
        try:
            df = main.get_taxis(spark)
            self.assertIsInstance(df, DataFrame, "get_taxis should return a DataFrame")
        except Exception as e:
            self.fail(f"get_taxis raised exception {e}")

if __name__ == '__main__':
    unittest.main()
"""

# Write the test content to the file
with open(test_file_path, "w") as f:
    f.write(test_content)

# COMMAND ----------

# Run the tests and generate an HTML report
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
report_path = f"/dbfs/databricks/unittest-results/test_report_{timestamp}.html"
os.makedirs(os.path.dirname(report_path), exist_ok=True)

# Run the tests
result = pytest.main(["-v", test_dir, f"--html={report_path}", "--self-contained-html"])

# COMMAND ----------

# Display the result
if result == 0:
    print("All tests passed!")
else:
    print(f"Some tests failed! Check the report at {report_path}")

# Create a JSON results file that can be easily parsed by automation tools
results_json = {
    "timestamp": timestamp,
    "success": result == 0,
    "report_path": report_path
}

json_path = f"/dbfs/databricks/unittest-results/results_{timestamp}.json"
with open(json_path, "w") as f:
    json.dump(results_json, f)

# Return the exit code for the job
sys.exit(result) 