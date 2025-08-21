"""
=== ANTI GPU SPIN - VERSÃO 3.0 TOTALMENTE CORRIGIDA ===
CORREÇÕES PRINCIPAIS:
- Detecção de movimento mais precisa
- Sistema de timing mais confiável
- Melhor tratamento de erros
- Interface mais clara
- Ações mais efetivas para manter GPU ativa
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
VERSAO = "3.0 - TOTALMENTE CORRIGIDA"
TEMPO_INATIVIDADE_MAX = 120  # 2 minutos em segundos  
INTERVALO_CHECK = 0.5  # Verifica a cada 0.5 segundos (mais responsivo)
TOLERANCIA_MOVIMENTO = 3  # Pixels de tolerância (mais sensível)

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.01  # Pausa mínima entre ações

# Variáveis globais para controle
programa_rodando = True
ultima_posicao_mouse = None
tempo_inicio_inatividade = None
contador_execucoes = 0

# ========================================
# FUNÇÕES AUXILIARES MELHORADAS
# ========================================
def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def log_acao(mensagem):
    """Registra ação com timestamp melhorado"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Com milissegundos
    print(f"[{timestamp}] {mensagem}")

def obter_posicao_mouse_segura():
    """Obtém posição do mouse com tratamento de erro"""
    try:
        return pyautogui.position()
    except Exception as e:
        log_acao(f"⚠️ Erro ao obter posição do mouse: {e}")
        return None

def calcular_distancia(pos1, pos2):
    """Calcula distância entre duas posições"""
    if pos1 is None or pos2 is None:
        return float('inf')
    return ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2) ** 0.5

def executar_acao_anti_spin():
    """
    FUNÇÃO PRINCIPAL MELHORADA: Executa ações mais efetivas
    """
    global contador_execucoes
    contador_execucoes += 1
    
    log_acao(f"🎯 EXECUTANDO ANTI-SPIN #{contador_execucoes}")
    
    # Salva posição inicial
    pos_inicial = obter_posicao_mouse_segura()
    if pos_inicial is None:
        log_acao("❌ Não foi possível obter posição inicial")
        return False
    
    try:
        # 1. DOUBLE CLICK mais efetivo
        log_acao("   → Double click para ativar GPU")
        pyautogui.doubleClick(interval=0.1)
        time.sleep(0.2)
        
        # 2. MOVIMENTO EM PADRÃO MAIS COMPLEXO
        log_acao("   → Movimento em padrão complexo")
        # Movimento em quadrado
        moves = [
            (20, 0), (0, 20), (-20, 0), (0, -20),  # Quadrado
            (10, 10), (-10, -10), (10, -10), (-10, 10)  # Diagonais
        ]
        
        for dx, dy in moves:
            nova_x = pos_inicial.x + dx
            nova_y = pos_inicial.y + dy
            pyautogui.moveTo(nova_x, nova_y, duration=0.05)
            time.sleep(0.02)
        
        # Volta para posição inicial
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.1)
        time.sleep(0.1)
        
        # 3. MÚLTIPLOS SCROLLS
        log_acao("   → Scrolls múltiplos")
        for _ in range(3):
            scroll_amount = random.choice([2, -2, 3, -3])
            pyautogui.scroll(scroll_amount)
            time.sleep(0.1)
        
        # 4. COMBINAÇÃO DE TECLAS SEGURAS
        log_acao("   → Teclas de controle")
        teclas_seguras = ['shift', 'ctrl', 'alt']
        for tecla in random.sample(teclas_seguras, 2):
            pyautogui.press(tecla)
            time.sleep(0.1)
        
        # 5. CLIQUES ADICIONAIS EM POSIÇÕES ALEATÓRIAS
        log_acao("   → Cliques adicionais")
        for _ in range(2):
            offset_x = random.randint(-30, 30)
            offset_y = random.randint(-30, 30)
            click_x = max(10, min(pyautogui.size().width - 10, pos_inicial.x + offset_x))
            click_y = max(10, min(pyautogui.size().height - 10, pos_inicial.y + offset_y))
            
            pyautogui.click(click_x, click_y)
            time.sleep(0.1)
        
        # Retorna para posição inicial final
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.2)
        
        log_acao("   ✅ ANTI-SPIN EXECUTADO COM SUCESSO!")
        return True
        
    except Exception as e:
        log_acao(f"   ❌ ERRO durante anti-spin: {e}")
        # Tenta retornar para posição inicial
        try:
            if pos_inicial:
                pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.1)
        except:
            pass
        return False

def mostrar_status_melhorado(tempo_inativo):
    """Interface de status melhorada"""
    tempo_restante = max(0, TEMPO_INATIVIDADE_MAX - tempo_inativo)
    porcentagem = min(100, (tempo_inativo / TEMPO_INATIVIDADE_MAX) * 100)
    
    # Barra de progresso colorida (usando caracteres especiais)
    barra_tamanho = 30
    barra_preenchida = int((porcentagem / 100) * barra_tamanho)
    
    if porcentagem < 50:
        char_barra = "▓"  # Verde (início)
    elif porcentagem < 80:
        char_barra = "▒"  # Amarelo (meio)
    else:
        char_barra = "█"  # Vermelho (quase executando)
    
    barra = char_barra * barra_preenchida + "░" * (barra_tamanho - barra_preenchida)
    
    status = f"\r⏱️ Inativo: {tempo_inativo:3.1f}s | Restante: {tempo_restante:3.1f}s | [{barra}] {porcentagem:5.1f}% | Exec: {contador_execucoes}"
    print(status, end="", flush=True)

