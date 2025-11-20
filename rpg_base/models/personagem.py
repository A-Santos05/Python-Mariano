from __future__ import annotations
from .base import Entidade, Atributos, Item
from .efeitos import EscudoDeGuerra, AmplificacaoArcana, FocoDoCacador, BencaoDivina, Zandatsu, Efeito
from typing import List, Union, Tuple
from dataclasses import asdict
import random
import math

class Personagem(Entidade):
    """
    Classe base única do jogador.
    Esta versão NÃO implementa a lógica principal de combate.
    """

    def __init__(self, nome: str, atrib: Atributos, taxas_crescimento: dict[str, int], arquetipo: str):
        super().__init__(nome, atrib)
        self.nivel = 1
        self.xp = 0
        self._taxas_crescimento = taxas_crescimento
        self.inventario: List[Item] = []
        self.classe = arquetipo

    def coletar_item(self, item: Item) -> None:
        """Adiciona um item ao inventário."""
        self.inventario.append(item)

    def usar_item(self, nome_item: str) -> bool:
        item_a_usar = next((item for item in self.inventario if item.nome.lower() == nome_item.lower()), None)
        
        if not item_a_usar:
            print(f"Item '{nome_item}' não encontrado.")
            return False
            
        if item_a_usar.tipo == "Consumível":
            if item_a_usar.efeito_atributo == "vida":
                # Lógica de cura
                cura = item_a_usar.efeito_quant + int(self._atrib.vida_max * 0.1) # Cura base + 10% da vida máxima
                self._atrib.vida = min(self._atrib.vida_max, self._atrib.vida + cura)
                print(f"\nUsou {item_a_usar.nome}. Curou {cura} HP.")
                print(f"HP atual: {self._atrib.vida}/{self._atrib.vida_max}")
                
            # Remove o item do inventário (consumível)
            self.inventario.remove(item_a_usar)
            return True
            
        else:
            print(f"Item {item_a_usar.nome} é do tipo {item_a_usar.tipo} e não pode ser usado no momento.")
            return False

    def calcular_dano_base(self) -> Tuple[int, int]:
        """Calcula o dano normal e o dano verdadeiro, considerando buffs de Mago e Arqueiro."""
        
        # Conversão base de Dano Verdadeiro
        conversao_verdadeira = self._atrib.dano_verdadeiro_perc / 100
        
        # 1. VERIFICAÇÃO DO BUFF DO MAGO (Transfusao Arcana)
        efeito_mago = next((e for e in self.efeitos_ativos if e.nome == "Amplificação Arcana"), None)
        if efeito_mago:
            # Assumindo que o bônus está armazenado no objeto Efeito
            conversao_verdadeira = conversao_verdadeira * (efeito_mago.bonus_conversao / 100)
        
        # Dano base antes do crítico
        dano_base = self._atrib.ataque

        # Dano normal e verdadeiro antes do crítico
        dano_verdadeiro = int(dano_base * min(conversao_verdadeira, 1.0))
        dano_normal = dano_base - dano_verdadeiro
        
        # Dano Critico (Chance e Multiplicador)
        chance_critico = self._atrib.crit_chance / 100
        multiplicador_critico = self._atrib.crit_dmg / 100

        # 2. VERIFICAÇÃO DO BUFF DE DANO CRITICO [foco do Caçador ou Zandatsu]
        bonus_critico = next((e for e in self.efeitos_ativos if e.nome == "Foco do Caçador" or e.nome == "Zandatsu"), None)
        if bonus_critico:
            chance_critico += bonus_critico.bonus_chance_crit / 100
            multiplicador_critico += bonus_critico.bonus_dano_crit / 100
            
        if random.random() < chance_critico:
            # Aplica o multiplicador no dano total (Normal + Verdadeiro)
            dano_total = dano_normal + dano_verdadeiro
            dano_critico = int(dano_total * multiplicador_critico)
            
            # Recalcula as proporções do dano crítico (mantendo a proporção Normal/Verdadeiro)
            dano_verdadeiro_final = int(dano_critico * min(conversao_verdadeira, 1.0))
            dano_normal_final = dano_critico - dano_verdadeiro_final
            
            # Print de crítico (opcional)
            print(f"[CRÍTICO]")
            return dano_normal_final, dano_verdadeiro_final
        else:
            return dano_normal, dano_verdadeiro
    
    def receber_dano(self, dano: Union[int, Tuple[int, int]]) -> int:
        """
        Recebe dano. Se for uma tupla, processa dano normal e verdadeiro.
        Tupla esperada: (dano_normal, dano_verdadeiro)
        """
        dano_total_recebido = 0

        if isinstance(dano, tuple):
            dano_normal, dano_verdadeiro = dano
            
            # 1. Cálculo do Dano Normal (reduzido pela defesa da Entidade)
            dano_reduzido = max(1, dano_normal - math.ceil(dano_normal * (self._atrib.defesa / 100)))
            
            # 2. Dano Verdadeiro é aplicado diretamente
            
            dano_total_recebido = dano_reduzido + dano_verdadeiro
            
            print(f"    (Dano Normal: {dano_normal} -> {dano_reduzido} | Dano Verdadeiro: {dano_verdadeiro})")
            
            # Aplica o dano total à vida do Personagem
            self._atrib.vida = max(0, self._atrib.vida - dano_total_recebido)
            return dano_total_recebido
        else:
            # Comportamento base (dano simples INT) - usa o método da Entidade
            return super().receber_dano(dano)

    def habilidade_especial(self) -> None: # NOVO
        """
        Gasta mana e aplica o efeito da habilidade especial da classe.
        Retorna uma string com o nome da habilidade aplicada.
        """
        # A Missão verifica a mana e gasta antes de chamar este método.
        efeito_aplicar: Efeito
        if self.classe == "Guerreiro":
            efeito_aplicar = EscudoDeGuerra(self)
        elif self.classe == "Mago":
            efeito_aplicar = AmplificacaoArcana()
        elif self.classe == "Arqueiro":
            efeito_aplicar = FocoDoCacador()
        elif self.classe == "Paladino":
            efeito_aplicar = BencaoDivina(self)
        elif self.classe == "Espadachim":
            efeito_aplicar = Zandatsu()
        else:
            return "Nenhuma habilidade especial implementada para esta classe."

        self.aplicar_efeito(efeito_aplicar)
        return
    
    @staticmethod
    def xp_necessario_para_nivel(nivel: int) -> int:
        """
        Define a quantidade de XP necessária para ir do início do nível (N) 
        para o início do próximo nível (N+1).
        
        Fórmula simples: XP = Nível * 100
        """
        if nivel <= 0:
            return 140 # Garante um valor mínimo
        # Fórmula de progressão de XP: 100 * (N * 1.4)
        # Explicação: Cada nível requer 30% a mais de XP que o nível anterior.
        # nivel 1 -> 130 XP
        # nivel 2 -> 260 XP
        # nivel 3 -> 390 XP 
        # nivel 4 -> 520 XP
        # nivel 5 -> 650 XP
        # nivel 6 -> 780 XP
        # nivel 7 -> 910 XP
        # nivel 8 -> 1040 XP
        # nivel 9 -> 1170 XP
        # nivel 10 -> 1300 XP
        
        return round(100 * (nivel * 1.3))
    
    def ganhar_xp(self, valor_xp: int) -> None:
        """
        Adiciona XP e verifica se o personagem deve subir de nível.
        """
        if valor_xp <= 0:
            return
        print("=================XP=================")
        print(f"XP + {valor_xp}")
        print(f"Nivel: {self.nivel} | XP Atual: {self.xp + valor_xp}/{Personagem.xp_necessario_para_nivel(self.nivel)}")
        print("====================================")
        self.xp += valor_xp
        
        self.verificar_subir_nivel()
        
    def verificar_subir_nivel(self) -> None:
        """
        Checa o XP atual contra o CAP e executa a subida de nível, se necessário.
        """
        cap_xp = Personagem.xp_necessario_para_nivel(self.nivel)
        
        while self.xp >= cap_xp:
            self.nivel += 1
            self.xp -= cap_xp # O XP restante 'passa' para o próximo nível
            
            print("=============Level Up!=============")
            print(f"{self.nome} atingiu o NÍVEL {self.nivel}!")
            print("====================================")
            
            #Incrementa os atributos com base nas taxas de crescimento da classe
            self._atrib.vida_max += self._taxas_crescimento.get("vida", 0)
            self._atrib.ataque += self._taxas_crescimento.get("ataque", 0)
            self._atrib.defesa += self._taxas_crescimento.get("defesa", 0)

            #Cura o personagem ao subir de nível
            self._atrib.vida = self._atrib.vida_max
            print("Atributos aumentados:")
            print(f"ATK + {self._taxas_crescimento.get('ataque', 0)}, HP + {self._taxas_crescimento.get('vida', 0)}, DEF + {self._taxas_crescimento.get('defesa', 0)}")
            print(f"Vida restaurada para {self._atrib.vida}/{self._atrib.vida_max} HP.")
            print("====================================")
            print("Atributos atuais:")
            print(f"ATK: {self._atrib.ataque}, HP: {self._atrib.vida_max}, DEF: {self._atrib.defesa}")
            print("====================================")
            
            # Recalcula o CAP para o novo nível
            cap_xp = Personagem.xp_necessario_para_nivel(self.nivel)

    def aplicar_sangramento(self, dano_por_turno: int, duracao_turnos: int) -> None:
        """Aplica ou atualiza o efeito de sangramento."""
        self._atrib.sangramento_dano = dano_por_turno
        self._atrib.sangramento_duracao = duracao_turnos
        print(f"** {self.nome} foi SANGRAMENTADO! Receberá {dano_por_turno} de dano por 🩸 {duracao_turnos} turnos! **")

    # NOVO: Processar dano de Sangramento
    def processar_sangramento(self) -> int:
        """Aplica o dano de sangramento se ativo e decrementa a duração."""
        dano_total = 0
        if self._atrib.sangramento_duracao > 0:
            dano_sangramento = self._atrib.sangramento_dano
            
            # Sangramento é Dano Verdadeiro (ignora defesa)
            self._atrib.vida = max(0, self._atrib.vida - dano_sangramento)
            self._atrib.sangramento_duracao -= 1
            dano_total += dano_sangramento
            
            print(f"🩸 Sangramento: {self.nome} perde {dano_sangramento} HP! (Restam {self._atrib.sangramento_duracao} turnos)")

            if self._atrib.sangramento_duracao == 0:
                print("Sangramento cessou.")

        return dano_total

    def to_dict(self) -> dict:
        """Converte o personagem e seu estado atual para um dicionário."""
        return {
            "nome": self.nome,
            "classe": self.classe,
            "nivel": self.nivel,
            "xp": self.xp,
            # Converte a dataclass Atributos para dict
            "atributos": asdict(self._atrib), 
            # Converte cada Item do inventário para dict
            "inventario": [item.to_dict() for item in self.inventario],
            "taxas_crescimento": self._taxas_crescimento
        }

    @classmethod
    def from_dict(cls, data: dict) -> Personagem:
        """Cria uma instância de Personagem a partir de um dicionário carregado."""
        
        # 1. Recria o objeto Atributos
        dados_atrib = data["atributos"]
        atributos = Atributos(**dados_atrib)
        
        # 2. Cria a instância do Personagem
        personagem = cls(
            nome=data["nome"],
            atrib=atributos,
            taxas_crescimento=data["taxas_crescimento"],
            arquetipo=data["classe"]
        )
        
        # 3. Restaura dados simples
        personagem.nivel = data["nivel"]
        personagem.xp = data["xp"]
        
        # 4. Restaura o inventário (convertendo dicts de volta para objetos Item)
        lista_itens_dicts = data.get("inventario", [])
        personagem.inventario = [Item.from_dict(item_data) for item_data in lista_itens_dicts]
        
        return personagem