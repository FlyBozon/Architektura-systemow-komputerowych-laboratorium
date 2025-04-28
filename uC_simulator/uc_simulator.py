import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                             QTextEdit, QLineEdit, QFileDialog, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCursor

class Register:
    def __init__(self, name):
        self.name = name
        self.value = 0
    
    def set_value(self, value):
        self.value = value & 0xFFFF
    
    def get_value(self):
        return self.value
    
    def get_high(self):
        return (self.value >> 8) & 0xFF
    
    def set_high(self, value):
        self.value = (self.value & 0x00FF) | ((value & 0xFF) << 8)
    
    def get_low(self):
        return self.value & 0xFF
    
    def set_low(self, value):
        self.value = (self.value & 0xFF00) | (value & 0xFF)


class Instruction:
    def __init__(self, opcode, destination, source, value=None):
        self.opcode = opcode
        self.destination = destination
        self.source = source
        self.value = value
    
    def __str__(self):
        if self.value is not None:
            return f"{self.opcode} {self.destination}, {self.value}"
        else:
            return f"{self.opcode} {self.destination}, {self.source}"


class ProcessorSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symulator Mikroprocesora 16-bitowego")
        self.setGeometry(100, 100, 900, 600)
        
        self.registers = {
            'AX': Register('AX'),
            'BX': Register('BX'),
            'CX': Register('CX'),
            'DX': Register('DX'),
            'AH': Register('AH'),
            'AL': Register('AL'),
            'BH': Register('BH'),
            'BL': Register('BL'),
            'CH': Register('CH'),
            'CL': Register('CL'),
            'DH': Register('DH'),
            'DL': Register('DL')
        }
        
        self.program = []
        self.current_line = 0
        self.running = False
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        register_group = QWidget()
        register_layout = QGridLayout()
        
        register_layout.addWidget(QLabel("Rejestr", font=QFont('Arial', 10, QFont.Bold)), 0, 0)
        register_layout.addWidget(QLabel("Wartość (DEC)", font=QFont('Arial', 10, QFont.Bold)), 0, 1)
        register_layout.addWidget(QLabel("Wartość (HEX)", font=QFont('Arial', 10, QFont.Bold)), 0, 2)
        
        for i, reg in enumerate(['AX', 'BX', 'CX', 'DX']):
            register_layout.addWidget(QLabel(reg), i+1, 0)
            
            value_label = QLabel("0")
            value_label.setAlignment(Qt.AlignRight)
            setattr(self, f"{reg.lower()}_dec", value_label)
            register_layout.addWidget(value_label, i+1, 1)
            
            hex_label = QLabel("0x0000")
            hex_label.setAlignment(Qt.AlignRight)
            setattr(self, f"{reg.lower()}_hex", hex_label)
            register_layout.addWidget(hex_label, i+1, 2)
        
        row = 5
        for reg in ['AH', 'AL', 'BH', 'BL', 'CH', 'CL', 'DH', 'DL']:
            register_layout.addWidget(QLabel(reg), row, 0)
            
            value_label = QLabel("0")
            value_label.setAlignment(Qt.AlignRight)
            setattr(self, f"{reg.lower()}_dec", value_label)
            register_layout.addWidget(value_label, row, 1)
            
            hex_label = QLabel("0x00")
            hex_label.setAlignment(Qt.AlignRight)
            setattr(self, f"{reg.lower()}_hex", hex_label)
            register_layout.addWidget(hex_label, row, 2)
            
            row += 1
        
        register_group.setLayout(register_layout)
        left_layout.addWidget(register_group)
        
        control_layout = QHBoxLayout()
        
        self.run_button = QPushButton("Uruchom")
        self.run_button.clicked.connect(self.run_program)
        control_layout.addWidget(self.run_button)
        
        self.step_button = QPushButton("Krok")
        self.step_button.clicked.connect(self.step_program)
        control_layout.addWidget(self.step_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_program)
        control_layout.addWidget(self.reset_button)
        
        left_layout.addLayout(control_layout)
        
        file_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Wczytaj")
        self.load_button.clicked.connect(self.load_program)
        file_layout.addWidget(self.load_button)
        
        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.save_program)
        file_layout.addWidget(self.save_button)
        
        left_layout.addLayout(file_layout)
        
        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, 1)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        editor_layout = QVBoxLayout()
        editor_layout.addWidget(QLabel("Edytor kodu"))
        
        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont('Courier New', 10))
        editor_layout.addWidget(self.code_editor)
        
        right_layout.addLayout(editor_layout, 2)
        
        execution_layout = QVBoxLayout()
        execution_layout.addWidget(QLabel("Wykonanie programu"))
        
        self.execution_display = QTableWidget()
        self.execution_display.setColumnCount(3)
        self.execution_display.setHorizontalHeaderLabels(["Linia", "Instrukcja", "Status"])
        self.execution_display.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        execution_layout.addWidget(self.execution_display)
        
        right_layout.addLayout(execution_layout, 1)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(main_layout)
        
        self.update_register_display()
    
    def parse_program(self):
        self.program = []
        lines = self.code_editor.toPlainText().strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            parts = line.split()
            if len(parts) < 3:
                QMessageBox.warning(self, "Błąd składni", f"Błędna instrukcja: {line}")
                return False
            
            opcode = parts[0].upper()
            if opcode not in ['MOV', 'ADD', 'SUB']:
                QMessageBox.warning(self, "Błąd składni", f"Nieznany opcode: {opcode}")
                return False
            
            destination = parts[1].rstrip(',').upper()
            if destination not in self.registers:
                QMessageBox.warning(self, "Błąd składni", f"Nieprawidłowy rejestr docelowy: {destination}")
                return False
            
            source = parts[2].upper()
            if source in self.registers:
                self.program.append(Instruction(opcode, destination, source))
            else:
                try:
                    if source.startswith('0X'):
                        value = int(source, 16)
                    else:
                        value = int(source)
                    self.program.append(Instruction(opcode, destination, None, value))
                except ValueError:
                    QMessageBox.warning(self, "Błąd składni", f"Nieprawidłowa wartość: {source}")
                    return False
        
        self.update_execution_display()
        return True
    
    def update_execution_display(self):
        self.execution_display.setRowCount(len(self.program))
        
        for i, instruction in enumerate(self.program):
            line_item = QTableWidgetItem(str(i+1))
            self.execution_display.setItem(i, 0, line_item)
            
            instr_item = QTableWidgetItem(str(instruction))
            self.execution_display.setItem(i, 1, instr_item)
            
            status_item = QTableWidgetItem("")
            self.execution_display.setItem(i, 2, status_item)
    
    def execute_instruction(self, instruction):
        if instruction.opcode == 'MOV':
            if instruction.value is not None:
                if instruction.destination.endswith('H'):
                    main_reg = instruction.destination[0] + 'X'
                    self.registers[main_reg].set_high(instruction.value)
                elif instruction.destination.endswith('L'):
                    main_reg = instruction.destination[0] + 'X'
                    self.registers[main_reg].set_low(instruction.value)
                else:
                    self.registers[instruction.destination].set_value(instruction.value)
            else:
                source_value = self.get_register_value(instruction.source)
                self.set_register_value(instruction.destination, source_value)
        
        elif instruction.opcode == 'ADD':
            dest_value = self.get_register_value(instruction.destination)
            if instruction.value is not None:
                result = dest_value + instruction.value
            else:
                source_value = self.get_register_value(instruction.source)
                result = dest_value + source_value
            
            self.set_register_value(instruction.destination, result)
        
        elif instruction.opcode == 'SUB':
            dest_value = self.get_register_value(instruction.destination)
            if instruction.value is not None:
                result = dest_value - instruction.value
            else:
                source_value = self.get_register_value(instruction.source)
                result = dest_value - source_value
            
            self.set_register_value(instruction.destination, result)
    
    def get_register_value(self, register):
        if register.endswith('H'):
            main_reg = register[0] + 'X'
            return self.registers[main_reg].get_high()
        elif register.endswith('L'):
            main_reg = register[0] + 'X'
            return self.registers[main_reg].get_low()
        else:
            return self.registers[register].get_value()
    
    def set_register_value(self, register, value):
        if register.endswith('H'):
            main_reg = register[0] + 'X'
            self.registers[main_reg].set_high(value)
        elif register.endswith('L'):
            main_reg = register[0] + 'X'
            self.registers[main_reg].set_low(value)
        else:
            self.registers[register].set_value(value)
    
    def update_register_display(self):
        for reg in ['AX', 'BX', 'CX', 'DX']:
            value = self.registers[reg].get_value()
            getattr(self, f"{reg.lower()}_dec").setText(str(value))
            getattr(self, f"{reg.lower()}_hex").setText(f"0x{value:04X}")
        
        for reg in ['AH', 'AL', 'BH', 'BL', 'CH', 'CL', 'DH', 'DL']:
            if reg.endswith('H'):
                main_reg = reg[0] + 'X'
                value = self.registers[main_reg].get_high()
            else:
                main_reg = reg[0] + 'X'
                value = self.registers[main_reg].get_low()
            
            getattr(self, f"{reg.lower()}_dec").setText(str(value))
            getattr(self, f"{reg.lower()}_hex").setText(f"0x{value:02X}")
    
    def highlight_current_line(self):
        if 0 <= self.current_line < len(self.program):
            for i in range(self.execution_display.rowCount()):
                for j in range(self.execution_display.columnCount()):
                    item = self.execution_display.item(i, j)
                    if item:
                        item.setBackground(QColor(255, 255, 255))
            
            for j in range(self.execution_display.columnCount()):
                item = self.execution_display.item(self.current_line, j)
                if item:
                    item.setBackground(QColor(200, 255, 200))
            
            status_item = self.execution_display.item(self.current_line, 2)
            if status_item:
                status_item.setText("Wykonano")
    
    def run_program(self):
        if not self.running:
            if not self.parse_program():
                return
            
            self.running = True
            self.current_line = 0
            self.run_button.setText("Stop")
            
            while self.current_line < len(self.program):
                self.execute_instruction(self.program[self.current_line])
                
                status_item = self.execution_display.item(self.current_line, 2)
                if status_item:
                    status_item.setText("Wykonano")
                
                self.current_line += 1
            
            self.update_register_display()
            self.running = False
            self.run_button.setText("Uruchom")
        else:
            self.running = False
            self.run_button.setText("Uruchom")
    
    def step_program(self):
        if self.running:
            return
        
        if self.current_line == 0:
            if not self.parse_program():
                return
        
        if self.current_line < len(self.program):
            self.execute_instruction(self.program[self.current_line])
            self.highlight_current_line()
            self.update_register_display()
            self.current_line += 1
        else:
            QMessageBox.information(self, "Koniec programu", "Program został wykonany do końca.")
    
    def reset_program(self):
        self.running = False
        self.run_button.setText("Uruchom")
        self.current_line = 0
        
        for reg in self.registers.values():
            reg.set_value(0)
        
        self.update_register_display()
        
        for i in range(self.execution_display.rowCount()):
            status_item = self.execution_display.item(i, 2)
            if status_item:
                status_item.setText("")
    
    def load_program(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wczytaj program", "", "Pliki programów (*.asm);;Wszystkie pliki (*)")
        
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.code_editor.setPlainText(file.read())
                self.reset_program()
            except Exception as e:
                QMessageBox.critical(self, "Błąd wczytywania", f"Nie można wczytać pliku: {str(e)}")
    
    def save_program(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Zapisz program", "", "Pliki programów (*.asm);;Wszystkie pliki (*)")
        
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.code_editor.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Błąd zapisywania", f"Nie można zapisać pliku: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessorSimulator()
    window.show()
    sys.exit(app.exec_())