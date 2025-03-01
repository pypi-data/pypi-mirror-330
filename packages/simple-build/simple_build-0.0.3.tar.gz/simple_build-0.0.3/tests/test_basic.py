from simple_build.analyse import analyse_package


def test_analyse(tmp_path, snapshot):
    tmp_path.joinpath("pyproject.toml").write_text(
        """
[project]
name = "simple-build"
version = "0.0.1"
""",
        "utf-8",
    )
    result = analyse_package(tmp_path)
    result.root = None  # exclude root path
    assert result == snapshot()
