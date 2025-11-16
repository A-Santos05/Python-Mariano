from __future__ import annotations
from dataclasses import dataclass
from .personagem import Personagem
from .inimigo import Inimigo
import random

@dataclass
class ResultadoMissao:
    """Resultado ilustrativo (placeholder)."""
    venceu: bool = False
    detalhes: str = "Missão simulada."


class Missao:
    """
    Estrutura da missão sem a mecânica de combate.
    Mantém a assinatura para futura integração com o jogo completo.
    """

    def __init__(self, titulo: str, inimigo: Inimigo):
        self.titulo = titulo
        self.inimigo = inimigo

    def executar(self, p: Personagem) -> ResultadoMissao:
        """
        Execução da missão: Combate Turno-a-Turno Simples.
        """
        # Verifica se o personagem está pronto para lutar
        if not p.vivo:
            return ResultadoMissao(venceu=False, detalhes=f"{p.nome} está esgotado.")
        
        # --- Configuração Inicial ---
        
        # Re-cria o inimigo (opcional) para garantir que comece com HP cheio. 
        # Ou simplesmente garante que self.inimigo esteja com vida máxima.
        # Aqui, vamos assumir que self.inimigo é a instância para o combate.
        i = self.inimigo
        i._atrib.vida = i._atrib.vida_max # Garante HP cheio no início do combate
        
        print(f"\n=== Missão: {self.titulo} ===")
        print(f"O combate entre {p.nome} (Lvl {p.nivel}) e {i.nome} (HP: {i._atrib.vida} DEF: {i._atrib.defesa} ATK: {i._atrib.ataque}) começa!")

        # --- Loop Principal do Combate ---
        turno = 1
        while p.vivo and i.vivo:
            print(f"\n--- Turno {turno} ---")
            
            p.processar_sangramento()

            # 1. PERSONAGEM ATACA INIMIGO
            # Chamada ao método que você deve implementar em Personagem
            try:
                # O Personagem.calcular_dano_base() agora retorna (dano_normal, dano_verdadeiro)
                dano_personagem_tuple = p.calcular_dano_base() 
                
                # Chamada ao método de Entidade/Inimigo para cálculo de dano
                dano_recebido_inimigo = i.receber_dano(dano_personagem_tuple)
                
                if p._atrib.mana < p._atrib.mana_pool:#Calculo de regeneração de mana
                    if p._atrib.mana + p._atrib.mana_regen > p._atrib.mana_pool:
                        p._atrib.mana = p._atrib.mana_pool
                    else:
                        p._atrib.mana += p._atrib.mana_regen

                if p._atrib.mana >= p._atrib.special_cost:#Implementar uso de habilidade especial
                    p._atrib.mana -= p._atrib.special_cost
                    print(f"{p.nome} usou a habilidade especial!")#Habilidade especial ainda não foi implementada apenas placeholder
                
                print(f"{p.nome} ataca! {i.nome} recebe {dano_recebido_inimigo} de dano.")
                print(f"MANA: {p._atrib.mana}/{p._atrib.mana_pool}")
                print(f"HP {i.nome}: {i.barra_hp(10)}")

            except NotImplementedError:
                print("ERRO: Implemente Personagem.calcular_dano_base() primeiro.")
                return ResultadoMissao(venceu=False, detalhes="Combate interrompido por erro de implementação.")
            
            if not i.vivo:
                print("Inimigo morreu")
                break

            print("Inimigo ainda vivo")
            # NOVO: Lógica para o ataque especial do Goblin Grandão
            if i.nome == "Globi":
                # 30% de chance para o ataque especial de Sangramento
                chance_especial = 0.3
                if random.random() < chance_especial:
                    # Se for Boss e a chance de ataque especial ocorrer
                    dano_recebido_personagem = i.atacar_especial(p)
                else:
                    # Se for Boss, mas o ataque especial falhar, faz o ataque normal
                    dano_inimigo = i.atacar()
                    dano_recebido_personagem = p.receber_dano(dano_inimigo)
                    print(f"{i.nome} ataca normalmente! {p.nome} recebe {dano_recebido_personagem} de dano.")
            else:
                # 2. INIMIGO ATACA PERSONAGEM
                
                # Usamos o método 'atacar' da classe Entidade (método base simples)
                dano_inimigo = i.atacar()
                # O Personagem.receber_dano (que herda de Entidade) ainda espera um 'int' de dano normal
                dano_recebido_personagem = p.receber_dano(dano_inimigo)
                
                print(f"{i.nome} revida! {p.nome} recebe {dano_recebido_personagem} de dano.")

            print(f"HP {p.nome}: {p.barra_hp(10)}")

            if not p.vivo:
                print("Personagem morreu")
                break
            print("Personagem ainda vivo")       
            turno += 1
                # Adicionar um pequeno delay ou pausa aqui se fosse um jogo real

            if not i.vivo:
                break
                
            # 2. INIMIGO ATACA PERSONAGEM
            
            # Usamos o método 'atacar' da classe Entidade (método base simples)
            dano_inimigo = i.atacar()
            # O Personagem.receber_dano (que herda de Entidade) ainda espera um 'int' de dano normal
            dano_recebido_personagem = p.receber_dano(dano_inimigo)
            
            print(f"{i.nome} revida! {p.nome} recebe {dano_recebido_personagem} de dano.")
            print(f"HP {p.nome}: {p.barra_hp(10)}")

            if not p.vivo:
                break
                
            turno += 1
            # Adicionar um pequeno delay ou pausa aqui se fosse um jogo real

        if not i.vivo:
            print("=============Vitória!=============")
            print(f"{i.nome} foi derrotado!")
            print("==================================")

        if not p.vivo:
            print("=============Derrota!=============")
            print(f"{p.nome} foi derrotado!")
            print("==================================")
                
        # --- Resultado Final ---
        if p.vivo:
            print(f"\n{p.nome} concluiu a missão {self.titulo}.\n")
            
            xp_ganho = i.xp_drop # Pega o XP que o inimigo dropa (definido em Inimigo)
            p.ganhar_xp(xp_ganho)
            # Lógica de XP/Recompensa aqui

            if i.itens_drop:
                item_sorteado = random.choice(i.itens_drop)
                print(f"{p.nome} ganhou o item: {item_sorteado.nome}")
                p.coletar_item(item_sorteado)

            return ResultadoMissao(venceu=True, detalhes=f"{p.nome} derrotou {i.nome}.")
        else:
            print(f"{p.nome} falhou na missão {self.titulo}.")
            return ResultadoMissao(venceu=False, detalhes=f"{p.nome} foi derrotado por {i.nome}.")