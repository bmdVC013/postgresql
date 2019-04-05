#!/usr/bin/python
import psycopg2
from config import config
import os

def write_blob(part_id, path_to_file, file_extension):
	"""Insert a BLOB into a table"""
	conn = None
	try:
		# read data from a picture
		drawing = open(path_to_file, 'rb').read()
		# read database configuration
		params = config()
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)
		# create a new cursor object
		cur = conn.cursor()
		# execute the INSERT statement
		cur.execute("""INSERT INTO part_drawings(part_id, file_extension, drawing_data)
					 VALUES (%s, %s, %s)""",
					 (part_id, file_extension, psycopg2.Binary(drawing)))
		# commit the changes to the database
		conn.commit()
		# close the communication with the PostgreSQL database
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

# if __name__ == '__main__':
# 	write_blob(1, 'images/simtray.jpg', 'jpg')
# 	write_blob(2, 'images/speaker.jpg', 'jpg')

def read_blob(part_id, path_to_dir):
	"""Read BLOB data from a table"""
	conn = None
	try:
		# read database configuration
		params = config()
		# connect to PostgreSQL database
		conn = psycopg2.connect(**params)
		# create a new cursor object
		cur = conn.cursor()
		# execute the SELECT statement
		cur.execute("""	SELECT part_name, file_extension, drawing_data
						FROM part_drawings
						INNER JOIN parts on parts.part_id = part_drawings.part_id
						WHERE parts.part_id = %s""",
						(part_id,))
		blob = cur.fetchone()

		if not os.path.exists(path_to_dir):
			os.mkdir(path_to_dir)
			print("Directory ", path_to_dir, " created.")
		else:
			print("Directory ", path_to_dir, " already exists.")
		
		file_name = blob[0] + '.' + blob[1]
		open(path_to_dir + file_name, 'wb').write(blob[2])
		print("Save ", file_name, " done.")
		# close the communication
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

if __name__ == '__main__':
	read_blob(1, 'images/blob/')
