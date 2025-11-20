from __future__ import annotations
from .base import Entidade, Atributos, Item
from .personagem import Personagem
from typing import Dict, Optional, Union, Tuple
import math
import random

class Inimigo(Entidade):
    """
    Inimigo genérico.
    Sem IA/variações — apenas o contêiner para atributos básicos.
    """

    from typing import List, Optional

    def __init__(self, nome: str, vida: int, ataque: int, defesa: int, recompensa_xp: int, itens_drop: Optional[List[Item]] = None, dano_verdadeiro_perc: int = 0, nivel: int = 1):
        super().__init__(nome, Atributos(
            vida=vida, ataque=ataque, defesa=defesa, vida_max=vida, recompensa_xp=recompensa_xp, dano_verdadeiro_perc=dano_verdadeiro_perc
        ))
        self.xp_drop = recompensa_xp
        self.itens_drop = itens_drop or []
        self.nivel = nivel

    def calcular_dano_base(self) -> Tuple[int, int]:
        """Implementa um cálculo de dano para o inimigo com variação e Dano Verdadeiro."""
        dano_base = self._atrib.ataque
        variacao = random.randint(0, 2)
        dano_total = max(1, dano_base + variacao)
        
        # 1. Divide o dano total em Dano Verdadeiro e Dano Normal
        dano_verdadeiro = int(dano_total * (self._atrib.dano_verdadeiro_perc / 100))
        dano_normal = dano_total - dano_verdadeiro
        
        return dano_normal, dano_verdadeiro

    @staticmethod
    def _calcular_multiplicador_nivel(nivel: int) -> float: # NOVO MÉTODO
        """
        Calcula o multiplicador de atributos com base no nível.
        Progressão suave: 1 + (nivel - 1) * 0.15 (15% de aumento por nível após o 1).
        """
        if nivel <= 1:
            return 1.0
        
        # Aumento de 15% por nível (ex: Nv 2 = 1.15, Nv 5 = 1 + 4 * 0.15 = 1.6)
        return 1.0 + (nivel - 1) * 0.15
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
    def GoblinNormal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:#recebe multiplicaderes de difuculdade(0.8, 1.0, 1.2...) e nivel do inimigo como int (1, 2, 3...)
        vida_base = 100
        ataque_base = 5
        defesa_base = 10
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Goblin Normal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    @classmethod
    def Goblincotoco(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 1
        defesa_base = 40
        vida_base = 100
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]
        mult_nivel = cls._calcular_multiplicador_nivel(nivel)
        return cls( 
            nome = "Goblin cotoco",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 2)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    @classmethod
    def GoblinArqueiro(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 10
        defesa_base = 10
        vida_base = 100
        xp_base = 40
        
        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Goblin Arqueiro",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    @classmethod
    def GoblinMago(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 20
        dano_verdadeiro_base = 25
        defesa_base = 10
        vida_base = 100
        xp_base = 50

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Goblin Mago",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) + (nivel * 5)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            dano_verdadeiro_perc = int(dano_verdadeiro_base * multiplicadores.get("dano_verdadeiro",1.0) + (nivel * 1)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 1)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def GoblinEscudeiro(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 3
        vida_base = 100
        defesa_base = 20
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)
        
        return cls(
            nome = "Goblin Escudeiro",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    

    # --- Cenário Trilha ---

    @classmethod
    def BandidodaTrilha(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 1
        defesa_base = 40
        vida_base = 100
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls( 
            nome = "Bandido da Trilha",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 2)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    
    @classmethod
    def LoboFerozdaTrilha(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        vida_base = 100
        ataque_base = 5
        defesa_base = 10
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Lobo Feroz da Trilha",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def DruidaImpurodaTrilha(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 20
        dano_verdadeiro_base = 25
        defesa_base = 10
        vida_base = 100
        xp_base = 50

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Druida Impuro da Trilha",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) + (nivel * 5)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            dano_verdadeiro_perc = int(dano_verdadeiro_base * multiplicadores.get("dano_verdadeiro",1.0) + (nivel * 1)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 1)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    
    @classmethod
    def GuardiaoEspinhosodaTrilha(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 10
        defesa_base = 10
        vida_base = 100
        xp_base = 40
        
        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Guardião Espinhoso da Trilha",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )


    @classmethod
    def GolemdaTrilha(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 3
        vida_base = 100
        defesa_base = 20
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)
        
        return cls(
            nome = "Golem da Trilha",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    

    # --- Cenário Caverna ---

    @classmethod
    def MorcegoCavernal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 1
        defesa_base = 40
        vida_base = 100
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls( 
            nome = "Morcego Cavernal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 2)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    

    @classmethod
    def AranhaCavernal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        vida_base = 100
        ataque_base = 5
        defesa_base = 10
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Aranha Cavernal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def EsqueletoBalisticoCavernal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 10
        defesa_base = 10
        vida_base = 100
        xp_base = 40
        
        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Esqueleto Balístico Cavernal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def XamaCavernal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 20
        dano_verdadeiro_base = 25
        defesa_base = 10
        vida_base = 100
        xp_base = 50

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Xamã Cavernal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) + (nivel * 5)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            dano_verdadeiro_perc = int(dano_verdadeiro_base * multiplicadores.get("dano_verdadeiro",1.0) + (nivel * 1)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 1)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def BarbadoCavernal(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 3
        vida_base = 100
        defesa_base = 20
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)
        
        return cls(
            nome = "Barbaro Cavernal",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    

    # --- Cenário Ruínas ---

    @classmethod
    def EsqueletodasRuinas(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 1
        defesa_base = 40
        vida_base = 100
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls( 
            nome = "Esqueleto das Ruínas",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 2)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )

    @classmethod
    def FantasmadasRuinas(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        vida_base = 100
        ataque_base = 5
        defesa_base = 10
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Fantasma das Ruínas",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def AtiradorEnferrujadodasRuinas(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 10
        defesa_base = 10
        vida_base = 100
        xp_base = 40
        
        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Atirador Enferrujado das Ruínas",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def GeomantedasRuinas(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 20
        dano_verdadeiro_base = 25
        defesa_base = 10
        vida_base = 100
        xp_base = 50

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)

        return cls(
            nome = "Geomante das Ruínas",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) + (nivel * 5)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            dano_verdadeiro_perc = int(dano_verdadeiro_base * multiplicadores.get("dano_verdadeiro",1.0) + (nivel * 1)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) + (nivel * 1)),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )
    
    @classmethod
    def GarguladasRuinas(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        ataque_base = 3
        vida_base = 100
        defesa_base = 20
        xp_base = 30

        lista_de_possiveis_drops = [
            Item("Poção de Cura Menor", "Consumível", 35, "vida"),
            Item("Poção de Cura Maior", "Consumível", 50, "vida"),
            Item("Bandagem Simples", "Consumível", 20, "vida"),
            # Adicione mais se quiser!
        ]

        mult_nivel = cls._calcular_multiplicador_nivel(nivel)
        
        return cls(
            nome = "Gargula das Ruínas",
            vida = int(vida_base * multiplicadores.get("vida", 1.0) * mult_nivel),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0) * mult_nivel),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0) * mult_nivel),
            itens_drop = lista_de_possiveis_drops,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0) * mult_nivel),
            nivel = nivel
        )


    @classmethod
    def ReiDoBostil(cls, multiplicadores: Dict[str, float], nivel) -> Inimigo:
        vida_base = 800
        ataque_base = 35
        defesa_base = 20
        xp_base = 500
        
        return cls(
            nome = "Globin",
            vida = int(vida_base * multiplicadores.get("vida", 1.0)),
            ataque = int(ataque_base * multiplicadores.get("ataque", 1.0)),
            defesa = int(defesa_base * multiplicadores.get("defesa", 1.0)),
            itens_drop = None,
            recompensa_xp = int(xp_base * multiplicadores.get("xp", 1.0))
        )
    
    def atacar_especial(self, alvo: Personagem) -> int:
        """
        Ataque especial do Boss que aplica Sangramento.
        Este ataque sempre acerta, mas não é um dano altíssimo.
        """
        # Dano base do ataque especial
        dano_base = int(self._atrib.ataque * 1)
        dano_variacao = random.randint(0, 5)
        dano_final = max(1, dano_base + dano_variacao)
        
        # O dano é aplicado como dano normal (reduzido pela defesa do Personagem)
        dano_recebido = alvo.receber_dano(dano_final)
        
        # Aplica o efeito de Sangramento
        # Sangramento padrão: 10 de dano por turno, duração de 2 turnos
        dano_sangramento = 10
        duracao = 2

        print(f"** {self.nome} usa ATAQUE SANGRENTO! {alvo.nome} recebe {dano_recebido} de dano! **")

        alvo.aplicar_sangramento(dano_sangramento, duracao)
        
        
        return dano_recebido