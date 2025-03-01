"""Sdist file writing.

See: https://peps.python.org/pep-0517/#source-distributions
"""

import contextlib
from gzip import GzipFile
import io
import os
from pathlib import Path
import shutil
import tarfile
from tempfile import TemporaryDirectory
from types import TracebackType
import typing as t

from ..analyse import PackageAnalysis
from ._files import gather_files, normalize_file_permissions
from ._metadata import create_metadata


def write_sdist(sdist: "SdistWriter", package: PackageAnalysis) -> None:
    """Write an sdist."""
    sdist_config = package.tool.get("sdist", {})
    file_paths = gather_files(
        package.root,
        use_git=sdist_config.get("use_git", True),
        user_includes=sdist_config.get("include", []),
        user_excludes=sdist_config.get("exclude", []),
    )
    pre_write_hooks = package.tool.get("pre_write_hooks", [])
    if not pre_write_hooks:
        for file_path in file_paths:
            rel_path = file_path.relative_to(package.root).parts
            sdist.write_path(rel_path, file_path)
    else:
        # if there are pre-write hooks, we must write the files to a temporary directory
        # and then call the hooks before writing the files to the wheel
        with TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            for file_path in file_paths:
                rel_path = file_path.relative_to(package.root).parts
                dest = tmp.joinpath(*rel_path)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file_path, dest)
            for hook in pre_write_hooks:
                hook("sdist", tmp, None, package)
            for file_path in tmp.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(tmp).parts
                    sdist.write_path(rel_path, file_path)

    metadata_text = create_metadata(package.project, package.root)
    sdist.write_text(("PKG-INFO",), metadata_text)


SdistWriterType = t.TypeVar("SdistWriterType", bound="SdistWriter")


class SdistWriter:
    """Write a sdist file, implementing https://peps.python.org/pep-0517/#source-distributions.

    Should be used as a context manager.
    """

    def __init__(self, directory: Path, name: str, version: str) -> None:
        """Initialize.

        :param directory: The directory to write to.
        :param name: The distribution name.
        :param version: The distribution version.
        """
        self._path = directory / f"{name}-{version}.tar.gz"
        self._dirname = f"{name}-{version}"
        self._fixed_timestamp: int | None = None
        with contextlib.suppress(KeyError, ValueError):
            self._fixed_timestamp = int(os.environ["SOURCE_DATE_EPOCH"])
        self._tf: tarfile.TarFile | None = None

    @staticmethod
    def raise_not_open() -> t.NoReturn:
        """Assert that the tar file is open."""
        raise OSError("Sdist file is not open.")

    def __enter__(self: SdistWriterType) -> SdistWriterType:
        """Enter the context manager."""
        gz = GzipFile(str(self._path), mode="wb", mtime=self._fixed_timestamp)
        self._tf = tarfile.TarFile(
            str(self._path), mode="w", fileobj=gz, format=tarfile.PAX_FORMAT
        )
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        if self._tf is None:
            self.raise_not_open()
        self._tf.close()
        if self._tf.fileobj:
            self._tf.fileobj.close()
        self._tf = None

    @property
    def path(self) -> Path:
        """Return the path to the sdist."""
        return self._path

    # methods that require an open tar file

    def list_files(self) -> list[str]:
        """Return a list of files in the sdist."""
        if self._tf is None:
            self.raise_not_open()
        return self._tf.getnames()

    def write_text(self, path: t.Sequence[str], text: str) -> None:
        """Write a text file to the sdist (with utf8 encoding)

        :param path: The path to write to in the sdist.
        :param text: The text to write.
        """
        if self._tf is None:
            self.raise_not_open()
        content = text.encode("utf-8")
        info = tarfile.TarInfo("/".join((self._dirname, *path)))
        info.size = len(content)
        self._tf.addfile(info, io.BytesIO(content))

    def write_path(self, path: t.Sequence[str], source: Path) -> None:
        """Write an external path to the sdist.

        :param path: The path to write to in the sdist.
        :param source: The path to write from.
        """
        if self._tf is None:
            self.raise_not_open()
        info = self._tf.gettarinfo(
            str(source), arcname="/".join((self._dirname, *path))
        )
        # make more reproducible
        info.uid = 0
        info.gid = 0
        info.uname = ""
        info.gname = ""
        info.mode = normalize_file_permissions(info.mode)
        if self._fixed_timestamp is not None:
            info.mtime = self._fixed_timestamp
        if info.isreg():
            with source.open(mode="rb") as handle:
                self._tf.addfile(info, handle)
        else:
            self._tf.addfile(info)
