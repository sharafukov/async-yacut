import re
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from yacut.constants import ALLOWED_CHARS, MAX_SHORT_ID_LENGTH
from yacut.models import URLMap


def validate_custom_id(form, field):
    if field.data:
        if field.data == 'files':
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        pattern = f'^[{re.escape(ALLOWED_CHARS)}]+$'
        if not re.match(pattern, field.data):
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=MAX_SHORT_ID_LENGTH),
            validate_custom_id
        ]
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Обязательное поле')]
    )
    submit = SubmitField('Загрузить')
