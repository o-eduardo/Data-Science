import mysql.connector
import pandas as pd
from re import sub


def snake_case(s):
    # método para converter string em Snake case
    return '_'.join(sub('([A-Z][a-z]+)', r' \1', sub('([A-Z]+)', r' \1', s.replace('-', ' '))).split()).lower()


def main():
    print("Conectando com MySQL...")

    # biblioteca mysql.connector permite conexão ao host MySQL
    conn_csgo = mysql.connector.connect(
        host="atmo-db.cncfsgdjnfjz.sa-east-1.rds.amazonaws.com",
        user="candidato",
        password="analista_atmo",
        database="CSGO"
    )
    print(conn_csgo)

    # Criando cursor para obter as bases
    cur_csgo = conn_csgo.cursor()

    # Exibindo as tabelas da database CSGO
    cur_csgo.execute("Show tables;")

    # Print dos nomes das tabelas de Database CSGO
    print(f"Tabelas de Database CSGO")
    tabelas_cs_go = cur_csgo.fetchall()
    for tabela in tabelas_cs_go:
        print(tabela[0])

    # Rodando os selects em cada uma das tabelas de Database CSGO
    print("Rodando os Selects nas tabelas de Database CSGO")
    tb_players = pd.read_sql("SELECT * FROM tb_players", conn_csgo)
    tb_players_medalha = pd.read_sql("SELECT * FROM tb_players_medalha", conn_csgo)
    tb_medalha = pd.read_sql("SELECT * FROM tb_medalha", conn_csgo)
    tb_lobby_stats_player = pd.read_sql("SELECT * FROM tb_lobby_stats_player", conn_csgo)

    # Ajustando nomes das colunas das tabelas para snake case
    print("Ajustando nomes das colunas das tabelas da base em Snake case")
    db_cs_go = [tb_players, tb_players_medalha, tb_medalha, tb_lobby_stats_player]

    for tabela in db_cs_go:
        colunas_tabela = tabela.columns.to_list()
        for coluna in colunas_tabela:
            coluna_snake_case = snake_case(coluna)
            tabela.rename(columns={coluna: coluna_snake_case}, inplace=True)

    print("dataframe tb_players")
    print(tb_players.head())
    print("dataframe tb_players_medalha")
    print(tb_players_medalha.head())
    print("dataframe tb_medalha")
    print(tb_medalha.head())
    print("dataframe tb_lobby_stats_player")
    print(tb_lobby_stats_player.head())

if __name__ == '__main__':
    main()

