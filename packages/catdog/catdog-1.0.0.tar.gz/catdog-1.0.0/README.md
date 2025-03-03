# CatDog

Простая библиотека для определения кошек и собак на изображениях.

## Установка

Установка через pip:

    pip install catdog

## Использование

Простой способ:

    import catdog
    result = catdog.predict("path/to/image.jpg")
    print(result)  # "cat" или "dog"

Расширенный способ:

    image = catdog.CatDogImage("path/to/image.jpg")
    print(image.is_cat)  # True/False
    print(image.is_dog)  # True/False
    print(image.confidence)  # Уверенность в процентах
    print(image)  # Полное описание

## Лицензия

MIT
