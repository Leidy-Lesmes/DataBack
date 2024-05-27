import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd


def generate_chart_top_departamentos(data_clean):
    top_departamentos = top_departamentos_mayor_cantidad_eventos(data_clean)
    fig, ax = plt.subplots()
    ax.bar(top_departamentos.index, top_departamentos.values)
    ax.set_xlabel('Departamento')
    ax.set_ylabel('Cantidad de Eventos')
    ax.set_title('Top 5 Departamentos con Mayor Cantidad de Eventos')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    chart = f"data:image/png;base64,{chart_image}"
    return chart

def top_departamentos_mayor_cantidad_eventos(data_clean):
    top_departamentos = data_clean['DEPARTAMENTO'].value_counts().head(5)
    return top_departamentos

def generate_chart_eventos_por_año(eventos_por_año):
    fig, ax = plt.subplots()
    eventos_por_año.plot(kind='bar', ax=ax)
    ax.set_xlabel('Año')
    ax.set_ylabel('Cantidad de Eventos')
    ax.set_title('Cantidad de Eventos por Año')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    chart = f"data:image/png;base64,{chart_image}"
    return chart


def cantidad_eventos_por_año(data_clean):
    data_clean['FECHA'] = pd.to_datetime(data_clean['FECHA'])
    eventos_por_año = data_clean['FECHA'].dt.year.value_counts().sort_index()
    return eventos_por_año


def top_5_eventos_naturales_2019(data_clean):
    data_2019 = data_clean[data_clean['FECHA'].dt.year == 2019]
    top_5_eventos = data_2019[data_2019['EVENTO'].str.contains('NATURAL')]['EVENTO'].value_counts().head(5)
    return top_5_eventos

def impacto_eventos_2019(data_clean):
    data_2019 = data_clean[data_clean['FECHA'].dt.year == 2019]
    impacto_eventos = data_2019.groupby('EVENTO').agg({'FALLECIDOS': 'sum', 'HERIDOS': 'sum', 'HECTAREAS': 'sum'})
    tipo_evento_mas_fallecidos = impacto_eventos['FALLECIDOS'].idxmax()
    tipo_evento_mas_heridos = impacto_eventos['HERIDOS'].idxmax()
    tipo_evento_mas_hectareas = impacto_eventos['HECTAREAS'].idxmax()
    return tipo_evento_mas_fallecidos, tipo_evento_mas_heridos, tipo_evento_mas_hectareas

def departamento_mas_movimientos_masa(data_clean):
    data_movimientos_masa = data_clean[(data_clean['EVENTO'] == 'MOVIMIENTO EN MASA') & (data_clean['FECHA'].dt.year.isin([2019, 2020, 2021]))]
    departamento_mas_movimientos = data_movimientos_masa['DEPARTAMENTO'].value_counts().idxmax()
    return departamento_mas_movimientos

def recursos_ejecutados_2019(data_clean):
    data_2019 = data_clean[data_clean['FECHA'].dt.year == 2019]
    total_recursos = data_2019['RECURSOS EJECUTADOS'].sum()
    total_kits_alimentos = data_2019['VALOR KIT DE ALIMENTO'].sum()
    total_materiales_construccion = data_2019['VALOR MATERIALES DE CONSTRUCCION'].sum()
    porcentaje_kits_alimentos = (total_kits_alimentos / total_recursos) * 100
    porcentaje_materiales_construccion = (total_materiales_construccion / total_recursos) * 100
    return total_recursos, porcentaje_kits_alimentos, porcentaje_materiales_construccion

def evento_max_recursos_2019(data_clean):
    data_2019 = data_clean[data_clean['FECHA'].dt.year == 2019]
    recursos_por_evento = data_2019.groupby('EVENTO')['RECURSOS EJECUTADOS'].sum()
    evento_max_recursos = recursos_por_evento.idxmax()
    max_recursos = recursos_por_evento.max()
    return evento_max_recursos, max_recursos

def generate_chart_eventos_por_mes(eventos_por_mes):
    fig, ax = plt.subplots()
    eventos_por_mes.plot(kind='bar', ax=ax)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de Eventos')
    ax.set_title('Cantidad de Eventos por Mes (2019-2021)')
    
    # Mejorar las etiquetas del eje x
    ax.set_xticklabels(eventos_por_mes.index.strftime('%Y-%m'), rotation=45, ha='right')

    # Ajustar el diseño para evitar superposiciones
    fig.tight_layout()

    # Guardar la figura en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Codificar la imagen en base64
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    chart = f"data:image/png;base64,{chart_image}"

    # Cerrar la figura para liberar memoria
    plt.close(fig)

    return chart

def cantidad_eventos_por_mes(data_clean):
    data_periodo = data_clean[(data_clean['FECHA'].dt.year >= 2019) & (data_clean['FECHA'].dt.year <= 2021)]
    eventos_por_mes = data_periodo['FECHA'].dt.to_period('M').value_counts().sort_index()
    return eventos_por_mes

def evento_con_mas_familias_afectadas_2019(data_clean):
    data_2019 = data_clean[data_clean['FECHA'].dt.year == 2019]
    evento_max_familias = data_2019.loc[data_2019['FAMILIAS'].idxmax()]
    municipio = evento_max_familias['MUNICIPIO']
    departamento = evento_max_familias['DEPARTAMENTO']
    familias_afectadas = evento_max_familias['FAMILIAS']
    return municipio, departamento, familias_afectadas

def generate_pie_chart_eventos_por_año(data_clean):
    eventos_por_año = porcentaje_eventos_por_ano(data_clean)
    fig, ax = plt.subplots()
    ax.pie(eventos_por_año, labels=eventos_por_año.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Porcentaje de Eventos por Año')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    chart = f"data:image/png;base64,{chart_image}"
    plt.close(fig)  # Cerrar la figura para liberar memoria
    return chart


def porcentaje_eventos_por_ano(data_clean):
    data_clean['ANO'] = data_clean['FECHA'].dt.year
    eventos_por_ano = data_clean['ANO'].value_counts().sort_index()
    porcentaje_eventos_por_ano = (eventos_por_ano / eventos_por_ano.sum()) * 100
    return porcentaje_eventos_por_ano

def clean_csv_data(csv_file):
    data = pd.read_csv(csv_file)
    return data
