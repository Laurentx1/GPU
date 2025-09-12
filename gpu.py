"""
=== ANTI GPU SPIN - VERSÃO 3.2 CORRIGIDA ===
CORREÇÕES PRINCIPAIS:
- Corrigido problema de detecção de movimento
- Melhorado sistema de logging
- Otimizada performance e responsividade
- Adicionado modo debug para troubleshooting
"""

import pyautogui
import time
import random
import os
import threading
from datetime import datetime
import sys
import traceback

# ========================================
# CONFIGURAÇÕES PRINCIPAIS
# ========================================
VERSAO = "3.2 - CORRIGIDA"
TEMPO_INATIVIDADE_MAX = 120  # 2 minutos em segundos  
INTERVALO_CHECK = 1.0  # Verifica a cada 1 segundo (mais estável)
TOLERANCIA_MOVIMENTO = 5  # Pixels de tolerância (ajustado)
DEBUG_MODE = True  # Ativa logs detalhados

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1  # Pausa entre ações

# Variáveis globais para controle
programa_rodando = True
ultima_posicao_mouse = None
tempo_inicio_inatividade = None
contador_execucoes = 0
lock = threading.Lock()  # Para thread safety

# ========================================
# FUNÇÕES AUXILIARES MELHORADAS
# ========================================
def limpar_tela():
    """Limpa a tela do terminal"""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

def debug_log(mensagem):
    """Log apenas em modo debug"""
    if DEBUG_MODE:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[DEBUG {timestamp}] {mensagem}")

