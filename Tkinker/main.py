import time
import threading
import random
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# ===================== Classes de Backend =====================

class EnergySource:
    """
    Representa a fonte de energia de um data center, com capacidade renovável e regular.

    A classe gerencia a alocação de energia renovável e regular para servidores com base na demanda de energia.

    Atributos:
        total_renewable_capacity (float): A capacidade total de energia renovável disponível (em kW).
        renewable_capacity_per_server (float): A capacidade de energia renovável alocada para cada servidor (em kW).
        regular_capacity (float): A capacidade de energia regular disponível (em kW).
        num_servers (int): O número de servidores que usam a energia.

    Métodos:
        __init__(renewable_capacity_kW, regular_capacity_kW, num_servers):
            Inicializa uma instância da classe EnergySource com os valores fornecidos.
        
        allocate_energy(demand_kW):
            Aloca energia renovável ou regular para atender à demanda de energia de um servidor.
            Retorna uma tupla contendo o tipo de energia alocada (renovável ou mista) e os valores de energia alocada.

        renewable_status():
            Retorna a quantidade de energia renovável restante.

        regular_status():
            Retorna a quantidade de energia regular restante.
    """

    def __init__(self, renewable_capacity_kW, regular_capacity_kW, num_servers):
        self.total_renewable_capacity = renewable_capacity_kW
        self.renewable_capacity_per_server = renewable_capacity_kW / num_servers
        self.regular_capacity = regular_capacity_kW
        self.num_servers = num_servers

    def allocate_energy(self, demand_kW):
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

    def renewable_status(self):
        return self.total_renewable_capacity

    def regular_status(self):
        return self.regular_capacity


class Server:
    """
    Representa um servidor em um data center.

    A classe armazena o consumo de energia do servidor e seu estado (ativo ou inativo).

    Atributos:
        server_id (int): O identificador único do servidor.
        energy_consumption (float): O consumo de energia do servidor (em kW).
        is_active (bool): O estado do servidor, se está ativo ou não.
        renewable_used (float): A quantidade de energia renovável usada pelo servidor (em kW).
        regular_used (float): A quantidade de energia regular usada pelo servidor (em kW).

    Métodos:
        __init__(server_id, energy_consumption_kW):
            Inicializa uma instância de Server com o id do servidor e o consumo de energia.

        activate(renewable_used, regular_used):
            Ativa o servidor e registra a quantidade de energia renovável e regular usada.

        deactivate():
            Desativa o servidor.

        __repr__():
            Retorna uma representação em string do servidor com seu id, estado e uso de energia.
    """

    def __init__(self, server_id, energy_consumption_kW):
        self.server_id = server_id
        self.energy_consumption = energy_consumption_kW
        self.is_active = False
        self.renewable_used = 0
        self.regular_used = 0

    def activate(self, renewable_used, regular_used):
        self.is_active = True
        self.renewable_used = renewable_used
        self.regular_used = regular_used

    def deactivate(self):
        self.is_active = False

    def __repr__(self):
        return f"Server(id={self.server_id}, active={self.is_active}, renewable_used={self.renewable_used}, regular_used={self.regular_used})"


class DataCenter:
    """
    Representa um centro de dados, que gerencia servidores e a alocação de energia.

    A classe controla a alocação de energia renovável e regular para os servidores, 
    além de gerenciar o estado dos servidores.

    Atributos:
        energy_source (EnergySource): A instância da classe EnergySource, responsável pela alocação de energia.
        servers (list): Lista de instâncias da classe Server, representando os servidores do data center.

    Métodos:
        __init__(renewable_capacity_kW, regular_capacity_kW, server_energy_consumption_kW, num_servers):
            Inicializa uma instância de DataCenter com a capacidade de energia renovável e regular, 
            o consumo de energia dos servidores e o número de servidores.

        assign_task(server_id):
            Atribui uma tarefa a um servidor, alocando a energia necessária para o seu funcionamento.

        deactivate_server(server_id):
            Desativa um servidor no data center.

        get_status():
            Retorna o status do data center, com o número de servidores ativos e ociosos, 
            e a quantidade de energia renovável e regular restante.
    """

    def __init__(self, renewable_capacity_kW, regular_capacity_kW, server_energy_consumption_kW, num_servers):
        self.energy_source = EnergySource(renewable_capacity_kW, regular_capacity_kW, num_servers)
        self.servers = [Server(i, server_energy_consumption_kW) for i in range(num_servers)]
        
    def assign_task(self, server_id):
        server = self.servers[server_id]
        if server.is_active:
            return
        energy_type, energy_used = self.energy_source.allocate_energy(server.energy_consumption)
        renewable_used, regular_used = energy_used
        server.activate(renewable_used, regular_used)

    def deactivate_server(self, server_id):
        server = self.servers[server_id]
        if server.is_active:
            server.deactivate()

    def get_status(self):
        active = sum(1 for s in self.servers if s.is_active)
        idle = sum(1 for s in self.servers if not s.is_active)
        renewable = self.energy_source.renewable_status()
        regular = self.energy_source.regular_status()
        return active, idle, renewable, regular

