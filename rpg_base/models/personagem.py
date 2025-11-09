from __future__ import annotations
from .base import Entidade, Atributos
import random

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

    def calcular_dano_base(self) -> int:
        """
        Implementação simples: Ataque base + aleatoriedade, ignorando crítico por enquanto.
        """
        # Vamos simular um dano que varia entre 80% e 120% do ATK base
        #dano_min = int(self._atrib.ataque * 0.8)
        #dano_max = int(self._atrib.ataque * 1.2)
        
        # O dano real que será usado como entrada para o 'receber_dano' do Inimigo
        #dano_base = random.randint(dano_min, dano_max)
        dano_critico = random.random() * 100 < self._atrib.crit_chance
        dano_base = self._atrib.ataque  # Implementação simplificada inicial
        dano_final = dano_base
        if dano_critico:
            multiplicador_critico = self._atrib.crit_dmg / 100
            dano_final = int(dano_base * multiplicador_critico)
            print(f"{self.nome} acerta um crítico!")
        return dano_final

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
