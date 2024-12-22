import os
import requests

# 确保目录存在
def ensure_directory_exists(directory):
    """确保下载目录存在，不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


# 从文件中读取 commit hashes
def read_commit_hashes(file_path):
    """从文件读取 commit hashes"""
    try:
        with open(file_path, 'r') as file:
            commit_hashes = [line.strip() for line in file.readlines()]
        return commit_hashes
    except Exception as e:
        print(f"Error reading commit hashes from {file_path}: {e}")
        return []


# 下载指定 commit 的文件
def download_file_from_commit(commit_hash, repo_owner, repo_name, file_path, save_dir):
    """根据 commit hash 下载文件"""
    # 构建 GitHub 原始文件 URL
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{commit_hash}/{file_path}"
    # 获取文件名（去掉扩展名）
    file_path_parts = file_path.split('/')[-1]
    file_name_without_ext, ext = os.path.splitext(file_path_parts)
    try:
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 根据 commit hash 构造保存的文件名
            file_name = f"{file_name_without_ext}-{commit_hash}{ext}"

            # 确保目录存在
            ensure_directory_exists(save_dir)

            # 保存文件到指定的目录
            file_path_to_save = os.path.join(save_dir, file_name)
            with open(file_path_to_save, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name} from commit {commit_hash} and saved to {save_dir}")
        else:
            print(f"Failed to download file for commit {commit_hash}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error downloading file for commit {commit_hash}: {e}")


# 下载所有 commit 对应的文件
def download_files_for_commits(commit_hashes, repo_owner, repo_name, file_path, save_dir):
    """下载多个 commit 对应的文件"""
    for commit_hash in commit_hashes:
        download_file_from_commit(commit_hash, repo_owner, repo_name, file_path, save_dir)


# 主函数
def main():
    # 设置参数
    repo_owner = "pnggroup"
    repo_name = "libpng"
    file_path = "pngrutil.c"

    # 获取文件名（去掉扩展名）
    file_path_parts = file_path.split('/')[-1]
    file_name_without_ext, ext = os.path.splitext(file_path_parts)

    # commit_hashes.txt 的路径
    comha_file_path = f"./{repo_name}/{file_name_without_ext}/commits_hashes.txt"

    # 读取 commit hashes
    commit_hashes = read_commit_hashes(comha_file_path)

    if not commit_hashes:
        print("No commit hashes found. Exiting.")
        return

    # 目标文件夹路径
    save_dir = os.path.join(repo_name, file_name_without_ext, "downloads")

    # 下载对应的文件并保存到指定目录
    download_files_for_commits(commit_hashes, repo_owner, repo_name, file_path, save_dir)


if __name__ == "__main__":
    main()