# ===================== Interface Gráfica ======================

class Application:
    """
    Representa a interface gráfica de um aplicativo de login utilizando Tkinter.

    A classe cria a janela de login, com campos para usuário e senha, e botões para "Entrar" e "Sair".
    Após o login bem-sucedido, a classe redireciona para um painel de controle (Dashboard).

    Atributos:
        master (Tk): A instância da janela principal do Tkinter.
    
    Métodos:
        __init__(master=None):
            Inicializa a interface gráfica, define o layout, campos de entrada e botões.

        centralizar_janela(largura, altura):
            Centraliza a janela na tela do computador.

        abrir_dashboard():
            Fecha a janela de login e abre o painel de controle (Dashboard).

        login():
            Realiza a validação de login. Se o login for bem-sucedido, exibe uma mensagem de sucesso e 
            redireciona para o painel de controle. Caso contrário, exibe uma mensagem de erro.

    """

    def __init__(self, master=None):
        self.master = master
        self.master.configure(bg="white")  # Fundo branco
        self.master.geometry("400x400")
        self.centralizar_janela(400, 400)

        # Título estilizado
        self.containerTitulo = Frame(master, bg="white")
        self.containerTitulo.pack(pady=20)
        self.msg = Label(self.containerTitulo, text="Login", font=("Calibri", 18, "bold"), bg="white", fg="#4CAF50")
        self.msg.pack()

        # Campo de usuário
        self.containerUsuario = Frame(master, bg="white")
        self.containerUsuario.pack(pady=10)
        self.inputLogin = Entry(self.containerUsuario, width=30, font=("Calibri", 12), bd=2, relief="solid")
        self.inputLogin.pack(ipady=8, padx=20)

        # Campo de senha
        self.containerSenha = Frame(master, bg="white")
        self.containerSenha.pack(pady=10)
        self.inputPassword = Entry(self.containerSenha, width=30, font=("Calibri", 12), bd=2, relief="solid", show="*")
        self.inputPassword.pack(ipady=8, padx=20)

        # Botões estilizados
        self.containerBotoes = Frame(master, bg="white")
        self.containerBotoes.pack(pady=20)
        self.botaoEntrar = Button(
            self.containerBotoes, text="Entrar", font=("Calibri", 12, "bold"), bg="#4CAF50", fg="white", 
            width=12, relief="flat", command=self.login
        )
        self.botaoEntrar.pack(side=LEFT, padx=10)

        self.botaoSair = Button(
            self.containerBotoes, text="Sair", font=("Calibri", 12, "bold"), bg="#f44336", fg="white", 
            width=12, relief="flat", command=quit
        )
        self.botaoSair.pack(side=LEFT, padx=10)

        # Mensagem de feedback
        self.containerMensagemLogin = Frame(master, bg="white")
        self.containerMensagemLogin.pack(pady=10)
        self.mensagemDoLogin = Label(self.containerMensagemLogin, text="", font=("Calibri", 12), bg="white")
        self.mensagemDoLogin.pack()

    def centralizar_janela(self, largura, altura):
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.master.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def abrir_dashboard(self):
        self.master.destroy()
        dashboard = Tk()
        Dashboard(dashboard)
        dashboard.mainloop()

    def login(self):
        usuario = self.inputLogin.get()
        senha = self.inputPassword.get()
        if usuario == "administrador" and senha == "admin":
            self.mensagemDoLogin["text"] = "Login realizado com sucesso!"
            self.mensagemDoLogin["foreground"] = "green"
            self.master.after(1000, self.abrir_dashboard)
        else:
            self.mensagemDoLogin["text"] = "O login falhou!"
            self.mensagemDoLogin["foreground"] = "red"


