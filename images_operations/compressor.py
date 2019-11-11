from PIL import Image
import os
import shutil

MEDIA_ROOT = '/Users/misha/Desktop/'


# Дебагер
def debug(var, text=''):
    if not text == '':
        text += ' >>> '
    import inspect
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    variable_name = [var_name for var_name,
                                  var_val in callers_local_vars if var_val is var]
    print(f'{text}{variable_name} = {var}')


# /Дебагер

# Пути
def get_file_path(path_to_file):
    return MEDIA_ROOT + path_to_file


def get_new_file_path(file_path):
    path = file_path.rsplit('/', 1)[0]
    file = file_path.rsplit('/', 1)[1]
    file_name = file.rsplit('.', 1)[0]
    file_path = f'{path}/{file_name}.jpg'
    return file_path


def get_new_path_to_file(path_to_file):
    return get_new_file_path(path_to_file)


# /Пути
# Удаление


def delete_file(file_path):
    try:
        os.remove(file_path)
        debug(file_path, 'Удаляю как файл')
    except PermissionError:
        shutil.rmtree(file_path)
        debug(file_path, 'Удаляю как папку')


def delete_if_not_jpg(file_path):
    file = file_path.rsplit('/', 1)[1]
    if not file.endswith('jpg'):
        delete_file(file_path)


# /Удаление

# Конвертор


def convert_file(file, file_path):
    file.convert('RGB').save(file_path)


def get_jpg_file_or_false(file_path):
    try:
        file = Image.open(file_path)
        debug(file_path, 'Открыл файл')
        debug(file, 'Файл')

        new_file_path = get_new_file_path(file.filename)

        debug(new_file_path, f'Собираюсь конвертировать {file.filename}')
        convert_file(file, new_file_path)
        debug(new_file_path, f'Сконвертировал файл {file.filename}')

        debug(file_path, 'Собираюсь удалить')
        delete_if_not_jpg(file_path)
        debug(file_path, 'Удалил')

        debug(new_file_path, 'Открываю новый файл')
        jpg_file = Image.open(new_file_path)
        debug(new_file_path, 'Открыл новый файл')
        debug(jpg_file)
        return jpg_file
    except:
        delete_file(file_path)
        return False


# /Конвертор
# Кроп
def resize_image(file, width, height):
    w, h = file.size
    print(f'[CROP] original w={w} h={h}')

    resized_image = file.resize((width, height))

    w, h = resized_image.size
    print(f'[CROP] resized w={w} h={h}')

    resized_image.save(file.filename)


def scale_image(file, width, height):
    w, h = file.size

    print(f'[CROP] original w={w} h={h}')

    file.thumbnail((width, height), Image.ANTIALIAS)

    w, h = file.size
    print(f'[CROP] scaled w={w} h={h}')

    file.save(file.filename)


def scale_or_resize(file, width, height):
    w, h = file.size
    if w < h:
        print('[ИЗОБРАЖЕНИЕ ВЕРТИКАЛЬНОЕ]')
        resize_image(file, width, height)
    elif w >= h:
        print('[ИЗОБРАЖЕНИЕ ГОРИЗОНТАЛЬНОЕ]')
        scale_image(file, width, height)
    file = Image.open(file.filename)
    return file


# /Кроп

def image_compression(path_to_file):
    file_path = get_file_path(path_to_file)
    debug(file_path, '[START]')
    file = get_jpg_file_or_false(file_path)
    debug(file, 'Получил из get_jpg_file_or_false')
    if file:
        file = scale_or_resize(file, width=800, height=800)
        file.save(file.filename, quality=70)
        debug(file.filename, 'Сжал')
        new_path_to_file = get_new_path_to_file(path_to_file)
        debug(new_path_to_file)
        return new_path_to_file
    debug(file_path, '[BAD FILE]')
