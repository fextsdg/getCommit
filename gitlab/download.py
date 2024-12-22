import os
import requests

# 下载 GitLab 上的 raw 文件并保存到本地
def download_file_from_commit(repo_owner, repo_name, commit_hash, file_path, save_dir):
    """
    下载 GitLab 上的 raw 文件并保存到本地。
    :param repo_owner: 仓库所有者
    :param repo_name: 仓库名称
    :param commit_hash: 提交的 hash
    :param file_path: 文件路径
    :param save_dir: 保存文件的本地路径
    """
    file_path_parts = file_path.split('/')[-1]
    file_name_without_ext, ext = os.path.splitext(file_path_parts)  # 去掉扩展名
    raw_url = f"https://gitlab.com/{repo_owner}/{repo_name}/-/raw/{commit_hash}/{file_path}"

    print(f"Downloading from: {raw_url}")
    response = requests.get(raw_url)

    if response.status_code == 200:
        # 创建文件夹
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"Created directory: {save_dir}")
        # 根据 commit hash 构造保存的文件名
        file_name = f"{file_name_without_ext}-{commit_hash}{ext}"

        # 保存文件到指定的目录
        file_path_to_save = os.path.join(save_dir, file_name)
        with open(file_path_to_save, 'wb') as file:
            file.write(response.content)
        print(f"File saved to: {file_path_to_save}")
    else:
        print(f"Failed to download file: {response.status_code}")
        print(f"Error: {response.text}")


# 从 commits.txt 文件中读取 commit hash
def read_commit_hashes(filename):
    commit_hashes = []
    with open(filename, 'r') as file:
        for line in file:
            commit_hashes.append(line.strip())
    return commit_hashes


# 主程序
def main():
    repo_owner = "libtiff"  # 仓库所有者
    repo_name = "libtiff"   # 仓库名称
    file_path = "libtiff/tif_dirwrite.c"  # 文件路径
    file_path_parts = file_path.split('/')[-1]
    file_name_without_ext, ext = os.path.splitext(file_path_parts)  # 去掉扩展名
    comha_file_path = f"./{repo_name}/{file_name_without_ext}/commits.txt"
    # 从 commits.txt 中读取所有 commit hash
    commit_hashes = read_commit_hashes(comha_file_path)

    if commit_hashes:
        # 遍历每个 commit hash 并下载文件
        for commit_hash in commit_hashes:
            # 生成保存路径
            save_dir = os.path.join(repo_name, file_name_without_ext,"downloads")
            download_file_from_commit(repo_owner, repo_name, commit_hash, file_path, save_dir)
    else:
        print("No commits found in commits.txt.")


if __name__ == "__main__":
    main()
