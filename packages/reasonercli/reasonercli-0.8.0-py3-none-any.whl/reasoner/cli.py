import json
import os
from pathlib import Path
from datetime import datetime
import pathlib

import httpx
import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from reasoner import Reasoner

from .config import (
    clear_config_file,
    config_file_path,
    read_config_file,
    write_config_file,
    get_env
)


env_settings = get_env()
app = typer.Typer(no_args_is_help=True)
console = Console()


def save_api_key(key):
    config_data = read_config_file()
    config_data["API_KEY"] = key
    write_config_file(config_data)

    typer.echo(f"API key saved to {config_file_path()}")


def get_api_key():
    """
    Get API key from ~/.reasoner/config file.
    Returns None if file doesn't exist or API_KEY not found.
    """
    config_data = read_config_file()

    if config_data and config_data.get("API_KEY"):
        return config_data["API_KEY"]

    typer.echo("Please run 'reasonercli auth' first to set up auth config")
    return None


def write_batch_info(batch_uid, batch_status):
    config_data = read_config_file()
    config_data["BATCH_UID"] = batch_uid
    config_data["BATCH_STATUS"] = batch_status
    write_config_file(config_data)


def get_batch_info():
    """
    Get batch UID and status from ~/.reasoner/config file.
    Returns tuple of (None, None) if file doesn't exist or values not found.
    """
    config_data = read_config_file()

    if config_data and config_data.get("BATCH_UID") and config_data.get("BATCH_STATUS"):
        return config_data["BATCH_UID"], config_data["BATCH_STATUS"]

    return None, None


@app.command()
def auth():
    import http.server
    import socketserver
    import webbrowser
    from urllib.parse import parse_qs, urlencode, urlparse

    LOCAL_WEBSOCKET_PORT = 5174
    CLIENT_ID = env_settings["CLIENT_ID"]
    AUTHORIZATION_URL = env_settings["AUTHORIZATION_URL"]
    REASONER_UI_BASE_URL = env_settings["REASONER_UI_BASE_URL"]
    REASONER_API_BASE_URL = env_settings["REASONER_API_BASE_URL"]
    REDIRECT_URI = env_settings["REDIRECT_URI"]

    # Open up web browser to WorkOS SSO authentication page
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "provider": "authkit",
    }
    authorization_url = f"{AUTHORIZATION_URL}?{urlencode(params)}"

    # Note: python < 3.12 doesn't have `name`
    if not hasattr(webbrowser.get(), "name") or not webbrowser.get().name == "null":
        webbrowser.open(authorization_url)
    else:
        typer.echo("Could not open a web browser automatically.")
        typer.echo(
            "Please use Reasoner Console and use `reasonercli verify-auth` to set your API key"
        )

    class OAuthHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def do_GET(self):
            parsed_url = urlparse(self.path)
            if parsed_url.path == "/callback":
                query_components = parse_qs(parsed_url.query)
                if "code" in query_components:
                    auth_code = query_components["code"][0]
                    self.server.auth_code = auth_code

                    # Redirect to reasoner console UI
                    # TODO: create a console success page
                    self.send_response(301)
                    self.send_header(
                        "Location", f"{REASONER_UI_BASE_URL}/console-success"
                    )
                    self.end_headers()

                    self.server.should_stop = True

    # Start the local server and handle the authorization code
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(
            ("localhost", LOCAL_WEBSOCKET_PORT), OAuthHandler
        ) as httpd:
            client = httpx.Client()

            httpd.handle_request()
            auth_code = httpd.auth_code

            # Close the server
            httpd.server_close()

            response = client.get(
                f"{REASONER_API_BASE_URL}/public/v1/auth/onboard?code={auth_code}",
                timeout=30.0,
            )
            api_key = (response.json() or {}).get("api_key")
            if not api_key:
                console.print("\n[red]Unable to find API key.[/red]")
                return

            # Make sure that the API key is valid and also hit it for the first time to "use it"
            # to advance onboarding flow.
            r = Reasoner(api_key=api_key)
            is_valid_key = r.auth.verify_auth()
            if not is_valid_key:
                console.print("\n[red]API key is invalid.[/red]")
                return

            # If the API key has changed, we should clear the rest of the keys (especially BATCH_UID and BATCH_STATUS)
            # because they might be pointing at another project.
            existing_api_key = get_api_key()
            if existing_api_key != api_key:
                clear_config_file()

            save_api_key(api_key)

            console.print("\n[green]🔐 Successfully authenticated! 🎉[/green]")

            console.print("\n[bold]Available commands:[/bold]")
            console.print(
                "\n[cyan]📚 Upload your PDF documents to start asking questions[/cyan]"
                "\n[yellow]reasonercli upload --path /path/to/docs/folder[/yellow]"
            )
            console.print(
                "\n[cyan]❓Trace your sources[/cyan]"
                '\n[yellow]reasonercli trace "Who was the king of England when Isaac Newton first published his Principia?"[/yellow]\n'
            )

    except OSError as err:
        if err.errno == 48:
            console.print(
                f"\n[red]Port {LOCAL_WEBSOCKET_PORT} is already open. Please close it and try again.[/red]"
            )
            return
        else:
            raise err
    except httpx.HTTPStatusError as err:
        if err.response.status_code == 403:
            console.print(
                "\n[red]Authentication failed. Please check your credentials and try again.[/red]"
            )
            return
        else:
            raise err


