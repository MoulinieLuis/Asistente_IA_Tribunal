# 🔍 Buscador IA - Asistente IA Tribunal

Una aplicación web moderna y sencilla para realizar búsquedas conectándose a APIs externas.

## 🚀 Características

- **Interfaz moderna y responsive**: Diseño elegante con gradientes y animaciones
- **Configuración flexible de API**: Permite configurar URL y API Key
- **Búsqueda en tiempo real**: Búsqueda automática después de escribir (opcional)
- **Manejo de errores**: Muestra errores de forma clara y amigable
- **Persistencia de configuración**: Guarda la configuración en el navegador
- **Compatibilidad**: Funciona en todos los navegadores modernos

## 📁 Estructura del Proyecto


## 🎯 Cómo Usar

### 1. Abrir la Página

Simplemente abre el archivo `Frontend/index.html` en tu navegador web.

### 2. Realizar Búsquedas

1. Escribe tu término o pregunta de búsqueda en el campo de texto de la página
2. Presiona Enter o haz clic en "Buscar"
3. Los resultados se mostrarán debajo del campo de búsqueda

# Funcionamiento de la API

## 🔧 Configuración de la API

### Formato Esperado de la API

La aplicación espera que tu API responda con uno de estos formatos:

#### Opción 1: Array de resultados
```json
[
  {
    "title": "Título del resultado",
    "description": "Descripción del resultado"
  },
  {
    "title": "Otro resultado",
    "description": "Otra descripción"
  }
]
```

#### Opción 2: Objeto con propiedad de resultados
```json
{
  "results": [
    {
      "title": "Título del resultado",
      "description": "Descripción del resultado"
    }
  ]
}
```

#### Opción 3: Objeto con otras propiedades comunes
```json
{
  "items": [
    {
      "title": "Título del resultado",
      "description": "Descripción del resultado"
    }
  ]
}
```

### Parámetros de Búsqueda

La aplicación envía la búsqueda como parámetro `q` en la URL:
```
GET /api/search?q=termino_busqueda
```

### Headers de Autenticación

Si configuras una API Key, se enviará como Bearer token:
```
Authorization: Bearer tu_api_key
```

## 🎨 Personalización

### Colores y Estilos

Los colores principales se pueden modificar en el CSS:

```css
/* Color principal */
--primary-color: #667eea;

/* Color secundario */
--secondary-color: #764ba2;

/* Color de fondo */
--background-color: #f8f9fa;
```

### Configuración por Defecto

Puedes cambiar la configuración por defecto editando el objeto `defaultConfig` en el JavaScript:

```javascript
const defaultConfig = {
    apiUrl: 'http://localhost:3000/api/search',
    apiKey: ''
};
```

## 🔍 Funcionalidades Avanzadas

### Búsqueda Automática

La aplicación incluye búsqueda automática después de escribir 3 caracteres (con un delay de 500ms).

### Debounce

Para evitar demasiadas peticiones, la búsqueda automática usa debounce.

### Persistencia

La configuración de la API se guarda en `localStorage` del navegador.

## 🐛 Solución de Problemas

### Error de CORS

Si obtienes errores de CORS, asegúrate de que tu API permita peticiones desde el origen de la página.

### API No Responde

1. Verifica que la URL de la API sea correcta
2. Asegúrate de que la API esté funcionando
3. Revisa la consola del navegador para más detalles

### Resultados No Se Muestran

1. Verifica que la API devuelva datos en el formato esperado
2. Revisa la consola del navegador para errores
3. Asegúrate de que la respuesta sea JSON válido

## 📝 Ejemplo de API Simple

Si quieres crear una API simple para probar, aquí tienes un ejemplo con Node.js:

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/search', (req, res) => {
    const query = req.query.q;
    
    // Simular resultados de búsqueda
    const results = [
        {
            title: `Resultado para: ${query}`,
            description: `Este es un resultado de ejemplo para la búsqueda "${query}"`
        },
        {
            title: `Otro resultado`,
            description: `Descripción del segundo resultado`
        }
    ];
    
    res.json(results);
});

app.listen(3000, () => {
    console.log('API corriendo en http://localhost:3000');
});


## Comando para correr el API en local
uvicorn main:app --reload
