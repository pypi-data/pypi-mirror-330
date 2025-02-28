from datetime import datetime
from enum import Enum
import time
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union
import aiofiles



SUPPORTED_FILE_TYPES = ["pdf"]


MAX_INDEX_BUILD_TIMEOUT_SECS = 3600
INDEXES_LIMIT = 50


class IndexStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class AnalysisLevel(str, Enum):
    LIGHT = "min"
    MAX = "max"


class Source(TypedDict):
    uid: str
    display_name: str
    value: Dict[str, Any]
    file_hash: Optional[str]
    gcs_path: Optional[str] = None
    user_id: Optional[int] = None
    status: str
    created_at: str
    updated_at: str
    doc_type: str


class Index(TypedDict):
    uid: str
    name: str
    status: str
    created_at: str
    updated_at: str


class IndexWithSources(Index):
    sources: List[Source] = []


class IndexCursor(TypedDict):
    before_created_at: datetime


class GetIndexesCursor(TypedDict):
    before_created_at: Union[datetime, None]


class GetIndexesResponse(TypedDict):
    indexes: List[IndexWithSources]
    next: GetIndexesCursor


class AddSourcesResponse(TypedDict):
    index: Index
    sources_added: List[Source]


class GenerateSignedUrlResponse(TypedDict):
    document: Source
    signed_url: str


