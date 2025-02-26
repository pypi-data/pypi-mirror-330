import datetime
import json
import typer
from documentcloud import DocumentCloud
from documentcloud.exceptions import (
    APIError,
    DuplicateObjectError,
    CredentialsFailedError,
    DoesNotExistError,
    MultipleObjectsReturnedError
)
from pathlib import Path
from rich import print
from rich.table import Table
from typing import Annotated


app = typer.Typer()

@app.command()
# Doesn't show 'INTEGER' in help instead shows '[RESULT_COUNT]' as type instead :/
def search(query: str, result_count: Annotated[int, typer.Argument(min=1, max=25)]=10):
    """
    Search DocumentCloud for a query. Optionally specify the number of results shown.
    """
    client = DocumentCloud()
    doc_list = client.documents.search(query).results[:result_count]
    if not doc_list:  # List is empty (no results for query)
        print("[bold red]Your query returned no results!")
    else:
        table = Table(title="[red]Search Results")
        table.add_column("Contributor", justify="center", style="cyan")
        table.add_column("Title", justify="center", style="magenta")
        table.add_column("Creation Date", justify="center", style="green")
        table.add_column("ID", justify="center", style="green")
        for doc in doc_list:
            table.add_row(f"{doc.contributor}",
                          f"[link={doc.canonical_url}]{doc.title}[/link]",
                          f"{doc.created_at.strftime('%b %d %Y')}",
                          f"{doc.id}")
        print(table)

@app.command()
def upload(
        file_path: Annotated[Path, typer.Argument(help="The path of the file to be uploaded.",
                                                  exists=True, file_okay=True, readable=True, resolve_path=True)],
        username: Annotated[str, typer.Option(help="Your username.", prompt=True)],
        password: Annotated[str, typer.Option(help="Your password.", prompt=True, hide_input=True)]
):
    """
    Upload a document from your machine to DocumentCloud.
    Will prompt for username and password if not entered initially.
    """
    try:
        client = DocumentCloud(username, password)
        client.documents.upload(file_path)
        print(f"Uploaded {file_path} to your DocumentCloud account.")
    except CredentialsFailedError:
        # Message from API implies both username *and* password are incorrect, even when not the case.
        print(f"\n[bold red]CredentialsFailedError: Invalid username and/or password!")
    except APIError as e:
        # Display specific APIError. Usually to do with the user lacking permissions (unverified account).
        print(f"\n[bold red]APIError: {json.loads(e.error)['detail']}")

@app.command()
# Doesn't show 'TEXT' in help instead shows '[PROJ_NAME]' as type instead :/
def upload_dir(
        dir_path: Annotated[Path, typer.Argument(help="The path of the directory to be uploaded.",
                                                 exists=True, dir_okay=True, readable=True, resolve_path=True)],
        username: Annotated[str, typer.Option(help="Your username.", prompt=True)],
        password: Annotated[str, typer.Option(help="Your password.", prompt=True, hide_input=True)],
        proj_name: Annotated[str, typer.Argument(
            help="The name of the new Project for the documents.")]=f"New Project {datetime.datetime.now()}"
):
    """
    Upload a directory of documents on your machine to DocumentCloud as a Project.
    Will prompt for project name, username, and password if not entered initially.
    """
    try:
        client = DocumentCloud(username, password)
        project = client.projects.get_or_create_by_title(proj_name)[0]
        doc_list = client.documents.upload_directory(dir_path)
        project.document_list = doc_list
        project.put()
        print(f"Uploaded {dir_path} contents to your DocumentCloud account, Project name: {proj_name}")
    except CredentialsFailedError:
        # Message from API implies both username *and* password are incorrect, even when not the case.
        print(f"\n[bold red]CredentialsFailedError: Invalid username and/or password!")
    except APIError as e:
        # Display the specific APIError. Usually to do with the user lacking permissions (unverified account).
        print(f"\n[bold red]APIError: {json.loads(e.error)['detail']}")

@app.command()
def get_document(doc_id: Annotated[int, typer.Argument(help="The numeric ID of the document to be fetched.")]):
    """
    Fetches a document from the numeric ID and displays its metadata.
    """
    doc = fetch_document(doc_id)

    table = Table(title="[red]Document Information")
    table.add_column("Contributor", justify="center", style="cyan")
    table.add_column("Title", justify="center", style="magenta")
    table.add_column("Creation Date", justify="center", style="green")
    table.add_column("Page Count", justify="center", style="green")
    table.add_column("URL", justify="center", style="green")
    table.add_row(f"{doc.contributor}",
                  f"{doc.title}",
                  f"{doc.created_at.strftime('%b %d %Y')}",
                  f"{doc.pages}",
                  f"{doc.canonical_url}")
    print(table)

@app.command()
def view_text(doc_id: Annotated[int, typer.Argument(help="The numeric ID of the document to be fetched.")]):
    """
    View the text of a document as parsed by DocumentCloud. Your mileage may vary.
    """
    doc = fetch_document(doc_id)
    print(f"[red] {'Document Text':^100}")
    print(f"[white] Document Text URL: {doc.full_text_url}")
    print(doc.full_text)

@app.command()
def save_text(doc_id: Annotated[int, typer.Argument(help="The numeric ID of the document.")],
              file_name: Annotated[str, typer.Argument(help="The name of the text file.")]
              =f"DocCloudTool {datetime.datetime.now().strftime('%b-%d-%Y-%H-%M-%S')}.txt"
              ):
    """
    Saves the text of a document to a .txt file.
    """
    doc = fetch_document(doc_id)
    try:
        with open(file_name, 'x') as f:
            try:
                f.write(doc.full_text)
            except (IOError, OSError):
                print(f"\n[bold red]Error writing to file!")
    except (FileNotFoundError, PermissionError, OSError):
        print(f"\n[bold red]Error opening file!")

def fetch_document(doc_id):
    """
    Helper method that fetches a document by ID and returns it.
    :param doc_id: The ID of a document to be fetched.
    :return: The Document object.
    """
    try:
        client = DocumentCloud()
        doc = client.documents.get(doc_id)
    except DoesNotExistError as e:
        print(f"\n[bold red]DoesNotExistError: {json.loads(e.error)['detail']}")
        raise typer.Exit()
    return doc

app()