from __future__ import annotations
from models.base import Atributos
from models.personagem import Personagem
from models.inimigo import Inimigo
from models.missao import Missao, ResultadoMissao
from typing import Any, Dict
import random

class Jogo:
    """
    Estrutura base com menus e submenus completos.
    Implementem a logica do jogo ou persistência real.
    """

    def __init__(self) -> None:
        self.personagem = {
            "nome": None,
            "arquetipo": None,   # ex.: "Guerreiro", "Mago" (placeholder textual)
        }

        self._personagem_obj: Personagem | None = None

        self.missao_config = {
            "dificuldade": "Fácil",  # Fácil | Média | Difícil
            "cenario": "Trilha",     # rótulo ilustrativo
        }
        self._ultimo_save = None
        self._ultimo_load = None

    def _obter_atributos_por_arquetipo(self, arquetipo: str) -> dict[str, Any] | None:
        """Retorna a instância de Atributos e as Taxas de Crescimento para o arquétipo."""
        
        # Mapeamento dos conjuntos de atributos
        mapa_atributos = {
            "Guerreiro":{
                "atributos_base": Atributos(
                    ataque=20, vida=100, defesa=40, 
                    crit_chance=35, crit_dmg=150, 
                    mana=0, mana_pool=30, mana_regen=3, special_cost=25
                ),
                "taxas_crescimento": {
                    "ataque": 2,
                    "vida": 10,
                    "defesa": 3,
                }
            },
            "Mago":{
                "atributos_base": Atributos(
                    ataque=40, vida=100, defesa=5, 
                    crit_chance=10, crit_dmg=200, 
                    mana=0,mana_pool=60, mana_regen=10, special_cost=25
                    ),
                "taxas_crescimento": {
                    "ataque": 4,
                    "vida": 5,
                    "defesa": 2,
                }
            },
            "Arqueiro":{
                "atributos_base": Atributos(
                    ataque=35, vida=100, defesa=8, 
                    crit_chance=25, crit_dmg=120, 
                    mana=0,mana_pool=40, mana_regen=4, special_cost=25
                    ),
                "taxas_crescimento": {
                    "ataque": 6,
                    "vida": 5,
                    "defesa": 1,
                }
            },
        }
        
        # Retorna a instância de Atributos ou None se não encontrado
        return mapa_atributos.get(arquetipo)

    

    def menu_criar_personagem(self) -> None:
        while True:
            print("\n=== Criar Personagem ===")
            print(f"Nome atual: {self.personagem['nome'] or '(não definido)'}")
            print(f"Arquétipo:  {self.personagem['arquetipo'] or '(não definido)'}")
            print("[1] Definir nome")
            print("[2] Escolher arquétipo")
            print("[3] Confirmar criação")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._definir_nome()
            elif op == "2":
                self._escolher_arquetipo()
            elif op == "3":
                self._confirmar_criacao()
            elif op == "9":
                self._ajuda_criar_personagem()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _definir_nome(self) -> None:
        nome = input("Digite o nome do personagem: ").strip()
        if nome:
            self.personagem["nome"] = nome
            print(f"Nome definido: {nome}")
        else:
            print("Nome não alterado.")

    def _escolher_arquetipo(self) -> None:
        print("\nArquétipos disponíveis (apenas ilustrativos):")
        print("[1] Guerreiro")
        print("[2] Mago")
        print("[3] Arqueiro")
        escolha = input("> ").strip()

        mapa = {
            "1": "Guerreiro",
            "2": "Mago",
            "3": "Arqueiro",
        }
        arq = mapa.get(escolha)
        if arq:
            self.personagem["arquetipo"] = arq
            print(f"Arquétipo definido: {arq}")
        else:
            print("Opção inválida. Arquétipo não alterado.")

    def _confirmar_criacao(self) -> None:
        if not self.personagem["nome"]:
            print("Defina um nome antes de confirmar a criação.")
            return
        if not self.personagem["arquetipo"]:
            print("Escolha um arquétipo antes de confirmar a criação.")
            return
        
        arquetipo = self.personagem["arquetipo"]
            
        # Chama o método que agora retorna o dicionário completo
        dados_arquetipo = self._obter_atributos_por_arquetipo(arquetipo) 
            
        if not dados_arquetipo:
            print("Erro interno: Arquétipo não encontrado.")
            return

        # Extrai os dois componentes necessários
        atributos_base = dados_arquetipo["atributos_base"]
        taxas_crescimento = dados_arquetipo["taxas_crescimento"]
        
        # Linha CORRIGIDA: passando o novo argumento obrigatório
        novo_personagem = Personagem(self.personagem["nome"], atributos_base, taxas_crescimento)

        self._personagem_obj = novo_personagem
        
        print("\nPersonagem criado com sucesso!")
        print(f"Nome: {novo_personagem.nome} | Arquétipo: {arquetipo}")
        print(f"ATK: {atributos_base.ataque} | DEF: {atributos_base.defesa} | HP: {atributos_base.vida}")
        print(f"Crit Chance: {atributos_base.crit_chance}% | Crit Dmg: {atributos_base.crit_dmg}%")
        print(f"Mana Pool: {atributos_base.mana_pool} | Mana Regen: {atributos_base.mana_regen}/turno")
        print(f"Vida Máxima Real: {novo_personagem._atrib.vida_max}")

    def _ajuda_criar_personagem(self) -> None:
        print("\nAjuda — Criar Personagem")
        print("- Defina um nome e um arquétipo para continuar.")
        print("- Esta etapa não cria atributos reais; é apenas o fluxo do menu.")
        print("- Implementações futuras podem usar essas escolhas para gerar status.")

    def menu_missao(self) -> None:
        while True:
            print("\n=== Missão ===")
            print(f"Dificuldade atual: {self.missao_config['dificuldade']}")
            print(f"Cenário atual:     {self.missao_config['cenario']}")
            print("[1] Escolher dificuldade")
            print("[2] Escolher cenário")
            print("[3] Pré-visualizar missão")
            print("[4] Iniciar missão (placeholder)")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._escolher_dificuldade()
            elif op == "2":
                self._escolher_cenario()
            elif op == "3":
                self._preview_missao()
            elif op == "4":
                self._iniciar_missao_teste()
            elif op == "9":
                self._ajuda_missao()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _escolher_dificuldade(self) -> None:
        print("\nDificuldades:")
        print("[1] Fácil")
        print("[2] Média")
        print("[3] Difícil")
        op = input("> ").strip()
        mapa = {"1": "Fácil", "2": "Média", "3": "Difícil"}
        dif = mapa.get(op)
        if dif:
            self.missao_config["dificuldade"] = dif
            print(f"Dificuldade definida: {dif}")
        else:
            print("Opção inválida.")

    def _escolher_cenario(self) -> None:
        print("\nCenários:")
        print("[1] Trilha")
        print("[2] Floresta")
        print("[3] Caverna")
        print("[4] Ruínas")
        op = input("> ").strip()
        mapa = {"1": "Trilha", "2": "Floresta", "3": "Caverna", "4": "Ruínas"}
        cen = mapa.get(op)
        if cen:
            self.missao_config["cenario"] = cen
            print(f"Cenário definido: {cen}")
        else:
            print("Opção inválida.")

    def _preview_missao(self) -> None:
        print("\nPré-visualização da Missão")
        print(f"- Dificuldade: {self.missao_config['dificuldade']}")
        print(f"- Cenário:     {self.missao_config['cenario']}")
        print("- Inimigos e recompensas: (em breve)")
        print("- Regras de combate: (em breve)")

    def _iniciar_missao_placeholder(self) -> None:
        if not self.personagem["nome"]:
            print("Crie um personagem antes de iniciar uma missão.")
            return
        print("\nIniciando missão...")
        print("(Placeholder) Combate e lógica de jogo serão implementados futuramente.")
        print("Missão finalizada (simulado). Retornando ao menu de Missão...")

    def _iniciar_missao_teste(self) -> None:
        """
        Método de teste para iniciar a missão com um inimigo aleatório.
        """
        if not self._personagem_obj:
            print("Crie um personagem antes de iniciar uma missão.")
            return

        # 1. Gera o Inimigo de Teste (aleatoriamente)
        inimigo_da_vez = self._gerar_inimigo_aleatorio()

        # 2. Cria a Missão
        missao_teste = Missao(
            titulo=f"Encontro na {self.missao_config['cenario']}",
            inimigo=inimigo_da_vez
        )

        # 3. Executa a Missão (necessita da implementação de combate)
        print("Iniciando combate...")
        resultado: ResultadoMissao = missao_teste.executar(self._personagem_obj)

        # 4. Exibe o resultado
        print(f"\n--- Resultado da Missão ---")
        print(f"Status: {'VITÓRIA!' if resultado.venceu else 'DERROTA!'}")
        print(f"Detalhes: {resultado.detalhes}")
        
    def _mapa_dificuldade(self) -> Dict[str, Dict[str, float]]:
        """Define os multiplicadores de atributos para cada nível de dificuldade."""
        return {
            "Fácil": {
                "ataque": 0.8,  # Inimigos causam 20% menos dano
                "defesa": 0.8,  # Inimigos têm 20% menos defesa
                "vida": 0.8,    # Inimigos têm 20% menos HP
                "xp": 1.0,      # XP é o mesmo
            },
            "Média": {
                "ataque": 1.0,  # Atributos base (Normal)
                "defesa": 1.0,
                "vida": 1.0,
                "xp": 1.0,
            },
            "Difícil": {
                "ataque": 1.2,  # Inimigos causam 20% mais dano
                "defesa": 1.2,  # Inimigos têm 20% mais defesa
                "vida": 1.2,    # Inimigos têm 20% mais HP
                "xp": 1.5,      # XP ganho é 50% maior (como recompensa pelo desafio)
            }
        }

    def _gerar_inimigo_aleatorio(self) -> Inimigo:
        """
        Gera e retorna uma instância aleatória de Inimigo chamando um método de fábrica.
        Desconsidera a dificuldade por enquanto.
        """
        dificuldade_atual = self.missao_config['dificuldade']
        mapa = self._mapa_dificuldade()
        multiplicadores = mapa.get(dificuldade_atual, mapa["Média"]) # Pega os multiplicadores, padrão Média

        print(f"Dificuldade: {dificuldade_atual} | Multiplicador de ATK/DEF/HP: {multiplicadores['ataque']}")

        # Mapeamento de todos os métodos de criação disponíveis
        # Estes são os métodos de classe que retornam uma instância de Inimigo
        metodos_fabrica = [
            Inimigo.GoblinNormal,
            Inimigo.GoblinArqueiro,
            Inimigo.GoblinEscudeiro,
        ]
            
        # 1. Escolhe um MÉTODO aleatoriamente
        metodo_escolhido = random.choice(metodos_fabrica)
        
        # 2. Executa o método para instanciar o objeto (ex.: Inimigo.goblin_normal())
        inimigo_instancia = metodo_escolhido(multiplicadores)
        
        print(f"Inimigo gerado: {inimigo_instancia.nome}")
        return inimigo_instancia

    def _ajuda_missao(self) -> None:
        print("\nAjuda — Missão")
        print("- Selecione dificuldade e cenário.")
        print("- A opção 'Iniciar missão' executará apenas um placeholder.")
        print("- Uma futura implementação pode usar essas escolhas para montar encontros.")

    def menu_salvar(self) -> None:
        while True:
            print("\n=== Salvar ===")
            print("[1] Salvar rápido (simulado)")
            print("[2] Salvar com nome (simulado)")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._salvar_rapido()
            elif op == "2":
                self._salvar_nomeado()
            elif op == "9":
                self._ajuda_salvar()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _salvar_rapido(self) -> None:
        self._ultimo_save = "quick_save.json"
        print(f"✔ Salvo (simulado) em: {self._ultimo_save}")

    def _salvar_nomeado(self) -> None:
        nome = input("Nome do arquivo de save (ex.: meu_jogo.json): ").strip() or "save.json"
        self._ultimo_save = nome
        print(f"✔ Salvo (simulado) em: {self._ultimo_save}")

    def _ajuda_salvar(self) -> None:
        print("\nAjuda — Salvar")
        print("- Salvar rápido usa um nome padrão fictício.")
        print("- Salvar nomeado permite escolher um nome fictício.")
        print("- Não há escrita em disco nesta base — é apenas navegação.")

    def menu_carregar(self) -> None:
        while True:
            print("\n=== Carregar ===")
            print("[1] Carregar último save (simulado)")
            print("[2] Carregar por nome (simulado)")
            print("[9] Ajuda")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "1":
                self._carregar_ultimo()
            elif op == "2":
                self._carregar_nomeado()
            elif op == "9":
                self._ajuda_carregar()
            elif op == "0":
                break
            else:
                print("Opção inválida.")

    def _carregar_ultimo(self) -> None:
        if self._ultimo_save:
            self._ultimo_load = self._ultimo_save
            print(f"✔ Carregado (simulado) de: {self._ultimo_load}")
        else:
            print("Nenhum save recente encontrado (simulado).")

    def _carregar_nomeado(self) -> None:
        nome = input("Nome do arquivo para carregar (ex.: meu_jogo.json): ").strip()
        if nome:
            self._ultimo_load = nome
            print(f"✔ Carregado (simulado) de: {self._ultimo_load}")
        else:
            print("Nome não informado.")

    def _ajuda_carregar(self) -> None:
        print("\nAjuda — Carregar")
        print("- O carregamento aqui é apenas ilustrativo (sem leitura real).")
        print("- Use o nome que você “salvou” anteriormente para simular.")

    def menu_atributos_personagem(self) -> None:
        while True:
            print("\n=== Atributos dos Personagens ===\n")
            print("Guerreiro -> ATK:20 | DEF:40 | HP:100 | Crit Chance:35% | Crit Dmg:150% | Mana Pool:30 | Mana Regen:3/turno \n" \
            "\nMago -> ATK:40 | DEF:5 | HP:100 | Crit Chance:10% | Crit Dmg:200% | Mana Pool:60 | Mana Regen:10/turno \n" \
            "\nArqueiro -> ATK:35 | DEF:8 | HP:100 | Crit Chance:25% | Crit Dmg:120% | Mana Pool:40 | Mana Regen:4/turno\n")
            print("[0] Voltar")
            op = input("> ").strip()

            if op == "0":
                break
            else:
                print("Opção inválida.")