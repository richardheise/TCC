import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import sys
import numpy as np

def plot_autoqueda_por_recursos(data, output_dir):
    plt.figure(figsize=(10, 6))
    cores = {
        "netshield": "blue",
        "walk4": "green",
        "walk4-aprimorado": "red",
        "xnb": "purple"
    }
    concorrentes = False
    for algoritmo, group in data.groupby("algoritmo"):
        plt.plot(group["k"], group["eigendrop"], label=algoritmo, color=cores[algoritmo], marker='o')
        if not concorrentes:
            for outro_algoritmo, outro_group in data.groupby("algoritmo"):
                if algoritmo != outro_algoritmo and group["eigendrop"].equals(outro_group["eigendrop"]):
                    concorrentes = True
                    break

    plt.xlabel("Recursos (k)")
    plt.ylabel("Autoqueda")
    plt.title("Autoqueda por Recursos")
    if concorrentes:
        plt.legend(title="Concorrentes: Dados iguais", loc="upper left")
    else:
        plt.legend()

    plt.xticks(sorted(data["k"].unique()))
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, "autoqueda_por_recursos.png"))
    plt.close()

def plot_tempo_por_autoqueda(data, output_dir):
    plt.figure(figsize=(10, 6))
    cores = {
        "netshield": "blue",
        "walk4": "green",
        "walk4-aprimorado": "red",
        "xnb": "purple"
    }
    concorrentes = False
    for algoritmo, group in data.groupby("algoritmo"):
        plt.plot(group["eigendrop"], group["time"], label=algoritmo, color=cores[algoritmo], marker='o')
        if not concorrentes:
            for outro_algoritmo, outro_group in data.groupby("algoritmo"):
                if algoritmo != outro_algoritmo and group["time"].equals(outro_group["time"]):
                    concorrentes = True
                    break

    plt.yscale('log')
    plt.xlabel("Autoqueda")
    plt.ylabel("Tempo (s)")
    plt.title("Tempo por Autoqueda")
    if concorrentes:
        plt.legend(title="Concorrentes: Dados iguais", loc="upper left")
    else:
        plt.legend()

    plt.yticks(sorted(data["time"].unique()), labels=[f"{val:.2e}" for val in sorted(data["time"].unique())])
    plt.grid(True, which="both", ls="--")
    plt.savefig(os.path.join(output_dir, "tempo_por_autoqueda.png"))
    plt.close()

def definir_ticks_log(ax, valores, eixo='x'):
    """ Define ticks logarítmicos com intervalo ajustado. """
    min_val = min(valores)
    max_val = max(valores)
    
    if eixo == 'x':
        ticks = np.logspace(np.log10(min_val), np.log10(max_val), num=10)
    elif eixo == 'y':
        ticks = np.linspace(min_val, max_val, num=10)
    
    # Define ticks
    ticks = np.unique(np.concatenate((ticks, [min_val, max_val])))
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{tick:.3f}" for tick in ticks])
    
    return ax

def plot_recursos_por_tempo(data, output_dir):
    plt.figure(figsize=(10, 6))
    cores = {
        "netshield": "blue",
        "walk4": "green",
        "walk4-aprimorado": "red",
        "xnb": "purple"
    }
    concorrentes = False
    for algoritmo, group in data.groupby("algoritmo"):
        plt.plot(group["time"], group["k"], label=algoritmo, color=cores[algoritmo], marker='o')
        if not concorrentes:
            for outro_algoritmo, outro_group in data.groupby("algoritmo"):
                if algoritmo != outro_algoritmo and group["k"].equals(outro_group["k"]):
                    concorrentes = True
                    break

    plt.xscale('log')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Recursos (k)")
    plt.title("Recursos por Tempo")
    if concorrentes:
        plt.legend(title="Concorrentes: Dados iguais", loc="upper left")
    else:
        plt.legend()

    ax = plt.gca()
    definir_ticks_log(ax, data["time"], eixo='x')
    plt.grid(True, which="both", ls="--")
    plt.savefig(os.path.join(output_dir, "recursos_por_tempo.png"))
    plt.close()

def process_csv_files(directory):
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    for file in csv_files:
        data = pd.read_csv(file)
        output_dir = os.path.splitext(file)[0]
        os.makedirs(output_dir, exist_ok=True)
        plot_autoqueda_por_recursos(data, output_dir)
        # plot_tempo_por_autoqueda(data, output_dir)
        plot_recursos_por_tempo(data, output_dir)
        print(f"Gráficos salvos na pasta: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <diretorio_com_csvs>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Erro: {directory} não é um diretório válido.")
        sys.exit(1)

    process_csv_files(directory)
