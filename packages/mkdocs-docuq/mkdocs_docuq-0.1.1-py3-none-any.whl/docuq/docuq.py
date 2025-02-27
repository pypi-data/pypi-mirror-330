import os

import markdown
from bs4 import BeautifulSoup
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin


class DocuQPlugin(BasePlugin):

    config_scheme = (("docuqURL", config_options.Type(str, required=True)),)

    def __init__(self):
        self.api_key = None
        self.client = None

        self.docs_content = {}
        self.docs_mapping = {}

    def on_config(self, config):
        self.docs_dir = config["docs_dir"]
        self.site_url = config.get("site_url", "")

    def on_pre_build(self, config):
        self.scan_and_read_docs(config)

    def scan_and_read_docs(self, config):
        self.docs_content = {}
        self.docs_mapping = {}
        for root, dirs, files in os.walk(self.docs_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        html_content = markdown.markdown(content)
                        soup = BeautifulSoup(html_content, "html.parser")
                        text_content = soup.get_text()
                        rel_path = os.path.relpath(file_path, self.docs_dir)
                        url = os.path.join(
                            self.site_url, rel_path.replace(os.sep, "/")
                        ).replace(".md", "/")
                        self.docs_content[file_path] = text_content
                        self.docs_mapping[file_path] = url

        self.add_nav_to_mapping(config["nav"])

    def add_nav_to_mapping(self, nav):
        for item in nav:
            if isinstance(item, dict):
                for title, path in item.items():
                    if isinstance(path, list):
                        self.add_nav_to_mapping(path)
                    else:
                        file_path = os.path.join(self.docs_dir, path)
                        url = os.path.join(
                            self.site_url, path.replace(os.sep, "/")
                        ).replace(".md", "/")
                        if file_path in self.docs_content:
                            self.docs_mapping[file_path] = url

    def on_post_build(self, config):

        for root, _, files in os.walk(config["site_dir"]):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    script_tag = """<script src="https://cdn.jsdelivr.net/npm/@smartandpoint/docuq@0.3.3/dist/docuq.js"></script>"""

                    with open(file_path, "r+", encoding="utf-8") as f:
                        content = f.read()
                        if "</body>" in content:
                            content = content.replace("</body>", f"{script_tag}</body>")
                            f.seek(0)
                            f.write(content)
                            f.truncate()

        return config


def get_plugin() -> DocuQPlugin:
    return DocuQPlugin()
