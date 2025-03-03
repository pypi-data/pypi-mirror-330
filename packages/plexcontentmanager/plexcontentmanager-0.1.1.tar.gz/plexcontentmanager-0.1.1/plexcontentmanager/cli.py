import click
from colorama import init, Fore, Style
from plexcontentmanager.config import Config
from plexcontentmanager.plex_manager import PlexManager

init()


@click.group()
@click.version_option()
def main():
    pass


@main.command("config")
@click.option("--server", help="Plex server URL (e.g., http://localhost:32400)")
@click.option("--token", help="Plex authentication token")
def configure(server, token):
    config = Config()

    if server:
        config.set_server_url(server)
        click.echo(f"Server URL set to: {server}")

    if token:
        config.set_token(token)
        click.echo(f"Authentication token set")

    if not server and not token:
        server_url = config.get_server_url()
        token_val = config.get_token()

        click.echo(f"Current configuration:")
        click.echo(f"Server URL: {server_url or 'Not set'}")
        click.echo(f"Token: {token_val[:6] + '...' if token_val else 'Not set'}")


@main.command("test-connection")
def test_connection():
    config = Config()
    server_url = config.get_server_url()
    token = config.get_token()

    if not server_url or not token:
        click.echo(Fore.RED + "Error: Server URL or token not configured." + Style.RESET_ALL)
        click.echo("Run 'plexcontent config --server URL --token TOKEN' to configure.")
        return

    plex = PlexManager(server_url, token)
    if plex.connect():
        click.echo(Fore.GREEN + "Connection successful!" + Style.RESET_ALL)
        libraries = plex.get_libraries()
        click.echo(f"Found {len(libraries)} libraries:")
        for library in libraries:
            click.echo(f"  - {library.title} ({library.type})")
    else:
        click.echo(Fore.RED + "Failed to connect to Plex server." + Style.RESET_ALL)


@main.command("list-empty-collections")
def list_empty_collections():
    config = Config()
    server_url = config.get_server_url()
    token = config.get_token()

    if not server_url or not token:
        click.echo(Fore.RED + "Error: Server URL or token not configured." + Style.RESET_ALL)
        click.echo("Run 'plexcontent config --server URL --token TOKEN' to configure.")
        return

    plex = PlexManager(server_url, token)
    if not plex.connect():
        return

    empty_collections = plex.get_empty_collections()
    if not empty_collections:
        click.echo(Fore.GREEN + "No empty collections found." + Style.RESET_ALL)
        return

    total_empty = sum(len(collections) for collections in empty_collections.values())
    click.echo(f"Found {total_empty} empty collections across {len(empty_collections)} libraries:")

    for library, collections in empty_collections.items():
        click.echo(f"\n{Fore.CYAN}{library} ({len(collections)} empty collections):{Style.RESET_ALL}")
        for i, collection in enumerate(collections, 1):
            click.echo(f"  {i}. {collection['title']} (ID: {collection['id']})")


@main.command("delete-empty-collections")
@click.option("--force", is_flag=True, help="Skip confirmation and delete all empty collections")
def delete_empty_collections(force):
    config = Config()
    server_url = config.get_server_url()
    token = config.get_token()

    if not server_url or not token:
        click.echo(Fore.RED + "Error: Server URL or token not configured." + Style.RESET_ALL)
        click.echo("Run 'plexcontent config --server URL --token TOKEN' to configure.")
        return

    plex = PlexManager(server_url, token)
    if not plex.connect():
        return

    empty_collections = plex.get_empty_collections()
    if not empty_collections:
        click.echo(Fore.GREEN + "No empty collections found. Nothing to delete." + Style.RESET_ALL)
        return

    total_empty = sum(len(collections) for collections in empty_collections.values())
    click.echo(f"Found {total_empty} empty collections across {len(empty_collections)} libraries:")

    for library, collections in empty_collections.items():
        click.echo(f"\n{Fore.CYAN}{library} ({len(collections)} empty collections):{Style.RESET_ALL}")
        for i, collection in enumerate(collections, 1):
            click.echo(f"  {i}. {collection['title']} (ID: {collection['id']})")

    if not force:
        confirmation = click.confirm(f"\nAre you sure you want to delete all {total_empty} empty collections?")
        if not confirmation:
            click.echo("Operation cancelled.")
            return

    click.echo("\nDeleting empty collections...")
    deleted_count = 0
    failed_count = 0

    for library, collections in empty_collections.items():
        for collection in collections:
            collection_id = collection['id']
            collection_title = collection['title']

            click.echo(f"Deleting '{collection_title}' from '{library}'... ", nl=False)
            if plex.delete_collection(collection_id):
                click.echo(Fore.GREEN + "Success" + Style.RESET_ALL)
                deleted_count += 1
            else:
                click.echo(Fore.RED + "Failed" + Style.RESET_ALL)
                failed_count += 1

    click.echo(f"\nOperation completed: {deleted_count} collections deleted, {failed_count} failed.")


if __name__ == "__main__":
    main()
