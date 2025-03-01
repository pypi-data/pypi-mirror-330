import typer
import rich
from typing import Optional
from pody.eng.user import UserDatabase
import docker
from ..eng.utils import parse_storage_size
from ..eng.docker import ContainerAction, DockerController

app = typer.Typer(
    help = "Manage users in the system",
    no_args_is_help=True
    )

@app.command()
def add(
    username: str,
    password: str,
    admin: bool = False,
    ):
    db = UserDatabase()
    db.add_user(username, password, admin)

@app.command()
def update(
    username: str, 
    password: Optional[str] = None,
    admin: Optional[bool] = None,
    ):
    db = UserDatabase()
    db.update_user(username, password=password, is_admin=admin)

@app.command(help="List users, optionally filter by username")
def list(usernames: Optional[list[str]] = typer.Argument(None)):
    console = rich.console.Console()
    db = UserDatabase()
    users = db.list_users(usernames)
    for idx, user in enumerate(users):
        console.print(f"{idx+1}. {user} {db.check_user_quota(user.name)}")

@app.command()
def update_quota(
    username: str, 
    max_pods: Optional[int] = None,
    gpu_count: Optional[int] = None,
    memory_limit: Optional[str] = None, 
    storage_limit: Optional[str] = None
    ):
    db = UserDatabase()
    db.update_user_quota(
        username, max_pods=max_pods, gpu_count=gpu_count, 
        memory_limit=parse_storage_size(memory_limit) if not memory_limit is None else None, 
        storage_limit=parse_storage_size(storage_limit) if not storage_limit is None else None
        )

@app.command(help="Delete user")
def delete(username: str):
    db = UserDatabase()
    db.delete_user(username)

@app.command(help="Delete user and all related containers")
def purge(
    username: str, 
    yes: bool= typer.Option(False, "--yes", "-y", help="Skip confirmation")
    ):
    if not yes:
        typer.confirm(f"Are you sure to purge user {username}?", abort=True)
    c = DockerController()
    db = UserDatabase()
    db.delete_user(username)
    containers = c.list_docker_containers(filter_name=username + "-")
    for container in containers:
        c.container_action(container, ContainerAction.DELETE)
        print(f"Container [{container}] removed")