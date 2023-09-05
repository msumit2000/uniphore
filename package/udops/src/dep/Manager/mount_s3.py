import os
import subprocess

class mount_s3:
    def mount_s3_bucket(self,bucket_name, mount_point):

        mount_point = "/home/ubuntu/mount/"+str(mount_point)
        print(f"mount_point-->{mount_point}")
        os.makedirs(mount_point, exist_ok=True)
        print("------------------")
        #Mount the S3 bucket using s3fs
       # cmd = f"mount-s3 {bucket_name}  {mount_point}"
        # subprocess.run(["mount-s3", bucket_name,  mount_point])

        cmd = ["goofys", bucket_name, mount_point, "-o", "allow_other"]
        subprocess.run(cmd, check=True)




        # cmd = f"s3fs {bucket_name} {mount_point} -o allow_other -o umask=022"
        # subprocess.run(cmd, shell=True, check=True)

        return mount_point
