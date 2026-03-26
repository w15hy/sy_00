"""
buses.py - Módulo de Buses de la Arquitectura
================================================================================
Define los buses de comunicación entre componentes de la CPU:
  - AddressBus: Lleva direcciones de memoria
  - DataBus: Lleva datos
  - ControlBus: Lleva señales de control (read/write/enable, etc.)

Estos buses son componentes EXPLÍCITOS de la arquitectura.
================================================================================
"""


class AddressBus:
    """
    Bus de Direcciones (Address Bus)
    ────────────────────────────────
    Líneas de señal que transportan direcciones de memoria.
    
    Especificación:
    - Ancho: 32 bits (permite direccionar hasta 4 GB)
    - Origen: CPU, destino: RAM
    - Dirección: Unidireccional (CPU → memoria)
    """
    
    def __init__(self, width: int = 32):
        """
        Args:
            width: Ancho del bus en bits (32 por defecto)
        """
        self.width = width
        self.address = 0  # Valor actual en el bus
        self.mask = (1 << width) - 1
    
    def set_address(self, address: int) -> None:
        """Coloca una dirección en el bus"""
        if not isinstance(address, int):
            raise TypeError(f"Dirección debe ser int, recibido: {type(address)}")
        if address < 0 or address > self.mask:
            raise ValueError(
                f"Dirección fuera de rango [0, {self.mask}]. Recibido: {address}"
            )
        self.address = address
    
    def get_address(self) -> int:
        """Lee la dirección actual del bus"""
        return self.address
    
    def clear(self) -> None:
        """Limpia el bus (reset a 0)"""
        self.address = 0
    
    def __repr__(self) -> str:
        return f"AddressBus(0x{self.address:08X})"


class DataBus:
    """
    Bus de Datos (Data Bus)
    ───────────────────────
    Líneas de señal que transportan datos entre CPU y memoria.
    
    Especificación:
    - Ancho: 64 bits
    - Origen/Destino: Bidireccional (CPU ↔ RAM)
    - Se usa para leer y escribir datos en memoria
    """
    
    def __init__(self, width: int = 64):
        """
        Args:
            width: Ancho del bus en bits (64 por defecto)
        """
        self.width = width
        self.data = 0  # Valor actual en el bus
        self.mask = (1 << width) - 1
    
    def write_data(self, data: int) -> None:
        """Coloca datos en el bus (escritura)"""
        if isinstance(data, str):  # Si viene como binario
            data = int(data, 2)
        if not isinstance(data, int):
            raise TypeError(f"Dato debe ser int o str binario, recibido: {type(data)}")
        if data < 0 or data > self.mask:
            raise ValueError(
                f"Dato fuera de rango [0, {self.mask}]. Recibido: {data}"
            )
        self.data = data
    
    def read_data(self) -> int:
        """Lee datos del bus"""
        return self.data
    
    def get_data_binary(self) -> str:
        """Retorna los datos como string binario de 64 bits"""
        return bin(self.data)[2:].zfill(self.width)
    
    def clear(self) -> None:
        """Limpia el bus (reset a 0)"""
        self.data = 0
    
    def __repr__(self) -> str:
        return f"DataBus(0x{self.data:016X})"


