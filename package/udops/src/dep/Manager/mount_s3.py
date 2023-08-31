import os
import subprocess

class mount_s3:
    def mount_s3_bucket(self,bucket_name, mount_point):
        mount_point = "/home/siddhant/mount"+{mount_point}
        os.makedirs(mount_point, exist_ok=True)

        # Mount the S3 bucket using s3fs
        cmd = f"mount-s3 {bucket_name}  /home/siddhant/mount/{mount_point}"
        subprocess.run(cmd, shell=True, check=True)

        return mount_point