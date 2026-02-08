import asyncio
from flask import render_template, url_for
from yacut import app, db
from yacut.forms import FileUploadForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.yandex_disk import upload_file_to_disk


@app.route('/files', methods=['GET', 'POST'])
def files_upload():
    form = FileUploadForm()
    if form.validate_on_submit():
        files = form.files.data
        results = asyncio.run(process_files(files))
        return render_template('files.html', form=form, results=results)
    return render_template('files.html', form=form)


async def process_files(files):
    tasks = []
    for file in files:
        file_data = file.read()
        filename = file.filename
        tasks.append(process_single_file(file_data, filename))
    return await asyncio.gather(*tasks)


async def process_single_file(file_data, filename):
    download_link = await upload_file_to_disk(file_data, filename)
    short_id = get_unique_short_id()
    url_map = URLMap(original=download_link, short=short_id)
    db.session.add(url_map)
    db.session.commit()
    short_link = url_for('index', _external=True) + short_id
    return {'filename': filename, 'short_link': short_link}
