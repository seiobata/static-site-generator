import os, shutil

from block_markdown import markdown_to_html_node


def main():
    print("Deleting public directory...")
    copy_source_to_dest("static", "public")

    print("Generating pages...")
    generate_pages_recursive("content", "template.html", "public")


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


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("file has no title")


def generate_page(source_path, template_path, dest_path):
    print(f"From {source_path} to {dest_path} using {template_path}")
    md = ""
    template = ""
    with open(source_path) as md_file:
        md = md_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html_file = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_path_directory = os.path.dirname(dest_path)
    if dest_path_directory != "":
        os.makedirs(dest_path_directory, exist_ok=True)
    with open(dest_path, "w") as new_file:
        new_file.write(html_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    paths = os.listdir(dir_path_content)
    for path in paths:
        source_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        if source_path.endswith(".md"):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
        if os.path.isfile(source_path):
            generate_page(source_path, template_path, dest_path)
        else:
            generate_pages_recursive(source_path, template_path, dest_path)


if __name__ == "__main__":
    main()