def monitor_inatividade():
    """Thread principal para monitorar inatividade"""
    global ultima_posicao_mouse, tempo_inicio_inatividade, programa_rodando
    
    log_acao("🚀 INICIANDO MONITORAMENTO DE INATIVIDADE...")
    
    # Inicializa posição
    ultima_posicao_mouse = obter_posicao_mouse_segura()
    tempo_inicio_inatividade = time.time()
    
    while programa_rodando:
        try:
            # Pequena pausa para não sobrecarregar CPU
            time.sleep(INTERVALO_CHECK)
            
            posicao_atual = obter_posicao_mouse_segura()
            if posicao_atual is None:
                continue
            
            # Calcula distância do movimento
            distancia = calcular_distancia(posicao_atual, ultima_posicao_mouse)
            tempo_atual = time.time()
            
            # Verifica se houve movimento significativo
            if distancia > TOLERANCIA_MOVIMENTO:
                # MOVIMENTO DETECTADO - Reset
                if tempo_inicio_inatividade is not None:
                    tempo_inativo_atual = tempo_atual - tempo_inicio_inatividade
                    if tempo_inativo_atual > 10:  # Só mostra se estava inativo por mais de 10s
                        print()  # Nova linha
                        log_acao(f"🟢 MOVIMENTO DETECTADO! (dist: {distancia:.1f}px) - Reset após {tempo_inativo_atual:.1f}s")
                
                # Reset das variáveis
                ultima_posicao_mouse = posicao_atual
                tempo_inicio_inatividade = tempo_atual
                
            else:
                # SEM MOVIMENTO - Verifica tempo de inatividade
                if tempo_inicio_inatividade is not None:
                    tempo_inativo_atual = tempo_atual - tempo_inicio_inatividade
                    
                    # Mostra status se inativo por mais de 5 segundos
                    if tempo_inativo_atual >= 5:
                        mostrar_status_melhorado(tempo_inativo_atual)
                    
                    # EXECUTA ANTI-SPIN se atingiu o limite
                    if tempo_inativo_atual >= TEMPO_INATIVIDADE_MAX:
                        print()  # Nova linha
                        log_acao(f"🔥 LIMITE ATINGIDO! {tempo_inativo_atual:.1f}s de inatividade")
                        
                        if executar_acao_anti_spin():
                            # Reset após execução bem-sucedida
                            ultima_posicao_mouse = obter_posicao_mouse_segura()
                            tempo_inicio_inatividade = time.time()
                            
                            log_acao("✅ Reiniciando contagem - próxima verificação em 2min")
                            print("-" * 60)
                        else:
                            log_acao("❌ Falha na execução - tentando novamente em 30s")
                            time.sleep(30)
                            
        except KeyboardInterrupt:
            programa_rodando = False
            break
        except pyautogui.FailSafeException:
            programa_rodando = False
            log_acao("🛑 FAILSAFE ATIVADO!")
            break
        except Exception as e:
            log_acao(f"⚠️ Erro no monitoramento: {e}")
            time.sleep(1)  # Pausa antes de tentar novamente

def main():
    """Função principal melhorada"""
    global programa_rodando
    
    limpar_tela()
    print("=" * 60)
    print(f"         ANTI GPU SPIN - VERSÃO {VERSAO}")
    print("=" * 60)
    print("🎯 OBJETIVO: Prevenir GPU de entrar em modo problemático")
    print("⏰ AÇÃO: A cada 2 minutos de inatividade do mouse")
    print("🔧 MELHORIAS: Detecção mais precisa + ações mais efetivas")
    print("🛑 PARAR: Ctrl+C ou mover mouse para canto superior esquerdo")
    print("📊 TOLERÂNCIA: Movimento mínimo de 3 pixels para detectar atividade")
    print("=" * 60)
    
    try:
        # Testa se PyAutoGUI está funcionando
        pos_teste = obter_posicao_mouse_segura()
        if pos_teste is None:
            raise Exception("PyAutoGUI não está funcionando corretamente")
        
        log_acao(f"✅ Sistema inicializado - Posição inicial: ({pos_teste.x}, {pos_teste.y})")
        log_acao("🔍 Iniciando monitoramento...")
        
        # Inicia thread de monitoramento
        thread_monitor = threading.Thread(target=monitor_inatividade, daemon=True)
        thread_monitor.start()
        
        # Loop principal (para capturar Ctrl+C)
        while programa_rodando:
            time.sleep(1)
            
    except KeyboardInterrupt:
        programa_rodando = False
        print("\n" + "=" * 60)
        log_acao("🛑 PROGRAMA INTERROMPIDO PELO USUÁRIO (Ctrl+C)")
        
    except pyautogui.FailSafeException:
        programa_rodando = False
        print("\n" + "=" * 60)
        log_acao("🛑 FAILSAFE ATIVADO! Mouse no canto superior esquerdo")
        
    except Exception as e:
        programa_rodando = False
        print("\n" + "=" * 60)
        log_acao(f"❌ ERRO CRÍTICO: {e}")
        log_acao("💡 Verifique se o PyAutoGUI está instalado: pip install pyautogui")
        
    finally:
        programa_rodando = False
        print("=" * 60)
        log_acao(f"📊 ESTATÍSTICAS FINAIS: {contador_execucoes} execuções anti-spin realizadas")
        log_acao("📋 PROGRAMA FINALIZADO")
        
        # Pausa para ver o resultado
        try:
            input("\n💡 Pressione Enter para fechar...")
        except:
            pass

# ========================================
# EXECUÇÃO
# ========================================
if __name__ == "__main__":
    # Verificação de dependências
    try:
        import pyautogui
        print("✅ PyAutoGUI encontrado")
    except ImportError:
        print("❌ PyAutoGUI não encontrado!")
        print("💡 Instale com: pip install pyautogui")
        input("Pressione Enter para continuar...")
        sys.exit(1)
    
    main()
