"""Console script for minhtml."""

import logging
import pathlib

import minify_html
import typer
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="[*] %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)


app = typer.Typer()
console = Console()


@app.command()
def main(input_dir: str = typer.Argument(None, "--input_dir", help="待处理html文件目录")):
    console.print("See Typer documentation at https://typer.tiangolo.com/")

    input_dirpath = pathlib.Path(input_dir) if input_dir is not None else pathlib.Path.cwd()

    if not input_dirpath.exists():
        logging.error(f"[red bold]待处理html文件目录[/]路径无效, 退出: {input_dirpath}")
        raise typer.Exit(code=2)

    output_dirpath = input_dirpath / "output"
    output_dirpath.mkdir(parents=True, exist_ok=True)
    extensions = [".html", ".mhtml"]
    files = list(f for f in input_dirpath.glob("*") if f.suffix.lower() in extensions)
    if not len(files):
        logging.error(f"当前路径下未找到后缀为{extensions}的文件, 退出")
        raise typer.Exit(code=2)

    for file in files:
        try:
            with open(file) as f:
                content = f.readlines()
        except OSError as e:
            logging.error(f"读取文件[red bold]{file}[/]失败: [red bold]{e}")
            return

        minified = minify_html.minify(content, minify_js=True, remove_processing_instructions=True)
        target_filepath = output_dirpath / file.name

        try:
            with open(target_filepath, "w") as f:
                f.writelines(minified)
        except OSError as e:
            logging.error(f"写入文件[red bold]{target_filepath}[/]失败: [red bold]{e}")
            return
        else:
            logging.error(f"写入内容到文件[red bold]{target_filepath}")


if __name__ == "__main__":
    app()
