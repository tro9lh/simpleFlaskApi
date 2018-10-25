from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from datetime import datetime
from copy import deepcopy


app = FlaskAPI(__name__)

hash_sums = ('8dfe7942aeb0d65782d76726e960baff', # admin:1337Aa
             '899419e103e065a5ca934b9576437f44', # admin:1337Ab
             'ffde69ede2c393fb5a120cd277c25e16') # admin:1337Ac
notes = {
    0: { # меню
        'gam': 12, # актуальная цена за единицу товара
        'cola': 8,
        'cheez': 13
        },
    1: 'build the codez',
    2: 'paint the door',
    3: {'gam':# позиция в меню
                {
                    'count': 3,# количество в заказе
                    'price': 3, # цена за единицу на момент заказа
                    'total_cost': 'здесь будет здесь будет стоимость позиции' # произведение количества на цену
                },
        'cola':
                    {
                        'count': 3,
                        'price': 3,
                        'total_cost': 'здесь будет здесь будет стоимость позиции'
                    },
        'cheez': # позиция в меню
                    {
                        'count': 3,
                        'price': 3,
                        'total_cost': 'здесь будет здесь будет стоимость позиции'
                    },
        'datatime': 'здесь будет дата и время заказа',
        'total_cost': 'здесь будет общая стоимость',
        'restaurant': 2, # номер ресторана
        'operator': 5,  #номер оператора в  ресторане
        'status': 1 # 1 - оплачен и действителен, 0 отменен
        }


}

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'order': notes[key]
    }

def menu_repr():
    return

@app.route("/", methods=['GET', 'POST', 'PUT'])
def notes_list():

    if request.method == 'POST': # при POST запросе необходимо передать строку, в которой через пробел будут указаны числовые передаваемые параметры и токен кассы : "text":"1 2 3 4 5 6 ffde69ede2c393fb5a120cd277c25e16"
        note = str(request.data.get('text',''))
        args_list = note.split(' ')
        if args_list[6] in hash_sums:
            idx = max(notes.keys()) + 1
            notes[idx] = deepcopy(notes[3])
            notes[idx]['gam']['count'] = int(args_list[0])
            notes[idx]['cola']['count'] = int(args_list[1])
            notes[idx]['cheez']['count'] = int(args_list[2])
            notes[idx]['gam']['price'] = notes[0]['gam']
            notes[idx]['cola']['price'] = notes[0]['cola']
            notes[idx]['cheez']['price'] = notes[0]['cheez']
            notes[idx]['gam']['total_cost'] = (notes[idx]['gam']['count']) * (notes[idx]['gam']['price'])
            notes[idx]['cola']['total_cost'] = (notes[idx]['cola']['count']) * (notes[idx]['cola']['price'])
            notes[idx]['cheez']['total_cost'] = (notes[idx]['cheez']['count']) * (notes[idx]['cheez']['price'])
            notes[idx]['datatime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            notes[idx]['total_cost'] = (notes[idx]['gam']['total_cost']) + (notes[idx]['cola']['total_cost']) + (notes[idx]['cheez']['total_cost'])
            notes[idx]['restaurant'] = int(args_list[3])
            notes[idx]['operator'] = int(args_list[4])
            notes[idx]['status'] = int(args_list[5])


            return note_repr(idx), status.HTTP_201_CREATED
        else:
            return status.HTTP_403_FORBIDDEN


    elif request.method == 'PUT': # при выполнении метода PUT выполняется изменение цен в меню
        note = str(request.data.get('text',''))
        args_list = note.split(' ')
        notes[0]['gam'] = int(args_list[0])
        notes[0]['cola'] = int(args_list[1])
        notes[0]['cheez'] = int(args_list[2])
        return notes[0]

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]



@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):

    if request.method == 'PUT':
        """
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)
        """
        note = str(request.data.get('text',''))
        args_list = note.split(' ')
        if args_list[6] in hash_sums:
            idx = key
            notes[idx]['gam']['count'] = int(args_list[0])
            notes[idx]['cola']['count'] = int(args_list[1])
            notes[idx]['cheez']['count'] = int(args_list[2])
            notes[idx]['gam']['price'] = notes[0]['gam']
            notes[idx]['cola']['price'] = notes[0]['cola']
            notes[idx]['cheez']['price'] = notes[0]['cheez']
            notes[idx]['gam']['total_cost'] = (notes[idx]['gam']['count']) * (notes[idx]['gam']['price'])
            notes[idx]['cola']['total_cost'] = (notes[idx]['cola']['count']) * (notes[idx]['cola']['price'])
            notes[idx]['cheez']['total_cost'] = (notes[idx]['cheez']['count']) * (notes[idx]['cheez']['price'])
            notes[idx]['datatime'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            notes[idx]['total_cost'] = (notes[idx]['gam']['total_cost']) + (notes[idx]['cola']['total_cost']) + (notes[idx]['cheez']['total_cost'])
            notes[idx]['restaurant'] = int(args_list[3])
            notes[idx]['operator'] = int(args_list[4])
            notes[idx]['status'] = int(args_list[5])


            return note_repr(idx)
        else:
            return status.HTTP_403_FORBIDDEN    
    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)



if __name__ == "__main__":
    app.run(debug=True)
