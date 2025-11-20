from __future__ import annotations
from models.base import Atributos
from models.personagem import Personagem
from models.inimigo import Inimigo
from models.missao import Missao, ResultadoMissao
from typing import Any, Dict
import json
import os
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
                    ataque = 30, vida = 120, defesa = 15, 
                    crit_chance = 35, crit_dmg = 130,
                    mana = 0, mana_pool = 30, mana_regen = 6, special_cost = 25
                ),
                "taxas_crescimento": {
                    "ataque": 3,
                    "vida": 15,
                    "defesa": 6,
                }
            },
            "Paladino":{
                "atributos_base": Atributos(
                    ataque = 20, vida = 120, defesa = 15,
                    crit_chance = 25, crit_dmg = 125, dano_verdadeiro_perc = 15,
                    mana = 0, mana_pool = 40, mana_regen = 7, special_cost = 25
                ),
                "taxas_crescimento": {
                    "ataque": 3,
                    "vida": 17,
                    "defesa": 6,
                }
            },
            "Mago":{
                "atributos_base": Atributos(
                    ataque = 20, vida = 100, defesa = 15, 
                    crit_chance = 15, crit_dmg = 200, dano_verdadeiro_perc = 25,
                    mana = 0,mana_pool = 60, mana_regen = 10, special_cost = 25
                    ),
                "taxas_crescimento": {
                    "ataque": 5,
                    "vida": 12,
                    "defesa": 5,
                }
            },
            "Arqueiro":{
                "atributos_base": Atributos(
                    ataque = 20, vida = 100, defesa = 20, 
                    crit_chance = 35, crit_dmg = 135,
                    mana = 0,mana_pool = 40, mana_regen = 5, special_cost = 25
                    ),
                "taxas_crescimento": {
                    "ataque": 6,
                    "vida": 12,
                    "defesa": 4,
                }
            },
            "Espadachim":{
                "atributos_base": Atributos(
                    ataque = 20, vida = 100, defesa = 20, 
                    crit_chance = 65, crit_dmg = 125,
                    mana = 0, mana_pool = 45, mana_regen = 5, special_cost = 25
                    ),
                "taxas_crescimento": {
                    "ataque": 10,
                    "vida": 12,
                    "defesa": 3,
                }
            },
        }
        
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
            if nome == "Cleiton":
                self.personagem["nome"] = "Cleiton Rasta"
                print(f"Nome definido: {nome}")
            else:
                self.personagem["nome"] = nome
                print(f"Nome definido: {nome}")
        else:
            print("Nome não alterado.")

    def _escolher_arquetipo(self) -> None:
        print("\nArquétipos disponíveis (apenas ilustrativos):")
        print("[1] Guerreiro")
        print("[2] Mago")
        print("[3] Arqueiro")
        print("[4] Paladino")
        print("[5] Espadachim")
        escolha = input("> ").strip()

        mapa = {
            "1": "Guerreiro",
            "2": "Mago",
            "3": "Arqueiro",
            "4": "Paladino",
            "5": "Espadachim",
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
            
        dados_arquetipo = self._obter_atributos_por_arquetipo(arquetipo) 
            
        if not dados_arquetipo:
            print("Erro interno: Arquétipo não encontrado.")
            return

        atributos_base = dados_arquetipo["atributos_base"]
        taxas_crescimento = dados_arquetipo["taxas_crescimento"]
        
        novo_personagem = Personagem(
            self.personagem["nome"],
            atributos_base, 
            taxas_crescimento, 
            arquetipo
        )

        self._personagem_obj = novo_personagem
        
        print("\nPersonagem criado com sucesso!")
        print(f"Nome: {novo_personagem.nome} | Arquétipo: {arquetipo}")
        print(f"ATK: {atributos_base.ataque} | DEF: {atributos_base.defesa} | HP: {atributos_base.vida}")
        print(f"Crit Chance: {atributos_base.crit_chance}% | Crit Dmg: {atributos_base.crit_dmg}%")
        print(f"Mana Pool: {atributos_base.mana_pool} | Mana Regen: {atributos_base.mana_regen} / turno")
        print(f"Vida Máxima Real: {novo_personagem._atrib.vida_max}")

    def _ajuda_criar_personagem(self) -> None:
        print("\n======= Ajuda Criar Personagem =======")
        print("- Defina um nome e um arquétipo e confirme sua criação para continuar.")
        print("- Cada arquétipo tem atributos base e taxas de crescimento diferentes.")
        print("- Voltar a esse menu durante a sessão e escolher 'Confirmar criação' irá reescrever o personagem atual.")
        while True:
            print("\n======= Arquétipos =======")
            print("[1] Guerreiro")
            print("[2] Mago")
            print("[3] Arqueiro")
            print("[4] Paladino")
            print("[5] Espadachim")
            print("[0] Voltar")
            op = input("> ").strip()
            
            if op == "1":
                print("Classe tank com alta defesa e vida, ataque baixo.")
            elif op == "2":
                print("Classe de dano mágico com alta regeneração de mana e dano verdadeiro.")
            elif op == "3":
                print("Classe de dano físico com alto ataque e chance crítica.")
            elif op == "4":
                print("Classe tank com altissima defesa e vida, atque baixo com dano verdadeiro.")
            elif op == "5":
                print("Classe de dano critico com alta chance crítica e ataque moderado, focado no uso da habilidade para dano significativo.")
            elif op == "0":
                break
            else:
                print("Opção inválida.")

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
        print("[5] Bostil")
        op = input("> ").strip()
        mapa = {"1": "Trilha", "2": "Floresta", "3": "Caverna", "4": "Ruínas", "5": "Bostil"}
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

        # 1. Gera o Inimigo
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
            "Fácil": { #Multiplicador dos atributos base (facil)
                "ataque": 0.8,
                "dano_verdadeiro": 0.8,
                "defesa": 0.8,
                "vida": 0.8,
                "xp": 1.0,
            },
            "Média": { #Multiplicador dos atributos base (normal)
                "ataque": 1.0,
                "dano_verdadeiro": 1.0,
                "defesa": 1.0,
                "vida": 1.0,
                "xp": 1.0,
            },
            "Difícil": { #Multiplicador dos atributos base (dificil)
                "ataque": 1.2,
                "dano_verdadeiro": 1.2,
                "defesa": 1.2,
                "vida": 1.2,
                "xp": 1.5,
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
        if self.missao_config["cenario"] == "Floresta":
            metodos_fabrica = [
                Inimigo.GoblinNormal,
                Inimigo.GoblinArqueiro,
                Inimigo.GoblinEscudeiro,
                Inimigo.GoblinMago,
                Inimigo.Goblincotoco,
            ]
        elif self.missao_config["cenario"] == "Trilha":
            metodos_fabrica = [
                Inimigo.BandidodaTrilha,
                Inimigo.LoboFerozdaTrilha,
                Inimigo.GolemdaTrilha,
                Inimigo.DruidaImpurodaTrilha,
                Inimigo.GuardiaoEspinhosodaTrilha,
            ]
        elif self.missao_config["cenario"] == "Caverna":
            metodos_fabrica = [
               Inimigo.AranhaCavernal,
               Inimigo.BarbadoCavernal,
               Inimigo.MorcegoCavernal,
               Inimigo.EsqueletoBalisticoCavernal,
               Inimigo.XamaCavernal,
            ]
        elif self.missao_config["cenario"] == "Ruínas":
            metodos_fabrica = [
               Inimigo.EsqueletodasRuinas,
               Inimigo.FantasmadasRuinas,
               Inimigo.GarguladasRuinas,
               Inimigo.GeomantedasRuinas,
               Inimigo.AtiradorEnferrujadodasRuinas,
            ]
            
        # Verifica se o usuário pode jogar o cenário do Boss
        if self._personagem_obj.nivel >= 9 and self.missao_config["cenario"] == "Bostil":
            metodo_escolhido = Inimigo.ReiDoBostil
        else:
            metodo_escolhido = random.choice(metodos_fabrica)
        
        # 2. Executa o método para instanciar o objeto (ex.: Inimigo.goblin_normal())
        nivel_do_inimigo = self._gerar_nivel_inimigo(self._personagem_obj.nivel)
        inimigo_instancia = metodo_escolhido(multiplicadores, nivel_do_inimigo)
        
        print(f"Inimigo gerado: {inimigo_instancia.nome}")
        return inimigo_instancia
    
    def _gerar_nivel_inimigo(self, nivel_jogador: int) -> int:
        """
        Gera um nível de inimigo próximo ao do jogador (e.g., Nv-1 a Nv+1).
        Você pode ajustar o range (random.randint) para variar a dificuldade.
        """
        # Exemplo: Nível do inimigo varia entre (Nv_Jogador - 1) e (Nv_Jogador + 1)
        variacao = random.randint(-1, 1) 
        
        nivel_gerado = nivel_jogador + variacao
        
        # Garante que o nível mínimo seja 1
        return max(1, nivel_gerado)

    def mostrar_status_personagem(self) -> None:
        """Exibe uma ficha completa do personagem atual."""
        
        if not self._personagem_obj:
            print("\nVocê precisa criar um personagem primeiro.")
            print("Use a opção [1] no menu principal.")
            input("\nPressione Enter para continuar...")
            return

        p = self._personagem_obj
        atrib = p._atrib
        
        print("\n=== Ficha do Personagem ===")
        print(f"Nome:     {p.nome}")
        print(f"Classe:   {p.classe}") # 'classe' foi definido no __init__ do Personagem
        print(f"Nível:    {p.nivel}")
        
        # Lógica de XP
        xp_necessario = p.xp_necessario_para_nivel(p.nivel)
        print(f"XP:       {p.xp} / {xp_necessario}")
        
        print("\n=== Atributos de Combate ===")
        print(f"HP:       {atrib.vida} / {atrib.vida_max}")
        print(f"Mana:     {atrib.mana} / {atrib.mana_pool}")
        print(f"Ataque:   {atrib.ataque}")
        print(f"Defesa:   {atrib.defesa}")
        
        print("\n=== Atributos Secundários ===")
        print(f"Regen. Mana: {atrib.mana_regen} / turno")
        print(f"Custo Espec: {atrib.special_cost} Mana")
        print(f"Chance Crít: {atrib.crit_chance}%")
        print(f"Dano Crít:   {atrib.crit_dmg}%")
        
        if atrib.dano_verdadeiro_perc > 0:
            print(f"Dano Verd.:  {atrib.dano_verdadeiro_perc}% (Conversão)")
        
        # Mostra efeitos ativos (se houver)
        if p.efeitos_ativos:
            print("\n=== Efeitos Ativos ===")
            for efeito in p.efeitos_ativos:
                print(f"- {efeito.nome} ({efeito.duracao_atual} turnos restantes)") #
        
        # Mostra sangramento ativo (se houver)
        if atrib.sangramento_duracao > 0:
            print("\n=== Efeitos Negativos ===")
            print(f"🩸 Sangramento ({atrib.sangramento_dano} dano/turno, {atrib.sangramento_duracao} turnos restantes)")

        print("\n==============================")
        input("Pressione Enter para voltar ao menu...")
    
    def menu_inventario(self) -> None:
        if not self._personagem_obj:
            print("Crie um personagem antes de acessar o inventário.")
            return

        p = self._personagem_obj
        
        while True:
            print("\n=== Inventário ===")
            print(f"HP Atual: {p.barra_hp(10)}")
            
            if not p.inventario:
                print("Seu inventário está vazio.")
            else:
                contagem_itens: Dict[str, int] = {}
                opcoes = []
                idx = 1
                
                # 1. Conta a quantidade de cada item único
                for item in p.inventario:
                    contagem_itens[item.nome] = contagem_itens.get(item.nome, 0) + 1

                print("\nItens Consumíveis:")
                
                # 2. Lista os itens e suas quantidades para uso
                for nome, quant in contagem_itens.items():
                    # Pega um item de exemplo para obter os detalhes de efeito
                    item_exemplo = next(item for item in p.inventario if item.nome == nome)
                    
                    if item_exemplo.tipo == "Consumível":
                        detalhe = f"(Cura {item_exemplo.efeito_quant + int(p._atrib.vida_max * 0.1)} {item_exemplo.efeito_atributo.upper()})"
                        opcoes.append(nome)
                        print(f"[{idx}] {nome} x{quant} {detalhe}")
                        idx += 1
                
                if not opcoes and p.inventario:
                    print("Nenhum item consumível para usar.")
                
            print("\n[0] Voltar")
            
            op = input("Digite o NÚMERO do item que deseja USAR ou [0] para Voltar: ").strip()
            
            if op == "0":
                break
            elif op.isdigit():
                try:
                    indice = int(op) - 1
                    if 0 <= indice < len(opcoes):
                        nome_item_escolhido = opcoes[indice]
                        p.usar_item(nome_item_escolhido) # Chama o método implementado em Personagem
                    else:
                        print("Opção inválida.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
            else:
                print("Opção inválida.")
                
    def _ajuda_missao(self) -> None:
        print("\n======= Ajuda Missão =======")
        print("- Selecione dificuldade e cenário.")
        print("- A dificuldade afeta ATK/DEF/HP dos inimigos.")
        print("- O cenário determina o tipo de inimigos encontrados.")
        print("============================")

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

    def _salvar_no_arquivo(self, nome_arquivo: str) -> None:
        """Método auxiliar que realmente grava no disco."""
        if not self._personagem_obj:
            print("Erro: Não há personagem criado para salvar.")
            return

        try:
            # Pega o dict do personagem
            dados = self._personagem_obj.to_dict()
            
            # Garante que tem a extensão .json
            if not nome_arquivo.endswith(".json"):
                nome_arquivo += ".json"

            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            
            print(f"Jogo salvo com sucesso em '{nome_arquivo}'!")
            self._ultimo_save = nome_arquivo

        except Exception as e:
            print(f"Erro ao salvar: {e}")

    def _salvar_rapido(self) -> None:
        self._salvar_no_arquivo("quicksave.json")

    def _salvar_nomeado(self) -> None:
        nome = input("Nome do arquivo de save (ex: meu_save): ").strip()
        if not nome:
            nome = "save_padrao"
        self._salvar_no_arquivo(nome)

    def _ajuda_salvar(self) -> None:
        print("\n======= Ajuda Salvar =======")
        print("- Salvar rápido usa um nome padrão.")
        print("- Salvar nomeado permite escolher um nome fictício.")
        print("- Salvar permite continuar a aventura mais tarde sem perder o progresso.")

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

    def _carregar_do_arquivo(self, nome_arquivo: str) -> None:
        """Método auxiliar que lê do disco e recria o objeto."""
        
        if not nome_arquivo.endswith(".json"):
            nome_arquivo += ".json"
            
        if not os.path.exists(nome_arquivo):
            print(f"Arquivo '{nome_arquivo}' não encontrado.")
            return

        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            # Recria o personagem usando o método estático que criamos
            self._personagem_obj = Personagem.from_dict(dados)
            
            # Atualiza o dicionário simples usado nos menus (para exibir nome/classe corretamente)
            self.personagem["nome"] = self._personagem_obj.nome
            self.personagem["arquetipo"] = self._personagem_obj.classe
            
            print(f"Personagem '{self._personagem_obj.nome}' carregado com sucesso!")
            self._ultimo_load = nome_arquivo

        except Exception as e:
            print(f"Erro ao carregar arquivo (pode estar corrompido): {e}")

    def _carregar_ultimo(self) -> None:
        # Tenta carregar o quicksave ou o último salvo na sessão
        alvo = self._ultimo_save or "quicksave.json"
        print(f"Tentando carregar: {alvo}")
        self._carregar_do_arquivo(alvo)

    def _carregar_nomeado(self) -> None:
        arquivos = [f for f in os.listdir('.') if f.endswith('.json')]
        if arquivos:
            print("Saves encontrados na pasta:")
            for arq in arquivos:
                print(f" - {arq}")
        
        nome = input("Nome do arquivo para carregar: ").strip()
        if nome:
            self._carregar_do_arquivo(nome)
        else:
            print("Nome inválido.")

    def _ajuda_carregar(self) -> None:
        print("\n======= Ajuda Carregar =======")
        print("- O carregamento é onde você recupera um personagem salvo.")
        print("- Use o nome que você “salvou” anteriormente ou carregar ultimo para carregar.")

    def menu_atributos_personagem(self) -> None:
        # Se criar uma nova classe no futuro, basta adicionar o nome aqui.
        lista_classes = ["Guerreiro", "Mago", "Arqueiro", "Paladino", "Espadachim"]

        while True:
            print("\n=== Atributos dos Personagens ===\n")
            
            for nome_classe in lista_classes:
                # Busca os dados reais definidos no método _obter_atributos_por_arquetipo
                dados = self._obter_atributos_por_arquetipo(nome_classe)
                
                if dados:
                    # Extrai o objeto Atributos
                    base = dados["atributos_base"]
                    
                    # Monta a string dinâmica
                    info = (
                        f"{nome_classe} -> "
                        f"ATK: {base.ataque} | "
                        f"DEF: {base.defesa} | "
                        f"HP: {base.vida} | "
                        f"Crit: {base.crit_chance}% | "
                        f"CritDmg: {base.crit_dmg}% | "
                        f"Mana: {base.mana_pool} | "
                        f"Mana Regen: {base.mana_regen} / turno"
                    )
                    
                    # Se a classe tiver Dano Verdadeiro, mostra também
                    if base.dano_verdadeiro_perc > 0:
                        info += f" | Dano Verdadeiro: {base.dano_verdadeiro_perc}%"

                    print(info + "\n")

            print("[0] Voltar")
            op = input("> ").strip()

            if op == "0":
                break
            else:
                print("Opção inválida.")