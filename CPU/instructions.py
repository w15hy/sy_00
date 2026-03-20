def nop(cpu, registros, ram):
    pass


def movi(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    inm8_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    inm8 = int(inm8_bin, 2)

    registros.set_reg(r1, inm8)

    return False


def halt(cpu, registros, ram):

    registros.show()

    cpu.running = False


def mov1(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val = registros.get_reg(r2)

    registros.set_reg(r1, val)

    return False


def mov2(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val = registros.get_reg(r2)

    registros.set_reg(r1, val)

    return False


def mov3(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val = registros.get_reg(r2)

    registros.set_reg(r1, val)

    return False


def ret(cpu, registros, ram):

    sp = registros.SP

    direccion = ram.read(sp)

    registros.SP += 1
    registros.PC = direccion

    return True


def iret(cpu, registros, ram):

    sp = registros.SP

    direccion = ram.read(sp)

    registros.SP += 1
    registros.PC = direccion

    return True


def int_(cpu, registros, ram):

    direccion = int(registros.IR_params(), 2)

    sp = registros.SP - 1
    registros.SP = sp

    ram.write(sp, registros.PC)

    registros.PC = direccion

    return True


def push(cpu, registros, ram):

    params = registros.IR_params()

    reg_bin = params[0:8]

    r = int(reg_bin, 2)

    val = registros.get_reg(r)

    sp = registros.SP - 1
    registros.SP = sp

    ram.write(sp, val)

    return False


def pop(cpu, registros, ram):

    params = registros.IR_params()

    reg_bin = params[0:8]

    r = int(reg_bin, 2)

    sp = registros.SP

    val = ram.read(sp)

    registros.SP += 1

    registros.set_reg(r, val)

    return False


def load(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    direccion = registros.get_reg(r2)

    val = ram.read(direccion)

    registros.set_reg(r1, val)

    return False


def store(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    direccion = registros.get_reg(r2)

    val = registros.get_reg(r1)

    ram.write(direccion, val)

    return False


def xchg(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    registros.set_reg(r1, val2)
    registros.set_reg(r2, val1)

    return False


def lea(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    direccion = registros.get_reg(r2)

    registros.set_reg(r1, direccion)

    return False


def add(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 + val2

    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="add")

    registros.set_reg(r1, result_raw)

    return False


def addi(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    inm8_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    inm8 = int(inm8_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = val1 + inm8

    registros.update_flags(result_raw, operand_a=val1, operand_b=inm8, operation="add")

    registros.set_reg(r1, result_raw)

    return False


def sub(cpu, registros, ram):

    # Extraer parámetros desde IR
    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    # Resta cruda
    result_raw = val1 - val2

    # Actualizar flags
    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="sub")

    registros.set_reg(r1, result_raw)

    return False


def mul(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 * val2

    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="mul")

    registros.set_reg(r1, result_raw)

    return False


def div(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    if val2 == 0:
        # División por cero, quizás set flag o algo, pero por simplicidad, no hacer nada o halt
        return False

    result_raw = val1 // val2

    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="div")

    registros.set_reg(r1, result_raw)

    return False


def inc(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = val1 + 1

    registros.update_flags(result_raw, operand_a=val1, operand_b=1, operation="add")

    registros.set_reg(r1, result_raw)

    return False


def dec(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = val1 - 1

    registros.update_flags(result_raw, operand_a=val1, operand_b=1, operation="sub")

    registros.set_reg(r1, result_raw)

    return False


def neg(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = -val1

    registros.update_flags(result_raw, operand_a=0, operand_b=val1, operation="sub")

    registros.set_reg(r1, result_raw)

    return False


def adc(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)
    carry = 1 if registros.flag_C else 0

    result_raw = val1 + val2 + carry

    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="add")

    registros.set_reg(r1, result_raw)

    return False


def sbb(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)
    borrow = 1 if registros.flag_C else 0

    result_raw = val1 - val2 - borrow

    registros.update_flags(result_raw, operand_a=val1, operand_b=val2, operation="sub")

    registros.set_reg(r1, result_raw)

    return False


def and_(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 & val2

    registros.update_flags(
        result_raw, operand_a=val1, operand_b=val2, operation="logic"
    )

    registros.set_reg(r1, result_raw)

    return False


def or_(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 | val2

    registros.update_flags(
        result_raw, operand_a=val1, operand_b=val2, operation="logic"
    )

    registros.set_reg(r1, result_raw)

    return False


def xor(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 ^ val2

    registros.update_flags(
        result_raw, operand_a=val1, operand_b=val2, operation="logic"
    )

    registros.set_reg(r1, result_raw)

    return False


def not_(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = (~val1) & 0xFF

    registros.update_flags(result_raw, operand_a=val1, operand_b=0, operation="logic")

    registros.set_reg(r1, result_raw)

    return False


def shl(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = (val1 << 1) & 0xFF

    registros.update_flags(result_raw, operand_a=val1, operand_b=0, operation="logic")

    registros.set_reg(r1, result_raw)

    return False


def rol(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = ((val1 << 1) | (val1 >> 7)) & 0xFF

    registros.update_flags(result_raw, operand_a=val1, operand_b=0, operation="logic")

    registros.set_reg(r1, result_raw)

    return False


def shr(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = val1 >> 1

    registros.update_flags(result_raw, operand_a=val1, operand_b=0, operation="logic")

    registros.set_reg(r1, result_raw)

    return False


def ror(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]

    r1 = int(reg1_bin, 2)

    val1 = registros.get_reg(r1)
    result_raw = ((val1 >> 1) | (val1 << 7)) & 0xFF

    registros.update_flags(result_raw, operand_a=val1, operand_b=0, operation="logic")

    registros.set_reg(r1, result_raw)

    return False


def cmp(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result = val1 - val2

    registros.flag_Z = result == 0
    registros.flag_N = result < 0
    registros.flag_C = val1 < val2

    return False


def test(cpu, registros, ram):

    params = registros.IR_params()

    reg1_bin = params[0:8]
    reg2_bin = params[8:16]

    r1 = int(reg1_bin, 2)
    r2 = int(reg2_bin, 2)

    val1 = registros.get_reg(r1)
    val2 = registros.get_reg(r2)

    result_raw = val1 & val2

    registros.update_flags(
        result_raw, operand_a=val1, operand_b=val2, operation="logic"
    )

    return False


def jmp(cpu, registros, ram):

    direccion = int(registros.IR_params(), 2)
    registros.PC = direccion
    return True


def jz(cpu, registros, ram):

    if registros.flag_Z:
        direccion = int(registros.IR_params(), 2)
        registros.PC = direccion
        return True

    return False


def jnz(cpu, registros, ram):

    if not registros.flag_Z:
        direccion = int(registros.IR_params(), 2)
        registros.PC = direccion
        return True

    return False


def jc(cpu, registros, ram):

    if registros.flag_C:
        direccion = int(registros.IR_params(), 2)
        registros.PC = direccion
        return True

    return False


def call(cpu, registros, ram):
    pass


def jn(cpu, registros, ram):
    if registros.flag_N:
        direccion = int(registros.IR_params(), 2)
        registros.PC = direccion
        return True

    return False


instr_dict = {
    0x00: (nop, 1),
    0x01: (halt, 1),
    # 0x02: (ret, 0),
    # 0x03: (iret, 0),
    # 0x04: (int_, 4),
    # 0x05: (mov1, 1),
    # 0x06: (mov2, 3),
    # 0x07: (mov3, 2),
    # 0x08: (push, 4),
    # 0x09: (pop, 4),
    # 0x0A: (load, 3),
    # 0x0B: (store, 3),
    # 0x0C: (xchg, 1),
    # 0x0D: (lea, 3),
    0x0E: (movi, 3),
    0x0F: (add, 3),
    0x10: (addi, 3),
    0x11: (sub, 3),
    0x12: (mul, 3),
    0x13: (div, 3),
    0x14: (inc, 2),
    0x15: (dec, 2),
    0x16: (neg, 2),
    0x17: (adc, 3),
    0x18: (sbb, 3),
    0x19: (and_, 3),
    0x1A: (or_, 3),
    0x1B: (xor, 3),
    0x1C: (not_, 2),
    0x1D: (shl, 2),
    0x1E: (rol, 2),
    0x1F: (shr, 2),
    0x20: (ror, 2),
    0x21: (cmp, 3),
    0x22: (test, 3),
    0x23: (jmp, 5),
    0x24: (jz, 5),
    0x25: (jnz, 5),
    0x26: (jc, 5),
    # 0x27: (call, 5),
    0x28: (jn, 5),
}


def decode_instruction(ir_binary: str, registros) -> str:
    """
    Decodifica una instrucción completa a formato assembly legible.
    
    Args:
        ir_binary (str): La instrucción en formato binario (ej: "00001110000000000011000")
        registros: Objeto de registros (para acceder a IR_params)
    
    Returns:
        str: La instrucción formateada (ej: "MOVI R0 48", "ADD R1 R2", "NOP")
    """
    # Extraer opcode (primeros 8 bits)
    opcode = int(ir_binary[:8], 2)
    instr_name = opcode_names.get(opcode, "UNKNOWN")
    
    # Instrucciones sin parámetros
    if opcode in [0x00, 0x01]:  # NOP, HALT
        return instr_name
    
    # Obtener los parámetros (todo después del opcode)
    if len(ir_binary) > 8:
        params = ir_binary[8:]
    else:
        return instr_name
    
    # Instrucciones con 2 registros (ADD, SUB, MUL, DIV, CMP, TEST, AND, OR, XOR, etc.)
    if opcode in [0x0F, 0x11, 0x12, 0x13, 0x19, 0x1A, 0x1B, 0x21, 0x22]:
        # params[0:8] = R1, params[8:16] = R2
        if len(params) >= 16:
            r1 = int(params[0:8], 2)
            r2 = int(params[8:16], 2)
            return f"{instr_name} R{r1} R{r2}"
    
    # Instrucciones con 1 registro + inmediato 8 bits (MOVI, ADDI)
    if opcode in [0x0E, 0x10]:
        if len(params) >= 16:
            r1 = int(params[0:8], 2)
            imm8 = int(params[8:16], 2)
            return f"{instr_name} R{r1} {imm8}"
    
    # Instrucciones de 1 registro (INC, DEC, NEG, NOT, SHL, SHR, ROL, ROR)
    if opcode in [0x14, 0x15, 0x16, 0x1C, 0x1D, 0x1E, 0x1F, 0x20]:
        if len(params) >= 8:
            r1 = int(params[0:8], 2)
            return f"{instr_name} R{r1}"
    
    # Instrucciones de salto (JMP, JZ, JNZ, JC, JN) con dirección de 32 bits
    if opcode in [0x23, 0x24, 0x25, 0x26, 0x28]:
        if len(params) >= 32:
            address = int(params[0:32], 2)
            return f"{instr_name} 0x{address:08X}"
    
    # Por defecto
    return instr_name

# Diccionario que mapea opcodes a nombres de instrucciones (assembly)
opcode_names = {
    0x00: "NOP",
    0x01: "HALT",
    0x0E: "MOVI",
    0x0F: "ADD",
    0x10: "ADDI",
    0x11: "SUB",
    0x12: "MUL",
    0x13: "DIV",
    0x14: "INC",
    0x15: "DEC",
    0x16: "NEG",
    0x17: "ADC",
    0x18: "SBB",
    0x19: "AND",
    0x1A: "OR",
    0x1B: "XOR",
    0x1C: "NOT",
    0x1D: "SHL",
    0x1E: "ROL",
    0x1F: "SHR",
    0x20: "ROR",
    0x21: "CMP",
    0x22: "TEST",
    0x23: "JMP",
    0x24: "JZ",
    0x25: "JNZ",
    0x26: "JC",
    0x28: "JN",
}


def get_instruction_name(opcode: int) -> str:
    """
    Retorna el nombre de la instrucción para un opcode dado.
    
    Args:
        opcode (int): El opcode (0-255)
    
    Returns:
        str: El nombre de la instrucción (ej: "MOVI", "ADD", etc.)
    """
    return opcode_names.get(opcode, "UNKNOWN")
