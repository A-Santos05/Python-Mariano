from __future__ import annotations
from .base import Entidade, Atributos, Item
from typing import List, Union, Tuple
import random
import math


class Personagem(Entidade):
    """
    Classe base única do jogador.
    Esta versão NÃO implementa a lógica principal de combate.
    """

    def __init__(self, nome: str, atrib: Atributos, taxas_crescimento: dict[str, int]):
        super().__init__(nome, atrib)
        self.nivel = 1
        self.xp = 0
        self._taxas_crescimento = taxas_crescimento # Armazena as taxas
        self.inventario: List[Item] = []

    def coletar_item(self, item: Item) -> None:
        """Adiciona um item ao inventário."""
        print(f"{self.nome} COLETADO: {item.nome}!")
        self.inventario.append(item)

    def usar_item(self, nome_item: str) -> bool:
        """Usa um item do inventário, aplicando seu efeito."""
        
        # Encontra o item, ignorando maiúsculas/minúsculas
        item_a_usar = next((item for item in self.inventario if item.nome.lower() == nome_item.lower()), None)
        
        if not item_a_usar:
            print(f"Item '{nome_item}' não encontrado.")
            return False
            
        if item_a_usar.tipo == "Consumível":
            if item_a_usar.efeito_atributo == "vida":
                # Lógica de cura
                cura = item_a_usar.efeito_quant
                self._atrib.vida = min(self._atrib.vida_max, self._atrib.vida + cura)
                print(f"\nUsou {item_a_usar.nome}. Curou {cura} HP.")
                print(f"HP atual: {self._atrib.vida}/{self._atrib.vida_max}")
                
            # Remove o item do inventário (consumível)
            self.inventario.remove(item_a_usar)
            return True
            
        else:
            print(f"Item {item_a_usar.nome} é do tipo {item_a_usar.tipo} e não pode ser usado no momento.")
            return False

    def calcular_dano_base(self) -> tuple[int, int]:
        """
        Implementação: Calcula dano normal (reduzido pela defesa) e dano verdadeiro (ignora defesa).
        Retorna: (dano_normal, dano_verdadeiro)
        """
        dano_critico = random.random() * 100 < self._atrib.crit_chance
        dano_base = self._atrib.ataque
        
        # 1. Calcula o dano base final, aplicando o crítico se necessário
        dano_final = dano_base
        if dano_critico:
            multiplicador_critico = self._atrib.crit_dmg / 100
            dano_final = int(dano_base * multiplicador_critico)
            print(f"{self.nome} acerta um crítico!")

        # 2. Divide o dano final em Dano Verdadeiro e Dano Normal
        dano_verdadeiro = int(dano_final * (self._atrib.dano_verdadeiro_perc / 100))
        dano_normal = dano_final - dano_verdadeiro
        
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

    def habilidade_especial(self) -> int:
        """
        Deve retornar dano especial (ou 0 se indisponível).
        (ex.: consumir self._atrib.mana e aplicar bônus de dano)
        """
        raise NotImplementedError("Implementar habilidade especial do Personagem.")
    
    @staticmethod
    def xp_necessario_para_nivel(nivel: int) -> int:
        """
        Define a quantidade de XP necessária para ir do início do nível (N) 
        para o início do próximo nível (N+1).
        
        Fórmula simples: XP = Nível * 100
        """
        if nivel <= 0:
            return 100 # Garante um valor mínimo
        
        # Fórmula de progressão de XP
        return nivel * 100
    
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
