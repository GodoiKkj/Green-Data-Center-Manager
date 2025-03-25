import time
from sortedcontainers import SortedList


class Server:
    """
    Representa um servidor no Data Center.

    Atributos:
    server_id (int): Identificador único do servidor.
    current_load (int): Carga atual do servidor.
    temperature (float): Temperatura atual do servidor.
    max_temp (float): Temperatura máxima permitida para o servidor.
    tasks_transferred (int): Quantidade de tarefas transferidas de/para o servidor.

    Métodos:
    add_task(load): Adiciona carga ao servidor e atualiza a temperatura.
    release_task(load): Libera carga do servidor e atualiza a temperatura.
    update_temperature(): Atualiza a temperatura do servidor com base na carga.
    cool_down(): Diminui a temperatura do servidor.
    __repr__(): Representação textual do servidor.
    """
    
    def __init__(self, server_id, max_temp=75):
        self.server_id = server_id
        self.current_load = 0
        self.temperature = 25
        self.max_temp = max_temp
        self.tasks_transferred = 0

    def add_task(self, load):
        """Adiciona carga ao servidor e atualiza sua temperatura."""
        self.current_load += load
        self.update_temperature()

    def release_task(self, load):
        """Libera carga do servidor e atualiza sua temperatura."""
        self.current_load -= load
        self.current_load = max(0, self.current_load)
        self.update_temperature()

    def update_temperature(self):
        """Atualiza a temperatura do servidor com base na carga atual."""
        self.temperature = 25 + (self.current_load * 0.5)

    def cool_down(self):
        """Diminui a temperatura do servidor em 5°C, com limite de 25°C."""
        self.temperature -= 5
        self.temperature = max(25, self.temperature)

    def __repr__(self):
        return f"Server(id={self.server_id}, load={self.current_load}, temp={self.temperature:.2f}°C)"


class DataCenter:
    """
    Representa um Data Center que gerencia servidores e a alocação de tarefas.

    Atributos:
    servers (SortedList): Lista de servidores ordenada por temperatura e carga.
    
    Métodos:
    add_task(load): Adiciona uma tarefa ao servidor com menor temperatura e carga.
    check_and_cool(): Verifica e resfria os servidores que ultrapassaram a temperatura máxima.
    redistribute_load(overheated_server): Redistribui a carga de um servidor que superou o limite de temperatura.
    status(): Exibe o status atual de todos os servidores e da carga de energia.
    """
    
    def __init__(self, num_servers=5):
        """Inicializa o Data Center com servidores."""
        self.servers = SortedList([Server(i) for i in range(num_servers)], key=lambda s: (s.temperature, s.current_load))

    def add_task(self, load):
        """
        Aloca uma tarefa para o servidor com menor temperatura e carga.

        Parâmetros:
        load (int): A carga da tarefa a ser alocada ao servidor.
        """
        selected_server = self.servers[0]
        selected_server.add_task(load)
        print(f"Tarefa de carga {load} alocada ao Servidor {selected_server.server_id} (Temp: {selected_server.temperature:.2f}°C)")
        self.check_and_cool()

    def check_and_cool(self):
        """Verifica se algum servidor está superaquecido e resfria quando necessário."""
        for server in self.servers:
            if server.temperature > server.max_temp:
                initial_temp = server.temperature
                self.redistribute_load(server)
                server.cool_down()
                temp_difference = initial_temp - server.temperature
                print(f"Servidor {server.server_id} reduziu sua temperatura em {temp_difference:.2f}°C.")

    def redistribute_load(self, overheated_server):
        """
        Redistribui a carga de um servidor que superou o limite de temperatura.

        Parâmetros:
        overheated_server (Server): O servidor que precisa ter sua carga redistribuída.
        """
        redistribute_amount = overheated_server.current_load // 2
        overheated_server.release_task(redistribute_amount)
        cooler_servers = sorted([s for s in self.servers if s != overheated_server], key=lambda s: s.temperature)

        for server in cooler_servers:
            if redistribute_amount <= 0:
                break
            task_chunk = min(redistribute_amount, 10)
            server.add_task(task_chunk)
            overheated_server.tasks_transferred += task_chunk
            redistribute_amount -= task_chunk
            print(f"Tarefa de carga {task_chunk} transferida para Servidor {server.server_id} (Temp: {server.temperature:.2f}°C)")

    def status(self):
        """Exibe o status atual de todos os servidores e da fonte de energia."""
        print("\n===== Status Atual dos Servidores =====")
        for server in self.servers:
            print(f"Servidor {server.server_id}:")
            print(f"  - Carga atual: {server.current_load} unidades")
            print(f"  - Temperatura: {server.temperature:.2f}°C")
            print(f"  - Tarefas transferidas: {server.tasks_transferred}")
        print("=======================================")


# Exemplo de uso
data_center = DataCenter(num_servers=5)

task_loads = [20, 40, 15, 10, 35, 50, 30]
for load in task_loads:
    data_center.add_task(load)
    time.sleep(1)
    data_center.status()
    print("\n---")
