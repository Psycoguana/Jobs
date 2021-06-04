import os
import re
import sys


def main():
    input_data = sys.argv[1]

    if os.path.isfile(input_data):
        replace_file(input_data)
    elif os.path.isdir(input_data):
        replace_in_folder(input_data)


def replace_in_folder(original_folder):
    """ Create a new folder if needed, and replace every file from the old folder. """
    cwd = os.getcwd()
    new_dir_path = os.path.join(cwd, f"{original_folder}_django")
    try:
        os.mkdir(new_dir_path)
    except FileExistsError:
        print("Folder already exists.")

    for file in os.listdir(original_folder):
        replace_file(file, original_path=original_folder, new_path=new_dir_path)


def replace_file(file_name, original_path=os.getcwd(), new_path=os.getcwd()):
    print(f"Replacing {file_name}")
    formatted_file = []

    file_path = os.path.join(original_path, file_name)
    with open(file_path, 'r') as opened_file:
        for line in opened_file:
            if 'url_for' in line:
                if 'src=' in line:
                    line = replace_src(line)
                if 'href=' in line:
                    line = replace_dots(line)
                    line = replace_href(line)

                # Here we can assume src and href tags have already been replaced, so
                # we only need to search something inside {{ here }}, aka variable names.
                if '{{' in line:
                    line = replace_vars(line)

            # Add this new line which may or may not have been converted from jinja2 format into django format
            # into a list that will later be used to write a new file.
            formatted_file.append(line)

    write_new_file(folder_path=new_path, file_name=file_name, file=formatted_file)


def replace_dots(line):
    pattern = r"url_for\('(\w.*)'\)}}"
    match = re.search(pattern, line)
    if match:
        no_dots_name = match.group(1).replace('.', '/')
        line = re.sub(pattern, f"url_for('{no_dots_name}')" + "}}", line)

    return line


def write_new_file(folder_path, file_name, file):
    # If we're only replacing one file, we change the name. If not, no action is needed.
    if folder_path == os.getcwd():
        file_name = f"django{file_name}"

    new_file_path = os.path.join(folder_path, file_name)

    with open(new_file_path, 'w') as new_file:
        for line in file:
            new_file.write(line)


def replace_href(line):
    if "filename" in line:
        pattern = r"href=\"{{ ?url_for\( ?'([A-z].+)', ?filename='([A-z].+)'\) ?}}\""
        matches = re.search(pattern, line)
        src, filename = matches.groups()
        new_line = re.sub(pattern, f'href="/{src}/{filename}"', line)
    else:
        pattern = r"href=\"{{url_for\('([A-z].+?)'\)}}\""
        matches = re.search(pattern, line)
        if matches:
            new_line = re.sub(pattern, f'href="/{matches.group(1)}"', line)
        else:
            new_line = line

    return new_line


def replace_src(line):
    pattern = r"src=\"{{ ?url_for\('([A-z].+)', ?filename='([A-z].+)'\) ?}}\""
    matches = re.search(pattern, line)

    src, filename = matches.groups()

    new_line = re.sub(pattern, f"src=\"{{% {src} '{filename}' %}}\"", line)
    return new_line


def replace_vars(line):
    pattern = r'{{? (\w+)? }}'
    match = re.match(pattern, line)
    if match:
        var_name = match.group(1)
        new_line = re.sub(pattern, f'{{% page_attribute "{var_name}" %}}', line)
        return new_line

    return line


if __name__ == '__main__':
    main()
