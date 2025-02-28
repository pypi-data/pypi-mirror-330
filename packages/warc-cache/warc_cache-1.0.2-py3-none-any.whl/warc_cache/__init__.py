from dataclasses import dataclass
from gzip import GzipFile
from io import BytesIO
from itertools import islice
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryFile
from typing import (
    IO,
    NamedTuple,
    Iterable,
    Iterator,
    Optional,
    Sequence,
    MutableSequence,
)
from uuid import uuid4
from warnings import warn

from more_itertools import spy, before_and_after
from tqdm.auto import tqdm
from warcio import ArchiveIterator, WARCWriter
from warcio.recordloader import ArcWarcRecord as WarcRecord


_DEFAULT_MAX_FILE_SIZE: int = 1_000_000_000  # 1GB
_DEFAULT_MAX_FILE_RECORDS: Optional[int] = None


class WarcCacheLocation(NamedTuple):
    key: str
    offset: int
    length: int


class WarcCacheRecord(NamedTuple):
    record: WarcRecord
    location: WarcCacheLocation


class _WarcCacheRecord(NamedTuple):
    record: WarcRecord
    location: Optional[WarcCacheLocation]


def _write_records(
    records: Iterable[WarcRecord],
    file: IO[bytes],
    key: str,
    max_file_size: int,
    max_file_records: Optional[int],
) -> Iterator[_WarcCacheRecord]:
    # Write WARC info record.
    with GzipFile(fileobj=file, mode="wb") as gzip_file:
        writer = WARCWriter(gzip_file, gzip=False)
        warc_info_record: WarcRecord = writer.create_warcinfo_record(
            filename=key, info={}
        )
        writer.write_record(warc_info_record)

    # Warn about low max file size.
    if file.tell() * 2 > max_file_size:
        warn(UserWarning(f"Very low max file size: {max_file_size} bytes"))

    if max_file_records is None:
        records_slice = records
    else:
        records_slice = islice(records, max_file_records)
    for record in records_slice:
        record_buffer: MutableSequence[_WarcCacheRecord] = []

        offset = file.tell()
        with TemporaryFile() as tmp_file:
            # Write record to temporary file.
            with GzipFile(fileobj=tmp_file, mode="wb") as tmp_gzip_file:
                writer = WARCWriter(tmp_gzip_file, gzip=False)
                writer.write_record(record)
            tmp_file.flush()
            length = tmp_file.tell()
            tmp_file.seek(0)

            # Check if record does not into file.
            if offset + length > max_file_size:
                # Does not fit, so break and return all remaining records
                # without location.
                record_buffer.append(_WarcCacheRecord(record=record, location=None))
                break

            # Write temporary file to file.
            copyfileobj(tmp_file, file)

            rec = _WarcCacheRecord(
                record=record,
                location=WarcCacheLocation(
                    key=key,
                    offset=offset,
                    length=length,
                ),
            )
            record_buffer.append(rec)

        yield from record_buffer

    for record in records:
        yield _WarcCacheRecord(record=record, location=None)


@dataclass(frozen=True)
class WarcCacheStore:
    cache_dir_path: Path
    max_file_size: int = _DEFAULT_MAX_FILE_SIZE
    """
    Maximum number of bytes to write to a single WARC file.
    """
    max_file_records: Optional[int] = _DEFAULT_MAX_FILE_RECORDS
    """
    Maximum number of WARC records to write to a single WARC file.
    No limit is imposed if set to None.
    """
    quiet: bool = False
    """
    Suppress logging and progress bars.
    """
    read_all_min_accumulated_bytes: int = 0
    """
    Minimum accumulated bytes of cached files to start reading.
    This is useful to pause reading until an appropriate amount of data is cached.
    """
    read_all_include_temporary_files: bool = False
    """
    Include temporary files when reading all cached records.
    """

    def __post_init__(self):
        self.cache_dir_path.mkdir(parents=True, exist_ok=True)

    def write(self, records: Iterable[WarcRecord]) -> Iterator[WarcCacheRecord]:
        records = iter(records)
        head: Sequence[WarcRecord]
        head, records = spy(records)
        while len(head) > 0:
            # Find next available key.
            key: str = f"{uuid4().hex}.warc.gz"
            while (self.cache_dir_path / key).exists() or (
                self.cache_dir_path / f".{key}"
            ).exists():
                key = f"{uuid4().hex}.warc.gz"

            tmp_file_path: Path = self.cache_dir_path / f".{key}"
            with tmp_file_path.open("wb") as tmp_file:
                # Write records to buffer.
                offset_records: Iterable[_WarcCacheRecord] = _write_records(
                    records=records,
                    file=tmp_file,
                    key=key,
                    max_file_size=self.max_file_size,
                    max_file_records=self.max_file_records,
                )
                # noinspection PyTypeChecker
                offset_records = tqdm(
                    offset_records,
                    desc="Write WARC records to buffer",
                    disable=self.quiet,
                )
                saved_records, unsaved_records = before_and_after(
                    lambda record: record.location is not None,
                    offset_records,
                )
                # Consume iterator to write records to buffer.
                saved_records = iter(list(saved_records))

            # Rename temporary file to final file.
            tmp_file_path.rename(self.cache_dir_path / key)

            for offset_record in saved_records:
                if offset_record.location is None:
                    raise RuntimeError("Expected location to be set.")
                yield WarcCacheRecord(
                    record=offset_record.record,
                    location=offset_record.location,
                )
            records = (offset_record.record for offset_record in unsaved_records)
            head, records = spy(records)

    def read(self, location: WarcCacheLocation) -> Iterator[WarcRecord]:
        file_path = self.cache_dir_path / location.key
        with file_path.open("rb") as file:
            file.seek(location.offset)
            buffer = file.read(location.length)

        with GzipFile(fileobj=BytesIO(buffer), mode="rb") as gzip_file:
            iterator = ArchiveIterator(gzip_file)
            yield from iterator

    def read_all(self) -> Iterator[WarcCacheRecord]:
        file_paths: Iterable[Path] = self.cache_dir_path.glob("*.warc.gz")
        if not self.read_all_include_temporary_files:
            file_paths = (
                file_path
                for file_path in file_paths
                if not file_path.name.startswith(".")
            )
        file_paths_list = list(file_paths)
        total_bytes = sum(file_path.stat().st_size for file_path in file_paths_list)
        if total_bytes < self.read_all_min_accumulated_bytes:
            # Skip reading files if total size is less than threshold.
            if not self.quiet:
                print(
                    f"Skipping reading because total size of cached files ({total_bytes} bytes) is less than {self.read_all_min_accumulated_bytes} bytes."
                )
            return

        file_paths = file_paths_list
        for file_path in file_paths:
            with file_path.open("rb") as file:
                with GzipFile(fileobj=file, mode="rb") as gzip_file:
                    iterator = ArchiveIterator(gzip_file)
                    last_offset = file.tell()
                    for record in iterator:
                        if record.rec_type == "warcinfo":
                            continue
                        current_offset = file.tell()
                        location = WarcCacheLocation(
                            key=str(file_path.relative_to(self.cache_dir_path)),
                            offset=last_offset,
                            length=current_offset - last_offset,
                        )
                        yield WarcCacheRecord(
                            record=record,
                            location=location,
                        )
                        last_offset = current_offset