class Indexes:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def create(self, name: str):
        response = self.client.post(
            f"{self.base_url}/public/v1/indexes", json={"name": name.strip()}
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return Index(**response_json.get("index"))

    def list(self, next: IndexCursor = None, limit: int = INDEXES_LIMIT):
        params = {}
        if next is not None:
            params["before_created_at"] = next["before_created_at"]
        if limit is not None:
            params["limit"] = limit

        response = self.client.get(f"{self.base_url}/public/v1/indexes", params=params)
        response.raise_for_status()

        indexes_response = GetIndexesResponse(**response.json())
        return indexes_response["indexes"], indexes_response["next"]

    def get(self, index_uid: str):
        response = self.client.get(f"{self.base_url}/public/v1/indexes/{index_uid}")
        response.raise_for_status()

        response_json = response.json() or {}
        return IndexWithSources(**response_json.get("index"))

    def add_urls(
        self,
        urls: List[str],
        index_uid: str,
        analysis_level: AnalysisLevel = AnalysisLevel.LIGHT,
    ):
        response = self.client.post(
            f"{self.base_url}/public/v1/indexes/{index_uid}/urls",
            json={"urls": urls, "analysis_level": analysis_level},
        )
        response.raise_for_status()
        response = AddSourcesResponse(**response.json())
        if not response.get("sources_added"):
            raise ValueError("No sources were created from the provided URLs")

        return response["sources_added"]

    def add_documents(
        self,
        files: List[Path],
        index_uid: str,
        analysis_level: AnalysisLevel = AnalysisLevel.LIGHT,
    ):
        sources_added = []

        # Handle both files and directories
        all_files = []
        for file in files:
            if file.is_dir():
                for file_type in SUPPORTED_FILE_TYPES:
                    all_files.extend(file.glob(f"*.{file_type}"))
            else:
                all_files.append(file)

        sources_added = []
        for file in all_files:
            filename = file.name
            filestream = file.open("rb")

            # Get signed URL for upload
            response = self._generate_signed_url(filename)
            sources_added.append(response["document"])

            # Upload file using signed URL
            upload_response = self.client.put(
                response["signed_url"],
                data=filestream,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()
            filestream.close()

            # Add to index
            response = self.client.post(
                f"{self.base_url}/public/v1/indexes/{index_uid}/documents",
                json={
                    "document_uid": response["document"]["uid"],
                    "analysis_level": analysis_level,
                },
            )
            response.raise_for_status()
            response = AddSourcesResponse(**response.json())
            sources_added += response["sources_added"]

        return sources_added

    def build(self, index_uid: str, wait=False):
        """Build the reasoning index."""
        response = self.client.post(
            f"{self.base_url}/public/v1/indexes/{index_uid}/build"
        )
        response.raise_for_status()
        response_json = response.json() or {}

        if wait:
            return self._poll_for_index_build(index_uid)
        else:
            return response_json

    def get_status(self, batch_uid: str):
        response = self.client.get(f"{self.base_url}/public/v1/indexes/{batch_uid}")
        response.raise_for_status()

        response_json = response.json() or {}
        return response_json.get("index")

    def delete(self, index_uid: str):
        response = self.client.delete(f"{self.base_url}/public/v1/indexes/{index_uid}")
        response.raise_for_status()

    def _generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = self.client.post(
            f"{self.base_url}/public/v1/documents/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())

    def _poll_for_index_build(self, index_uid: str):
        # Poll until index is successfully built
        start_time = time.time()
        while True:
            response_json = self.get_status(index_uid)
            status = response_json.get("status")

            if status == IndexStatus.SUCCESS.value:
                return response_json
            elif status == IndexStatus.FAILED.value:
                raise ValueError("Index build failed")

            if time.time() - start_time > MAX_INDEX_BUILD_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Index build timed out after {MAX_INDEX_BUILD_TIMEOUT_SECS}s"
                )

            time.sleep(5)


class IndexesAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def create(self, name: str):
        response = await self.client.post(
            f"{self.base_url}/public/v1/indexes", json={"name": name.strip()}
        )
        response.raise_for_status()
        response_json = response.json() or {}
        return Index(**response_json.get("index"))

    async def list(self, next: IndexCursor = None, limit: int = INDEXES_LIMIT):
        params = {}
        if next is not None:
            params["before_created_at"] = next["before_created_at"]
        if limit is not None:
            params["limit"] = limit

        response = await self.client.get(
            f"{self.base_url}/public/v1/indexes", params=params
        )
        response.raise_for_status()

        indexes_response = GetIndexesResponse(**response.json())
        return indexes_response["indexes"], indexes_response["next"]

    async def get(self, index_uid: str):
        response = await self.client.get(
            f"{self.base_url}/public/v1/indexes/{index_uid}"
        )
        response.raise_for_status()

        response_json = response.json() or {}
        return IndexWithSources(**response_json.get("index"))

    async def add_urls(
        self,
        urls: List[str],
        index_uid: str,
        analysis_level: AnalysisLevel = AnalysisLevel.LIGHT,
    ):
        response = await self.client.post(
            f"{self.base_url}/public/v1/indexes/{index_uid}/urls",
            json={"urls": urls, "analysis_level": analysis_level},
        )
        response.raise_for_status()
        response = AddSourcesResponse(**response.json())
        if not response["sources_added"]:
            raise ValueError("No sources were created from the provided URLs")

        return response["sources_added"]

    async def add_documents(
        self,
        files: List[Path],
        index_uid: str,
        analysis_level: AnalysisLevel = AnalysisLevel.LIGHT,
    ):
        sources_added = []

        # Handle both files and directories
        all_files = []
        for file in files:
            if file.is_dir():
                for file_type in SUPPORTED_FILE_TYPES:
                    all_files.extend(file.glob(f"*.{file_type}"))
            else:
                all_files.append(file)

        sources_added = []
        for file in all_files:
            filename = file.name

            # Get signed URL for upload
            response = await self._generate_signed_url(filename)
            sources_added.append(response["document"])

            # Read file asynchronously
            async with aiofiles.open(file, mode="rb") as filestream:
                file_content = await filestream.read()

            # Upload file using signed URL
            upload_response = await self.client.put(
                response["signed_url"],
                content=file_content,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()

            # Add to index
            response = await self.client.post(
                f"{self.base_url}/public/v1/indexes/{index_uid}/documents",
                json={
                    "document_uid": response["document"]["uid"],
                    "analysis_level": analysis_level,
                },
            )
            response.raise_for_status()
            response = AddSourcesResponse(**response.json())
            sources_added += response["sources_added"]

        return sources_added

    async def build(self, index_uid: str, wait=False):
        """Build the reasoning index."""
        response = await self.client.post(
            f"{self.base_url}/public/v1/indexes/{index_uid}/build"
        )
        response.raise_for_status()
        response_json = response.json() or {}

        if wait:
            return await self._poll_for_index_build(index_uid)
        else:
            return response_json

    async def get_status(self, batch_uid: str):
        response = await self.client.get(
            f"{self.base_url}/public/v1/indexes/{batch_uid}"
        )
        response.raise_for_status()

        response_json = response.json() or {}
        return response_json.get("index")

    async def delete(self, index_uid: str):
        response = await self.client.delete(
            f"{self.base_url}/public/v1/indexes/{index_uid}"
        )
        response.raise_for_status()

    async def _generate_signed_url(self, filename: str) -> GenerateSignedUrlResponse:
        """Generate a pre-signed URL for file upload."""
        response = await self.client.post(
            f"{self.base_url}/public/v1/documents/presigned-url",
            params={"filename": filename},
        )
        response.raise_for_status()
        return GenerateSignedUrlResponse(**response.json())

    async def _poll_for_index_build(self, index_uid: str):
        # Poll until index is successfully built
        start_time = time.time()
        while True:
            response_json = await self.get_status(index_uid)
            status = response_json.get("status")

            if status == IndexStatus.SUCCESS.value:
                return response_json
            elif status == IndexStatus.FAILED.value:
                raise ValueError("Index build failed")

            if time.time() - start_time > MAX_INDEX_BUILD_TIMEOUT_SECS:
                raise TimeoutError(
                    f"Index build timed out after {MAX_INDEX_BUILD_TIMEOUT_SECS}s"
                )

            await asyncio.sleep(5)
