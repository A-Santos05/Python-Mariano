from typing import TYPE_CHECKING

# Importar apenas para checagem de tipos, evitando importação circular
if TYPE_CHECKING:
    from models.personagem import Personagem

class Efeito:
    """Classe base para todos os efeitos temporários (buffs)."""
    
    def __init__(self, nome: str, duracao_max: int):
        self.nome = nome
        # Duração em turnos. A contagem regressiva começa no final do turno.
        self.duracao_atual = duracao_max 
    
    def aplicar(self, alvo: 'Personagem'):
        """Aplica o efeito no personagem. Implementado nas subclasses."""
        pass

    def remover(self, alvo: 'Personagem'):
        """Remove o efeito do personagem. Implementado nas subclasses."""
        pass
        
    def decrementar(self) -> bool:
        """Decrementa a duração do efeito e retorna True se expirou."""
        self.duracao_atual -= 1
        return self.duracao_atual <= 0

    def __repr__(self) -> str:
        return f"<{self.nome}: {self.duracao_atual} turnos>"

# --- Efeitos Específicos de Classe ---

class EscudoDeGuerra(Efeito):
    """Guerreiro: Aumenta a defesa por 2 turnos."""
    
    def __init__(self):
        super().__init__("Escudo de Guerra", 2)
        self.bonus_defesa = 5 # Valor fixo de aumento de defesa
        
    def aplicar(self, alvo: 'Personagem'):
        # Aplicamos o bônus diretamente nos atributos.
        # Ele é removido em 'remover'.
        alvo._atrib.defesa += self.bonus_defesa

    def remover(self, alvo: 'Personagem'):
        # Removemos o bônus, restaurando o valor original de defesa.
        alvo._atrib.defesa -= self.bonus_defesa
        print(f"[{alvo.nome}]: Efeito Escudo de Guerra expirou.")

class TransfusaoArcana(Efeito):
    """Mago: Aumenta a conversão de ATK para dano verdadeiro por 2 turnos."""
    
    def __init__(self):
        super().__init__("Transfusão Arcana", 2)
        self.bonus_conversao = 200 #Funciona como o dano critico, se 25% vira TRUE DMG, se o bonus_conversao for 100, TRUE DMG vai continuar como 25%, 200 vira 50% de TRUE DMG
        
    def aplicar(self, alvo: 'Personagem'):
        # Não muda o atributo diretamente, pois o cálculo está em Personagem.calcular_dano_base()
        pass

    def remover(self, alvo: 'Personagem'):
        print(f"[{alvo.nome}]: Efeito Transfusão Arcana expirou.")

class FocoDoCacador(Efeito):
    """Arqueiro: Aumenta chance e dano crítico por 2 turnos."""
    
    def __init__(self):
        super().__init__("Foco do Caçador", 2)
        self.bonus_chance_crit = 20 # +20% de chance crítica
        self.bonus_dano_crit = 50 # +50% de dano crítico
        
    def aplicar(self, alvo: 'Personagem'):
        # Não muda o atributo diretamente, o cálculo está em Personagem.calcular_dano_base()
        pass

    def remover(self, alvo: 'Personagem'):
        print(f"[{alvo.nome}]: Efeito Foco do Caçador expirou.")