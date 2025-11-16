from __future__ import annotations
from .base import Entidade, Atributos, Item
from typing import Dict, Optional, Union, Tuple
import math
import random

class Inimigo(Entidade):
    """
    Inimigo genérico.
    Sem IA/variações — apenas o contêiner para atributos básicos.
    """

    from typing import List, Optional

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int, recompensa_xp: int, itens_drop: Optional[List[Item]] = None, dano_verdadeiro_perc: int = 0):
    super().__init__(nome, Atributos(
        vida=vida, ataque=ataque, defesa=defesa, vida_max=vida, recompensa_xp=recompensa_xp, dano_verdadeiro_perc=dano_verdadeiro_perc
    ))
    self.xp_drop = recompensa_xp
    self.itens_drop = itens_drop or []

    
    def calcular_dano_base(self) -> Tuple[int, int]:
        """Implementa um cálculo de dano para o inimigo com variação e Dano Verdadeiro."""
        dano_base = self._atrib.ataque
        variacao = random.randint(0, 2)
        dano_total = max(1, dano_base + variacao)
        
        # 1. Divide o dano total em Dano Verdadeiro e Dano Normal
        dano_verdadeiro = int(dano_total * (self._atrib.dano_verdadeiro_perc / 100))
        dano_normal = dano_total - dano_verdadeiro
        
        return dano_normal, dano_verdadeiro

    # Atualiza o atacar para retornar a tupla (dano_normal, dano_verdadeiro)
    def atacar(self) -> Tuple[int, int]: 
        """Ataque do Inimigo: retorna a tupla (dano_normal, dano_verdadeiro)."""
        return self.calcular_dano_base()
    
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
            
            # 2. Cálculo do Dano Verdadeiro (não reduzido)
            # O dano verdadeiro é aplicado diretamente
            
            dano_total_recebido = dano_reduzido + dano_verdadeiro
            
            print(f"(Dano Normal: {dano_normal} -> {dano_reduzido} | Dano Verdadeiro: {dano_verdadeiro})")

        else:
            # Comportamento antigo, se for apenas um inteiro (usado pelo Inimigo atacando o Personagem)
            dano_total_recebido = super().receber_dano(dano)
            return dano_total_recebido # Já atualiza a vida em Entidade.receber_dano

        # Aplica o dano total à vida do inimigo
        self._atrib.vida = max(0, self._atrib.vida - dano_total_recebido)
        return dano_total_recebido

    # Pendente definir metodo e recber dano/defesa e sobrepor o metodo receber dano da classe Entidade
    
    """Definições de atributos para inimigos específicos"""

    @classmethod
    def GoblinNormal(cls, multiplicadores: Dict[str, float]) -> Inimigo:
        vida_base = 100
        ataque_base = 5
        defesa_base = 10
        xp_base = 10 # definir recompensa de xp futura

        drop_chance = random.random() < 0.5
        item_dropar = Item(
            nome = "Poção de Cura Menor", 
            tipo = "Consumível", 
            efeito_quant = 25, 
            efeito_atributo = "vida"
        ) if drop_chance else None
        
        return cls(
            nome = "Goblin Normal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            item_drop = item_dropar,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0)))
        
    @classmethod
    def GoblinArqueiro(cls, multiplicadores: Dict[str, float]) -> Inimigo:
        ataque_base = 10
        defesa_base = 10
        vida_base = 100
        xp_base = 10 # definir recompensa de xp futura
        
        drop_chance = random.random() < 0.7
        item_dropar = Item(
            nome = "Bandagem Simples", 
            tipo = "Consumível", 
            efeito_quant = 10, 
            efeito_atributo = "vida"
        ) if drop_chance else None
        
        return cls(
            nome = "Goblin Arqueiro",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            item_drop = item_dropar,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0))
        )

    @classmethod
    def GoblinMago(cls, multiplicadores: Dict[str, float]) -> Inimigo:
        ataque_base = 20
        dano_verdadeiro_base = 25
        defesa_base = 10
        vida_base = 100
        xp_base = 10

        drop_chance = random.random() < 0.3
        
        item_dropar = Item(
            nome = "Poção de Cura",
            tipo = "Consumível",
            efeito_quant = 25,
            efeito_atributo = "vida"
        ) if drop_chance else None
        """
        item_dropar = Item(
            nome="Poção de Mana", 
            tipo="Consumível", 
            efeito_quant=10, 
            efeito_atributo="mana"
        ) if drop_chance else None
        """
        return cls(
            nome = "Goblin Mago",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            dano_verdadeiro_perc = int(dano_verdadeiro_base * multiplicadores.get("dano_verdadeiro",1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            item_drop = item_dropar,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0))
        )
    
    @classmethod
    def GoblinEscudeiro(cls, multiplicadores: Dict[str, float]) -> Inimigo:
        ataque_base = 3
        vida_base = 100
        defesa_base = 20
        xp_base = 10 # definir recompensa de xp futura

        drop_chance = random.random() < 0.7
        item_dropar = Item(
            nome="Bandagem Simples", 
            tipo="Consumível", 
            efeito_quant=10, 
            efeito_atributo="vida"
        ) if drop_chance else None
        
        return cls(
            nome = "Goblin Escudeiro",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            item_drop = item_dropar,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0))
        )

    # atributos_GoblinGrandao = Inimigo(
    #     nome = "Goblin Grandão",
    #     ataque = # em definição
    #     defesa = # em definição
    #     vida = # em definição
    #     habilidade especial(buscar atributo para utilziar habilidade especial em 'Entidades')
    #     recompensa_xp = # definir recompensa de xp futura
    # )
