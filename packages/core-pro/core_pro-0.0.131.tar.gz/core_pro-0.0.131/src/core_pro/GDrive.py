import io
import polars as pl
import mimetypes
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path
from time import perf_counter
from rich import print
from tqdm.auto import tqdm
from .config import GoogleAuthentication


class Drive(GoogleAuthentication):
    def __init__(self, debug: bool = True):
        super().__init__('drive')
        self.debug = debug
        self.status = '[orange]🦑 Drive[/orange]'

    def _progress_bar(self, request, file_size, mode: str = 'Downloading'):
        pbar = tqdm(
            total=file_size,
            desc=f'Drive {mode} - {file_size:,.0f}MB',
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        )
        response = None
        while not response:
            status, response = request.next_chunk()
            if status:
                pbar.update(status.resumable_progress - pbar.n)
        pbar.close()
        return response

    def upload_file(self, file_dir: Path | str, folder_id: str, name_on_drive: str = None) -> dict:
        # config
        start = perf_counter()
        if isinstance(file_dir, str):
            file_dir = Path(file_dir).resolve()
        file_size = file_dir.stat().st_size / (1024 ** 2)
        name_on_drive = name_on_drive or file_dir.name
        # media
        content_type, _ = mimetypes.guess_type(str(file_dir))
        media = MediaFileUpload(
            str(file_dir),
            mimetype=content_type,
            resumable=True,
            chunksize=1024 ** 2  # 1MB chunks for optimal performance
        )
        # request
        body = {
            'name': name_on_drive,
            'parents': [folder_id]
        }
        request = self.service.files().create(
            body=body,
            media_body=media,
            fields='id,webContentLink,webViewLink',
            supportsAllDrives=True
        )
        # progress
        response = self._progress_bar(request, file_size, 'Uploading')
        return {
            'file_id': response['id'],
            'web_link': response.get('webContentLink'),
            'view_link': response.get('webViewLink'),
            'size_mb': file_size,
            'path': file_dir,
            'upload_time': perf_counter() - start
        }

    def get_file_info(self, file_id: str):
        return self.service.files().get(
            fileId=file_id,
            fields='id,name,mimeType,kind,size,fileExtension',
            supportsAllDrives=True
        ).execute()

    def download_file(self, file_id: str, download_dir: str | Path) -> dict:
        # config
        start = perf_counter()
        file_info = self.get_file_info(file_id)
        file_size = float(file_info['size']) / (1024 ** 2)
        save_path = Path(f"{download_dir}/{file_info['name']}")
        # check exist
        if save_path.exists():
            print(
                f"{self.status} File already exists\n"
                f"Path: {save_path.parent} \n"
                f"File name: {save_path.name}\n"
            )
            return {
                'path': save_path,
                'size_mb': file_size,
                'download_time': 0,
                'status': 'skipped'
            }
        # download
        request = self.service.files().get_media(fileId=file_id)
        with io.FileIO(str(save_path), 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            if self.debug:
                print(
                    f"{self.status} Download:\n"
                    f"File id: {file_id} \n"
                    f"Path: {save_path.parent} \n"
                    f"File name: {save_path.name}\n"
                    f"Size: {file_size:,.0f}MB"
                )
            # progress
            self._progress_bar(request=downloader, file_size=file_size, mode='Downloading')

        return {
            'path': save_path,
            'size_mb': file_size,
            'download_time': perf_counter() - start,
            'status': 'completed'
        }

    def create_new_folder(
            self,
            name: str,
            parent_id=None
    ):
        """
        create new folder on Google Drive
        :param name: Name of folder
        :param parent_id: id of parent folder , default None
        :return: return folder id if True
        """

        body = {
            'name': name,
            'parents': [parent_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if not parent_id:
            body.pop('parents')
        file = self.service.files().create(body=body, fields='id', supportsAllDrives=True).execute()
        print(
            f"{self.status} Successfully created folder: {name}\n"
            f"Folder ID: {file.get('id')}"
        )
        return file.get('id')

    def rename_file(self, file_id: str, new_name: str):
        file = {'name': new_name}
        self.service.files().update(fileId=file_id, body=file).execute()

    def remove_file(self, file_id: str, move_to_trash: bool = True):
        if move_to_trash:
            body_value = {'trashed': True}
            resp = self.service.files().update(fileId=file_id, body=body_value, supportsAllDrives=True).execute()
        else:
            resp = self.service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        print(f"{self.status} Remove: {file_id} Trash: {move_to_trash}")
        return resp

    def empty_trash(self):
        resp = self.service.files().emptyTrash().execute()
        print(f"{self.status} Empty trash")
        return resp

    def download_gsheet(self, file_id, file_location, file_name, file_type):
        request = self.service.files().export_media(fileId=file_id, mimeType=file_type)
        fh = io.FileIO(file_location + file_name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

    def search_files(self, folder_id: str):
        fields = 'nextPageToken, files(id, name, createdTime, modifiedTime)'
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query, fields=fields, includeItemsFromAllDrives=True, supportsAllDrives=True
        ).execute()
        return results.get('files', [])

    def share_file(
            self,
            file_id,
            email: str = None,
            role: str = 'reader',
            domain: str = '@shopee.com'
    ):
        """
        :param file_id: abc
        :param email: abc@example.com
        :param role: reader/writer
        :param domain: @example.com
        :return: text
        """
        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f"Request_Id: {request_id}")
                print(f'Permission Id: {response.get("id")}')
                ids.append(response.get("id"))

        ids = []
        batch = self.service.new_batch_http_request(callback=callback)
        if email:
            body = {
                "type": "user",
                "role": role,
                "emailAddress": email,
            }
            batch.add(self.service.permissions().create(fileId=file_id, body=body, fields="id", supportsAllDrives=True))
        else:
            body = {
                "type": "domain",
                "role": role,
                "domain": domain,
            }
            batch.add(self.service.permissions().create(fileId=file_id, body=body, fields="id"))
        batch.execute()
        print(f"{self.status} Shared {body['type']} {body.get('emailAddress', 'domain')}: {file_id}")

    def remove_share_publicly(self, file_id: str):
        body = 'anyoneWithLink'
        self.service.permissions().delete(fileId=file_id, permissionId=body, fields='id', supportsAllDrives=True).execute()
        print(f"{self.status} Removed sharing: {file_id}")

    def remove_duplicates(self, file_id: str):
        lst = self.search_files(file_id)
        all_files = (
            pl.DataFrame(lst)
            .with_columns(
                pl.col(i).str.strptime(pl.Datetime, strict=False)
                for i in ['createdTime', 'modifiedTime']
            )
            .sort(['name', 'createdTime'], descending=True)
            .with_columns(
                pl.col('createdTime').rank(method='max', descending=True).over('name').alias('rank')
            )
            .to_dicts()
        )
        for f in all_files:
            if f['rank'] != 1:
                Drive().remove_file(f['id'])
