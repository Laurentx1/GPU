"""
=== ANTI GPU SPIN - VERSÃO 3.3 TIMING CORRIGIDO ===
CORREÇÃO CRÍTICA:
- Corrigida lógica de temporização
- Agora monitora REAL tempo de inatividade
- Executa ação apenas quando realmente necessário
- Sistema de timing mais preciso
"""

import pyautogui
import time
import random
import os
import threading
from datetime import datetime
import sys

# ========================================
# CONFIGURAÇÕES PRINCIPAIS
# ========================================
VERSAO = "3.3 - TIMING CORRIGIDO"
TEMPO_INATIVIDADE_MAX = 120  # 2 minutos = 120 segundos
INTERVALO_CHECK = 2.0  # Verifica a cada 2 segundos
TOLERANCIA_MOVIMENTO = 3  # Pixels mínimos para considerar movimento
MOSTRAR_STATUS_APOS = 30  # Só mostra status após 30s de inatividade

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Variáveis globais
programa_rodando = True
posicao_anterior = None
timestamp_ultima_atividade = None
contador_movimentos = 0
lock = threading.Lock()

# ========================================
# FUNÇÕES AUXILIARES
# ========================================
def log_com_tempo(mensagem):
    """Log com timestamp preciso"""
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {mensagem}")

def obter_posicao_mouse():
    """Obtém posição do mouse com segurança"""
    try:
        return pyautogui.position()
    except:
        return None

def calcular_distancia(pos1, pos2):
    """Calcula distância entre duas posições"""
    if not pos1 or not pos2:
        return 0
    return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2) ** 0.5

def executar_movimento_preventivo():
    """Executa o movimento preventivo"""
    global contador_movimentos
    
    with lock:
        contador_movimentos += 1
        num_movimento = contador_movimentos
    
    log_com_tempo(f"🎯 EXECUTANDO MOVIMENTO PREVENTIVO #{num_movimento}")
    
    try:
        # Salva posição atual
        pos_inicial = obter_posicao_mouse()
        if not pos_inicial:
            log_com_tempo("❌ Erro: não conseguiu obter posição inicial")
            return False
        
        # Calcula movimento pequeno e seguro
        screen_w, screen_h = pyautogui.size()
        margem = 100
        
        # Movimento aleatório pequeno
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-20, 20)
        
        # Nova posição dentro dos limites seguros
        nova_x = max(margem, min(screen_w - margem, pos_inicial.x + offset_x))
        nova_y = max(margem, min(screen_h - margem, pos_inicial.y + offset_y))
        
        log_com_tempo(f"   → Movimento: ({pos_inicial.x},{pos_inicial.y}) -> ({nova_x},{nova_y})")
        
        # Move suavemente para nova posição
        pyautogui.moveTo(nova_x, nova_y, duration=1.0)
        time.sleep(0.5)
        
        # Retorna para posição original
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=1.0)
        
        log_com_tempo(f"   ✅ MOVIMENTO CONCLUÍDO! Offset aplicado: ({offset_x}, {offset_y})")
        return True
        
    except Exception as e:
        log_com_tempo(f"   ❌ ERRO durante movimento: {e}")
        return False

