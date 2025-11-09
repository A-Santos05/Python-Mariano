from __future__ import annotations
from .base import Entidade, Atributos
import random

class Inimigo(Entidade):
    """
    Inimigo genérico.
    Sem IA/variações — apenas o contêiner para atributos básicos.
    """

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int, recompensa_xp: int):
        super().__init__(nome, Atributos(vida=vida, ataque=ataque, defesa=defesa, vida_max=vida))
        self.xp_drop = recompensa_xp # Experiência concedida ao jogador ao derrotar o inimigo

    def atacar(self) -> int: #Sobrepondo o método atacar da classe Entidade
        """Implementa um ataque simples com variação de dano."""
        dano_base = self._atrib.ataque
        variacao = random.randint(-2, 2)  # Variação simples de dano pra mais ou pra menos
        dano_final = max(1, dano_base + variacao)
        self.receber_dano(dano_final) # É necessário?
        return dano_final
    
    def receber_dano(self, dano: int) -> int:
        return super().receber_dano(dano)

    # Pendente definir metodo e recber dano/defesa e sobrepor o metodo receber dano da classe Entidade
    
    """Definições de atributos para inimigos específicos"""

    @classmethod
    def GoblinNormal(cls) -> Inimigo:
       return cls(
        nome = "Goblin Normal",
        vida = 100,
        ataque = 5,
        defesa = 10,
        recompensa_xp = 0 # definir recompensa de xp futura
    )
    
    @classmethod
    def GoblinArqueiro(cls) -> Inimigo:
        return cls(
        nome = "Goblin Arqueiro",
        ataque = 10,
        defesa = 10,
        vida = 100,
        recompensa_xp = 0 # definir recompensa de xp futura
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
    def GoblinEscudeiro(cls) -> Inimigo:
        return cls(
        nome = "Goblin Escudeiro",
        ataque = 3,
        vida = 100,
        defesa = 20,
        recompensa_xp = 0 # definir recompensa de xp futura
    )
    # atributos_GoblinGrandao = Inimigo(
    #     nome = "Goblin Grandão",
    #     ataque = # em definição
    #     defesa = # em definição
    #     vida = # em definição
    #     habilidade especial(buscar atributo para utilziar habilidade especial em 'Entidades')
    #     recompensa_xp = # definir recompensa de xp futura
    # )
