import os, cx_Oracle, pandas as pd 
def load_data(sql_string):
	"""Connect to DB and return data.
	Parameters
	----------
	sql_string : string
	An sql string.
	Returns
	-------
	df : dataframe
	A dataframe according to database.
	"""
	# Add database path
	os.environ['PATH'] = r'C:\\oracle\\instantclient_11_2\\;' + os.environ['PATH']

	# Tests/Connects database connection
	dsn_tns = cx_Oracle.makedsn(
	    'dtdm-scan.odontoprev.com.br', '1521', service_name='DCMS')
	conn = cx_Oracle.connect(user=r'admprod', password='cessys',
	                         dsn=dsn_tns, mode=cx_Oracle.DEFAULT_AUTH)

	# Load table to a DataFrame
	df = pd.read_sql(sql_string, conn)

	# Close database connection
	conn.close()

	return df
