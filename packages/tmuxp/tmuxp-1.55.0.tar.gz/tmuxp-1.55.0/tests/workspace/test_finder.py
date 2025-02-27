"""Test config file searching for tmuxp."""

from __future__ import annotations

import argparse
import pathlib
import typing as t

import pytest

from tmuxp import cli
from tmuxp.cli.utils import tmuxp_echo
from tmuxp.workspace.finders import (
    find_workspace_file,
    get_workspace_dir,
    in_cwd,
    in_dir,
    is_pure_name,
)

if t.TYPE_CHECKING:
    import _pytest.capture


def test_in_dir_from_config_dir(tmp_path: pathlib.Path) -> None:
    """config.in_dir() finds configs config dir."""
    cli.startup(tmp_path)
    yaml_config = tmp_path / "myconfig.yaml"
    yaml_config.touch()
    json_config = tmp_path / "myconfig.json"
    json_config.touch()
    configs_found = in_dir(tmp_path)

    assert len(configs_found) == 2


def test_ignore_non_configs_from_current_dir(tmp_path: pathlib.Path) -> None:
    """cli.in_dir() ignore non-config from config dir."""
    cli.startup(tmp_path)

    junk_config = tmp_path / "myconfig.psd"
    junk_config.touch()
    conf = tmp_path / "watmyconfig.json"
    conf.touch()
    configs_found = in_dir(tmp_path)
    assert len(configs_found) == 1


def test_get_configs_cwd(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """config.in_cwd() find config in shell current working directory."""
    confdir = tmp_path / "tmuxpconf2"
    confdir.mkdir()

    monkeypatch.chdir(confdir)
    with pathlib.Path(".tmuxp.json").open("w+b") as config1:
        config1.close()

    configs_found = in_cwd()
    assert len(configs_found) == 1
    assert ".tmuxp.json" in configs_found


class PureNameTestFixture(t.NamedTuple):
    """Test fixture for verifying pure name path validation."""

    test_id: str
    path: str
    expect: bool


PURE_NAME_TEST_FIXTURES: list[PureNameTestFixture] = [
    PureNameTestFixture(
        test_id="current_dir",
        path=".",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="current_dir_slash",
        path="./",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="empty_path",
        path="",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="tmuxp_yaml",
        path=".tmuxp.yaml",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="parent_tmuxp_yaml",
        path="../.tmuxp.yaml",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="parent_dir",
        path="../",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="absolute_path",
        path="/hello/world",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="home_tmuxp_path",
        path="~/.tmuxp/hey",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="home_work_path",
        path="~/work/c/tmux/",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="home_work_tmuxp_yaml",
        path="~/work/c/tmux/.tmuxp.yaml",
        expect=False,
    ),
    PureNameTestFixture(
        test_id="pure_name",
        path="myproject",
        expect=True,
    ),
]


@pytest.mark.parametrize(
    list(PureNameTestFixture._fields),
    PURE_NAME_TEST_FIXTURES,
    ids=[test.test_id for test in PURE_NAME_TEST_FIXTURES],
)
def test_is_pure_name(
    test_id: str,
    path: str,
    expect: bool,
) -> None:
    """Test is_pure_name() is truthy when file, not directory or config alias."""
    assert is_pure_name(path) == expect


def test_tmuxp_configdir_env_var(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tests get_workspace_dir() when TMUXP_CONFIGDIR is set."""
    monkeypatch.setenv("TMUXP_CONFIGDIR", str(tmp_path))

    assert get_workspace_dir() == str(tmp_path)


def test_tmuxp_configdir_xdg_config_dir(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test get_workspace_dir() when XDG_CONFIG_HOME is set."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    tmux_dir = tmp_path / "tmuxp"
    tmux_dir.mkdir()

    assert get_workspace_dir() == str(tmux_dir)


@pytest.fixture
def homedir(tmp_path: pathlib.Path) -> pathlib.Path:
    """Fixture to ensure and return a home directory."""
    home = tmp_path / "home"
    home.mkdir()
    return home


@pytest.fixture
def configdir(homedir: pathlib.Path) -> pathlib.Path:
    """Fixture to ensure user directory for tmuxp and return it, via homedir fixture."""
    conf = homedir / ".tmuxp"
    conf.mkdir()
    return conf


@pytest.fixture
def projectdir(homedir: pathlib.Path) -> pathlib.Path:
    """Fixture to ensure and return an example project dir."""
    proj = homedir / "work" / "project"
    proj.mkdir(parents=True)
    return proj


def test_resolve_dot(
    tmp_path: pathlib.Path,
    homedir: pathlib.Path,
    configdir: pathlib.Path,
    projectdir: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test find_workspace_file() resolves dots as relative / current directory."""
    monkeypatch.setenv("HOME", str(homedir))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(homedir / ".config"))

    tmuxp_conf_path = projectdir / ".tmuxp.yaml"
    tmuxp_conf_path.touch()
    user_config_name = "myconfig"
    user_config = configdir / f"{user_config_name}.yaml"
    user_config.touch()

    project_config = tmuxp_conf_path

    monkeypatch.chdir(projectdir)

    expect = str(project_config)
    assert find_workspace_file(".") == expect
    assert find_workspace_file("./") == expect
    assert find_workspace_file("") == expect
    assert find_workspace_file("../project") == expect
    assert find_workspace_file("../project/") == expect
    assert find_workspace_file(".tmuxp.yaml") == expect
    assert find_workspace_file(f"../../.tmuxp/{user_config_name}.yaml") == str(
        user_config,
    )
    assert find_workspace_file("myconfig") == str(user_config)
    assert find_workspace_file("~/.tmuxp/myconfig.yaml") == str(user_config)

    with pytest.raises(FileNotFoundError):
        find_workspace_file(".tmuxp.json")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".tmuxp.ini")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("../")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("mooooooo")

    monkeypatch.chdir(homedir)

    expect = str(project_config)
    assert find_workspace_file("work/project") == expect
    assert find_workspace_file("work/project/") == expect
    assert find_workspace_file("./work/project") == expect
    assert find_workspace_file("./work/project/") == expect
    assert find_workspace_file(f".tmuxp/{user_config_name}.yaml") == str(user_config)
    assert find_workspace_file(f"./.tmuxp/{user_config_name}.yaml") == str(
        user_config,
    )
    assert find_workspace_file("myconfig") == str(user_config)
    assert find_workspace_file("~/.tmuxp/myconfig.yaml") == str(user_config)

    with pytest.raises(FileNotFoundError):
        find_workspace_file("")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".tmuxp.yaml")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("../")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("mooooooo")

    monkeypatch.chdir(configdir)

    expect = str(project_config)
    assert find_workspace_file("../work/project") == expect
    assert find_workspace_file("../../home/work/project") == expect
    assert find_workspace_file("../work/project/") == expect
    assert find_workspace_file(f"{user_config_name}.yaml") == str(user_config)
    assert find_workspace_file(f"./{user_config_name}.yaml") == str(user_config)
    assert find_workspace_file("myconfig") == str(user_config)
    assert find_workspace_file("~/.tmuxp/myconfig.yaml") == str(user_config)

    with pytest.raises(FileNotFoundError):
        find_workspace_file("")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".tmuxp.yaml")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("../")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("mooooooo")

    monkeypatch.chdir(tmp_path)

    expect = str(project_config)
    assert find_workspace_file("home/work/project") == expect
    assert find_workspace_file("./home/work/project/") == expect
    assert find_workspace_file(f"home/.tmuxp/{user_config_name}.yaml") == str(
        user_config,
    )
    assert find_workspace_file(f"./home/.tmuxp/{user_config_name}.yaml") == str(
        user_config,
    )
    assert find_workspace_file("myconfig") == str(user_config)
    assert find_workspace_file("~/.tmuxp/myconfig.yaml") == str(user_config)

    with pytest.raises(FileNotFoundError):
        find_workspace_file("")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".")
    with pytest.raises(FileNotFoundError):
        find_workspace_file(".tmuxp.yaml")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("../")
    with pytest.raises(FileNotFoundError):
        find_workspace_file("mooooooo")


