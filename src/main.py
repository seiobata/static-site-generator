import os, shutil


def main():
    print("Deleting public directory...")
    copy_source_to_dest("static", "public")


def copy_source_to_dest(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    paths = os.listdir(source)
    for path in paths:
        source_path = os.path.join(source, path)
        dest_path = os.path.join(dest, path)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copying {source_path} to {dest_path}")
        else:
            copy_source_to_dest(source_path, dest_path)


if __name__ == "__main__":
    main()
