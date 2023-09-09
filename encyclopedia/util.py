import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def markdown_to_html(title):
    # Read Markdown content from a file or a database field
    markdown_content = get_entry(title)

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)
    return html_content


def separate_markdown_content(html_content):
    pattern = r'<h1>(.*?)<\/h1>'
    for line in html_content.splitlines():
        match = re.search(pattern, line)
        if match:
            header = match.group(1)
            return header
    