import os
import shutil
import tempfile
import unittest
from io import BytesIO
import tarfile
from zipfile import ZipFile, ZIP_STORED

from pytmpdir.spooled_named_temporary_file import SpooledNamedTemporaryFile


class TestSpooledNamedTemporaryFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(self.test_dir))

    def test_operations_after_name(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"test data")
            name = f.name  # Access name property
            f.write(b"more data")
            f.read()

    def test_cleanup_after_name(self):
        file_path = None
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"test data")
            file_path = f.name
            self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.exists(file_path))

    def test_destructor_cleanup(self):
        file_path = None
        f = SpooledNamedTemporaryFile(dir=self.test_dir)
        f.write(b"test data")
        file_path = f.name
        self.assertTrue(os.path.exists(file_path))
        del f
        self.assertFalse(os.path.exists(file_path))

    def test_basic_write_read(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"test data")
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"test data")

            # Should be able to write after read
            f.write(b" more")
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"test data more")

    def test_rollover_on_size(self):
        with SpooledNamedTemporaryFile(max_size=5, dir=self.test_dir) as f:
            f.write(b"test data")  # This will cause rollover
            self.assertTrue(os.path.exists(f.name))
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"test data")

    def test_write_under_max_size(self):
        max_size = 100
        test_data = b"x" * (max_size - 10)  # Write less than max_size
        with SpooledNamedTemporaryFile(
            max_size=max_size, dir=self.test_dir
        ) as f:
            f.write(test_data)
            f.seek(0)
            content = f.read()
            self.assertEqual(content, test_data)

    def test_write_force_rollover(self):
        max_size = 100
        test_data = b"x" * (max_size + 10)  # Write more than max_size
        with SpooledNamedTemporaryFile(
            max_size=max_size, dir=self.test_dir
        ) as f:
            f.write(test_data)
            self.assertTrue(f._rolled)  # Should have rolled over
            f.seek(0)
            content = f.read()
            self.assertEqual(content, test_data)

    def test_multiple_writes_with_rollover(self):
        max_size = 50
        with SpooledNamedTemporaryFile(
            max_size=max_size, dir=self.test_dir
        ) as f:
            # Write before rollover
            f.write(b"first_data")
            self.assertFalse(f._rolled)

            # Write that causes rollover
            f.write(b"x" * max_size)
            self.assertTrue(f._rolled)

            # Write after rollover
            f.write(b"last_data")

            f.seek(0)
            content = f.read()
            self.assertTrue(b"first_data" in content)
            self.assertTrue(b"last_data" in content)

    def test_partial_reads(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"test_data")
            f.seek(0)
            partial = f.read(4)
            self.assertEqual(partial, b"test")

            # Write after partial read
            f.write(b"_more")
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"test_more")

    def test_seek_operations(self):
        with SpooledNamedTemporaryFile(max_size=100, dir=self.test_dir) as f:
            f.write(b"0123456789")
            f.seek(5)
            partial = f.read(2)
            self.assertEqual(partial, b"56")

            # Write at current position
            f.write(b"XX")
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"0123456XX9")

    def test_cleanup_after_write(self):
        file_path = None
        with SpooledNamedTemporaryFile(dir=self.test_dir) as tmpFile:
            tmpFile.write(b"test content")
            file_path = tmpFile.name
            self.assertTrue(os.path.exists(file_path))
        self.assertFalse(os.path.exists(file_path))

    def test_tar_archive_lifecycle(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as tmpFile:
            with tarfile.open(
                fileobj=tmpFile, mode="w", bufsize=1024 * 1024
            ) as tar:
                data = b"test content"
                info = tarfile.TarInfo(name="test.txt")
                info.size = len(data)
                tar.addfile(info, BytesIO(data))

            self.assertGreater(
                os.stat(tmpFile.name).st_size,
                0,
                "Tar archive file size should not be zero",
            )
            with tarfile.open(tmpFile.name, "r") as tar:
                member = tar.getmember("test.txt")
                self.assertEqual(
                    tar.extractfile(member).read(), b"test content"
                )

    def test_zip_archive_lifecycle(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as tmpFile:
            with ZipFile(tmpFile, "w", compression=ZIP_STORED) as zip:
                zip.writestr("test.txt", "test content")

            tmpFile.seek(0)
            self.assertGreater(
                os.stat(tmpFile.name).st_size,
                0,
                "Zip archive file size should not be zero",
            )
            with ZipFile(tmpFile.name, "r") as zip:
                self.assertEqual(zip.read("test.txt"), b"test content")

    def test_multiple_files_archive(self):
        files = {
            "file1.txt": b"content1",
            "file2.txt": b"content2",
            "file3.txt": b"content3",
        }

        with SpooledNamedTemporaryFile(dir=self.test_dir) as tmpFile:
            with tarfile.open(
                fileobj=tmpFile, mode="w", bufsize=1024 * 1024
            ) as tar:
                for filename, content in files.items():
                    info = tarfile.TarInfo(name=filename)
                    info.size = len(content)
                    tar.addfile(info, BytesIO(content))

            self.assertGreater(
                os.stat(tmpFile.name).st_size,
                0,
                "Multiple files tar archive size should not be zero",
            )

            with tarfile.open(name=tmpFile.name, mode="r") as tar:
                for filename, expected_content in files.items():
                    member = tar.getmember(filename)
                    self.assertEqual(
                        tar.extractfile(member).read(), expected_content
                    )

    def test_overwrite_in_middle(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"0123456789")
            f.seek(5)
            f.write(b"XXX")
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"01234XXX89")

    def test_truncate_memory_file(self):
        with SpooledNamedTemporaryFile(max_size=100, dir=self.test_dir) as f:
            f.write(b"0123456789")
            new_size = f.truncate(5)
            self.assertEqual(new_size, 5)
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"01234")

    def test_truncate_disk_file(self):
        with SpooledNamedTemporaryFile(max_size=5, dir=self.test_dir) as f:
            f.write(b"0123456789")  # This will cause rollover
            new_size = f.truncate(5)
            self.assertEqual(new_size, 5)
            f.seek(0)
            content = f.read()
            self.assertEqual(content, b"01234")

    def test_truncate_extend(self):
        with SpooledNamedTemporaryFile(dir=self.test_dir) as f:
            f.write(b"0123456789")
            new_size = f.truncate(15)
            self.assertEqual(new_size, 15)
            f.seek(0)
            content = f.read()
            # First 10 bytes should be original content
            self.assertEqual(content[:10], b"0123456789")
            # Remaining bytes should be zeros
            self.assertEqual(content[10:], b"\x00" * 5)


if __name__ == "__main__":
    unittest.main()
