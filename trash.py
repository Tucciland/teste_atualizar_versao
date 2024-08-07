import firebirdsql as fb
import mysql.connector as my
import datetime as dt
from datetime import timedelta
import schedule
import time
import urllib.request
import os
import shutil

def conectar_banco_gestor():
    db_path = 'C:\\GESTOR\\Dados\\DADOS.FDB'
    user = 'SYSDBA'
    password = 'masterkey'
    host = 'localhost'
    charset = 'ISO8859_1'
    
    conn = fb.connect(user=user, password=password, database=db_path, host=host, charset=charset)
    return conn

def conectar_banco_nuvem():
    host = 'topsoft.info'
    database = 'topsof28_dadosemp'
    user = 'topsof28_dadosemp'
    password = '@dadosemp@2024@'
    port = 3306
    
    conn = my.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    return conn

def existe_registro_nuvem(query, params=None, commit=False):
    conn = conectar_banco_nuvem()
    cur = conn.cursor()
    
    if params is None:
        cur.execute(query)
    elif isinstance(params, tuple):
        cur.execute(query, params)
    else:
        cur.execute(query, (params,))
    
    registro_nuvem = cur.fetchall()

    if commit:
        conn.commit()

    cur.close()
    conn.close()
    return registro_nuvem

def existe_registro_gestor(query, params=None, commit=False):
    conn = conectar_banco_gestor()
    cur = conn.cursor()

    if params is None:
        cur.execute(query)
    elif isinstance(params, tuple):
        cur.execute(query, params)
    else:
        cur.execute(query, (params,))
    
    registro_gestor = cur.fetchall()

    if commit:
        conn.commit()

    cur.close()
    conn.close()
    return registro_gestor

def verifica_versao_nuvem():
    sql_versao = "select ultima_versao from versao"
    versao = existe_registro_nuvem(sql_versao)
    print(versao)
    return versao

def atualiza_versao(ver_atual):
    versao_nuvem = verifica_versao_nuvem()[0][0]  # Ajuste para acessar o valor da tupla retornada

    if ver_atual != versao_nuvem:
        url_versao_nova = 'https://raw.githubusercontent.com/Tucciland/teste_atualizar_versao/main/trash.py'
        destino = r'C:\GESTOR\teste\trash.py'
        pasta_inicializacao = r'C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        novo_arquivo = os.path.join(pasta_inicializacao, 'trash.py')
        
        # Cria a pasta de destino se ela não existir
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        
        # Renomeia o arquivo existente, se houver
        if os.path.exists(destino):
            novo_nome = r'C:\GESTOR\teste\trash{}.py'.format(ver_atual)
            os.rename(destino, novo_nome)
            print(f'Arquivo existente renomeado para: {novo_nome}')
        
        # Baixa o novo arquivo
        urllib.request.urlretrieve(url_versao_nova, destino)
        print(f'Nova versão baixada e salva em: {destino}')
        
        # Move o novo arquivo para a pasta de inicialização
        shutil.move(destino, novo_arquivo)
        print(f'Nova versão movida para: {novo_arquivo}')
    else:
        print('Você já está usando a versão mais recente.')

versao_atual = 1536
atualiza_versao(versao_atual)