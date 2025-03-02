import click
import subprocess

def run_command(command: str):
    """Helper function to execute shell commands."""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        click.echo(result.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e.output.decode('utf-8')}", err=True)
        raise


@click.command()
@click.option("--project", required=True, help="Google Cloud project ID")
@click.option("--zone", required=True, help="Computer instance zone")
@click.option("--instance", required=True, help="Compute instance name to start")
def start(project, zone, instance):
    """Start your VM"""
    click.echo(f"Starting VM: {instance}")
    command = f"gcloud compute instances start {instance} --project {project} --zone {zone}"
    run_command(command)

@click.command()
@click.option("--project", required=True, help="Google Cloud project ID")
@click.option("--zone", required=True, help="Computer instance zone")
@click.option("--instance", required=True, help="Compute instance name to start")
def stop(project, zone, instance):
    """STOP your VM"""
    click.echo(f"Stopping VM: {instance}")
    command = f"gcloud compute instances stop {instance} --project {project} --zone {zone}"
    run_command(command)

@click.command()
@click.option("--project", required=True, help="Google Cloud project ID")
@click.option("--zone", required=True, help="Computer instance zone")
@click.option("--instance", required=True, help="Compute instance name to start")
def connect(project, zone, instance):
    """Connect to your VM in vscode inside your code"""
    click.echo(f"Connecting to VM: {instance}")
    command = f"gcloud compute ssh {instance} --project {project} --zone {zone}"
    run_command(command)
