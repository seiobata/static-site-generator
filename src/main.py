import os, shutil

from block_markdown import markdown_to_html_node


def main():
    print("Deleting public directory...")
    copy_source_to_dest("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    template = ""
    with open(from_path) as md_file:
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


if __name__ == "__main__":
    main()
