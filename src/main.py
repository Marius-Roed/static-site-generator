import os
import shutil


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


def main():
    cur_dir = os.getcwd()
    if os.path.exists(cur_dir + '/public'):
        shutil.rmtree(cur_dir + '/public')

    os.mkdir(cur_dir + '/public')
    copy_to_public(cur_dir + '/static', cur_dir)


if __name__ == "__main__":
    main()
