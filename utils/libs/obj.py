class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:  # Por default open ya está en read-text
            self.lines = file.read().splitlines()  # Lee el documento línea por línea

        # Variables para almacenar la lectura del documento
        self.vertices = []
        self.textures = []  # Coordenadas de texturas
        self.textures2 = []
        self.normals = []
        self.normals2 = []
        self.faces = []

        self.saveData()

    def saveData(self):
        # Formato de OBJ
        # v -0.8523 -0.6325 -0.5238 → letra = prefijo, valores = coordenadas
        newTexture = False
        for line in self.lines:
            # Asegurar que la línea no está en blanco
            if line:
                prefix, value = line.split(' ', 1)  # Separar el prefijo del valor
                if prefix == 'v':  # Vertices
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':  # Coordenadas de textura
                    if not newTexture:
                        self.textures.append(list(map(float, value.split(' '))))
                    elif newTexture:
                        self.textures2.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':  # Normales
                    if not newTexture:
                        self.normals.append(list(map(float, value.split(' '))))
                    elif newTexture:
                        self.normals2.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int, vertex.split('/'))) for vertex in value.split(' ')])