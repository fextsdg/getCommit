import requests
import os


def get_project_id(project_url):
    gitlab_api_url = "https://gitlab.com/api/v4/projects/"
    project_url_encoded = project_url.replace("/", "%2F")

    response = requests.get(gitlab_api_url + project_url_encoded)
    if response.status_code == 200:
        project_info = response.json()
        return project_info['id']
    else:
        print(f"Failed to fetch project info: {response.status_code}")
        print(f"Error Details: {response.text}")
        return None


def fetch_commits_after_since_commit(project_id, since_commit, file_path, output_file):
    # URL 编码路径
    file_path_encoded = file_path.replace("/", "%2F")

    # 每页返回的提交数
    per_page = 100
    page = 1
    found_since_commit = False

    with open(output_file, "w") as file:
        while True:
            # 构建查询提交记录的 API URL
            commits_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits?path={file_path_encoded}&page={page}&per_page={per_page}"
            response = requests.get(commits_url)

            if response.status_code == 200:
                commits = response.json()

                if not commits:
                    print("No more commits found.")
                    break

                for commit in commits:
                    commit_id = commit['id']
                    message = commit['message']
                    created_at = commit['created_at']

                    # 如果还没有找到 since_commit，就继续遍历
                    if not found_since_commit:
                        if commit_id == since_commit:
                            # 找到目标 commit 后，开始保存后续提交
                            found_since_commit = True
                            file.write(f"{commit_id}\n")
                            print(f"Found since_commit: {commit_id}, now saving subsequent commits.")
                        continue

                    # 如果已经找到了目标 commit，就保存后续的所有提交
                    print(f"Commit ID: {commit_id}")
                    print(f"Message: {message}")
                    print(f"Time: {created_at}")
                    print("-" * 80)
                    file.write(f"{commit_id}\n")

                page += 1
            else:
                print(f"Failed to fetch commits: {response.status_code}")
                print(f"Error Details: {response.text}")
                break

    print(f"Commit records have been saved to '{output_file}'.")


def main():
    repo_owner = "libtiff"
    repo_name = "libtiff"
    project_url = f"{repo_owner}/{repo_name}"  # 项目名称
    since_commit = "802d3cbf3043be5dce5317e140ccb1c17a6a2d39"  # 设置目标 commit
    file_path = "libtiff/tif_dirwrite.c"  # 设置文件路径

    # 动态生成输出文件名称
    file_path_parts = file_path.split('/')
    output_file = f"./{repo_name}/{file_path_parts[-1].split('.')[0]}/commits.txt"

    # 确保文件夹存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    project_id = get_project_id(project_url)
    if project_id:
        fetch_commits_after_since_commit(project_id, since_commit, file_path, output_file)


if __name__ == "__main__":
    main()
