
# PhotoTextSearcher

Библиотека для распознавания текста на изображениях с помощью Tesseract OCR.

## Установка

Для установки библиотеки требуется Python версии 3.9 или выше.

Установите библиотеку с помощью pip:

```bash
pip install PhotoTextSearcher
```

И всё готово!

## Пример использования

Вот пример того, как можно использовать библиотеку для распознавания текста на изображении:

```python
from PhotoTextSearcher import TextRecognizer

recognizer = TextRecognizer()
text = recognizer.recognize_text("example.jpg")
print("📜 Распознанный текст:\n", text)

```

## Зависимости

- `easyocr`
- `Pillow`
- `numpy`

Эти библиотеки автоматически установятся при установке `PhotoTextSearcher`.

## Лицензия

Этот проект лицензирован под лицензией MIT. См. файл LICENSE для подробностей.
