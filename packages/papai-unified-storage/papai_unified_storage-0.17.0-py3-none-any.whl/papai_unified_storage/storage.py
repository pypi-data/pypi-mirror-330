from io import BytesIO, StringIO, TextIOWrapper
from typing import Any, Callable, Literal, overload

import fsspec
import pandas as pd
import pyarrow
import pyarrow.parquet
from fsspec import AbstractFileSystem
from fsspec.spec import AbstractBufferedFile

from .utils import (
    GlobPath,
    StorageError,
    convert_decimal_columns_to_double_with_arrow_casting,
    create_dir_tree,
    dummy_fn,
)


def filesystem(
    protocol: str,
    logging_debug_function: Callable = dummy_fn,
    logging_error_function: Callable = dummy_fn,
    **storage_options,
):
    """Generate a supercharged fsspec storage instance for a given protocol.

    Parameters
    ----------
    protocol : str
        name of the protocol to use. See options at
        https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations
    logging_debug_function : Callable, optional
        Function to use to log operations. Its first argument must be a
        string, by default dummy_fn, which does nothing.
    logging_error_function : Callable, optional
        Function to use to log errors. Its first argument must be a
        string, by default dummy_fn, which does nothing.
    Returns
    -------
    Storage(fsspec.AbstractFileSystem)
        Supercharged fsspec storage instance.
    """
    internal_fs_class = fsspec.get_filesystem_class(protocol)
    internal_fs = get_storage_wrapper(internal_fs_class, storage_options)
    fs = Storage(internal_fs, logging_debug_function, logging_error_function)
    return fs


def get_storage_wrapper(storage_class: AbstractFileSystem, storage_options):
    class FileSystemWrapper(storage_class):
        def get_file(self, rpath, lpath, **kwargs):
            create_dir_tree(fsspec.filesystem("file"), lpath)
            super().get_file(rpath, lpath, **kwargs)

        def put_file(self, lpath, rpath, **kwargs):
            create_dir_tree(self, rpath)
            super().put_file(lpath, rpath, **kwargs)

    return FileSystemWrapper(**storage_options)


