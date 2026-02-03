#!/usr/bin/env python3
"""
Ejemplo de código Python para demostración en el TFG/TFM.
Este archivo puede incluirse con \codigoarchivo{python}{recursos/ejemplos/ejemplo.py}
"""

from dataclasses import dataclass
from typing import List, Optional
import json


@dataclass
class Estudiante:
    """Representa un estudiante de la EPS."""
    nombre: str
    dni: str
    titulacion: str
    nota_media: float = 0.0
    
    def es_matricula_honor(self) -> bool:
        """Verifica si el estudiante tiene matrícula de honor."""
        return self.nota_media >= 9.0
    
    def to_dict(self) -> dict:
        """Convierte el estudiante a diccionario."""
        return {
            "nombre": self.nombre,
            "dni": self.dni,
            "titulacion": self.titulacion,
            "nota_media": self.nota_media
        }


class GestorEstudiantes:
    """Gestiona una colección de estudiantes."""
    
    def __init__(self):
        self._estudiantes: List[Estudiante] = []
    
    def agregar(self, estudiante: Estudiante) -> None:
        """Agrega un estudiante al sistema."""
        if self.buscar_por_dni(estudiante.dni) is None:
            self._estudiantes.append(estudiante)
        else:
            raise ValueError(f"Ya existe un estudiante con DNI {estudiante.dni}")
    
    def buscar_por_dni(self, dni: str) -> Optional[Estudiante]:
        """Busca un estudiante por su DNI."""
        for est in self._estudiantes:
            if est.dni == dni:
                return est
        return None
    
    def listar_por_titulacion(self, titulacion: str) -> List[Estudiante]:
        """Lista estudiantes de una titulación específica."""
        return [e for e in self._estudiantes if e.titulacion == titulacion]
    
    def exportar_json(self, archivo: str) -> None:
        """Exporta todos los estudiantes a un archivo JSON."""
        datos = [e.to_dict() for e in self._estudiantes]
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)


def main():
    """Función principal de demostración."""
    gestor = GestorEstudiantes()
    
    # Crear estudiantes de ejemplo
    estudiantes = [
        Estudiante("Ana García", "12345678A", "Informática", 8.5),
        Estudiante("Pedro López", "87654321B", "Informática", 9.2),
        Estudiante("María Sánchez", "11111111C", "Telecomunicaciones", 7.8),
    ]
    
    for est in estudiantes:
        gestor.agregar(est)
    
    # Mostrar estudiantes con matrícula de honor
    print("Estudiantes con matrícula de honor:")
    for est in gestor._estudiantes:
        if est.es_matricula_honor():
            print(f"  - {est.nombre} ({est.nota_media})")
    
    # Exportar a JSON
    gestor.exportar_json("estudiantes.json")
    print("\nDatos exportados a estudiantes.json")


if __name__ == "__main__":
    main()
