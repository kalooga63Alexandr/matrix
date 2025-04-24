import aiohttp
import asyncio


async def get_matrix(url):
    """
    Асинхронно загружает матрицу с указанного URL и возвращает её в виде плоского списка,
    обрабатывая возможные ошибки сервера и сети.

    Аргументы:
        url (str): Полный URL, куда отправляется запрос.

    Возвращает:
        list[int]: Сплошной список элементов матрицы или пустой список при ошибке.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                # Проверка успешности ответа (статус-код менее 400)
                if resp.status >= 400:
                    error_message = f"Сервер ответил с ошибкой ({resp.status})"
                    if resp.status >= 500:
                        error_message += ": проблема на стороне сервера."
                    elif resp.status == 404:
                        error_message += ": страница не найдена."
                    else:
                        error_message += ": проверьте URL или доступ."

                    print(error_message)
                    return []

                # Читаем тело ответа как строку
                elements = await resp.text()

                # Разбиваем строку на отдельные элементы (используя пробелы или запятые)
                elements = elements.replace(
                    '+-----+-----+-----+-----+', '').split('\n')

                # Конвертируем каждую строку элемента в целое число создаём список.
                matrix = []

                for nt in elements:
                    result = nt.split('|')
                    if not result == ['']:
                        matrix_flat = []
                        for r in result:
                            if r != '':
                                matrix_flat.append(int(r))
                        matrix.append(matrix_flat)

                # Обход в нужной последовательности.
                if not matrix:
                    return []

                result = []
                top, bottom = 0, len(matrix) - 1
                left, right = 0, len(matrix[0]) - 1
                while top <= bottom and left <= right:

                    if left <= right:
                        # Обход левого столбца (сверху вниз)
                        for i in range(top, bottom + 1):
                            result.append(matrix[i][left])
                        left += 1

                        # Обход нижней строки
                        for i in range(left, right + 1):
                            result.append(matrix[bottom][i])
                        bottom -= 1

                    if top <= bottom:
                        # Обход правого столбца (снизу вверх)
                        for i in range(bottom, top - 1, -1):
                            result.append(matrix[i][right])
                        right -= 1

                    if left <= right:
                        # Обход верхней строки
                        for i in range(right, left - 1, -1):
                            result.append(matrix[top][i])
                        top += 1

                return result

        except aiohttp.ClientConnectorError as conn_err:
            print(
                f"Ошибка соединения с сервером: {conn_err}. Возможно, сервер недоступен.")
            return []
        except aiohttp.ServerTimeoutError as timeout_err:
            print(f"Тайм-аут соединения: {timeout_err}. Попробуйте позже.")
            return []
        except aiohttp.ContentTypeError as content_type_err:
            print(
                f"Сервер вернул некорректный контент: {content_type_err}. Проверьте URL.")
            return []
        except Exception as general_err:
            print(f"Возникла непредвиденная ошибка: {general_err}.")
            return []


async def get_matrix():
    url = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
    result = await get_matrix(url)

asyncio.run(get_matrix())
