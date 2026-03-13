import json
import os
import subprocess
from datetime import datetime

# CONFIGURACIÓN
GOAL_MMR = 11000
DATA_FILE = "mmr_history.json"

def auto_push():
    """Ejecuta los comandos de Git automáticamente"""
    try:
        print("\n☁️ Sincronizando con GitHub...")
        # Agregar el archivo JSON al commit
        subprocess.run(["git", "add", DATA_FILE], check=True)
        
        # Mensaje de commit con la fecha actual
        commit_msg = f"Update MMR: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Subir los cambios
        subprocess.run(["git", "push"], check=True)
        print("✅ ¡Sincronizado con éxito en tu GitHub!")
    except Exception as e:
        print(f"⚠️ Error al sincronizar: {e}")
        print("Tip: Revisa que tu conexión a internet esté estable y el repo configurado.")

def calcular_progreso(current):
    faltante = GOAL_MMR - current
    partidas_netas = faltante / 25
    progreso = (current / GOAL_MMR) * 100
    return faltante, partidas_netas, progreso

def main():
    print("--- 🎮 DOTA 2 MMR TRACKER (EL CAMINO A LOS 11K) ---")
    
    # Paso 0: Intentar bajar datos nuevos de GitHub (por si jugaste en la casa)
    try:
        subprocess.run(["git", "pull"], check=True)
    except:
        print("Aviso: No se pudo hacer pull (quizás el repo está vacío).")

    try:
        current_mmr = int(input("\nIngresa tu MMR actual: "))
    except ValueError:
        print("Escribe un número válido, no te aisles.")
        return

    # Cargar historial
    history = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

    # Comparación con el último registro
    if history:
        last_mmr = history[-1]['mmr']
        diff = current_mmr - last_mmr
        if diff > 0:
            print(f"📈 ¡Ganaste {diff} puntos! Estás modo pro.")
        elif diff < 0:
            print(f"📉 Perdiste {abs(diff)} puntos... Toca enfocarse.")
        else:
            print("Te mantienes igual. El grind no para.")
    else:
        print("¡Primer registro del historial! Vamos por esos 11k.")

    faltante, netas, progreso = calcular_progreso(current_mmr)
    print("-" * 45)
    print(f"📊 Progreso total: {progreso:.2f}%")
    print(f"🚩 Faltan: {faltante} MMR (~{int(netas)} wins netas)")
    print("-" * 45)

    # Guardar localmente
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mmr": current_mmr
    })
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

    # Sincronización automática
    auto_push()

if __name__ == "__main__":
    main()