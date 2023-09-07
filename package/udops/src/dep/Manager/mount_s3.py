import os
import subprocess


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
