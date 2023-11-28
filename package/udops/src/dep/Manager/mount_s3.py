import os
import subprocess
from psycopg2.extras import RealDictCursor
from udops.src.dep.config.Connection import *
from udops.src.dep.InputProperties import *

import os
prop = properties()
connection = Connection()
conn = connection.get_connection()
class mount_s3:

    def mount_s3_bucket(self,destination_base_path, mount_point):
        # slicing of bucket name
        try:
            path = destination_base_path.replace("s3://", "")
            first_index = path.find("/")
            if first_index != -1:
                bucket_name = path[:first_index] + ":/" + path[first_index + 1:]
            else:
                bucket_name = destination_base_path

            mount_point = "/home/ubuntu/mount/"+str(mount_point)
            os.makedirs(mount_point, exist_ok=True)
            command = f"s3fs {bucket_name} {mount_point}"
            subprocess.run(command, shell=True, check=True)
            return mount_point

        except Exception as e:
            err = str(e)
            print(err)
            return mount_point

    def mount_s3_bucket_indiviual(self,teamname):
        # slicing of bucket name
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select mount_location from cfg_udops_teams_metadata where teamname = '{teamname}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            mount_location = rows['mount_location']
            conn.commit()

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select s3_destination_path from cfg_udops_teams_metadata where teamname = '{teamname}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            s3_destination_path = rows['s3_destination_path']
            conn.commit()

            path = s3_destination_path.replace("s3://", "")
            first_index = path.find("/")
            if first_index != -1:
                bucket_name = path[:first_index] + ":/" + path[first_index + 1:]
            else:
                bucket_name = s3_destination_path
            print(f"bucket_name--> {bucket_name}")

            #mount_point = "/home/ubuntu/mount/"+str()
            os.makedirs(mount_location, exist_ok=True)
            command = f"s3fs {bucket_name} {mount_location}"
            subprocess.run(command, shell=True, check=True)
            return 1

        except Exception as e:
            err = str(e)
            print(err)
            return 2

    def unmount_s3_bucket(self, teamname):
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"select mount_location from cfg_udops_teams_metadata where teamname = '{teamname}';"
            cursor.execute(query)
            rows = cursor.fetchone()
            mount_location = rows['mount_location']
            conn.commit()

            subprocess.run(["fusermount", "-u", ], check=True)
            print(f"S3 bucket at {mount_location} successfully unmounted.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Unable to unmount S3 bucket. {e}")
