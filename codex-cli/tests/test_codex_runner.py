from unittest.mock import Mock, patch

from src.codex_runner import candidate_commands, codex_status, resolve_codex


@patch("src.codex_runner._npm_codex", return_value="C:/npm/codex.cmd")
@patch("src.codex_runner.shutil.which")
def test_candidates_prefer_npm_shim(mock_which, _mock_npm, monkeypatch):
    monkeypatch.delenv("CODEX_CLI_PATH", raising=False)
    mock_which.side_effect = lambda name: "C:/WindowsApps/codex.exe" if name == "codex" else "C:/node/npx.cmd"
    assert candidate_commands()[0] == ["C:/npm/codex.cmd"]


@patch("src.codex_runner.candidate_commands", return_value=[["bad"], ["good"]])
@patch("src.codex_runner.subprocess.run")
def test_resolve_skips_inaccessible_candidate(mock_run, _mock_candidates):
    mock_run.side_effect = [OSError("denied"), Mock(returncode=0, stdout="codex-cli 1.0")]
    assert resolve_codex() == ["good"]


@patch("src.codex_runner.resolve_codex", return_value=["codex"])
@patch("src.codex_runner.subprocess.run")
def test_login_status(mock_run, _mock_resolve):
    mock_run.return_value = Mock(returncode=0, stdout="Logged in using ChatGPT", stderr="")
    assert codex_status()["loggedIn"] is True
