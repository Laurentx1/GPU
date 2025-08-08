"""
=== ANTI GPU SPIN - VERSÃO 2.0 ===
PROMPT DE MANUTENÇÃO:
"Esse código resolve o problema de GPU que fica maluca após 23 minutos de inatividade.
Ele move o mouse e faz double click automaticamente para controlar a fan da placa de vídeo.
Sempre que enviar este código, você deve analisar e melhorar mantendo a funcionalidade principal."

FUNCIONALIDADES:
- Detecta inatividade do mouse por 2 minutos (120 segundos)  
- Executa múltiplas ações: double click, movimentos, scroll, teclas
- Previne que a GPU entre em modo problemático
- Interface melhorada com status em tempo real
- Failsafe para emergência (mover mouse para canto superior esquerdo)

PRÓXIMOS PASSOS/MELHORIAS FUTURAS:
- Adicionar logs em arquivo
- Interface gráfica simples
- Configurações personalizáveis via arquivo
- Detecção de jogos/aplicações em tela cheia
"""

import pyautogui
import time
import random
import os
from datetime import datetime

# ========================================
# CONFIGURAÇÕES PRINCIPAIS
# ========================================
VERSAO = "2.0"
TEMPO_INATIVIDADE_MAX = 120  # 2 minutos em segundos  
INTERVALO_CHECK = 1  # Verifica a cada 1 segundo
TOLERANCIA_MOVIMENTO = 5  # Pixels de tolerância para detectar movimento

# Configurações do PyAutoGUI
pyautogui.FAILSAFE = True  # Emergência: mover mouse para canto superior esquerdo
pyautogui.PAUSE = 0.05     # Pausa menor entre ações para mais fluidez

