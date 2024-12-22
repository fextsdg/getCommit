import os
repo_name = "libpng"
file_path = "pngrutil.c"
file_name_without_ext, p = os.path.splitext(file_path)  # 去掉扩展名
print(file_name_without_ext, p)
# 目标文件夹路径
save_dir = os.path.join(repo_name, file_name_without_ext)

# 创建文件夹
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"Created directory: {save_dir}")
else:
    print(f"Directory already exists: {save_dir}")