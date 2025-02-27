import typer
from xlsxparse_joeypas.parse import parse_all_sheets, parse_single_sheet
from typing_extensions import Annotated

def entry(
    file: Annotated[str, typer.Argument(help="Path to the .xlsx WorkBook")],
    sheet_name: Annotated[str, typer.Argument(help="Name of the sheet to parse (if none provided, parse all sheets)")] = ""
):
    if sheet_name:
        refs = parse_single_sheet(file, sheet_name)
        for cell, data in refs.items():
            print(f"Cell: {cell}, Formula: {data['formula']}, Refrences: {data['references']}")
    else:
        refs = parse_all_sheets(file)
        for sheet, item in refs.items():
            for cell, data in item['items'].items():
                print(f"Sheet: {sheet}, Metrics: {data['names']}, Cell: {cell}, Formula: {data['formula']}, References: {data['references']}")


app = typer.Typer()
app.command()(entry)

if __name__ == "__main__":
    app()
