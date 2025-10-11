import re
import os
import shutil
from .parser import markdown_to_html


def copy_to_public(dir, root):
    files = os.listdir(dir)
    public = root + "/public"

    for file in files:
        path = dir + '/' + file
        subdir = dir.replace(root + "/static", "")
        if not os.path.isfile(path):
            copy_to_public(path, root)
        else:
            if not os.path.exists(public + subdir):
                os.mkdir(public + subdir)
            shutil.copy(path, public + subdir + "/" + file)


def extract_title(md):
    m = re.search(r"^# \s*(.+?)$", md, re.MULTILINE)
    if not m:
        raise ValueError("Document is missing a title")
    return m.group(1)


def generate_page(src, template, dest):
    print(f"Generating new page from {src} to {dest}, using {template}")
    with open(src) as fp:
        src_page = fp.read()
    with open(template) as fp:
        template_page = fp.read()

    html = markdown_to_html(src_page)
    title = extract_title(src_page)

    template_page = template_page.replace("{{ Title }}", title)
    template_page = template_page.replace("{{ Content }}", html)

    with open(dest, "x") as fp:
        fp.write(template_page)


def generate_pages(src, template, dest):
    items = os.listdir(src)
    for item in items:
        path = src + "/" + item
        to_path = path.replace("content", "public").replace(".md", ".html")
        if os.path.isdir(path):
            if not os.path.exists(to_path):
                print(f"creating path {to_path}")
                os.mkdir(to_path)
            generate_pages(path, template, dest)
        else:
            generate_page(path, template, to_path)


def main():
    cur_dir = os.getcwd()

    if os.path.exists(cur_dir + '/public'):
        shutil.rmtree(cur_dir + '/public')

    os.mkdir(cur_dir + '/public')
    copy_to_public(cur_dir + '/static', cur_dir)
    generate_pages('./content', './template.html', './public')


if __name__ == "__main__":
    main()