class Dashboard:
    """
    Representa o painel de controle do Gerenciador de Data Center.

    A classe cria uma interface gráfica para monitorar o consumo de energia, status dos servidores 
    e a distribuição de carga no data center. Inclui gráficos interativos e indicadores de status.

    Atributos:
        master (Tk): Instância da janela principal do Tkinter.
        data_center (DataCenter): Instância do DataCenter que contém servidores e fontes de energia.
        running (bool): Controle de execução do painel de controle.
        container (Frame): Frame principal que contém todos os elementos da interface.
        frame_indicators (Frame): Frame que contém os indicadores de status.
        frame_graphs (Frame): Frame que contém os gráficos de consumo de energia e cargas de servidores.
        renewable_data (deque): Armazena dados de consumo de energia renovável.
        regular_data (deque): Armazena dados de consumo de energia comum.
        active_servers_data (deque): Armazena dados sobre servidores ativos.
        server_loads (list): Lista que contém a carga de cada servidor.
        backend_thread (Thread): Thread que executa o backend, simulando tarefas e atualizando os dados.
    
    Métodos:
        __init__(master=None):
            Inicializa o painel de controle com gráficos, indicadores e uma thread para simular tarefas no backend.

        centralizar_janela(largura, altura):
            Centraliza a janela do dashboard na tela.

        create_indicator(parent, title, value, color):
            Cria um indicador com título e valor estilizados.

        update_backend():
            Atualiza dinamicamente os dados do painel (gráficos e indicadores), simulando a execução de tarefas e consumo de energia.

        simulate_tasks():
            Simula a oscilação no número de tarefas ativas e ajusta os servidores com base na energia disponível.

        redistribute_load(server_loads, max_capacity=200000):
            Redistribui a carga entre os servidores para garantir que nenhum ultrapasse a capacidade máxima.

        exit_dashboard():
            Encerra o painel de controle e interrompe a thread de atualização.

    """
    
    def __init__(self, master=None):
        self.master = master
        self.master.geometry("900x700")
        self.centralizar_janela(900, 700)
        self.master.title("Green Data Center Manager - Dashboard")
        
        # Variáveis de controle
        self.data_center = DataCenter(renewable_capacity_kW=100, regular_capacity_kW=50, 
                                      server_energy_consumption_kW=5, num_servers=20)
        self.running = True

        # Frame principal
        self.container = Frame(master)
        self.container.pack(fill=BOTH, expand=True)

        # Indicadores com botão de sair
        self.frame_indicators = Frame(self.container, bg="white")
        self.frame_indicators.pack(side=TOP, fill=X, padx=10, pady=10)

        self.indicator_width = 15

        self.lbl_active = self.create_indicator(
            self.frame_indicators, "Servidores Ativos", "0", "#4CAF50"
        )
        self.lbl_idle = self.create_indicator(
            self.frame_indicators, "Servidores Ociosos", "20", "#FF9800"
        )
        self.lbl_renewable = self.create_indicator(
            self.frame_indicators, "Energia Renovável (kW)", "100", "#2196F3"
        )
        self.lbl_regular = self.create_indicator(
            self.frame_indicators, "Energia Comum (kW)", "50", "#E91E63"
        )

        # Botão de sair
        self.exit_button = Button(
            self.frame_indicators, text="Sair", font=("Calibri", 12), 
            bg="#f44336", fg="white", width=self.indicator_width, 
            command=self.exit_dashboard
        )
        self.exit_button.pack(side=RIGHT, padx=20)

        # Gráficos
        self.frame_graphs = Frame(self.container)
        self.frame_graphs.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.figure = Figure(figsize=(9, 6), dpi=100)
        self.ax1 = self.figure.add_subplot(221)
        self.ax2 = self.figure.add_subplot(222)
        self.ax3 = self.figure.add_subplot(212)

        # Gráfico de consumo de energia
        self.ax1.set_title("Consumo de Energia Renovável")
        self.ax2.set_title("Consumo de Energia Comum")

        self.renewable_data = deque([100] * 20, maxlen=20)
        self.regular_data = deque([50] * 20, maxlen=20)
        self.active_servers_data = deque([0] * 20, maxlen=20)
        self.server_loads = [0] * self.data_center.energy_source.num_servers

        # Gráfico de cargas de servidores
        self.ax3.set_title("Cargas de Servidores e Ativação")
        self.ax3.set_xticks(range(len(self.server_loads)))  # Define 1 servidor por unidade no eixo X
        self.ax3.set_xticklabels([str(i) for i in range(len(self.server_loads))], rotation=90)  # Rotula os servidores no eixo X
        
        self.line1, = self.ax1.plot(self.renewable_data, marker='o', label="kW")
        self.line2, = self.ax2.plot(self.regular_data, marker='o', label="kW")
        self.bar_servers = self.ax3.bar(range(len(self.server_loads)), self.server_loads, label="Cargas por Servidor")


        canvas = FigureCanvasTkAgg(self.figure, self.frame_graphs)
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # Thread para backend
        self.backend_thread = threading.Thread(target=self.update_backend)
        self.backend_thread.daemon = True
        self.backend_thread.start()

    def create_indicator(self, parent, title, value, color):
        """Cria uma label estilizada com título e valor."""
        frame = Frame(parent, bg="white", width=self.indicator_width)
        frame.pack(side=LEFT, padx=20)

        lbl_title = Label(
            frame, text=title, font=("Calibri", 10, "bold"), bg="white"
        )
        lbl_title.pack()

        lbl_value = Label(
            frame, text=value, font=("Calibri", 14), bg="white", fg=color
        )
        lbl_value.pack()

        return lbl_value

    def centralizar_janela(self, largura, altura):
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.master.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def update_backend(self):
        while self.running:
            # Simula o incremento controlado de energia
            if self.data_center.energy_source.total_renewable_capacity < 80:
                self.data_center.energy_source.total_renewable_capacity += 5
            if self.data_center.energy_source.regular_capacity < 40:
                self.data_center.energy_source.regular_capacity += 3

            # Simula tarefas dinamicamente
            self.simulate_tasks()

            # Atualizar gráficos e indicadores
            active, idle, renewable, regular = self.data_center.get_status()
            renewable_used = sum(server.renewable_used for server in self.data_center.servers)
            regular_used = sum(server.regular_used for server in self.data_center.servers)

            self.renewable_data.append(renewable_used)
            self.regular_data.append(regular_used)
            self.active_servers_data.append(active)

            self.lbl_active.config(text=active)
            self.lbl_idle.config(text=idle)
            self.lbl_renewable.config(text=f"{renewable:.2f} kW")
            self.lbl_regular.config(text=f"{regular:.2f} kW")

            # Atualiza os gráficos
            self.line1.set_ydata(self.renewable_data)
            self.line2.set_ydata(self.regular_data)

            # Ajuste os valores das cargas para serem proporcionais a 200 mil
            scaled_loads = [load * 20000 for load in self.server_loads]

            for bar, load in zip(self.bar_servers, scaled_loads):
                bar.set_height(load)

            # Ajuste os limites dos eixos Y
            max_renewable = max(self.renewable_data) if self.renewable_data else 1
            max_regular = max(self.regular_data) if self.regular_data else 1

            self.ax1.set_ylim(0, max(max_renewable + 10, 20))  # Certifica-se de que o mínimo é sempre 20
            self.ax2.set_ylim(0, max(max_regular + 10, 20))
            self.ax3.set_ylim(0, 210000)  # Mantém o limite fixo para os servidores

            self.figure.canvas.draw_idle()  # Atualiza os gráficos
            time.sleep(1)


    def simulate_tasks(self):
        # Simula uma oscilação de tarefas
        new_tasks = max(0, min(50, self.active_servers_data[-1] + (1 if random.random() > 0.5 else -1)))

        # Ajusta os servidores
        for i, server in enumerate(self.data_center.servers):
            if i < new_tasks:
                if not server.is_active and self.data_center.energy_source.total_renewable_capacity >= server.energy_consumption:
                    self.data_center.assign_task(i)
                self.server_loads[i] = min(self.server_loads[i] + 1, 200000)  # Ajusta a capacidade máxima
            else:
                if server.is_active:
                    self.data_center.deactivate_server(i)
                self.server_loads[i] = max(self.server_loads[i] - 1, 0)

        # Redistribui as cargas se necessário
        self.server_loads = self.redistribute_load(self.server_loads, max_capacity=200000)

    def redistribute_load(self, server_loads, max_capacity=200000):
        """
        Redistribui a carga dos servidores caso algum ultrapasse a capacidade máxima.

        Args:
            server_loads (list): Lista com a carga atual de cada servidor.
            max_capacity (int): Capacidade máxima de cada servidor.

        Returns:
            list: Lista de cargas ajustadas após a redistribuição.
        """
        while any(load > max_capacity for load in server_loads):
            for i, load in enumerate(server_loads):
                if load > max_capacity:
                    excess = load - max_capacity
                    server_loads[i] = max_capacity  # Limita o servidor sobrecarregado
                    # Redistribuir o excesso para outros servidores com espaço disponível
                    for j, other_load in enumerate(server_loads):
                        if i != j and other_load < max_capacity:
                            available_space = max_capacity - other_load
                            transfer = min(excess, available_space)
                            server_loads[j] += transfer
                            excess -= transfer
                            if excess == 0:
                                break
        return server_loads

    def exit_dashboard(self):
        self.running = False
        self.master.destroy()


# Configuração da janela principal
window = Tk()
window.title("Green Data Center Manager")

# Instância da aplicação
Application(window)

# Loop principal
window.mainloop()
