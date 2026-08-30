"""Smoke tests for repo path layout."""


from agilentirformats.paths import (
    DEFAULT_CLUSTER_LIBRARY,
    FIXTURES_DIR,
    INPUTS_DIR,
    LIBRARIES_DIR,
    OUTPUTS_DIR,
    REPO_ROOT,
    ensure_work_dirs,
)


def test_repo_root_contains_pyproject():
    assert (REPO_ROOT / "pyproject.toml").is_file()


def test_standard_dirs_exist():
    assert INPUTS_DIR.is_dir()
    assert OUTPUTS_DIR.is_dir()
    assert LIBRARIES_DIR.is_dir()
    assert FIXTURES_DIR.is_dir()


def test_default_cluster_library_present():
    assert DEFAULT_CLUSTER_LIBRARY.is_file()


def test_ensure_work_dirs():
    ensure_work_dirs()
    assert INPUTS_DIR.is_dir()
    assert OUTPUTS_DIR.is_dir()


def test_package_exports_agilent_ir_file():
    from agilentirformats import AgilentIRFile

    assert AgilentIRFile.filetype()
