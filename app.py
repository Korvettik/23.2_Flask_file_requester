import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
# проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
# с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
# вернуть пользователю сформированный результат


# http://127.0.0.1:25000/perform_query?cmd1=1&value1=1&cmd2=2&value2=2&file_name=apache_logs.txt
@app.route("/perform_query", methods=['GET', 'POST'])
def perform_query():
    cmd1 = request.args.get('cmd1')
    value1 = request.args.get('value1')
    cmd2 = request.args.get('cmd2')
    value2 = request.args.get('value2')
    file_name = request.args.get('file_name')

    if None in [cmd1, value1]:
        return "Введите значения параметров cmd1, value1, cmd2, value2", 400
    try:
        # print(DATA_DIR + '/' + file_name)
        with open(DATA_DIR + '/' + file_name, 'r') as file:
            data = file.readlines()
    except Exception:
        return f'Файл {file_name} не был найден', 400

    # return app.response_class('', content_type="text/plain")
    # return 'Привет!'


    # filter, map, unique, sort, limit

    with open(DATA_DIR + '/' + file_name, 'r') as file:
        data = [x for x in file.readlines()]
        # print(data[:2])
        res = func_response(cmd1, value1, data)
        # print(type(res))
        if cmd2 and value2:
            res = func_response(cmd2, value2, res)
            # print(type(res))
        res = "\n".join(res)
    return app.response_class(res, content_type="text/plain")


def func_response(cmd, value, data):
    if cmd == 'filter':   # выбираем те строки, где встречается value
        res = filter(lambda x: value in x, data)
        return res
    elif cmd == 'map':   # делим строку в список по пробелам. Выводим нужный индекс каждой строки - как бы колонку
        value = int(value)
        res = [x.split()[value] for x in data]
        return res
    elif cmd == 'unique':   # множество исключает одинаковые строки
        return list(set(data))
    elif cmd == 'sort':   # сортируем список строк.
        if value == "desc":
            reverse = value
            return sorted(data, reverse=reverse)
    elif cmd == 'limit':   # ограничиваем показ списка строк срезом от 0 и "до"
        value = int(value)
        return list(data)[:value]
    else:
        return "Нет такой команды"





if __name__ == '__main__':
    app.run(host="127.0.0.1", port=25000, debug=True)