def log_acao(mensagem):
    """Registra ação com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def obter_posicao_mouse_segura():
    """Obtém posição do mouse com tratamento robusto de erro"""
    try:
        pos = pyautogui.position()
        debug_log(f"Posição obtida: ({pos.x}, {pos.y})")
        return pos
    except Exception as e:
        debug_log(f"Erro ao obter posição: {e}")
        return None

def calcular_distancia(pos1, pos2):
    """Calcula distância euclidiana entre duas posições"""
    if pos1 is None or pos2 is None:
        return float('inf')
    
    dist = ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2) ** 0.5
    debug_log(f"Distância calculada: {dist:.2f}px entre ({pos1.x},{pos1.y}) e ({pos2.x},{pos2.y})")
    return dist

def executar_movimento_simples():
    """
    FUNÇÃO PRINCIPAL: Executa movimento suave do mouse
    """
    global contador_execucoes
    
    with lock:
        contador_execucoes += 1
        exec_num = contador_execucoes
    
    log_acao(f"🎯 EXECUTANDO MOVIMENTO #{exec_num}")
    
    try:
        # Obtém posição inicial
        pos_inicial = obter_posicao_mouse_segura()
        if pos_inicial is None:
            log_acao("❌ Falha ao obter posição inicial")
            return False
        
        # Obtém dimensões da tela
        try:
            screen_width, screen_height = pyautogui.size()
            debug_log(f"Dimensões da tela: {screen_width}x{screen_height}")
        except Exception as e:
            log_acao(f"❌ Erro ao obter dimensões da tela: {e}")
            return False
        
        # Calcula movimento pequeno e seguro
        margem = 50  # Margem de segurança das bordas
        max_deslocamento = 20  # Movimento máximo
        
        # Gera deslocamento aleatório
        dx = random.randint(-max_deslocamento, max_deslocamento)
        dy = random.randint(-max_deslocamento, max_deslocamento)
        
        # Calcula nova posição com limites seguros
        nova_x = max(margem, min(screen_width - margem, pos_inicial.x + dx))
        nova_y = max(margem, min(screen_height - margem, pos_inicial.y + dy))
        
        log_acao(f"   → Movendo de ({pos_inicial.x},{pos_inicial.y}) para ({nova_x},{nova_y})")
        
        # Executa movimento suave
        pyautogui.moveTo(nova_x, nova_y, duration=0.8, tween=pyautogui.easeInOutQuad)
        time.sleep(0.5)  # Pausa no destino
        
        # Retorna suavemente para posição original
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.8, tween=pyautogui.easeInOutQuad)
        
        log_acao(f"   ✅ MOVIMENTO CONCLUÍDO! Deslocamento: ({dx}, {dy})")
        return True
        
    except pyautogui.FailSafeException:
        log_acao("🛑 FAILSAFE ativado durante movimento")
        return False
    except Exception as e:
        log_acao(f"❌ ERRO no movimento: {e}")
        debug_log(f"Stack trace: {traceback.format_exc()}")
        return False

def mostrar_status(tempo_inativo):
    """Mostra status de forma mais limpa"""
    tempo_restante = max(0, TEMPO_INATIVIDADE_MAX - tempo_inativo)
    porcentagem = min(100, (tempo_inativo / TEMPO_INATIVIDADE_MAX) * 100)
    
    # Barra de progresso simples
    barra_tamanho = 20
    preenchido = int((porcentagem / 100) * barra_tamanho)
    barra = "█" * preenchido + "░" * (barra_tamanho - preenchido)
    
    status = f"\r⏱️ Inativo: {tempo_inativo:6.1f}s | Restam: {tempo_restante:6.1f}s | [{barra}] {porcentagem:5.1f}% | Movs: {contador_execucoes}"
    print(status, end="", flush=True)

def verificar_sistema():
    """Verifica se o sistema está funcionando corretamente"""
    log_acao("🔧 VERIFICANDO SISTEMA...")
    
    try:
        # Testa posição do mouse
        pos = obter_posicao_mouse_segura()
        if pos is None:
            raise Exception("Não consegue obter posição do mouse")
        log_acao(f"✅ Mouse detectado em: ({pos.x}, {pos.y})")
        
        # Testa dimensões da tela
        w, h = pyautogui.size()
        log_acao(f"✅ Tela detectada: {w}x{h} pixels")
        
        # Testa pequeno movimento
        log_acao("🔧 Testando movimento...")
        original_x, original_y = pos.x, pos.y
        pyautogui.moveTo(original_x + 1, original_y + 1, duration=0.1)
        time.sleep(0.1)
        pyautogui.moveTo(original_x, original_y, duration=0.1)
        log_acao("✅ Movimento testado com sucesso")
        
        return True
        
    except Exception as e:
        log_acao(f"❌ FALHA na verificação: {e}")
        return False

def monitor_inatividade():
    """Thread principal de monitoramento - VERSÃO CORRIGIDA"""
    global ultima_posicao_mouse, tempo_inicio_inatividade, programa_rodando
    
    log_acao("🚀 INICIANDO MONITORAMENTO...")
    
    # Inicialização robusta
    try:
        posicao_inicial = obter_posicao_mouse_segura()
        if posicao_inicial is None:
            log_acao("❌ Falha na inicialização - não consegue ler posição do mouse")
            return
        
        ultima_posicao_mouse = posicao_inicial
        tempo_inicio_inatividade = time.time()
        
        log_acao(f"✅ Monitoramento iniciado. Posição inicial: ({posicao_inicial.x}, {posicao_inicial.y})")
        
    except Exception as e:
        log_acao(f"❌ ERRO na inicialização: {e}")
        return
    
    ultima_exibicao_status = 0
    
    # Loop principal de monitoramento
    while programa_rodando:
        try:
            time.sleep(INTERVALO_CHECK)
            
            # Obtém posição atual
            posicao_atual = obter_posicao_mouse_segura()
            if posicao_atual is None:
                debug_log("Falha ao obter posição atual, pulando ciclo")
                continue
            
            tempo_atual = time.time()
            
            # Calcula distância do último movimento
            distancia = calcular_distancia(posicao_atual, ultima_posicao_mouse)
            
            # Verifica se houve movimento significativo
            if distancia > TOLERANCIA_MOVIMENTO:
                # MOVIMENTO DETECTADO
                tempo_inativo_anterior = tempo_atual - tempo_inicio_inatividade if tempo_inicio_inatividade else 0
                
                if tempo_inativo_anterior > 10:  # Só reporta se estava inativo por um tempo
                    print()  # Nova linha para limpar status
                    log_acao(f"🟢 MOVIMENTO DETECTADO! Distância: {distancia:.1f}px - Reset após {tempo_inativo_anterior:.1f}s")
                
                # Reset completo
                with lock:
                    ultima_posicao_mouse = posicao_atual
                    tempo_inicio_inatividade = tempo_atual
                
                debug_log(f"Reset: nova posição ({posicao_atual.x}, {posicao_atual.y})")
                
            else:
                # SEM MOVIMENTO SIGNIFICATIVO
                if tempo_inicio_inatividade is not None:
                    tempo_inativo = tempo_atual - tempo_inicio_inatividade
                    
                    # Mostra status a cada 2 segundos se inativo por mais de 10s
                    if tempo_inativo >= 10 and (tempo_atual - ultima_exibicao_status) >= 2:
                        mostrar_status(tempo_inativo)
                        ultima_exibicao_status = tempo_atual
                    
                    # EXECUTA AÇÃO se atingiu limite
                    if tempo_inativo >= TEMPO_INATIVIDADE_MAX:
                        print()  # Nova linha
                        log_acao(f"🔥 LIMITE DE INATIVIDADE ATINGIDO! {tempo_inativo:.1f}s")
                        
                        sucesso = executar_movimento_simples()
                        
                        if sucesso:
                            # Reset após execução
                            with lock:
                                ultima_posicao_mouse = obter_posicao_mouse_segura()
                                tempo_inicio_inatividade = time.time()
                            
                            log_acao("✅ Reset completo - próxima verificação em 2 minutos")
                            print("-" * 70)
                        else:
                            log_acao("❌ Movimento falhou - tentativa em 30 segundos")
                            time.sleep(30)
                            
        except KeyboardInterrupt:
            programa_rodando = False
            break
        except pyautogui.FailSafeException:
            programa_rodando = False
            log_acao("🛑 FAILSAFE ATIVADO! Mouse no canto superior esquerdo")
            break
        except Exception as e:
            log_acao(f"⚠️ ERRO no monitoramento: {e}")
            debug_log(f"Stack trace: {traceback.format_exc()}")
            time.sleep(5)  # Pausa maior em caso de erro

def main():
    """Função principal CORRIGIDA"""
    global programa_rodando
    
    limpar_tela()
    print("=" * 70)
    print(f"         ANTI GPU SPIN - VERSÃO {VERSAO}")
    print("=" * 70)
    print("🎯 OBJETIVO: Prevenir GPU de entrar em modo de economia problemático")
    print("⏰ FUNCIONAMENTO: Move mouse suavemente a cada 2min de inatividade")
    print("🖱️ AÇÃO: Apenas movimento suave (ida e volta)")
    print("🛑 PARAR: Ctrl+C ou mover mouse para canto superior esquerdo")
    print(f"📊 SENSIBILIDADE: {TOLERANCIA_MOVIMENTO}px mínimo para detectar movimento")
    print("=" * 70)
    
    try:
        # Verificação inicial do sistema
        if not verificar_sistema():
            raise Exception("Verificação do sistema falhou")
        
        log_acao("🔍 Sistema verificado - iniciando monitoramento...")
        
        # Inicia thread de monitoramento
        thread_monitor = threading.Thread(target=monitor_inatividade, daemon=True)
        thread_monitor.start()
        
        log_acao("✅ Thread de monitoramento iniciada")
        log_acao("💡 Deixe o mouse parado por 2 minutos para testar...")
        
        # Loop principal para capturar interrupções
        while programa_rodando and thread_monitor.is_alive():
            time.sleep(1)
            
    except KeyboardInterrupt:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_acao("🛑 INTERRUPÇÃO DO USUÁRIO (Ctrl+C)")
        
    except pyautogui.FailSafeException:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_acao("🛑 FAILSAFE ATIVADO!")
        
    except Exception as e:
        programa_rodando = False
        print("\n" + "=" * 70)
        log_acao(f"❌ ERRO CRÍTICO: {e}")
        if DEBUG_MODE:
            debug_log(f"Stack trace completo:\n{traceback.format_exc()}")
        
    finally:
        programa_rodando = False
        print("=" * 70)
        log_acao(f"📊 RELATÓRIO FINAL: {contador_execucoes} movimentos executados")
        log_acao("📋 PROGRAMA FINALIZADO")
        
        try:
            input("\n💡 Pressione Enter para fechar...")
        except:
            time.sleep(2)

# ========================================
# EXECUÇÃO PRINCIPAL
# ========================================
if __name__ == "__main__":
    try:
        import pyautogui
        print("✅ PyAutoGUI carregado com sucesso")
    except ImportError:
        print("❌ ERRO: PyAutoGUI não encontrado!")
        print("💡 Instale com: pip install pyautogui")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    main()