@app.command()
def verify_auth(key: str = typer.Option(..., help="API key for authentication")):
    """
    Verify authentication using the provided key.
    """
    typer.echo("Verifying authentication...")
    r = Reasoner(api_key=key)
    is_valid = r.auth.verify_auth()
    if is_valid:
        console.print("\n[green]🔐 API key is valid! 🎉[/green]")
        save_api_key(key)


@app.command()
def upload(
    path: str = typer.Option(..., help="Path to folder containing PDF documents"),
):
    try:
        # Get all PDF files in the folder
        folder = Path(path)
        if not folder.exists():
            console.print(f"\n[red]Error: Path {path} does not exist[/red]")
            return

        pdf_paths = list(folder.glob("*.pdf"))
        if not pdf_paths:
            console.print(f"\n[red]Error: No PDF files found in {path}[/red]")
            return

        files = []

        for path in pdf_paths:
            # files.append(open(path, "rb"))
            files.append(pathlib.Path(path))

        typer.echo(f"\nFound {len(pdf_paths)} PDF files in {path}:")
        for path in pdf_paths:
            typer.echo(f"  • {path.name}")
        typer.echo("")

        key = get_api_key()
        r = Reasoner(api_key=key)

        # Verify auth with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            auth_task = progress.add_task("Verifying authentication...", total=None)
            auth_result = r.auth.verify_auth()
            if not auth_result:
                raise Exception("Authentication failed")
            progress.update(auth_task, description="Authentication verified ✓")

        # Upload files with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            upload_task = progress.add_task("Uploading documents...", total=100)
            
            index = r.indexes.create(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            index_uid = index["uid"]

            r.indexes.add_documents(files=files, index_uid=index_uid)

            r.indexes.build(index_uid=index_uid, wait=False)

            progress.update(
                upload_task, completed=100, description="Documents uploaded ✓"
            )

        # Save environment info
        write_batch_info(index_uid, "processing")

        console.print(
            "\n[green]🚀 Reasoner Environment setup initiated! Run `reasonercli trace <question>` to check index status and query.[/green]"
        )

    except httpx.HTTPStatusError as err:
        if err.response.status_code == 401:
            console.print(
                "\n[red]Authentication failed. You might need to run `reasonercli auth`[/red]"
            )
            return
        else:
            raise err
    except Exception as exc:
        console.print(f"\n[red]Error: {exc}[/red]")
        raise


@app.command()
def trace(
    query: str = typer.Argument(None, help="Question to ask"),
    input_file: str = typer.Option(
        None, "--in", "-i", help="Input file containing the question"
    )
):
    """
    Query reasoner with a specific question.
    """
    try:
        if not query and not input_file:
            raise typer.BadParameter("Must provide either --query or --in parameter")

        if input_file:
            try:
                with open(input_file, "r") as f:
                    query = f.read().strip()
            except Exception as e:
                raise typer.BadParameter(f"Failed to read input file: {e}")

        if not query:
            raise typer.BadParameter("Query cannot be empty")

        batch_uid, batch_status = get_batch_info()

        # Either batch or example docs are required
        if (not batch_uid or not batch_status):
            raise Exception(
                "Reasoner Environment not set up. To get started, run `reasonercli auth`. "  
                "Then upload documents with `reasonercli upload --path /path/to/docs`."
            )

        key = get_api_key()
        r = Reasoner(api_key=key)

        # If batch is specified, make sure that it's ready to be queried.

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
        ) as progress:
            process_task = progress.add_task(
                "Checking environment status...", total=None
            )

            updated_batch = r.indexes.get_status(batch_uid)
            batch_status = updated_batch["status"]

            write_batch_info(batch_uid, batch_status)

            if batch_status == "failed":
                raise Exception("Document processing failed")
            elif batch_status != "success":
                console.print(
                    "\n[yellow]Reasoner Environment still processing. Try again later.[/yellow]"
                )
                return

            progress.update(process_task, description="Environment ready ✓")

        console.print("[green]🚀 Reasoner Environment is ready![/green]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
        ) as progress:
            query_task = progress.add_task("Executing query...", total=None)

            response = r.trace( query=query, index_uid=batch_uid, wait=True)

            progress.update(query_task, description="Query completed ✓\n")

        console.print(f"\nQuestion: {query}")

        console.print("\n[bold]JSON Response:[/bold]")
        console.print(json.dumps(response, indent=2))

        answer_json = response.get("response", {})
        
        if not answer_json:
            raise ValueError("Unable to parse the answer response")
        
        if response.get("progress") and response["progress"] < 0:
            raise ValueError("Query trace failed") 

        concise_answer = answer_json.get("concise") + "\n"
        long_answer = answer_json.get("detailed")

        console.print(f"\n[bold]Concise Response:[/bold] {concise_answer}\n")
        console.print(f"{long_answer}\n")

    except httpx.HTTPStatusError as err:
        if err.response.status_code == 401:
            console.print(
                "\n[red]Authentication failed. You might need to run `reasonercli auth`[/red]"
            )
            return
        elif err.response.status_code == 403:
            console.print(
                "\n[red]Your API key does not have access to this set of documents.[/red]"
            )
            return
        else:
            raise err
    except Exception as exc:
        console.print(f"\n[red]Error: {exc}[/red]")


if __name__ == "__main__":
    app()
