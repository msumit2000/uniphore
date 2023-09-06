import os
import subprocess
class mount_s3:
    def mount_s3_bucket(self,destination_base_path, mount_point):
        # slicing of bucket name
        path  = destination_base_path.replace("s3://", "")
        first_index = s3_path.find("/")
        if first_index != -1:
            bucket_name = path[:first_index] + ":/" + path[first_index + 1:]
        print(f"bucket_name---> {bucket_name}")

        mount_point = "/home/ubuntu/mount/"+str(mount_point)
        os.makedirs(mount_point, exist_ok=True)

        command = f"s3fs {bucket_name}:/Anjali/sumit {mount_point}"
        subprocess.run(command, shell=True, check=True)

        return mount_point
