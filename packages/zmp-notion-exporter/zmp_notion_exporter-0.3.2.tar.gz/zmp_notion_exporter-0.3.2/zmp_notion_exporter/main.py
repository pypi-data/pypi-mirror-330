import os
import argparse
from dotenv import load_dotenv
import time
from zmp_notion_exporter import NotionPageExporter, extract_notion_page_id
import threading
import sys

load_dotenv()


class ProgressIndicator:
    def __init__(self, exporter: NotionPageExporter):
        self.exporter = exporter
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\n")
        sys.stdout.flush()

    def _animate(self):
        while self.running:
            try:
                total, exported = self.exporter.total_and_exported_pages
                progress = self.exporter.progress

                # 프로그레스 바 생성 (50칸 기준)
                bar_width = 50
                filled = int(bar_width * progress / 100)
                bar = "=" * filled + "-" * (bar_width - filled)

                # 프로그레스 정보 출력
                info = f"\rProgress: [{bar}] {progress}% ({exported}/{total})"
                sys.stdout.write(info)
                sys.stdout.flush()

            except ValueError:
                animation_chars = ["-", "\\", "|", "/"]
                animation_idx = getattr(self, "_animation_idx", 0)
                sys.stdout.write(
                    f"\rInitializing node tree... {animation_chars[animation_idx]}"
                )
                sys.stdout.flush()
                animation_idx = (animation_idx + 1) % len(animation_chars)
                setattr(self, "_animation_idx", animation_idx)

            time.sleep(0.5)
            # 마지막 라인 지우기
            sys.stdout.write("\033[K")


def parse_args():
    parser = argparse.ArgumentParser(description="Notion Page Export Tool")

    parser.add_argument(
        "-t",
        "--notion-token",
        help="Notion API Token. You can set it by NOTION_TOKEN environment variable.",
        default=os.environ.get("NOTION_TOKEN", ""),
        metavar="",
    )
    parser.add_argument(
        "-r",
        "--root-page-id",
        help="Root page ID to start export. You can set it by ROOT_PAGE_ID environment variable.",
        default=os.environ.get("ROOT_PAGE_ID", ""),
        required=True,
        metavar="",
    )
    parser.add_argument(
        "-c",
        "--child-page-id",
        help="Child page ID to start export. You can set it by CHILD_PAGE_ID environment variable.",
        default=os.environ.get("CHILD_PAGE_ID", ""),
        required=False,
        metavar="",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Directory path for export results. You can set it by OUTPUT_DIR environment variable.",
        default=os.environ.get("OUTPUT_DIR", ""),
        required=True,
        metavar="",
    )
    parser.add_argument(
        "-i",
        "--include-subpages",
        help="Include subpages in the export(default: True)",
        default=True,
        metavar="",
    )
    parser.add_argument(
        "-f",
        "--file-type",
        help="File type for export(default: mdx). support: md, mdx, html",
        default="mdx",
        metavar="",
        choices=["md", "mdx", "html"],
    )

    return parser.parse_args()


def run():
    args = parse_args()

    notion_token = args.notion_token
    if not notion_token:
        print("NOTION_TOKEN is not set.")
        return

    root_page_id = args.root_page_id
    if not root_page_id:
        print("ROOT_PAGE_ID is not set.")
        return

    output_dir = args.output_dir
    if not output_dir:
        print("OUTPUT_DIR is not set.")
        return

    child_page_id = args.child_page_id
    include_subpages = args.include_subpages
    file_type = args.file_type

    print(">>> Starting Notion export with following parameters")
    print("--------------------------------------------------------")
    print(f"@ --notion-token: {notion_token[:5]}...{notion_token[-5:]}")
    print(f"@ --root-page-id: {root_page_id}")
    print(f"@ --child-page-id: {child_page_id}")
    print(f"@ --output-dir: {output_dir}")
    print(f"@ --include-subpages: {include_subpages}")
    print(f"@ --file-type: {file_type}")
    print("--------------------------------------------------------")

    target_page_id = child_page_id if child_page_id != "" else root_page_id
    if target_page_id == root_page_id:
        print(f">>> Exporting root page: {root_page_id}")
    else:
        print(f">>> Exporting child page: {child_page_id}")

    exporter = NotionPageExporter(
        notion_token=notion_token,
        root_page_id=extract_notion_page_id(root_page_id),
        root_output_dir=output_dir,
    )

    start_time = time.time()
    progress = ProgressIndicator(exporter)
    progress.start()

    try:
        if file_type == "md":
            exporter.markdown(
                page_id=extract_notion_page_id(target_page_id),
                include_subpages=include_subpages,
            )
        elif file_type == "mdx":
            exporter.markdownx(
                page_id=extract_notion_page_id(target_page_id),
                include_subpages=include_subpages,
            )
        elif file_type == "html":
            exporter.html(
                page_id=extract_notion_page_id(target_page_id),
                include_subpages=include_subpages,
            )
        time.sleep(1)
    finally:
        progress.stop()

    docs_node, static_image_node = exporter.get_output_nodes()

    print(
        f"- Result (Total pages / Exported pages): {exporter.total_and_exported_pages}"
    )
    print(f"- Progress: {exporter.progress}%")

    docs_node.print_pretty(include_leaf_node=True)
    static_image_node.print_pretty(include_leaf_node=False)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f">>> Export completed successfully in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    run()
