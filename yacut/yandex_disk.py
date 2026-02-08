import os
import urllib.parse
import aiohttp


API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
DISK_TOKEN = os.getenv('DISK_TOKEN')


async def upload_file_to_disk(file_data, filename):
    headers = {'Authorization': f'OAuth {DISK_TOKEN}'}

    request_upload_url = f'{API_HOST}{API_VERSION}/disk/resources/upload'
    params = {'path': f'app:/{filename}', 'overwrite': 'True'}  # noqa: E231

    async with aiohttp.ClientSession() as session:
        async with session.get(
            request_upload_url,
            headers=headers,
            params=params
        ) as response:
            upload_data = await response.json()
            upload_url = upload_data['href']

        async with session.put(upload_url, data=file_data) as response:
            location = response.headers['Location']
            location = urllib.parse.unquote(location)
            location = location.replace('/disk', '')

        download_link_url = f'{API_HOST}{API_VERSION}/disk/resources/download'
        params = {'path': location}

        async with session.get(
            download_link_url,
            headers=headers,
            params=params
        ) as response:
            download_data = await response.json()
            return download_data['href']
