import re
from flask import jsonify, request, url_for
from http import HTTPStatus
from yacut import app, db
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.constants import ALLOWED_CHARS, MAX_SHORT_ID_LENGTH


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'message': 'Отсутствует тело запроса'}), HTTPStatus.BAD_REQUEST
    
    if 'url' not in data:
        return jsonify({'message': '"url" является обязательным полем!'}), HTTPStatus.BAD_REQUEST
    
    custom_id = data.get('custom_id')
    
    if custom_id:
        if len(custom_id) > MAX_SHORT_ID_LENGTH:
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), HTTPStatus.BAD_REQUEST
        
        pattern = f'^[{re.escape(ALLOWED_CHARS)}]+$'
        if not re.match(pattern, custom_id):
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), HTTPStatus.BAD_REQUEST
        
        if URLMap.query.filter_by(short=custom_id).first():
            return jsonify({
                'message': 'Предложенный вариант короткой ссылки уже существует.'
            }), HTTPStatus.BAD_REQUEST
    else:
        custom_id = get_unique_short_id()
    
    url_map = URLMap(original=data['url'], short=custom_id)
    db.session.add(url_map)
    db.session.commit()
    
    return jsonify({
        'url': url_map.original,
        'short_link': url_for('index', _external=True) + url_map.short
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        return jsonify({'message': 'Указанный id не найден'}), HTTPStatus.NOT_FOUND
    return jsonify({'url': url_map.original}), HTTPStatus.OK
