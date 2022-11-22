import pandas as pd
import requests
import json

# Funções auxiliares para extração da base pokemons
def get_info_pokemon(name_pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{name_pokemon}"
    print(url)
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def get_habilidades_pokemon(info_pokemon):
    habilidade_pokemon = []
    habilidades = info_pokemon['abilities']
    for hab in habilidades:
        habilidade_pokemon.append(hab['ability']['name'])
    return ';'.join(habilidade_pokemon)


def get_tipo_pokemon(info_pokemon):
    tipo_pokemon = []
    tipos = info_pokemon['types']
    for tipo in tipos:
        tipo_pokemon.append(tipo['type']['name'])
    return ';'.join(tipo_pokemon)


def get_stat_pokemon(info_pokemon, poke_stat):
    hp = []
    stats_pokemon = info_pokemon['stats']
    for stat in stats_pokemon:
        if stat['stat']['name'] == poke_stat:
            return stat['base_stat']


def get_localizacao_pokemon(info_pokemon):
    url_localizacao = info_pokemon['location_area_encounters']
    response = requests.get(url_localizacao)
    data = json.loads(response.text)
    if data == []:
        return 'unknow'
    else:
        return data[0]['location_area']['name']


def main():
    print("ETL Base Pokemons...")

    # estrutura da base pokemons - colunas que vamos popular com dados vindos da API
    base_pokemon = {
        "nome": [],
        "habilidades": [],
        "local": [],
        "tipo": [],
        "HP": [],
        "ataque": [],
        "defesa": [],
        "velocidade": []
    }
    # url da API
    url = "https://pokeapi.co/api/v2/pokemon/"

    # API pokemon tem estrutura de páginas, com limite bde pokemons por pag
    # parametro de numero de pokemons por request da API - 10 por chamada
    params = {'limit': 10}

    print("Extração Base Pokemons via pokeapi...")
    # e numero da página  - offset
    for offset in range(0, 150, 10):
        # laço para iterar em cada página com 10 pokemons em cada, até a página 15 --> total de 150 pokemons
        params['offset'] = offset
        response = requests.get(url, params=params)

        # se status code da resposta da API não for sucess(200), print o response
        if response.status_code != 200:
            print(response.text)
        else:
            data = response.json()
            # para cada pokemon em results, vamos pegar as infos deste pokemon e popular a base
            for item in data['results']:

                # nome do pokemon
                pokemon = item['name']
                base_pokemon['nome'].append(pokemon)

                info_pokemon = get_info_pokemon(pokemon)

                # habilidades do pokemon
                habilidade_pokemon = get_habilidades_pokemon(info_pokemon)
                base_pokemon['habilidades'].append(habilidade_pokemon)

                # areas que localizamos o pokemon
                localizacao_pokemon = get_localizacao_pokemon(info_pokemon)
                base_pokemon['local'].append(localizacao_pokemon)

                # tipo do pokemon
                tipo_pokemon = get_tipo_pokemon(info_pokemon)
                base_pokemon['tipo'].append(tipo_pokemon)

                # Stat - HP
                hp_pokemon = get_stat_pokemon(info_pokemon, 'hp')
                base_pokemon['HP'].append(hp_pokemon)

                # Stats - ataque
                ataque_pokemon = get_stat_pokemon(info_pokemon, 'attack')
                base_pokemon['ataque'].append(ataque_pokemon)

                # Stats - defesa
                defesa_pokemon = get_stat_pokemon(info_pokemon, 'defense')
                base_pokemon['defesa'].append(defesa_pokemon)

                # Stats - velocidade
                velocidade_pokemon = get_stat_pokemon(info_pokemon, 'speed')
                base_pokemon['velocidade'].append(velocidade_pokemon)

    # após popular o dicionario com as linhas da base, vamos obter o dataframe da base pokemon
    df_pokemon = pd.DataFrame.from_dict(base_pokemon, orient='index')
    df_pokemon = df_pokemon.transpose()
    print("Extração da base Pokemon Geração 1 - Finalizada")
    print(df_pokemon.head())
    print("Consolidando base em arquivo .csv")
    df_pokemon.to_csv('db_pokemon.csv')

if __name__ == '__main__':
    main()

