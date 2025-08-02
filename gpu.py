import subprocess
import time
import re

print("CONTROLE DE CURVA DA VENTOINHA GPU")
print("Baseado no gráfico fornecido")
print("Pressione Ctrl+C para parar")

def get_gpu_temp():
    """Pega a temperatura da GPU usando nvidia-smi"""
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            temp = int(result.stdout.strip())
            return temp
        else:
            return None
    except:
        return None

def calculate_fan_speed(temp):
    """Calcula a velocidade da ventoinha baseado na temperatura"""
    # Curva modificada: 0% até 50°C, depois cresce até 100% aos 80°C
    if temp < 50:
        return 0  # Ventoinha desligada
    elif temp >= 80:
        return 100  # Velocidade máxima
    else:
        # Interpolação linear entre 50°C (0%) e 80°C (100%)
        # Fórmula: y = mx + b
        # m = (100-0)/(80-50) = 100/30 = 3.33
        # b = 0 - 3.33*50 = -166.67
        fan_speed = 3.33 * temp - 166.67
        return min(100, max(0, int(fan_speed)))

def set_fan_speed(speed):
    """Define a velocidade da ventoinha (requer MSI Afterburner ou similar)"""
    try:
        # Exemplo usando MSI Afterburner command line
        # Você pode precisar ajustar o caminho
        subprocess.run([
            'MSIAfterburner.exe', 
            '-Profile1', 
            f'-FanSpeed={speed}'
        ], capture_output=True)
        return True
    except:
        return False

# Loop principal
while True:
    try:
        # Pega temperatura atual
        temp = get_gpu_temp()
        
        if temp is not None:
            # Calcula velocidade da ventoinha
            fan_speed = calculate_fan_speed(temp)
            
            # Mostra informações
            print(f"Temp: {temp}°C | Ventoinha: {fan_speed}%")
            
            # Define velocidade (descomente se tiver MSI Afterburner)
            # set_fan_speed(fan_speed)
            
        else:
            print("Erro ao ler temperatura da GPU")
        
        # Espera 5 segundos antes da próxima leitura
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\nPARADO!")
        break
    except Exception as e:
        print(f"ERRO: {e}")
        time.sleep(5)

print("FIM!")
input("Enter para fechar")
