import os
import re


def iter_files(start_dir, file_type: str | None =None):
    for name in os.listdir(start_dir):
        new_path = os.path.join(start_dir, name)
        if os.path.isdir(new_path):
            if name in ('.venv', '.git', '.idea', '.vscode'):
               continue
            yield from iter_files(new_path, file_type)
        elif os.path.isfile(new_path):
            if not file_type or name.endswith(file_type):
                yield new_path

def get_import_stat(file_path):
    p1 = re.compile(r'^\s*import\s+(?P<name>[a-zA-Z0-9_.]+).*$')
    p2 = re.compile(r'\s*from\s+(?P<name>[a-zA-Z0-9_.]+)+\s+import\s+[a-zA-Z0-9_.]+.*$')
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            obj = p1.match(line) or p2.match(line)
            if obj:
                data.append((line, obj.groupdict()))
        return data

def get_current_project_package(start_dir):
    for name in os.listdir(start_dir):
        new_path = os.path.join(start_dir, name)
        if os.path.isdir(new_path):
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                yield name




def get_installer_package():
    import subprocess
    result = subprocess.check_output(['pip', 'list'], text=True)
    data = result.splitlines()[2:]
    return dict(row.split() for row in data)

def create_installer_package_func():
    installer_package = get_installer_package()
    def find(name):
        for pn, pv in installer_package.items():
            if compare_name(pn, name):
                return f'{pn}=={pv}'
        return ""

    return find


get_pk = create_installer_package_func()
def find_package_name_mapper():
    import sys
    from pathlib import Path
    path = Path(sys.executable).parent.parent / 'lib' / 'site-packages'
    if not path.exists():
        raise ValueError('无法识别到解释器路径！')
    mapper = {}
    for name in os.listdir(path):
        file_path = os.path.join(path, name, 'top_level.txt')
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            continue
        name = name.split('-')[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    continue
                pk = get_pk(name)
                if not pk:
                    raise ValueError(f'not found package: {name}')
                mapper[line] = pk
    return mapper

def compare_name(name1: str, name2: str):
    name1 = name1.replace('-', '_').lower()
    name2 = name2.replace('-', '_').lower()
    return name1 == name2



def main():
    all_names = set()
    current_names = set(get_current_project_package('.'))
    for file in iter_files(os.path.abspath('.'), file_type='.py'):
        for stat, name_dict in get_import_stat(file):
            all_names.add(name_dict['name'])
    third_package_names = set()
    for name in all_names:
        if name.startswith('.'):
            continue
        name = name.split('.')[0]
        if name in current_names:
            continue
        third_package_names.add(name)
    package_name_mapper = find_package_name_mapper()
    result = []
    for third_package_name in third_package_names:
        pk = get_pk(third_package_name) or package_name_mapper.get(third_package_name)
        if not pk:
            continue
        # print(third_package_name, pk)
        result.append(pk)
    print('识别到依赖包\n', '\n'.join(result), sep='')
    return result


if __name__ == '__main__':
    main()
