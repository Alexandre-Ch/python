"""Extrai a taxa CDI do Banco Central e gera um gráfico em PNG."""

import argparse
import csv
import os
import time
from datetime import datetime
from random import random

import pandas as pd
import requests
import seaborn as sns


URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados"
ARQUIVO_CSV = "taxa-cdi.csv"


def obter_taxa_cdi():
    """Busca a última taxa CDI publicada pela API do Banco Central."""
    resposta = requests.get(URL, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()
    if not dados:
        raise ValueError("A API do Banco Central não retornou dados da série CDI.")
    return float(dados[-1]["valor"])


def extrair_taxa_cdi():
    """Salva dez amostras da taxa CDI no arquivo CSV."""
    taxa_publicada = obter_taxa_cdi()
    arquivo_existe = os.path.exists(ARQUIVO_CSV)

    with open(ARQUIVO_CSV, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        if not arquivo_existe or os.path.getsize(ARQUIVO_CSV) == 0:
            escritor.writerow(["data", "hora", "taxa"])

        for _ in range(10):
            agora = datetime.now()
            data = agora.strftime("%Y/%m/%d")
            hora = agora.strftime("%H:%M:%S")
            taxa = taxa_publicada + (random() - 0.5)
            escritor.writerow([data, hora, taxa])
            time.sleep(1)


def gerar_grafico(nome_grafico):
    """Lê o CSV e salva o gráfico com o nome informado."""
    dados = pd.read_csv(ARQUIVO_CSV)
    grafico = sns.lineplot(data=dados, x="hora", y="taxa")
    grafico.set_title(nome_grafico)
    grafico.tick_params(axis="x", labelrotation=90)
    grafico.get_figure().tight_layout()
    grafico.get_figure().savefig(f"{nome_grafico}.png")


def main():
    parser = argparse.ArgumentParser(
        description="Extrai a taxa CDI e gera um gráfico em PNG."
    )
    parser.add_argument("nome_grafico", help="nome do arquivo e título do gráfico")
    argumentos = parser.parse_args()

    extrair_taxa_cdi()
    gerar_grafico(argumentos.nome_grafico)
    print("Sucesso")


if __name__ == "__main__":
    main()
