import os
import json
import fnmatch

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content.replace('`', '\\`')
    except UnicodeDecodeError:
        return None

def parse_gitignore(gitignore_path):
    ignore_patterns = []
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    except FileNotFoundError:
        pass
    return ignore_patterns

def is_ignored(file_path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def is_in_submodule(file_path, submodule_paths):
    for submodule_path in submodule_paths:
        if file_path.startswith(submodule_path):
            return True
    return False

def dir_to_json(directory, submodules):
    result = {}
    ignore_patterns = ['.git', '.git/*']
    submodule_paths = [os.path.join(directory, submodule['path']) for submodule in submodules]
    
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')

        relative_root = os.path.relpath(root, directory)
        if is_in_submodule(root, submodule_paths) and not any('README' in file for file in files):
            continue

        gitignore_path = os.path.join(root, '.gitignore')
        ignore_patterns.extend(parse_gitignore(gitignore_path))

        relative_path = os.path.relpath(root, directory)
        if relative_path == ".":
            relative_path = ""

        sub_result = result
        if relative_path:
            for part in relative_path.split(os.sep):
                sub_result = sub_result.setdefault(part, {})

        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, directory)

            if is_ignored(relative_file_path, ignore_patterns):
                continue

            if is_in_submodule(file_path, submodule_paths) and 'README' not in file:
                continue

            file_content = read_file(file_path)
            if file_content is not None:
                sub_result[file] = file_content

    return result

def load_submodules(gitmodules_path):
    submodules = []
    try:
        with open(gitmodules_path, 'r', encoding='utf-8') as gitmodules_file:
            current_submodule = None
            for line in gitmodules_file:
                line = line.strip()
                if line.startswith('[submodule'):
                    if current_submodule:
                        submodules.append(current_submodule)
                    current_submodule = {}
                elif line.startswith('path') and current_submodule is not None:
                    _, path = line.split('=', 1)
                    current_submodule['path'] = path.strip()
            if current_submodule:
                submodules.append(current_submodule)
    except FileNotFoundError:
        pass
    return submodules

def main():
    directory = r'.'
    gitmodules_path = os.path.join(directory, '.gitmodules')
    submodules = load_submodules(gitmodules_path)
    
    json_data = dir_to_json(directory, submodules)
    json_output = os.path.join(directory, 'output.json')

    with open(json_output, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    print(f"JSON data has been written to {json_output}")

if __name__ == "__main__":
    main()
