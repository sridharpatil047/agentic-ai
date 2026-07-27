import os
import io
import time
import tarfile
from deepagents.backends.sandbox import BaseSandbox
from deepagents.backends.protocol import (
    ExecuteResponse, 
    FileUploadResponse, 
    FileDownloadResponse
)

class DockerSandbox(BaseSandbox):
    """Docker sandbox backend for Deep Agents."""
    
    def __init__(self, container, work_dir: str = "/workspace"):
        self._container = container
        self._work_dir = work_dir
        
    @property
    def id(self) -> str:
        return self._container.id
        
    def execute(self, command: str, **kwargs) -> ExecuteResponse:
        exit_code, output = self._container.exec_run(
            ["sh", "-c", command],
            workdir=self._work_dir,
        )
        return ExecuteResponse(
            output=output.decode("utf-8", errors="replace"),
            exit_code=exit_code,
        )

    def upload_files(self, files: list[tuple[str, bytes]]) -> list[FileUploadResponse]:
        """Uploads raw bytes into the container via Docker tar streams."""
        responses = []
        for file_path, file_content in files:
            try:
                # 1. Resolve container paths
                target_path = os.path.join(self._work_dir, file_path.lstrip("/"))
                target_dir = os.path.dirname(target_path)
                file_name = os.path.basename(target_path)
                
                # 2. Ensure target directory exists
                self._container.exec_run(["mkdir", "-p", target_dir])
                
                # 3. Create a tar archive in memory containing just this file
                tar_stream = io.BytesIO()
                with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                    tarinfo = tarfile.TarInfo(name=file_name)
                    tarinfo.size = len(file_content)
                    tarinfo.mtime = int(time.time())
                    tar.addfile(tarinfo, io.BytesIO(file_content))
                tar_stream.seek(0)
                
                # 4. Push the archive to Docker
                self._container.put_archive(target_dir, tar_stream)
                responses.append(FileUploadResponse(path=file_path))
                
            except Exception:
                # The deepagents protocol handles partial batch failures via the error field
                responses.append(FileUploadResponse(path=file_path, error="permission_denied"))
                
        return responses

    def download_files(self, paths: list[str]) -> list[FileDownloadResponse]:
        """Reads files from the container and returns them as raw bytes."""
        responses = []
        for file_path in paths:
            try:
                target_path = os.path.join(self._work_dir, file_path.lstrip("/"))
                
                # 1. Request the file archive from Docker
                stream, stat = self._container.get_archive(target_path)
                
                # 2. Read the byte stream into memory
                file_stream = io.BytesIO()
                for chunk in stream:
                    file_stream.write(chunk)
                file_stream.seek(0)
                
                # 3. Extract the actual file bytes from the tar wrapper
                with tarfile.open(fileobj=file_stream, mode='r') as tar:
                    member = tar.getmembers()[0]
                    extracted_f = tar.extractfile(member)
                    content = extracted_f.read() if extracted_f else b""
                    
                responses.append(FileDownloadResponse(path=file_path, content=content))
                
            except Exception:
                responses.append(FileDownloadResponse(path=file_path, error="file_not_found"))
                
        return responses