class Storage:
    def __init__(
        self,
        filesystem: AbstractFileSystem,
        logging_debug_function: Callable = dummy_fn,
        logging_error_function: Callable = dummy_fn,
    ):
        """Create storage proxy to a remote file system.

        Parameters
        ----------
        logging_debug_function : Callable, optional
            Function to use to log operations. Its first argument must be a
            string, by default dummy_fn, which does nothing.
        logging_error_function : Callable, optional
            Function to use to log errors. Its first argument must be a
            string, by default dummy_fn, which does nothing.
        """
        self.filesystem = filesystem
        self.log_debug_fn = logging_debug_function
        self.log_error_fn = logging_error_function

    @overload
    def get(
        self,
        remote_path: str | list[str] | GlobPath | list[GlobPath],
        local_path: str,
        recursive: bool = False,
    ): ...
    @overload
    def get(self, remote_path: list[str], local_path: list[str], recursive: bool = False): ...
    def get(self, remote_path, local_path, recursive=False):
        """Copy remote file(s) to local.

        Copies a specific file or tree of files (if recursive=True). If
        rpath ends with a "/", it will be assumed to be a directory, and
        target files will go within. Can submit a list of paths, which may
        be glob-patterns and will be expanded.

        If both remote_path and local_path are lists, they must be the same
        length and paths will not be expanded. That means that you can't
        download a folder recursively to different location than the rest.

        If you set recursive=True, then remote_paths that are folders
        will be downloaded recursively. If you use a glob pattern in a
        remote_path (e.g. `folder/*`), it will download the folder `folder`
        recursively, but not the other non-glob pattern path of `remote_path`.

        Calls get_file for each source.

        Examples
        --------
        >>> fs.get(["file1", "folder"], "download", recursive=True)
        >>> pathlib.Path("download").rglob('*')
        [download/file1, download/folder/file2]
        >>> fs.get(["file1", "folder/**"], "download", recursive=False)
        >>> pathlib.Path("download").rglob('*')
        [download/file1, download/folder/file2]
        >>> # You can't download a folder at a different location than the rest
        >>> fs.get(["file1", "folder/*"], ["download/1/file1", "download/2/"])
        >>> pathlib.Path("download").rglob('*')
        [download/1/file1, download/2/]
        >>> fs.get("file1", "download/path/to/file")
        >>> pathlib.Path("download").rglob('*')
        [download/path/to/file]
        """
        self.log_debug_fn(f"Copying remote file(s) at {remote_path} to local at {local_path}")
        try:
            self.filesystem.get(remote_path, local_path, recursive)
        except Exception:
            error_txt = f"Failed to copy remote file(s) at {remote_path} to local at {local_path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def get_file(self, rpath, lpath, **kwargs):
        self.log_debug_fn(f"Copying remote file at {rpath} to local at {lpath}")
        try:
            return self.filesystem.get_file(rpath, lpath, **kwargs)
        except Exception:
            error_txt = f"Failed to copy remote file at {rpath} to local at {lpath}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def put(self, local_path: str | list[str], remote_path: str | list[str], recursive=False):
        """Copy file(s) from local to remote.

        Copies a specific file or tree of files (if recursive=True). If
        rpath ends with a "/", it will be assumed to be a directory, and
        target files will go within. Can submit a list of paths, which may
        be glob-patterns and will be expanded.

        If both remote_path and local_path are lists, they must be the same
        length and paths will not be expanded. That means that you can't
        upload a folder recursively to different location than the rest.

        If you set recursive=True, then local_paths that are folders
        will be uploaded recursively. If you use a glob pattern in a
        local_path (e.g. `folder/*`), it will upload the folder `folder`
        recursively, but not the other non-glob pattern path of `local_path`.

        Calls put_file for each source.

        Examples
        --------
        >>> fs.put(["file1", "folder"], "upload", recursive=True)
        >>> fs.glob('upload/**')
        [upload/file1, upload/folder/file2]
        >>> fs.put(["file1", "folder/**"], "upload", recursive=False)
        >>> fs.glob('upload/**')
        [upload/file1, upload/folder/file2]
        >>> # You can't upload a folder at a different location than the rest
        >>> fs.put(["file1", "folder/"], ["upload/1/file1", "upload/2/"], recursively=True)
        >>> fs.glob('upload/**')
        []
        >>> fs.put("file1", "upload/path/to/file")
        >>> fs.glob('upload/**')
        [upload/path/to/file]
        """
        self.log_debug_fn(f"Copying local file(s) at {local_path} to remote at {remote_path}")
        try:
            self.filesystem.put(local_path, remote_path, recursive)
        except Exception:
            error_txt = f"Failed to copy local file(s) at {local_path} to remote at {remote_path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def put_file(self, lpath, rpath, **kwargs):
        self.log_debug_fn(f"Copying local file at {lpath} to remote at {rpath}")
        try:
            self.filesystem.put_file(lpath, rpath, **kwargs)
        except Exception:
            error_txt = f"Failed to copy local file at {lpath} to remote at {rpath}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def _open_with_logs(self, path, mode, *, log=True, **kwargs):
        if log is True:
            self.log_debug_fn(f"Opening remote file at {path} with {mode=}")

        try:
            return self.filesystem.open(path, mode, **kwargs)
        except Exception as exc:
            error_txt = f"Failed to open remote file at {path} with {mode=}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt) from exc

    def open(self, path: str, mode: str, **kwargs):
        return self._open_with_logs(path, mode, **kwargs)

    def open_for_writing(
        self, path: str, text: bool = False, *, log: bool = True
    ) -> TextIOWrapper | AbstractBufferedFile:
        mode = "wb" if text is False else "w"
        return self._open_with_logs(path, mode, log=log)

    def open_for_reading(
        self, path: str, text: bool = False, *, log: bool = True
    ) -> TextIOWrapper | AbstractBufferedFile:
        mode = "rb" if text is False else "r"
        return self._open_with_logs(path, mode, log=log)

    def move(self, source_path: str, destination_path: str):
        """Move file(s) from one location to another.

        This fails if the target file system is not capable of creating the
        directory, for example if it is write-only or if auto_mkdir=False. There is
        no command line equivalent of this scenario without an explicit mkdir to
        create the new directory.
        See https://filesystem-spec.readthedocs.io/en/latest/copying.html for more
        information.
        """
        self.log_debug_fn(f"Moving remote file(s) from {source_path} to {destination_path}")
        try:
            self.filesystem.mv(source_path, destination_path)
        except Exception:
            error_txt = f"Failed to move file(s) from {source_path} to {destination_path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def _remove_prefix(
        self, files: list[str], remove_root_folder: bool = True, remove_prefix: str | None = None
    ):
        if remove_root_folder is True:
            files = [file.lstrip("/").partition("/")[2] for file in files]

        if remove_prefix is not None:
            files = [
                (file.replace(remove_prefix, "", 1) if file.startswith(remove_prefix) else file)
                for file in files
            ]

        return files

    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def list_files(
        self,
        path: str,
        recursive: bool = False,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    def list_files(
        self, path, recursive=False, remove_root_folder=False, remove_prefix=None, detail=False
    ):
        """List files in a remote directory.

        Parameters
        ----------
        path : str
            Path at which to list objects.
        recursive : bool, optional
            Whether to list objects that are deeper than `path`,
            by default False.
        remove_root_folder : bool, optional
            Whether to remove the root folder of `path` in the results,
            by default False.
        remove_prefix : str, optional
            If not None, will remove prefix `remove_prefix` from the results,
            by default None.
        detail : bool, optional
            If True, return a list of dictionaries with details about the
            files. It also disables the `remove_root_folder` and
            `remove_prefix` options. By default False.

        Returns
        -------
        list[str]
            List of objects that exist under `path`.
        """
        if recursive is True:
            maxdepth = None
        else:
            maxdepth = 1

        self.log_debug_fn(f"Listing remote files at {path}")

        try:
            files = self.filesystem.find(path, maxdepth, detail=detail)
        except Exception:
            error_txt = f"Failed to list remote files at {path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

        if detail is False:
            files = self._remove_prefix(files, remove_root_folder, remove_prefix)
        return files

    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[False] = False,
    ) -> list[str]: ...
    @overload
    def glob_files(
        self,
        pattern: str,
        remove_root_folder: bool = False,
        remove_prefix: str | None = None,
        detail: Literal[True] = True,
    ) -> dict[str, dict[str, Any]]: ...
    def glob_files(self, pattern, remove_root_folder=False, remove_prefix=None, detail=False):
        """List files in a remote directory that match a pattern.

        Parameters
        ----------
        pattern : str
            pattern to list objects with.
        remove_root_folder : bool, optional
            Whether to remove the root folder of `path` in the results,
            by default False.
        remove_prefix : str, optional
            If not None, will remove prefix `remove_prefix` from the results,
            by default None.
        detail : bool, optional
            If True, return a list of dictionaries with details about the
            files. It also disables the `remove_root_folder` and
            `remove_prefix` options. By default False.

        Returns
        -------
        list[str]
            List of objects that matches `pattern`.
        """
        self.log_debug_fn(f"Listing remote files matching {pattern}")

        try:
            files = self.filesystem.glob(pattern, detail=detail)
        except Exception:
            error_txt = f"Failed to list remote files matching {pattern}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

        if detail is False:
            files = self._remove_prefix(files, remove_root_folder, remove_prefix)
        return files

    def remove_files(self, paths: str | list[str], recursive: bool = False):
        self.log_debug_fn(f"Removing remote file(s) at {paths}")
        try:
            self.filesystem.rm(paths, recursive)
        except Exception:
            error_txt = f"Failed to remove remote file(s) at {paths}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def read_dataset_from_parquet(self, path: str) -> pd.DataFrame:
        self.log_debug_fn(f"Reading remote dataset from {path}")
        try:
            parquet = pyarrow.parquet.ParquetDataset(path, filesystem=self.filesystem)
            table = parquet.read_pandas()
            table = convert_decimal_columns_to_double_with_arrow_casting(table)
            return table.to_pandas()
        except Exception:
            error_txt = f"Failed to read remote dataset from {path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def write_dataframe_to_parquet(self, path: str, df: pd.DataFrame):
        self.log_debug_fn(f"Writing dataset to remote file at {path}")
        table = pyarrow.Table.from_pandas(df)
        try:
            pyarrow.parquet.write_table(table, path, filesystem=self.filesystem)
        except Exception:
            error_txt = f"Failed to write dataset to remote file at {path}"
            self.log_error_fn(error_txt)
            raise StorageError(error_txt)

    def loader(self, path: str, load_method: Callable, text: bool = False):
        self.log_debug_fn(f"Loading object with {load_method.__name__} from remote file at {path}")
        with self.open_for_reading(path, text) as f:
            try:
                return load_method(f)
            except Exception:
                error_txt = (
                    f"Failed to load object with {load_method.__name__} from remote file at {path}"
                )
                self.log_error_fn(error_txt)
                raise StorageError(error_txt)

    def write_to_file(self, path: str, content: str | bytes | BytesIO | StringIO):
        if isinstance(content, (str, StringIO)):
            text = True
        else:
            text = False

        if isinstance(content, (BytesIO, StringIO)):
            content.seek(0)
            content = content.read()

        self.log_debug_fn(f"Writing content to remote file at {path}")

        create_dir_tree(self.filesystem, path)

        with self.open_for_writing(path, text, log=False) as f:
            try:
                # f.write actually supports both str and bytes
                f.write(content)  # type: ignore[arg-type]
            except Exception:
                error_txt = f"Failed to write content to remote file at {path}"
                self.log_error_fn(error_txt)
                raise StorageError(error_txt)

    def exists(self, path: str) -> bool:
        return self.filesystem.exists(path)
