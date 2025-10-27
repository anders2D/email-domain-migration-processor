"""
Summary Generator - Genera summary.txt según formato PDD
"""
from datetime import datetime
from typing import Dict


class SummaryGenerator:
    @staticmethod
    def generate(stats: Dict, output_file: str = "summary.txt"):
        """Genera reporte resumen con estadísticas de ejecución"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary = f"""============================================================
           REPORTE DE PROCESAMIENTO DE CORREOS
============================================================

Fecha y hora: {timestamp}

ESTADISTICAS:
  Total procesados:     {stats['total']}
  Exitosos:             {stats['processed']} ({stats['success_rate']:.1f}%)
  Rechazados:           {stats['errors']}
  Duplicados:           {stats.get('duplicates', 0)}
  Advertencias:         {stats.get('warnings', 0)}

TIEMPO DE EJECUCION:
  Duracion:             {stats.get('duration', 'N/A')}

ARCHIVOS GENERADOS:
  CSV de salida:        {stats.get('output_file', 'N/A')}
  Log de errores:       {stats.get('error_log', 'error_log.txt')}
  Reporte resumen:      {output_file}

DOMINIO:
  Dominio destino:      {stats.get('new_domain', 'N/A')}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary.strip())
        
        return output_file
