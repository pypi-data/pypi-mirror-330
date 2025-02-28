def get_content_of_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"Cannot decode content of {path}"

def get_list_of_content_files(directory_dict: dict):

    paths = []
    contents = []
    stack = [directory_dict]

    while stack:
        current = stack.pop()

        if isinstance(current, dict) and "path" in current and "type" in current:
            paths.append(current["path"])
            if current["type"] == "file":
                contents.append(current)
            if "contents" in current and isinstance(current["contents"], list):
                for item in current["contents"]:
                    stack.append(item)

        elif isinstance(current, list):
            for item in current:
                stack.append(item)

    return paths, contents

if __name__ == "__main__":
    paths, contents = get_list_of_content_files({'type': 'directory', 'name': 'test_repo', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo', 'contents': [{'type': 'directory', 'name': 'database', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/database', 'contents': [{'type': 'file', 'name': 'ignore', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/database/ignore'}, {'type': 'directory', 'name': '__pycache__', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/database/__pycache__', 'contents': []}]}, {'type': 'directory', 'name': '.pytest_cache', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/.pytest_cache', 'contents': []}, {'type': 'file', 'name': '.gitignore', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/.gitignore'}, {'type': 'directory', 'name': '.venv', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/.venv', 'contents': [{'type': 'file', 'name': 'ignore', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/.venv/ignore'}]}, {'type': 'file', 'name': 'main', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/main'}, {'type': 'directory', 'name': 'coverage', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/coverage', 'contents': [{'type': 'file', 'name': 'ignore', 'path': '/Users/anjie.wav/llmrepo/tests/test_repo/coverage/ignore'}]}]})
    content = get_content_of_file('/llmrepo/tests/test_repo/coverage/ignore')