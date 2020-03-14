import json
import os
import pprint
import requests
import sys

def api(handler, context):
    with open('database.json', 'r') as json_file:
        data = json.load(json_file)

    health_secretary_data = get_data_from_health_secretary()

    data['data']['brazil']['latest']['cases'] = health_secretary_data.get('total_cases')
    data['data']['brazil']['states'] = health_secretary_data.get('states')
    data['meta']['last_update'] = health_secretary_data.get('last_update')
    

    return {
            "statusCode": 200,
            "body": json.dumps(data),
            "headers": {
                "Access-Control-Allow-Origin": "*"
            }
        }



def get_data_from_health_secretary():


    def get_states():
        return {
            11 : {'state': 'Rondonia', 'UF': 'RO'},
            12 : {'state': 'Acre', 'UF': 'AC'},
            13 : {'state': 'Amazonas', 'UF': 'AM'},
            14 : {'state': 'Roraima', 'UF': 'RR'},
            15 : {'state': 'Pará', 'UF': 'PA'},
            16 : {'state': 'Amapá', 'UF': 'AP'},
            17 : {'state': 'Tocantis', 'UF': 'TO'},
            21 : {'state': 'Maranhão', 'UF': 'MA'},
            22 : {'state': 'Piauí', 'UF': 'PI'},
            23 : {'state': 'Ceará', 'UF': 'CE'},
            24 : {'state': 'Rio Grande do Norte', 'UF': 'RN'},
            25 : {'state': 'Paraíba', 'UF': 'PB'},
            26 : {'state': 'Pernambuco', 'UF': 'PE'},
            27 : {'state': 'Alagoas', 'UF': 'AL'},
            28 : {'state': 'Sergipe', 'UF': 'SE'},
            29 : {'state': 'Bahia', 'UF': 'BA'},
            31 : {'state': 'Minas Gerais', 'UF': 'MG'},
            32 : {'state': 'Espírito Santo', 'UF': 'ES'},
            33 : {'state': 'Rio de Janeiro', 'UF': 'RJ'},
            35 : {'state': 'São Paulo', 'UF': 'SP'},
            41 : {'state': 'Paraná', 'UF': 'PR'},
            42 : {'state': 'Santa Catarina', 'UF': 'SC'},
            43 : {'state': 'Rio Grande do Sul', 'UF': 'RS'},
            50 : {'state': 'Mato Grosso do Sul', 'UF': 'MS'},
            51 : {'state': 'Mato Grosso', 'UF': 'MT'},
            52 : {'state': 'Goiás', 'UF': 'GO'},
            53 : {'state': 'Distrito Federal', 'UF': 'DF'}
        }

    r = requests.get('http://plataforma.saude.gov.br/novocoronavirus/resources/scripts/database.js?v=1584112990');

    if not r.status_code == requests.codes.ok:
        return None 

    resp = json.loads(r.text.replace('var database=',''))

    total_numbers = len(resp.get('brazil'))
    official_numbers = resp.get('brazil')

    official_numbers = official_numbers[len(official_numbers) - 1]

    total_cases = 0

    last_update = official_numbers.get('date') + ' ' + official_numbers.get('time')

    states = []

    for data in official_numbers.get('values'):
        total_cases += data.get('cases', 0)
        state = get_states()
        state = state.get(data.get('uid'))
        state['cases'] = data.get('cases')
        states.append(state)

    return {
        'total_cases': total_cases,
        'last_update': last_update,
        'states': states
    }




if __name__ == '__main__':
    print(api(None, None))