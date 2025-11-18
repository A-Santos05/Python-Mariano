from __future__ import annotations
from dataclasses import dataclass, asdict
from .efeitos import Efeito
from typing import List, Dict, Any
import math

@dataclass
#Classe para representar um Item
class Item:
    nome: str
    tipo: str # Ex: "Consumível", "Equipamento"
    efeito_quant: int # Ex: 30 para 30 HP
    efeito_atributo: str = "" # Ex: "vida", "ataque", etc.    

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Item:
        return cls(**data)

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
    sangramento_dano: int = 0
    sangramento_duracao: int = 0

class Entidade:
    """Base para Personagem e Inimigo (sem regras avançadas)."""

    def __init__(self, nome: str, atrib: Atributos):
        self._nome = nome
        if atrib.vida_max is None:
            atrib.vida_max = atrib.vida
        self._atrib = atrib
        self.efeitos_ativos: List[Efeito] = []

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
        """Barra de HP"""
        v = max(0, self._atrib.vida)
        vmax = max(1, self._atrib.vida_max)
        cheio = int(largura * v / vmax)
        return "[" + " ❤️ " * cheio + " ♡ " * (largura - cheio) + f"] {v}/{vmax} HP"

    def barra_mana(self, largura: int = 20) -> str:
        """Barra de MANA"""
        m = max(0, self._atrib.mana)
        m_max = max(1, self._atrib.mana_pool)
        cheio = int(largura * m / m_max)
        return "[" + " 💧 " * cheio + "-" * (largura - cheio) + f"] {m}/{m_max} MP"

    def aplicar_efeito(self, efeito: Efeito):
        """Adiciona um efeito, aplicando-o."""
        # Se o efeito já estiver ativo, você pode re-aplicá-lo (resetar a duração)
        # ou apenas ignorar. Aqui, vamos re-aplicar e remover o antigo (se houver)
        for e in self.efeitos_ativos:
            if e.nome == efeito.nome:
                e.remover(self) # Chama o método 'remover' do efeito
                self.efeitos_ativos.remove(e)
                break

        self.efeitos_ativos.append(efeito)
        efeito.aplicar(self)
        print(f"[{self.nome}]: {efeito.nome} aplicado por {efeito.duracao_atual} turnos.")

    def limpar_efeitos(self, ao_final_da_luta: bool = False):
        """Remove todos os efeitos ativos, restaurando os atributos."""
        # Apenas remove se a flag for True (no final da luta) ou se o efeito já expirou (em Missao.executar)
        if ao_final_da_luta:
            for efeito in list(self.efeitos_ativos): # Cria uma cópia para iterar
                efeito.remover(self)
            self.efeitos_ativos.clear()
            print(f"[{self.nome}]: Todos os efeitos removidos.") # Opcional