def mostrar_status_inatividade(segundos_inativos):
    """Mostra status da inatividade de forma limpa"""
    restantes = TEMPO_INATIVIDADE_MAX - segundos_inativos
    porcentagem = (segundos_inativos / TEMPO_INATIVIDADE_MAX) * 100
    
    # Barra de progresso
    barra_len = 25
    preenchido = int((porcentagem / 100) * barra_len)
    barra = "█" * preenchido + "░" * (barra_len - preenchido)
    
    # Formata tempo como MM:SS
    min_inativos = int(segundos_inativos // 60)
    seg_inativos = int(segundos_inativos % 60)
    min_restantes = int(restantes // 60)
    seg_restantes = int(restantes % 60)
    
    status = (f"\r⏰ Inativo: {min_inativos:02d}:{seg_inativos:02d} | "
              f"Restam: {min_restantes:02d}:{seg_restantes:02d} | "
              f"[{barra}] {porcentagem:5.1f}% | Movimentos: {contador_movimentos}")
    
    print(status, end="", flush=True)

def thread_monitoramento():
    """Thread principal que monitora a inatividade do mouse"""
    global posicao_anterior, timestamp_ultima_atividade, programa_rodando
    
    log_com_tempo("🚀 Iniciando monitoramento de inatividade...")
    
    # Inicialização
    posicao_anterior = obter_posicao_mouse()
    timestamp_ultima_atividade = time.time()
    ultimo_status_mostrado = 0
    
    if not posicao_anterior:
        log_com_tempo("❌ ERRO: Não foi possível obter posição inicial do mouse")
        return
    
    log_com_tempo(f"✅ Posição inicial registrada: ({posicao_anterior.x}, {posicao_anterior.y})")
    log_com_tempo(f"⏱️ Monitorando... Limite de inatividade: {TEMPO_INATIVIDADE_MAX}s")
    
    while programa_rodando:
        try:
            time.sleep(INTERVALO_CHECK)
            
            # Obtém posição atual
            posicao_atual = obter_posicao_mouse()
            if not posicao_atual:
                continue
            
            agora = time.time()
            
            # Calcula distância do movimento
            distancia = calcular_distancia(posicao_atual, posicao_anterior)
            
            # Verifica se houve movimento significativo
            if distancia > TOLERANCIA_MOVIMENTO:
                # ✅ MOVIMENTO DETECTADO - RESET COMPLETO
                tempo_que_estava_inativo = agora - timestamp_ultima_atividade
                
                # Só reporta se estava inativo por mais de 15 segundos
                if tempo_que_estava_inativo > 15:
                    print()  # Nova linha para limpar status
                    log_com_tempo(f"🟢 ATIVIDADE DETECTADA! Movimento de {distancia:.1f}px "
                                f"após {tempo_que_estava_inativo:.0f}s de inatividade")
                
                # RESET: atualiza posição e timestamp
                posicao_anterior = posicao_atual
                timestamp_ultima_atividade = agora
                ultimo_status_mostrado = 0
                
            else:
                # ❌ SEM MOVIMENTO - Verifica tempo de inatividade
                tempo_inativo = agora - timestamp_ultima_atividade
                
                # Mostra status apenas se inativo por mais tempo e a intervalos
                if (tempo_inativo >= MOSTRAR_STATUS_APOS and 
                    (agora - ultimo_status_mostrado) >= 3):  # Status a cada 3s
                    
                    mostrar_status_inatividade(tempo_inativo)
                    ultimo_status_mostrado = agora
                
                # 🔥 EXECUTA AÇÃO se atingiu o limite
                if tempo_inativo >= TEMPO_INATIVIDADE_MAX:
                    print()  # Nova linha
                    
                    min_inativo = int(tempo_inativo // 60)
                    seg_inativo = int(tempo_inativo % 60)
                    log_com_tempo(f"🔥 LIMITE ATINGIDO! Mouse inativo por {min_inativo:02d}:{seg_inativo:02d}")
                    
                    # Executa movimento
                    sucesso = executar_movimento_preventivo()
                    
                    if sucesso:
                        # RESET após movimento bem-sucedido
                        posicao_anterior = obter_posicao_mouse()
                        timestamp_ultima_atividade = time.time()
                        log_com_tempo("✅ Timer resetado - próximo movimento em 2 minutos")
                        print("-" * 70)
                    else:
                        log_com_tempo("❌ Movimento falhou - tentativa em 30s")
                        time.sleep(30)
                        
        except KeyboardInterrupt:
            programa_rodando = False
            break
        except Exception as e:
            log_com_tempo(f"⚠️ Erro no monitoramento: {e}")
            time.sleep(5)

def main():
    """Função principal"""
    global programa_rodando
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 70)
    print(f"        ANTI GPU SPIN - {VERSAO}")
    print("=" * 70)
    print("🎯 FUNÇÃO: Simula atividade para CPU parar ventiladores")
    print("🖱️ MÉTODO: Movimento AMPLO em cruz (esquerda→direita→cima→baixo)")
    print("⚡ EFEITO: Sistema detecta atividade real e para fans da CPU")
    print("🔄 SEQUÊNCIA: Movimentos grandes + retorna posição original")
    print("🛑 PARAR: Ctrl+C ou mover mouse para canto superior esquerdo")
    print(f"📏 DETECÇÃO: {TOLERANCIA_MOVIMENTO}px = seu movimento para cancelar")
    print("=" * 70)
    
    try:
        # Testa sistema
        pos_teste = obter_posicao_mouse()
        if not pos_teste:
            raise Exception("PyAutoGUI não está funcionando")
        
        screen_w, screen_h = pyautogui.size()
        log_com_tempo(f"✅ Sistema OK - Tela: {screen_w}x{screen_h}, Mouse: ({pos_teste.x},{pos_teste.y})")
        
        # Inicia thread de monitoramento
        thread_monitor = threading.Thread(target=thread_monitoramento, daemon=True)
        thread_monitor.start()
        
        log_com_tempo("🎮 TESTE: Deixe o mouse parado por exatos 2 minutos para verificar!")
        
        # Loop principal
        while programa_rodando and thread_monitor.is_alive():
            time.sleep(1)
            
    except KeyboardInterrupt:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_com_tempo("🛑 PROGRAMA INTERROMPIDO pelo usuário")
        
    except pyautogui.FailSafeException:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_com_tempo("🛑 FAILSAFE ATIVADO - mouse no canto superior esquerdo")
        
    except Exception as e:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_com_tempo(f"❌ ERRO: {e}")
        
    finally:
        programa_rodando = False
        print("=" * 70)
        log_com_tempo(f"📊 TOTAL DE MOVIMENTOS EXECUTADOS: {contador_movimentos}")
        log_com_tempo("👋 Programa finalizado")
        
        try:
            input("\nPressione Enter para fechar...")
        except:
            pass

# ========================================
# EXECUÇÃO
# ========================================
if __name__ == "__main__":
    try:
        import pyautogui
        print("✅ PyAutoGUI carregado")
    except ImportError:
        print("❌ ERRO: Instale o PyAutoGUI com: pip install pyautogui")
        input("Pressione Enter...")
        sys.exit(1)
    
    main()
