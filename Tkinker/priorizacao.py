from sortedcontainers import SortedList
from typing import Tuple

class EnergySource:
    """
    Representa a fonte de energia de um DataCenter, incluindo capacidades renováveis e comuns.
    """
    def __init__(self, renewable_capacity_kW: float, regular_capacity_kW: float, num_servers: int):
        """
        Inicializa a fonte de energia.

        Args:
            renewable_capacity_kW (float): Capacidade total de energia renovável em kW.
            regular_capacity_kW (float): Capacidade total de energia comum em kW.
            num_servers (int): Número de servidores.
        """
        self.total_renewable_capacity = renewable_capacity_kW
        self.renewable_capacity_per_server = renewable_capacity_kW / num_servers
        self.regular_capacity = regular_capacity_kW
        self.num_servers = num_servers

    def allocate_energy(self, demand_kW: float, server_id: int) -> Tuple[str, Tuple[float, float]]:
        """
        Aloca energia para um servidor com base na demanda.

        Args:
            demand_kW (float): A demanda de energia do servidor.
            server_id (int): O ID do servidor.

        Returns:
            Tuple[str, Tuple[float, float]]: Tipo de energia usada (renovável, mista) e a quantidade de energia consumida.
        """
        available_renewable = self.renewable_capacity_per_server

        if demand_kW <= available_renewable:
            renewable_used = demand_kW
            self.total_renewable_capacity -= renewable_used
            self.renewable_capacity_per_server = self.total_renewable_capacity / self.num_servers
            return 'renewable', (renewable_used, 0)
        else:
            renewable_used = available_renewable
            self.total_renewable_capacity -= renewable_used
            self.renewable_capacity_per_server = self.total_renewable_capacity / self.num_servers

            regular_needed = demand_kW - renewable_used
            if regular_needed <= self.regular_capacity:
                regular_used = regular_needed
                self.regular_capacity -= regular_used
            else:
                regular_used = self.regular_capacity
                self.regular_capacity = 0

            return 'mixed', (renewable_used, regular_used)

    def renewable_status(self) -> float:
        """
        Retorna o status da energia renovável disponível.

        Returns:
            float: A energia renovável total disponível.
        """
        return self.total_renewable_capacity

    def regular_status(self) -> float:
        """
        Retorna o status da energia comum disponível.

        Returns:
            float: A energia comum total disponível.
        """
        return self.regular_capacity

    def __repr__(self):
        return f"EnergySource(renewable_total={self.total_renewable_capacity} kW, regular={self.regular_capacity} kW)"

class Server:
    """
    Representa um servidor no DataCenter.
    """
    def __init__(self, server_id: int, energy_consumption_kW: float):
        """
        Inicializa um servidor.

        Args:
            server_id (int): Identificador do servidor.
            energy_consumption_kW (float): Consumo de energia do servidor por tarefa.
        """
        self.server_id = server_id
        self.energy_consumption = energy_consumption_kW
        self.is_active = False
        self.renewable_used = 0
        self.regular_used = 0

    def activate(self, renewable_used: float, regular_used: float):
        """
        Ativa o servidor com a energia alocada.

        Args:
            renewable_used (float): Energia renovável usada.
            regular_used (float): Energia comum usada.
        """
        self.is_active = True
        self.renewable_used = renewable_used
        self.regular_used = regular_used
        print(f"Servidor {self.server_id} ativado.")

    def deactivate(self):
        """
        Desativa o servidor.
        """
        self.is_active = False
        print(f"Servidor {self.server_id} desativado.")

    def __repr__(self):
        return f"Server(id={self.server_id}, consumption={self.energy_consumption} kW, active={self.is_active}, renewable_used={self.renewable_used} kW, regular_used={self.regular_used} kW)"

class DataCenter:
    """
    Representa o DataCenter, gerenciando a alocação de servidores e energia.
    """
    def __init__(self, renewable_capacity_kW: float, regular_capacity_kW: float, server_energy_consumption_kW: float, num_servers: int):
        """
        Inicializa o DataCenter com capacidade de energia e servidores.

        Args:
            renewable_capacity_kW (float): Capacidade de energia renovável total.
            regular_capacity_kW (float): Capacidade de energia comum total.
            server_energy_consumption_kW (float): Consumo de energia por servidor.
            num_servers (int): Número de servidores.
        """
        self.energy_source = EnergySource(renewable_capacity_kW, regular_capacity_kW, num_servers)
        self.servers = SortedList([Server(i, server_energy_consumption_kW) for i in range(num_servers)], key=lambda server: server.server_id)

    def assign_task(self, server_id: int):
        """
        Atribui uma tarefa a um servidor, alocando a energia necessária.

        Args:
            server_id (int): Identificador do servidor.
        """
        server = self.servers[server_id]
        if server.is_active:
            print(f"Servidor {server_id} já está ativo.")
            return

        energy_type, energy_used = self.energy_source.allocate_energy(server.energy_consumption, server_id)
        renewable_used, regular_used = energy_used

        if energy_type == 'insufficient':
            print(f"Não há energia suficiente para ativar o servidor {server_id}.")
        else:
            server.activate(renewable_used, regular_used)
            if energy_type == 'mixed':
                print(f"Servidor {server_id} está usando energia mista: {renewable_used} kW renovável e {regular_used} kW comum.")

    def deactivate_server(self, server_id: int):
        """
        Desativa um servidor.

        Args:
            server_id (int): Identificador do servidor.
        """
        server = self.servers[server_id]
        if not server.is_active:
            print(f"Servidor {server_id} já está desativado.")
            return

        server.deactivate()

    def status(self):
        """
        Exibe o status dos servidores e da fonte de energia.
        """
        print("\nStatus dos Servidores:")
        for server in self.servers:
            print(server)
        print("\nStatus da Fonte de Energia:")
        print(f"Energia renovável total disponível: {self.energy_source.renewable_status()} kW")
        print(f"Energia comum disponível: {self.energy_source.regular_status()} kW")


# Configuração do DataCenter com capacidades fictícias e servidores
data_center = DataCenter(renewable_capacity_kW=300, regular_capacity_kW=500, server_energy_consumption_kW=50, num_servers=5)

# Ativa servidores e aloca energia
for i in range(5):
    data_center.assign_task(i)
    data_center.status()
    print("\n---")

# Desativa um servidor
data_center.deactivate_server(1)
data_center.status()
