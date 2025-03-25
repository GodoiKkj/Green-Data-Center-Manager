import time
import random
from sortedcontainers import SortedList
import math


class Server:
    """
    Classe que representa um servidor no data center.

    Atributos:
        server_id (int): ID único do servidor.
        current_load (int): Carga atual do servidor.
        temperature (float): Temperatura atual do servidor.
        max_temp (float): Temperatura máxima que o servidor pode atingir antes de precisar resfriar.
        tasks_transferred (int): Número de tarefas transferidas para outros servidores devido ao superaquecimento.

    Métodos:
        add_task(load): Adiciona uma carga ao servidor e atualiza a temperatura.
        release_task(load): Libera uma carga do servidor e atualiza a temperatura.
        update_temperature(): Atualiza a temperatura do servidor com base na carga.
        cool_down(): Resfria o servidor em 5°C, sem permitir que a temperatura fique abaixo de 25°C.
        __repr__(): Retorna uma representação do servidor com ID, carga e temperatura.
    """

    def __init__(self, server_id, max_temp=75):
        self.server_id = server_id
        self.current_load = 0
        self.temperature = 25
        self.max_temp = max_temp
        self.tasks_transferred = 0

    def add_task(self, load):
        self.current_load += load
        self.update_temperature()

    def release_task(self, load):
        self.current_load -= load
        self.current_load = max(0, self.current_load)
        self.update_temperature()

    def update_temperature(self):
        self.temperature = 25 + (self.current_load * 0.5)

    def cool_down(self):
        self.temperature -= 5
        self.temperature = max(25, self.temperature)

    def __repr__(self):
        return f"Server(id={self.server_id}, load={self.current_load}, temp={self.temperature:.2f}°C)"


class DataCenter:
    """
    Classe que gerencia os servidores de um data center e a alocação de tarefas.

    Atributos:
        servers (SortedList): Lista ordenada de servidores no data center, mantida com base na temperatura e carga.

    Métodos:
        add_task(load): Adiciona uma carga de tarefa ao servidor com a menor temperatura e carga.
        check_and_cool(): Verifica se algum servidor ultrapassou a temperatura máxima e realiza o resfriamento.
        redistribute_load(overheated_server): Redistribui a carga de um servidor sobrecarregado para servidores mais frios.
        status(): Exibe o status atual dos servidores e suas cargas de trabalho.
    """

    def __init__(self, num_servers=5):
        self.servers = SortedList(key=lambda s: (s.temperature, s.current_load))
        for i in range(num_servers):
            server = Server(i)
            self.servers.add(server)

    def add_task(self, load):
        selected_server = self.servers[0]
        selected_server.add_task(load)
        print(f"Tarefa de carga {load} alocada ao Servidor {selected_server.server_id} (Temp: {selected_server.temperature:.2f}°C)")
        self.check_and_cool()

    def check_and_cool(self):
        for server in self.servers:
            if server.temperature > server.max_temp:
                initial_temp = server.temperature
                self.redistribute_load(server)
                server.cool_down()
                temp_difference = initial_temp - server.temperature
                print(f"Servidor {server.server_id} reduziu sua temperatura em {temp_difference:.2f}°C.")

    def redistribute_load(self, overheated_server):
        redistribute_amount = overheated_server.current_load // 2
        overheated_server.release_task(redistribute_amount)
        cooler_servers = [s for s in self.servers if s != overheated_server]
        cooler_servers.sort(key=lambda s: s.temperature)

        for server in cooler_servers:
            if redistribute_amount <= 0:
                break
            task_chunk = min(redistribute_amount, 10)
            server.add_task(task_chunk)
            overheated_server.tasks_transferred += task_chunk
            redistribute_amount -= task_chunk
            print(f"Tarefa de carga {task_chunk} transferida para Servidor {server.server_id} (Temp: {server.temperature:.2f}°C)")

    def status(self):
        print("\n===== Status Atual dos Servidores =====")
        for server in self.servers:
            print(f"Servidor {server.server_id}:")
            print(f"  - Carga atual: {server.current_load} unidades")
            print(f"  - Temperatura: {server.temperature:.2f}°C")
            print(f"  - Tarefas transferidas: {server.tasks_transferred}")
        print("=======================================")


def generate_user_tasks(num_users):
    return [random.randint(5, 50) for _ in range(num_users)]


def test_performance(num_users, data_center, task_delay=0.01):
    """
    Testa o desempenho do sistema simulando a adição de tarefas para uma quantidade específica de usuários.

    Args:
        num_users (int): O número de usuários (tarefas) a serem simulados.
        data_center (DataCenter): O objeto do data center no qual as tarefas serão alocadas.
        task_delay (float): Tempo de espera entre as alocações de tarefas (em segundos).
    """
    max_time = math.log2(num_users)  # Tempo máximo baseado em log2(N)
    tasks = generate_user_tasks(num_users)
    start_time = time.time()

    for load in tasks:
        # Verifique se o tempo máximo foi atingido
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            print(f"Tempo máximo de {max_time:.2f} segundos alcançado. Teste interrompido.")
            break
        
        data_center.add_task(load)
        time.sleep(task_delay)  # Ajustável, simula tempo entre as tarefas
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTempo total de execução para {num_users} tarefas: {elapsed_time:.4f} segundos")
    
    # Verificar se o tempo máximo foi excedido
    if elapsed_time > max_time:
        print(f"Atenção: O tempo máximo de {max_time:.2f} segundos foi excedido.")
    else:
        print(f"O teste foi concluído dentro do tempo máximo.")
    

# Exemplo de uso
data_center = DataCenter(num_servers=5)

# Testando com 1.000, 10.000 e 100.000 usuários
for num_users in [1000, 10000, 100000]:
    print(f"\nTestando com {num_users} usuários:")
    test_performance(num_users, data_center, task_delay=0.01)
    data_center.status()
    print("\n---")
