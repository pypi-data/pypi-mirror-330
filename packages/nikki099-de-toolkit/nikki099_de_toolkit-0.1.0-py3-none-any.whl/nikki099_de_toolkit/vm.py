import click
import subprocess

@click.command()
def start():
    """Start your vm"""
    # your code here
    try:
        vm_zone = "europe-west1-d"
        vm_name = "lewagon-data-eng-vm-nikki099"
        subprocess.run(["gcloud", "compute", "instances", "start",
                        -f"--zone={vm_zone}", vm_name],
                       check=True
                       )
        click.echo("VM started successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error starting VM: {e}")

@click.command()
def stop():
    """Stop your vm"""
    # your code here
    try:
        vm_zone = "europe-west1-d"
        vm_name = "lewagon-data-eng-vm-nikki099"
        subprocess.run(["gcloud", "compute", "instances", "stop",
                        f"--zone={vm_zone}", vm_name],
                       check=True
                       )
        click.echo("VM stopped successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error stopping VM: {e}")


@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/nikki099/folder """
    # your code here
    try:
        username = "nxie" #nikkilw2025
        vm_ip = "34.38.162.9"
        vm_path = "/home/<username>/code/nikki099/nikki099-de-toolkit"
        subprocess.run(
            [
                "code",
                "--folder-uri",
                f"vscode-remote://ssh-remote+{username}@{vm_ip}{vm_path}"
            ],
            check=True
        )
        click.echo("Connected to VM in VSCode!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error connecting to VM: {e}")
