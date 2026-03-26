#!/usr/bin/env python3
"""
example_buses.py - Ejemplo de uso de la Arquitectura con Buses Explícitos
===========================================================================

Este script demuestra cómo los buses están ahora explícitos en la máquina
y cómo puedes acceder a ellos directamente.
"""

from CPU.cpu import CPU
from CPU.ram import RAM

def example_1_bus_state():
    """Ejemplo 1: Ver el estado de los buses"""
    print("\n" + "="*70)
    print("EJEMPLO 1: Estado de los Buses")
    print("="*70)
    
    ram = RAM(256)
    cpu = CPU(ram)
    
    print("\nEstado inicial de los buses:")
    print(f"  AddressBus: {cpu.buses.address_bus}")
    print(f"  DataBus:    {cpu.buses.data_bus}")
    print(f"  ControlBus: {cpu.buses.control_bus}")


def example_2_read_write():
    """Ejemplo 2: Leer y escribir memoria usando buses explícitos"""
    print("\n" + "="*70)
    print("EJEMPLO 2: Leer/Escribir memoria vía buses")
    print("="*70)
    
    ram = RAM(256)
    cpu = CPU(ram)
    
    # Escribir en memoria (dirección 0x10) usando buses explícitos
    print("\n1️⃣ Escribiendo en dirección 0x10...")
    cpu.write_memory_via_bus(0x10, "11010011")
    print(f"  Address Bus: 0x{cpu.buses.address_bus.get_address():08X}")
    print(f"  Data Bus:    0x{cpu.buses.data_bus.read_data():016X}")
    print(f"  Control:     WRITE={'1' if cpu.buses.control_bus.WRITE else '0'}")
    
    # Leer de memoria (dirección 0x10) usando buses explícitos
    print("\n2️⃣ Leyendo desde dirección 0x10...")
    data = cpu.read_memory_via_bus(0x10, 1)
    print(f"  Address Bus: 0x{cpu.buses.address_bus.get_address():08X}")
    print(f"  Data Bus:    {data}")
    print(f"  Control:     READ={'1' if cpu.buses.control_bus.READ else '0'}")


def example_3_control_signals():
    """Ejemplo 3: Ver las señales de control durante operaciones"""
    print("\n" + "="*70)
    print("EJEMPLO 3: Señales de Control")
    print("="*70)
    
    ram = RAM(256)
    cpu = CPU(ram)
    
    print("\nSeñales de control iniciales:")
    signals = cpu.buses.control_bus.get_signals()
    for sig, val in signals.items():
        print(f"  {sig:12} = {'1' if val else '0'}")
    
    # Activar READ manualmente para ver cómo cambia
    cpu.buses.control_bus.set_read(True)
    print("\nDespués de activar READ:")
    signals = cpu.buses.control_bus.get_signals()
    for sig, val in signals.items():
        print(f"  {sig:12} = {'1' if val else '0'}")


def example_4_address_space():
    """Ejemplo 4: Recorrer el espacio de direcciones"""
    print("\n" + "="*70)
    print("EJEMPLO 4: Recorriendo el espacio de direcciones")
    print("="*70)
    
    ram = RAM(32)  # RAM pequeña para el ejemplo
    cpu = CPU(ram)
    
    # Escribir datos en varias direcciones
    print("\nEscribiendo datos en direcciones consecutivas:")
    for addr in range(0, 8):
        data_byte = f"{addr:08b}"  # Cada byte contiene su dirección
        cpu.write_memory_via_bus(addr, data_byte)
        print(f"  Dirección 0x{addr:02X}: datos = {data_byte}")
    
    # Leer de nuevo para verificar
    print("\nVerificando lectura:")
    for addr in range(0, 8):
        data = cpu.read_memory_via_bus(addr, 1)
        print(f"  Dirección 0x{addr:02X}: datos = {data}")


def example_5_bus_timing():
    """Ejemplo 5: Ver cómo evolucionan los buses durante ciclos"""
    print("\n" + "="*70)
    print("EJEMPLO 5: Evolución de los buses durante ciclos")
    print("="*70)
    
    ram = RAM(256)
    cpu = CPU(ram)
    
    # Simular varios ciclos de acceso
    test_data = ["10101010", "11110000", "01010101"]
    
    for i, data in enumerate(test_data):
        addr = 0x20 + i
        print(f"\nCiclo {i+1}: Escribir en 0x{addr:02X}")
        
        print(f"  Antes: AddressBus=0x{cpu.buses.address_bus.get_address():08X}, "
              f"DataBus=0x{cpu.buses.data_bus.read_data():016X}")
        
        cpu.write_memory_via_bus(addr, data)
        
        print(f"  Después: AddressBus=0x{cpu.buses.address_bus.get_address():08X}, "
              f"DataBus=0x{cpu.buses.data_bus.read_data():016X}")
        print(f"  Control: READ={cpu.buses.control_bus.READ}, "
              f"WRITE={cpu.buses.control_bus.WRITE}, "
              f"ENABLE={cpu.buses.control_bus.ENABLE}")


if __name__ == "__main__":
    print("\n" + "◀"*70)
    print("DEMOSTRACIONES DE BUSES EXPLÍCITOS")
    print("▶"*70)
    
    example_1_bus_state()
    example_2_read_write()
    example_3_control_signals()
    example_4_address_space()
    example_5_bus_timing()
    
    print("\n" + "="*70)
    print("✅ Todos los ejemplos completados")
    print("="*70 + "\n")
