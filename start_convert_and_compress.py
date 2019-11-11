from images_operations.compressor import image_compression

# Просто измени path_to_file на свой
path_to_file = 'img/misha.w/1.jpg'
print(f'[Получил "{path_to_file}"]')
print(f'[Отдал "{image_compression(path_to_file)}"]')