def test_find_workspace_file_arg(
    homedir: pathlib.Path,
    configdir: pathlib.Path,
    projectdir: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test find_workspace_file() via file path."""
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_file", type=str)

    def config_cmd(workspace_file: str) -> None:
        tmuxp_echo(find_workspace_file(workspace_file, workspace_dir=configdir))

    monkeypatch.setenv("HOME", str(homedir))
    tmuxp_config_path = projectdir / ".tmuxp.yaml"
    tmuxp_config_path.touch()
    user_config_name = "myconfig"
    user_config = configdir / f"{user_config_name}.yaml"
    user_config.touch()

    project_config = projectdir / ".tmuxp.yaml"

    def check_cmd(config_arg: str) -> _pytest.capture.CaptureResult[str]:
        args = parser.parse_args([config_arg])
        config_cmd(workspace_file=args.workspace_file)
        return capsys.readouterr()

    monkeypatch.chdir(projectdir)
    expect = str(project_config)
    assert expect in check_cmd(".").out
    assert expect in check_cmd("./").out
    assert expect in check_cmd("").out
    assert expect in check_cmd("../project").out
    assert expect in check_cmd("../project/").out
    assert expect in check_cmd(".tmuxp.yaml").out
    assert str(user_config) in check_cmd(f"../../.tmuxp/{user_config_name}.yaml").out
    assert user_config.stem in check_cmd("myconfig").out
    assert str(user_config) in check_cmd("~/.tmuxp/myconfig.yaml").out

    with pytest.raises(FileNotFoundError, match="file not found"):
        assert "file not found" in check_cmd(".tmuxp.json").err
    with pytest.raises(FileNotFoundError, match="file not found"):
        assert "file not found" in check_cmd(".tmuxp.ini").err
    with pytest.raises(FileNotFoundError, match="No tmuxp files found"):
        assert "No tmuxp files found" in check_cmd("../").err
    with pytest.raises(
        FileNotFoundError,
        match="workspace-file not found in workspace dir",
    ):
        assert "workspace-file not found in workspace dir" in check_cmd("moo").err
