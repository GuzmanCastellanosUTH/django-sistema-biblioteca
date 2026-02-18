from rest_framework import serializers
from .models import Libro, Autor, Categoria, Editorial, Prestamo

class AutorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Autor"""
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'apellido', 'nombre_completo', 
                'nacionalidad', 'biografia', 'fecha_nacimiento']

class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class EditorialSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Editorial"""
    class Meta:
        model = Editorial
        fields = ['id', 'nombre', 'pais', 'sitio_web', 'fecha_fundacion']

class LibroSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Libro"""
    
    autor_nombre = serializers.CharField(source='autor.nombre_completo', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    editorial_nombre = serializers.CharField(source='editorial.nombre', read_only=True)
    
    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'isbn', 'descripcion', 'fecha_publicacion',
            'numero_paginas', 'idioma', 'stock_total', 'stock_disponible',
            'estado', 'autor', 'autor_nombre', 'categoria', 'categoria_nombre',
            'editorial', 'editorial_nombre',
            'fecha_registro', 'ultima_actualizacion'
        ]
        read_only_fields = ['fecha_registro', 'ultima_actualizacion']


class PrestamoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Prestamo"""
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Prestamo
        fields = [
            'id', 'libro', 'libro_titulo', 'usuario', 'usuario_nombre',
            'fecha_prestamo', 'fecha_devolucion_esperada', 'fecha_devolucion_real',
            'estado', 'renovaciones', 'multa', 'notas'
        ]
        read_only_fields = ['fecha_prestamo']
    
    def validate(self, data):
        """Validar que hay stock disponible"""
        libro = data.get('libro')
        if libro and libro.stock_disponible <= 0:
            raise serializers.ValidationError(
                "No hay ejemplares disponibles de este libro."
            )
        return data
    
    def create(self, validated_data):
        """Crear préstamo y actualizar stock"""
        prestamo = super().create(validated_data)
        libro = prestamo.libro
        libro.stock_disponible -= 1
        libro.save()
        return prestamo