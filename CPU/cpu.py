from CPU.instructions import instr_dict
from CPU.ram import RAM
from CPU.registers import Registers
from CPU.instructions import get_instruction_name, decode_instruction
import time


class CPU:
    def __init__(self, ram):
        # La memoria RAM debera ser cargada desde la ubicacion donde se cree la instancia
        self.ram = ram
        self.reg = Registers()
        self.running = True
        self.step_count = 0

    def step(self):
        """Ejecuta una única instrucción (fetch, decode, execute, update PC)"""
        # FETCH
        opcode = int(self.ram.read(self.reg.PC), 2)

        # DECODE
        func, size = instr_dict[opcode]

        # FETCH COMPLETO
        instr = self.ram.read_block(self.reg.PC, size)
        self.reg.IR = instr

        # EXECUTE
        # En caso de que jumped sea verdadero entonces la funcion habra actualizado el PC
        jumped = func(self, self.reg, self.ram)

        # UPDATE PC
        if not jumped:
            self.reg.increment_PC(size)
        
        self.step_count += 1

    def display_state(self):
        """Muestra el estado actual del CPU (registros, flags, memoria)"""
        # Decodificar opcode de la instrucción
        opcode = int(self.reg.IR[:8], 2)
        instr_name = get_instruction_name(opcode)
        instr_full = decode_instruction(self.reg.IR, self.reg)
        
        print("\n" + "=" * 80)
        print(f"  PASO #{self.step_count}  |  PC = 0x{self.reg.PC:08X}  |  IR = {self.reg.IR}")
        print(f"  INSTRUCCION: {instr_full}  (Opcode: 0x{opcode:02X})")
        print("=" * 80)
        
        # Mostrar registros generales
        print("\n  REGISTROS GENERALES:")
        for i in range(16):
            val = self.reg.get_reg(i)
            print(f"    R{i:2d} = 0x{val:02X}  ({val:3d})  [{val:08b}]", end="")
            if (i + 1) % 2 == 0:
                print()
        
        print("\n  REGISTROS ESPECIALES:")
        print(f"    PC = 0x{self.reg.PC:08X}  ({self.reg.PC})")
        print(f"    SP = 0x{self.reg.SP:08X}  ({self.reg.SP})")
        
        # Mostrar flags
        flags = self.reg.get_flags()
        flags_str = " | ".join(f"{k}={'1' if v else '0'}" for k, v in flags.items())
        print(f"\n  FLAGS: {flags_str}")
        
        # Mostrar memoria alrededor del PC (primeras 8 líneas)
        print("\n  MEMORIA (primeras 8 líneas):")
        self.ram.display(0, 64)
        print("=" * 80 + "\n")

    def run_all(self):
        """Modo 1: Ejecuta el programa completo sin parar"""
        print("\n[*] Iniciando modo EJECUCIÓN COMPLETA...")
        print("[*] El programa se ejecutará sin interrupciones.\n")
        
        self.step_count = 0
        while self.running:
            self.step()
        
        print(f"\n[OK] Programa terminado después de {self.step_count} instrucciones.")

    def run_step_manual(self):
        """Modo 2: Paso a paso manual - ejecuta una instrucción por entrada del usuario"""
        print("\n[*] Iniciando modo DEBUG - PASO A PASO MANUAL")
        print("[*] Se ejecutará una instrucción por cada entrada.")
        print("[*] Comandos: 'Enter' para siguiente paso, 'q' para salir\n")
        
        self.step_count = 0
        while self.running:
            self.display_state()
            
            user_input = input("[DEBUG] Presiona ENTER para siguiente paso (o 'q' para salir): ").strip().lower()
            if user_input == 'q':
                print("[*] Ejecución pausada por el usuario.")
                break
            
            self.step()
        
        if self.running:
            print(f"\n[OK] Debug terminado. Se ejecutaron {self.step_count} instrucciones.")
        else:
            print(f"\n[OK] Programa completado. Total: {self.step_count} instrucciones.")

    def run_step_timed(self, delay: float = 1.0):
        """
        Modo 3: Paso a paso automatizado con delay
        
        Args:
            delay (float): Tiempo en segundos entre instrucciones (default: 1.0)
        """
        print(f"\n[*] Iniciando modo DEBUG - PASO A PASO CON DELAY")
        print(f"[*] Delay entre instrucciones: {delay} segundo(s)")
        print("[*] El programa se ejecutará automáticamente.\n")
        
        self.step_count = 0
        while self.running:
            self.display_state()
            
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                print("\n[*] Ejecución interrumpida por el usuario.")
                break
            
            self.step()
        
        if self.running:
            print(f"\n[OK] Debug terminado. Se ejecutaron {self.step_count} instrucciones.")
        else:
            print(f"\n[OK] Programa completado. Total: {self.step_count} instrucciones.")