class ControlBus:
    """
    Bus de Control (Control Bus)
    ─────────────────────────────
    Líneas de señal que coordinan la operación entre componentes.
    
    Señales de control:
    - READ: Solicita lectura de memoria
    - WRITE: Solicita escritura en memoria
    - ENABLE: Habilita la memoria
    - READY: Indica que la memoria está lista
    - INTERRUPT: Señal de interrupción
    - CLOCK: Pulso de reloj (sincronización)
    """
    
    def __init__(self):
        """Inicializa todas las señales de control en False/0"""
        # Señales del CPU a la memoria
        self.READ = False      # 1 = leer, 0 = no leer
        self.WRITE = False     # 1 = escribir, 0 = no escribir
        self.ENABLE = False    # 1 = memoria habilitada
        
        # Señales de la memoria al CPU
        self.READY = True      # 1 = dato listo, 0 = esperando
        self.INTERRUPT = False # 1 = interrupción pendiente
        
        # Señal de reloj
        self.CLOCK = False     # Pulso de reloj para sincronización
    
    def set_read(self, value: bool) -> None:
        """Activa o desactiva la lectura"""
        self.READ = bool(value)
    
    def set_write(self, value: bool) -> None:
        """Activa o desactiva la escritura"""
        self.WRITE = bool(value)
    
    def set_enable(self, value: bool) -> None:
        """Habilita o deshabilita la memoria"""
        self.ENABLE = bool(value)
    
    def set_ready(self, value: bool) -> None:
        """Señala que el dato está listo"""
        self.READY = bool(value)
    
    def set_interrupt(self, value: bool) -> None:
        """Activa o desactiva una interrupción"""
        self.INTERRUPT = bool(value)
    
    def pulse_clock(self) -> None:
        """Simula un pulso de reloj (HIGH → LOW)"""
        self.CLOCK = not self.CLOCK
    
    def get_signals(self) -> dict:
        """Retorna el estado actual de todas las señales"""
        return {
            "READ": self.READ,
            "WRITE": self.WRITE,
            "ENABLE": self.ENABLE,
            "READY": self.READY,
            "INTERRUPT": self.INTERRUPT,
            "CLOCK": self.CLOCK,
        }
    
    def reset(self) -> None:
        """Reinicia todas las señales a su estado inicial"""
        self.READ = False
        self.WRITE = False
        self.ENABLE = False
        self.READY = True
        self.INTERRUPT = False
        self.CLOCK = False
    
    def __repr__(self) -> str:
        signals = " | ".join(f"{k}={'1' if v else '0'}" for k, v in self.get_signals().items())
        return f"ControlBus({signals})"


class BusInterface:
    """
    Interfaz de Buses (Bus Interface Unit - BIU)
    ─────────────────────────────────────────────
    Proporciona una vista consolidada de los tres buses para
    simplificar su uso. Es el punto central de comunicación.
    """
    
    def __init__(self):
        self.address_bus = AddressBus(width=32)
        self.data_bus = DataBus(width=64)
        self.control_bus = ControlBus()
    
    def read_from_memory(self, address: int) -> int:
        """
        Cycle de lectura:
        1. Coloca la dirección en AddressBus
        2. Activa READ en ControlBus
        3. Espera READY
        4. Lee datos del DataBus
        """
        self.address_bus.set_address(address)
        self.control_bus.set_read(True)
        self.control_bus.set_enable(True)
        # En una máquina real, aquí esperar READY
        # Por ahora asumimos acceso instantáneo
        self.control_bus.set_read(False)
        return self.data_bus.read_data()
    
    def write_to_memory(self, address: int, data: int) -> None:
        """
        Cycle de escritura:
        1. Coloca la dirección en AddressBus
        2. Coloca los datos en DataBus
        3. Activa WRITE en ControlBus
        4. Espera READY
        """
        self.address_bus.set_address(address)
        self.data_bus.write_data(data)
        self.control_bus.set_write(True)
        self.control_bus.set_enable(True)
        # En una máquina real, aquí esperar READY
        self.control_bus.set_write(False)
    
    def reset(self) -> None:
        """Reinicia todos los buses"""
        self.address_bus.clear()
        self.data_bus.clear()
        self.control_bus.reset()
    
    def display(self) -> None:
        """Muestra el estado actual de los buses"""
        print(f"  {self.address_bus}")
        print(f"  {self.data_bus}")
        print(f"  {self.control_bus}")
    
    def __repr__(self) -> str:
        return f"BusInterface({self.address_bus}, {self.data_bus}, {self.control_bus})"
