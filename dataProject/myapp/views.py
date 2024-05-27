import os

import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import UploadFileForm
from .utils import *
from .utils import (cantidad_eventos_por_año, cantidad_eventos_por_mes,
                    clean_csv_data, departamento_mas_movimientos_masa,
                    evento_con_mas_familias_afectadas_2019,
                    evento_max_recursos_2019, impacto_eventos_2019,
                    porcentaje_eventos_por_ano, recursos_ejecutados_2019,
                    top_5_eventos_naturales_2019,
                    top_departamentos_mayor_cantidad_eventos)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el archivo CSV del formulario
            csv_file = request.FILES['file']
            
            # Guardar el archivo en el servidor
            file_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, csv_file.name), csv_file)
            
            # Obtener el nombre del archivo y codificarlo en base64
            file_name_b64 = urlsafe_base64_encode(file_path.encode('utf-8'))
            
            # Redirigir al usuario a la vista del dashboard con el nombre del archivo como parámetro GET en la URL
            return HttpResponseRedirect(reverse('dashboard') + f'?file_name={file_name_b64}')
    else:
        form = UploadFileForm()
    return render(request, 'myapp/upload.html', {'form': form})

def dashboard(request):
    # Obtener el nombre del archivo CSV como parámetro GET en la URL
    file_name_b64 = request.GET.get('file_name', None)
    
    # Inicializar variables por defecto
    top_departamentos = []
    eventos_por_año = []
    top_5_eventos_naturales_2019_list = []
    evento_mas_fallecidos = None
    evento_mas_heridos = None
    evento_mas_hectareas = None
    departamento_mas_movimientos_mas = None
    total_recursos = 0
    porcentaje_kits_alimentos = 0
    porcentaje_materiales_construccion = 0
    evento_max_recursos = None
    max_recursos = 0
    chart_eventos_por_mes = None
    municipio_mas_familias_afectadas = None
    departamento_mas_familias_afectadas = None
    familias_afectadas = 0
    chart_porcentaje_eventos_por_ano = None
    chart_top_departamentos = None  # Variable para almacenar el gráfico de top de departamentos

    # Verificar si se proporcionó un nombre de archivo
    if file_name_b64:
        try:
            # Decodificar el nombre del archivo
            file_path = urlsafe_base64_decode(file_name_b64).decode('utf-8')
            
            # Cargar el archivo CSV correspondiente
            data_clean = pd.read_csv(file_path)
            
            # Procesar los datos limpios y generar los resultados
            top_departamentos = top_departamentos_mayor_cantidad_eventos(data_clean)
            eventos_por_año = cantidad_eventos_por_año(data_clean)
            top_5_eventos_naturales_2019_list = top_5_eventos_naturales_2019(data_clean)
            evento_mas_fallecidos, evento_mas_heridos, evento_mas_hectareas = impacto_eventos_2019(data_clean)
            departamento_mas_movimientos_mas = departamento_mas_movimientos_masa(data_clean)
            total_recursos, porcentaje_kits_alimentos, porcentaje_materiales_construccion = recursos_ejecutados_2019(data_clean)
            evento_max_recursos, max_recursos = evento_max_recursos_2019(data_clean)
            chart_eventos_por_mes = cantidad_eventos_por_mes(data_clean)
            municipio_mas_familias_afectadas, departamento_mas_familias_afectadas, familias_afectadas = evento_con_mas_familias_afectadas_2019(data_clean)
            chart_porcentaje_eventos_por_ano = generate_pie_chart_eventos_por_año(data_clean)

            # Generar el gráfico del top de departamentos
            chart_top_departamentos = generate_chart_top_departamentos(data_clean)  # Asegúrate de tener esta función definida

            # Generar el gráfico de eventos por año
            chart_eventos_por_año = generate_chart_eventos_por_año(eventos_por_año)

            
            return render(request, 'myapp/dashboard.html', {
                'top_departamentos': top_departamentos,
                'eventos_por_año': eventos_por_año,
                'top_5_eventos_naturales_2019': top_5_eventos_naturales_2019_list,
                'evento_mas_fallecidos': evento_mas_fallecidos,
                'evento_mas_heridos': evento_mas_heridos,
                'evento_mas_hectareas': evento_mas_hectareas,
                'departamento_mas_movimientos_mas': departamento_mas_movimientos_mas,
                'total_recursos': total_recursos,
                'porcentaje_kits_alimentos': porcentaje_kits_alimentos,
                'porcentaje_materiales_construccion': porcentaje_materiales_construccion,
                'evento_max_recursos': evento_max_recursos,
                'max_recursos': max_recursos,
                'chart_eventos_por_mes': generate_chart_eventos_por_mes(chart_eventos_por_mes),
                'municipio_mas_familias_afectadas': municipio_mas_familias_afectadas,
                'departamento_mas_familias_afectadas': departamento_mas_familias_afectadas,
                'familias_afectadas': familias_afectadas,
                'chart_porcentaje_eventos_por_ano': chart_porcentaje_eventos_por_ano,
                'chart_top_departamentos': chart_top_departamentos,  # Pasamos el gráfico del top de departamentos a la plantilla
                'chart_eventos_por_año': chart_eventos_por_año, 
            })
        except Exception as e:
            # Manejar el caso de error al cargar el archivo CSV
            return HttpResponse(f"Error al cargar el archivo CSV: {str(e)}")
    else:
        # Manejar el caso en que no se proporcionó un nombre de archivo
        return HttpResponse("No se proporcionó un nombre de archivo CSV.")
