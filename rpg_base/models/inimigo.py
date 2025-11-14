from __future__ import annotations
from .base import Entidade, Atributos, Item
from typing import Dict, Any, Optional
import math
import random

class Inimigo(Entidade):
    """
    Inimigo genérico.
    Sem IA/variações — apenas o contêiner para atributos básicos.
    """

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int, recompensa_xp: int, item_drop: Optional[Item] = None):
        super().__init__(nome, Atributos(
            vida=vida, ataque=ataque, defesa=defesa, vida_max=vida, recompensa_xp=recompensa_xp
        ))
        self.xp_drop = recompensa_xp
        self.item_drop = item_drop

    def atacar(self) -> int: #Sobrepondo o método atacar da classe Entidade
        """Implementa um ataque simples com variação de dano."""
        dano_base = self._atrib.ataque
        variacao = random.randint(-2, 2)  # Variação simples de dano pra mais ou pra menos
        dano_final = max(1, dano_base + variacao)
        return dano_final
    
    def receber_dano(self, dano: int) -> int:
        return super().receber_dano(dano)

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
            nome="Poção de Cura Menor", 
            tipo="Consumível", 
            efeito_quant=30, 
            efeito_atributo="vida"
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
            nome="Bandagem Simples", 
            tipo="Consumível", 
            efeito_quant=10, 
            efeito_atributo="vida"
        ) if drop_chance else None
        
        return cls(
            nome = "Goblin Arqueiro",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            item_drop = item_dropar,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0))
        )

    """
    def GoblinMago(cls) -> Inimigo:
        return cls(
        nome = "Goblin Mago",
       # ataque = implementar ataque mágico futuramente (ataque de dano verdadeiro)
        defesa  = 15,
        vida = 100, # podendo diminuir a vida com base no ataque mágico em definição
        recompensa_xp = 0# definir recompensa de xp futura
    )
    """
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