# ========================================
# FUNÇÕES AUXILIARES  
# ========================================
def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def log_acao(mensagem):
    """Registra ação com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def detectar_movimento(pos1, pos2, tolerancia=TOLERANCIA_MOVIMENTO):
    """Detecta se houve movimento significativo do mouse"""
    distancia = ((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2) ** 0.5
    return distancia > tolerancia

def fazer_atividade_anti_spin():
    """
    FUNÇÃO PRINCIPAL: Executa sequência de ações para manter GPU ativa
    Esta função resolve o problema da placa de vídeo que fica maluca
    """
    log_acao("🎯 INICIANDO SEQUÊNCIA ANTI-SPIN...")
    
    # Salva posição inicial para retornar depois
    pos_inicial = pyautogui.position()
    
    try:
        # 1. Double Click - Principal ação para controlar fan da GPU
        log_acao("   ✓ Executando double click (controle da fan)")
        pyautogui.doubleClick()
        time.sleep(0.3)
        
        # 2. Movimento circular suave - Simula atividade natural
        log_acao("   ✓ Movimento circular suave")
        raio = 15
        for i in range(12):  # Movimento mais suave com mais pontos
            angulo = (i * 30) * (3.14159 / 180)  # Converte para radianos
            x_offset = int(raio * pyautogui.math.cos(angulo)) if hasattr(pyautogui, 'math') else int(raio * 0.5)
            y_offset = int(raio * pyautogui.math.sin(angulo)) if hasattr(pyautogui, 'math') else int(raio * 0.5)
            pyautogui.moveTo(pos_inicial.x + x_offset, pos_inicial.y + y_offset, duration=0.05)
        
        # Volta para posição inicial
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.1)
        time.sleep(0.2)
        
        # 3. Scroll vertical - Atividade adicional
        log_acao("   ✓ Scroll vertical aleatório")
        scroll_amount = random.choice([2, -2, 3, -3, 1, -1])
        pyautogui.scroll(scroll_amount)
        time.sleep(0.2)
        
        # 4. Pressionar tecla neutra (Shift) - Não interfere em aplicações
        log_acao("   ✓ Tecla neutra (Shift)")
        pyautogui.press('shift')
        time.sleep(0.2)
        
        # 5. Movimento final aleatório pequeno
        log_acao("   ✓ Movimento final aleatório")
        for _ in range(2):
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            pyautogui.move(dx, dy, duration=0.1)
            time.sleep(0.1)
        
        # Retorna para posição inicial
        pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.15)
        
        log_acao("   ✅ SEQUÊNCIA ANTI-SPIN CONCLUÍDA COM SUCESSO!")
        
    except Exception as e:
        log_acao(f"   ❌ ERRO durante atividade anti-spin: {e}")
        # Tenta retornar para posição inicial mesmo com erro
        try:
            pyautogui.moveTo(pos_inicial.x, pos_inicial.y, duration=0.1)
        except:
            pass

def mostrar_status(tempo_inativo, ultima_acao="Nenhuma"):
    """Mostra status atual do programa"""
    tempo_restante = TEMPO_INATIVIDADE_MAX - tempo_inativo
    porcentagem = (tempo_inativo / TEMPO_INATIVIDADE_MAX) * 100
    
    # Barra de progresso visual
    barra_tamanho = 20
    barra_preenchida = int((porcentagem / 100) * barra_tamanho)
    barra = "█" * barra_preenchida + "░" * (barra_tamanho - barra_preenchida)
    
    print(f"\r⏱️  Inativo: {tempo_inativo:3d}s | Restante: {tempo_restante:3d}s | [{barra}] {porcentagem:5.1f}% | Última: {ultima_acao}", end="", flush=True)

# ========================================
# PROGRAMA PRINCIPAL
# ========================================
def main():
    limpar_tela()
    print("=" * 50)
    print(f"    ANTI GPU SPIN - VERSÃO {VERSAO}")
    print("=" * 50)
    print("🎯 OBJETIVO: Prevenir GPU maluca após inatividade")
    print("⏰ TEMPO: Ação a cada 2 minutos de inatividade")
    print("🛑 PARAR: Ctrl+C ou mover mouse para canto superior esquerdo")
    print("=" * 50)
    
    # Variáveis de controle
    ultima_posicao = pyautogui.position()
    tempo_inativo = 0
    contador_acoes = 0
    ultima_acao_executada = "Início do programa"
    
    log_acao("🚀 PROGRAMA INICIADO - Monitorando atividade...")
    
    try:
        while True:
            time.sleep(INTERVALO_CHECK)
            posicao_atual = pyautogui.position()
            
            # Verifica se houve movimento significativo
            if detectar_movimento(posicao_atual, ultima_posicao):
                if tempo_inativo > 10:  # Só mostra se estava inativo por um tempo
                    print()  # Nova linha após a barra de status
                    log_acao("🟢 Movimento detectado! Resetando contador de inatividade")
                
                tempo_inativo = 0
                ultima_posicao = posicao_atual
                ultima_acao_executada = "Movimento do mouse"
                
            else:
                # Incrementa tempo de inatividade
                tempo_inativo += INTERVALO_CHECK
                
                # Mostra status em tempo real (sobrescreve a linha)
                if tempo_inativo >= 10:  # Só mostra status após 10 segundos
                    mostrar_status(tempo_inativo, ultima_acao_executada)
                
                # Executa ação anti-spin após tempo limite
                if tempo_inativo >= TEMPO_INATIVIDADE_MAX:
                    print()  # Nova linha após a barra de status
                    contador_acoes += 1
                    
                    log_acao(f"🔥 ATIVANDO ANTI-SPIN (Execução #{contador_acoes})")
                    fazer_atividade_anti_spin()
                    
                    # Reset do contador
                    tempo_inativo = 0
                    ultima_posicao = pyautogui.position()
                    ultima_acao_executada = f"Anti-spin #{contador_acoes}"
                    
                    print("-" * 50)
                
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        log_acao("🛑 PROGRAMA INTERROMPIDO PELO USUÁRIO (Ctrl+C)")
        log_acao(f"📊 ESTATÍSTICAS: {contador_acoes} ações anti-spin executadas")
        
    except pyautogui.FailSafeException:
        print("\n" + "=" * 50)
        log_acao("🛑 FAILSAFE ATIVADO! Mouse movido para canto superior esquerdo")
        log_acao("ℹ️  Esta é uma medida de segurança para parar o programa")
        
    except Exception as e:
        print("\n" + "=" * 50)
        log_acao(f"❌ ERRO INESPERADO: {e}")
        log_acao("🔧 Verifique se PyAutoGUI está funcionando corretamente")
        
    finally:
        print("=" * 50)
        log_acao("📋 PROGRAMA FINALIZADO")
        input("\n💡 Pressione Enter para fechar a janela...")

# ========================================
# EXECUÇÃO
# ========================================
if __name__ == "__main__":
    main()
