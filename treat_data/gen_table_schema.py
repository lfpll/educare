import pandas as pd

file_path = r'/home/luizfernandolobo/PycharmProjects/download_zips/files/Censo Escolar/2017 (Atualizado em 02/ANEXOS/ANEXO I - Dicionário de Dados e Tabelas Auxiliares/Tabela de Docente.csv'

pd.read_csv(file_path,delimiter='|')