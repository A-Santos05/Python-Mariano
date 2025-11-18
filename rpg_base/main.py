from __future__ import annotations
from jogo import Jogo

def menu() -> None:
    """Menu principal do aplicativo."""
    jogo = Jogo()
    while True:
        print("\n=== RPG OO — Menu Principal ===")
        print("[1] Criar personagem")
        print("[2] Encarar missão")
        print("[3] Salvar")
        print("[4] Carregar")
        print("[5] Ver atributos dos personagens")
        print("[6] Abrir Inventário")
        print("[7] Exibir status do personagem")
        print("[0] Sair")
        op = input("> ").strip()

        if op == "1":
            jogo.menu_criar_personagem()
        elif op == "2":
            jogo.menu_missao()
        elif op == "3":
            jogo.menu_salvar()
        elif op == "4":
            jogo.menu_carregar()
        elif op == "5":
            jogo.menu_atributos_personagem()
        elif op == "6": 
            jogo.menu_inventario()
        elif op == "7":
            jogo.mostrar_status_personagem()
        elif op == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()