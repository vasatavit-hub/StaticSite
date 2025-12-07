#Clean public
#Copy static to public
import os
import shutil

src = "./static"
dst = "./public"

def static_to_public():
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    data = os.listdir(src)
    for dat in data:
        create(dat)

def create(data,path=""):
    if os.path.isfile(src + path+"/"+data):
        print(f"Copy {data} to {dst+path}")
        shutil.copy(src+path+"/"+data,dst+path+"/"+data)
    else:
        print(f"Creating {data} directory in {dst+path}")
        path += "/" + data
        os.mkdir(dst+path)
        data = os.listdir(src+path)
        for dat in data:
            create(dat,path)