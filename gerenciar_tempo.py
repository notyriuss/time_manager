import os
import json
import time
from datetime import datetime

PASTA = "Data/cronometro"
ARQ_ATUAL = os.path.join(PASTA, "tempo_atual.json")
ARQ_EM_ANDAMENTO = os.path.join(PASTA, "cronometro_em_andamento.json")
ARQ_HISTORICO = os.path.join(PASTA, "historico.json")

GRUPOS = {
    "A": "Exercício",
    "B": "Projeto",
    "C": "AOE4",
    "D": "Concurso",
    "E": "Doutorado"
}

os.makedirs(PASTA, exist_ok=True)

def carregar_json(path, default):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default

def salvar_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def segundos_para_str(seg):
    h = int(seg // 3600)
    m = int((seg % 3600) // 60)
    s = int(seg % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def mostrar_tempos():
    tempos = carregar_json(ARQ_ATUAL, {})
    print("\n⏱️  Tempo total por grupo:")
    for grupo, nome in GRUPOS.items():
        tempo = tempos.get(grupo, 0)
        print(f"- {nome:10}: {segundos_para_str(tempo)}")

def iniciar_cronometro():
    if os.path.exists(ARQ_EM_ANDAMENTO):
        print("\n⚠️  Já existe um cronômetro em andamento. Pare-o antes de iniciar outro.")
        return
    print("\nEscolha um grupo:")
    for k, v in GRUPOS.items():
        print(f"  {k} - {v}")
    grupo = input("Digite a letra do grupo: ").upper()
    if grupo not in GRUPOS:
        print("Grupo inválido.")
        return
    inicio = time.time()
    salvar_json(ARQ_EM_ANDAMENTO, {"grupo": grupo, "inicio": inicio})
    print(f"Cronômetro iniciado para '{GRUPOS[grupo]}' às {datetime.fromtimestamp(inicio).strftime('%H:%M:%S')}")

def parar_cronometro():
    if not os.path.exists(ARQ_EM_ANDAMENTO):
        print("\n⚠️  Nenhum cronômetro em andamento.")
        return
    dados = carregar_json(ARQ_EM_ANDAMENTO, {})
    grupo = dados["grupo"]
    inicio = dados["inicio"]
    duracao = time.time() - inicio

    tempos = carregar_json(ARQ_ATUAL, {})
    tempos[grupo] = tempos.get(grupo, 0) + duracao
    salvar_json(ARQ_ATUAL, tempos)
    os.remove(ARQ_EM_ANDAMENTO)

    print(f"\n⏹️  Cronômetro parado. {GRUPOS[grupo]} teve +{segundos_para_str(duracao)} adicionados.")

def resetar_tempos():
    tempos = carregar_json(ARQ_ATUAL, {})
    if not tempos:
        print("\nℹ️  Nenhum tempo para resetar.")
        return
    historico = carregar_json(ARQ_HISTORICO, [])
    historico.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tempos": tempos
    })
    salvar_json(ARQ_HISTORICO, historico)
    salvar_json(ARQ_ATUAL, {})
    print("\n✅ Tempo atual resetado e salvo no histórico.")

def adicionar_tempo_manual():
    print("\nEscolha um grupo para adicionar tempo manualmente:")
    for k, v in GRUPOS.items():
        print(f"  {k} - {v}")
    grupo = input("Digite a letra do grupo: ").upper()
    if grupo not in GRUPOS:
        print("Grupo inválido.")
        return

    try:
        tempo_str = input("Digite o tempo a adicionar (formato HH:MM:SS): ")
        h, m, s = map(int, tempo_str.strip().split(":"))
        segundos = h * 3600 + m * 60 + s
    except Exception:
        print("Tempo inválido. Use o formato HH:MM:SS.")
        return

    tempos = carregar_json(ARQ_ATUAL, {})
    tempos[grupo] = tempos.get(grupo, 0) + segundos
    salvar_json(ARQ_ATUAL, tempos)

    print(f"✅ Adicionado +{segundos_para_str(segundos)} ao grupo '{GRUPOS[grupo]}'.")

def menu():
    while True:
        print("\n📋 Menu:")
        print("1 - Consultar tempo por grupo")
        print("2 - Começar contagem")
        print("3 - Parar contagem")
        print("4 - Resetar contador (salva histórico)")
        print("5 - Adicionar tempo manualmente")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            mostrar_tempos()
        elif escolha == "2":
            iniciar_cronometro()
        elif escolha == "3":
            parar_cronometro()
        elif escolha == "4":
            resetar_tempos()
        elif escolha == "5":
            adicionar_tempo_manual()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
