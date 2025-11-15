from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass

#Classe para representar um Item
class Item:
    nome: str
    tipo: str # Ex: "Consumível", "Equipamento"
    efeito_quant: int # Ex: 30 para 30 HP
    efeito_atributo: str = "" # Ex: "vida", "ataque", etc.

@dataclass
class Atributos:
    """Estrutura simples de atributos."""
    vida: int
    ataque: int
    defesa: int
    dano_verdadeiro_perc: int = 0
    crit_chance: int = 0
    crit_dmg: int = 100
    mana: int = 0
    mana_pool: int = 0
    mana_regen: int = 0
    special_cost: int = 0
    xp: int = 0
    recompensa_xp: int = 0
    vida_max: int | None = None

class Entidade:
    """Base para Personagem e Inimigo (sem regras avançadas)."""

    def __init__(self, nome: str, atrib: Atributos):
        self._nome = nome
        if atrib.vida_max is None:
            atrib.vida_max = atrib.vida
        self._atrib = atrib

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def vivo(self) -> bool:
        return self._atrib.vida > 0

    def atacar(self) -> int:
        """Ataque base fixo (placeholder)."""
        return self._atrib.ataque

    def receber_dano(self, dano: int) -> int:
        efetivo = max(1, dano - math.ceil(dano * (self._atrib.defesa / 100)))
        self._atrib.vida = max(0, self._atrib.vida - efetivo)

        return efetivo

    def barra_hp(self, largura: int = 20) -> str:
        """Barra de HP meramente visual (placeholder)."""
        v = max(0, self._atrib.vida)
        vmax = max(1, self._atrib.vida_max)
        cheio = int(largura * v / vmax)
        return "[" + " ❤️ " * cheio + " ♡ " * (largura - cheio) + f"] {v}/{vmax} HP"

