from application.app import app

import argparse

def saudacao(nome):
    print(f"Olá, {nome}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Um simples script de saudação')
    parser.add_argument("nome", help="O nome da pessoa a ser saudada")
    args = parser.parse_args()
    saudacao(args.nome)