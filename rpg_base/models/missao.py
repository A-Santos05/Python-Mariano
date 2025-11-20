from __future__ import annotations
from dataclasses import dataclass
from .base import Entidade
from .personagem import Personagem
from .inimigo import Inimigo
import random
import time

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
        
        print(f"\n=== Missão: {self.titulo} ===\n")
        print(f"{p.nome} [Lvl {p.nivel}] VS {i.nome} [Lvl {i.nivel}]")

        # --- Loop Principal do Combate ---
        turno = 1
        while p.vivo and i.vivo:
            print(f"\n======= Turno {turno} =======\n")
            
            p.processar_sangramento()
            self._decrementar_efeitos(p)

            # 1. PERSONAGEM ATACA INIMIGO
            # Chamada ao método que você deve implementar em Personagem
            habilidade_usada = False
            acao_realizada = False
            while not acao_realizada:
                print("======== Status =======")
                print(f"{p.nome} | Nível {p.nivel}")
                print(f"HP: {p.barra_hp(10)}")
                print(f"MANA: {p.barra_mana(10)}")
                print(f"ATK: {p._atrib.ataque} | DEF: {p._atrib.defesa}")
                if p.efeitos_ativos:
                    if p.efeitos_ativos[0].duracao_atual > 0:
                        print("======= Efeitos =======")
                        for e in p.efeitos_ativos:
                                print(f"[{e.nome}] {e.duracao_atual} turno(s) restante(s)")
                    #print(f"{[e.nome for e in p.efeitos_ativos]}")
                print("======== Ações ========")
                print("[1] Atacar")
                print(f"[2] Habilidade Especial {p._atrib.mana} / {p._atrib.mana_pool}")
                print("[3] Usar item")
                print("[4] Inspecionar Inimigo")
                print("=======================")
                acao = input("> ").strip()

                if acao == "1":#Atacar
                    # O Personagem.calcular_dano_base() agora retorna (dano_normal, dano_verdadeiro)
                    dano_personagem_tuple = p.calcular_dano_base() 
                    
                    # Chamada ao método de Entidade/Inimigo para cálculo de dano
                    dano_recebido_inimigo = i.receber_dano(dano_personagem_tuple)
                    
                    print(f"{p.nome} ataca! {i.nome} recebe {dano_recebido_inimigo} de dano.")
                    print(f"HP {i.nome}: {i.barra_hp(10)}")
                    acao_realizada = True

                elif acao == "2":#Habilidade Especial
                    if p._atrib.mana >= p._atrib.special_cost and habilidade_usada == False:#Verifica se o personagem tem mana suficiente
                        p._atrib.mana -= p._atrib.special_cost#Gasta a mana da habilidade especial
                        p.habilidade_especial()
                        #print(f"{p.nome} usou [{habilidade_nome}]")
                        habilidade_usada = True
                        
                    elif habilidade_usada == True:
                        print(f"{p.nome} já usou a habilidade especial nesta luta!")

                    else:
                        print(f"{p.nome} não tem mana suficiente para usar a habilidade especial!")

                elif acao == "3":#Usar item
                    # --- IMPLEMENTAÇÃO DO INVENTÁRIO DE BATALHA ---
                    if not p.inventario:
                        print("\nSeu inventário está vazio!")
                        continue # Volta para o menu de ações
                    
                    # Filtra apenas consumíveis para combate
                    consumiveis = [item for item in p.inventario if item.tipo == "Consumível"]
                    
                    if not consumiveis:
                        print("\nVocê não tem itens usáveis em combate!")
                        continue

                    print("\n--- Escolha um item ---")
                    # Agrupa itens por nome para exibição
                    nomes_unicos = sorted(list(set(i.nome for i in consumiveis)))
                    
                    for idx, nome_item in enumerate(nomes_unicos):
                        qtd = len([x for x in consumiveis if x.nome == nome_item])
                        # Pega o primeiro para ver descrição
                        ref = next(x for x in consumiveis if x.nome == nome_item) 
                        print(f"[{idx + 1}] {nome_item} (x{qtd}) - Cura {ref.efeito_quant} {ref.efeito_atributo}")
                    
                    print("[0] Voltar")
                    
                    escolha_item = input("> ").strip()
                    
                    if escolha_item == "0":
                        print("Cancelado.")
                        continue # Volta para o menu de ações sem gastar turno
                    
                    try:
                        idx_escolhido = int(escolha_item) - 1
                        if 0 <= idx_escolhido < len(nomes_unicos):
                            nome_para_usar = nomes_unicos[idx_escolhido]
                            # Tenta usar o item usando o método da classe Personagem
                            usou = p.usar_item(nome_para_usar) #
                            if usou:
                                acao_realizada = True # Sucesso! O turno passa.
                        else:
                            print("Opção inválida.")
                    except ValueError:
                        print("Digite um número válido.")
   
                elif acao == "4":#Inspecionar Inimigo
                    print(f"===== {i.nome} =====")
                    print(f"HP {i.nome}: {i.barra_hp(10)}")
                    print(f"Ataque: {i._atrib.ataque}")
                    print(f"Defesa: {i._atrib.defesa}")
                    
                    if i._atrib.dano_verdadeiro_perc > 0:
                        print(f"Dano Verdadeiro (%): {i._atrib.dano_verdadeiro_perc}%")
                
                else:
                    print("Ação inválida.")
            
            if p._atrib.mana < p._atrib.mana_pool:#Verifica se o personagem pode regenerar mana
                if (p._atrib.mana + p._atrib.mana_regen) > p._atrib.mana_pool:#Evita que a mana ultrapasse o limite
                    p._atrib.mana = p._atrib.mana_pool
                else:
                    p._atrib.mana += p._atrib.mana_regen#Regenera mana a cada ataque normal

            time.sleep(2)# Pequena pausa para melhor leitura
            
            if not i.vivo:
                break

            print("\n===== Turno do inimigo =====")
            #print("Inimigo ainda vivo")
            #Lógica para o ataque especial do REI DO BOSTIL
            if i.nome == "Globin":
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
                
            self._decrementar_efeitos(i)
            print(f"HP {p.nome}: {p.barra_hp(10)}")
            #print(f"Efeitos: {p.efeitos_ativos}")

            if not p.vivo:
                break
       
            turno += 1

            input("\nPressione Enter para o próximo turno...")

        if not i.vivo:
            print("=============Vitória!=============")
            print(f"{i.nome} foi derrotado!")
            print("==================================")

        if not p.vivo:
            print("=============Derrota!=============")
            print(f"{p.nome} foi derrotado!")
            print("==================================")

        time.sleep(2)# Pequena pausa para melhor leitura

        p.limpar_efeitos(ao_final_da_luta=True)
        i.limpar_efeitos(ao_final_da_luta=True)
                
        # --- Resultado Final ---
        if p.vivo:
            print(f"\n{p.nome} concluiu a missão {self.titulo}.\n")
            
            xp_ganho = i.xp_drop # Pega o XP que o inimigo dropa (definido em Inimigo)
            p.ganhar_xp(xp_ganho)

            time.sleep(2)# Pequena pausa para melhor leitura


            if i.itens_drop:
                item_sorteado = random.choice(i.itens_drop)
                print("\n=================LOOT=================")
                print(f"{p.nome} coletou: {item_sorteado.nome}")
                print("======================================")
                
                p.coletar_item(item_sorteado)

                time.sleep(2)# Pequena pausa para melhor leitura

            return ResultadoMissao(venceu=True, detalhes=f"{i.nome} foi derrotado.")
        
        else:
            print(f"{p.nome} falhou na missão {self.titulo}.")
            return ResultadoMissao(venceu=False, detalhes=f"{p.nome} foi derrotado por {i.nome}.")
        
    time.sleep(2)# Pequena pausa para melhor leitura
        
    def _decrementar_efeitos(self, entidade: Entidade): # NOVO MÉTODO AUXILIAR
        """Decrementa a duração dos efeitos ativos e remove os que expiraram."""
        efeitos_expirados = []
        for efeito in list(entidade.efeitos_ativos):
            if efeito.decrementar():
                efeito.remover(entidade) # Chamada para remover (restaurar atributos, etc.)
                efeitos_expirados.append(efeito)
    
        # Remove os efeitos expirados da lista
        for efeito in efeitos_expirados:
            entidade.efeitos_ativos.remove(efeito)