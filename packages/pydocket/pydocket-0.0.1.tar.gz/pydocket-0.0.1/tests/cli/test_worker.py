from typer.testing import CliRunner

from docket.cli import app


def test_worker_command_outputs_todo(runner: CliRunner):
    """Should output a TODO message when the worker command is invoked."""
    result = runner.invoke(app, ["worker"])
    assert result.exit_code == 0
    assert "TODO" in result.stdout.strip()
