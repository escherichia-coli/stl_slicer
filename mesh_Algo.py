import numpy as np
from time import clock

# *************************************************************************************
# Objet de calcul pour mesh_UI
# *************************************************************************************


class Slicer_Algo(object):
    def __init__(self):
        pass
# ****************************************************************************************************************
    '''
    Lit un fichier .stl
    Retourne les vecteurs normaux aux faces, les faces et les triangles
    (seul les triangles sont utilisé ici)
    '''

    def __read_STL(self, f_path):
        file = open(f_path, 'r')
        raw_lines = file.readlines()
        file.close()
        vertex = []
        facet = []
        for line in raw_lines:
            line = line.replace('\n', '')
            line = line.replace('\t', ' ')
            line = line.split(' ')
            for i in range(line.count('')):
                line.remove('')

            if line[0] == 'facet':
                facet.append([line[2], line[3], line[4]])
            if line[0] == 'vertex':
                vertex.append([line[1], line[2], line[3]])
        triangles = []
        file.close()
        for i in range(0, len(vertex), 3):
            triangles.append([vertex[i], vertex[i + 1], vertex[i + 2]])

        return facet, vertex, triangles


# ****************************************************************************************************************
    '''
    Lit les fichiers .txt issus des maillages
    Le formatage des fichier doit être : 
        Ligne 1 : int(nombre de triangles) int(nombre de connections)
        ligne 2 à nb_triangle : n°point coord_x coord_y coord_z
        ligne nb_triangle + 1 à nb_triangle + nb_connection : n°connection point_a point_b point c

    Retourne un tableau contenant les triangles (formaté comme __read_STL) :
    triangles
        triangle_1
            point_1
                x, y, z
            point_2
                x, y, z
            point_3
                x, y, z
        triangle_2
            point_1
                x, y, z
        ...
        ..
        .
    '''

    def __read_TXT(self, f_path):
        nb_pnts, nb_connect = np.loadtxt(f_path, dtype='int', max_rows=1)
        nb_pnts = int(nb_pnts)
        nb_connect = int(nb_connect)
        points = np.loadtxt(f_path, dtype='float', skiprows=1, max_rows=nb_pnts)[:, 1:]
        connections = np.loadtxt(f_path, dtype='int', skiprows=(nb_pnts + 1))[:, 1:] - 1
        tri = []
        for connection in connections:
            temp_tri = []
            for node in connection:
                temp_tri.append(points[node])
            tri.append(temp_tri)

        return tri

# ****************************************************************************************************************
    '''
    Appel __read_STL ou __read_TXT en fonction de l'extension
    Convertis la liste triangle en tableau numpy
    '''

    def read_file(self, f_path):
        # print(f_path)
        if f_path.split('.')[-1] == 'stl':
            facet, vertex, self.tri = self.__read_STL(f_path)
        elif f_path.split('.')[-1] == 'txt':
            self.tri = self.__read_TXT(f_path)
        self.tri = np.array(self.tri).astype(np.float)
        return self.tri

# ****************************************************************************************************************
    '''
    Calcul la distance signée d'un point à un plan
    Accepte un plan defini par un point et une normale
    Retourne une distance signée (np.float)
    '''

    def __pointPlaneDistance(self, pnt, plane):
        a = plane[1][0]
        b = plane[1][1]
        c = plane[1][2]
        d = plane[1][0] * plane[0][0] + plane[1][1] * plane[0][1] + plane[1][2] * plane[0][2]

        return (a * pnt[0] + b * pnt[1] + c * pnt[2] - d) / (a ** 2 + b ** 2 + c ** 2) ** 0.5

# ****************************************************************************************************************
    '''
    Verifie si un triangle donné a une intersection avec un plan 
    Si il existe une intersection :
        Retourne les deux points d'intersection
    Sinon ne retourne rien
    '''

    # def __compute_intersection(self, tri, plane):
    #     dist = np.zeros(3)
    #     for i in range(3):
    #         dist[i] = self.__pointPlaneDistance(tri[i], plane)

    #     dist = np.round(dist, 5)
    #     if abs(np.sum(dist)) != np.sum(abs(dist)) or np.count_nonzero(dist) != 3:
    #         if np.count_nonzero(dist) == 1:
    #             inv_ver = np.delete(tri, np.argmax(abs(dist)), axis=0)
    #             return inv_ver
    #         elif np.count_nonzero(dist) == 2:
    #             inv_ver = np.delete(tri, np.argmin(abs(dist)), axis=0)
    #             inv_dist = np.delete(dist, np.argmin(abs(dist)), axis=0)
    #             if np.sign(inv_dist[0]) == np.sign(inv_dist[1]):
    #                 return [tri[np.argmin(abs(dist))], tri[np.argmin(abs(dist))]]
    #             else:
    #                 vertex1 = np.array([inv_ver[0], inv_ver[1]])

    #                 inter1 = [vertex1[0][0] - dist[1] / (inv_dist[0] - dist[1]) * (vertex1[1][0] - vertex1[0][0]),
    #                           vertex1[0][1] - dist[1] / (inv_dist[0] - dist[1]) * (vertex1[1][1] - vertex1[0][1]),
    #                           vertex1[0][2] - dist[1] / (inv_dist[0] - dist[1]) * (vertex1[1][2] - vertex1[0][2])]
    #                 return [tri[np.argmin(abs(dist))], inter1]

    #         else:
    #             i_1 = np.argmax(abs(np.sign(dist) - np.sum(np.sign(dist))))
    #             inv_ver = np.delete(tri, i_1, axis=0)
    #             inv_dist = np.delete(dist, i_1, axis=0)
    #             vertex1 = np.array([tri[i_1], inv_ver[0]])
    #             vertex2 = np.array([tri[i_1], inv_ver[1]])
    #             inter1 = [vertex1[0][0] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][0] - vertex1[0][0]),
    #                       vertex1[0][1] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][1] - vertex1[0][1]),
    #                       vertex1[0][2] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][2] - vertex1[0][2])]

    #             inter2 = [vertex2[0][0] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][0] - vertex2[0][0]),
    #                       vertex2[0][1] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][1] - vertex2[0][1]),
    #                       vertex2[0][2] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][2] - vertex2[0][2])]

    #             return [inter1, inter2]
    def __compute_intersection(self, tri, plane):
        dist = np.zeros(3)
        for i in range(3):
            dist[i] = self.__pointPlaneDistance(tri[i], plane)

        dist = np.round(dist, 5)
        if abs(np.sum(dist)) != np.sum(abs(dist)) or np.count_nonzero(dist) != 3:
            i_1 = np.argmax(abs(np.sign(dist) - np.sum(np.sign(dist))))
            inv_ver = np.delete(tri, i_1, axis=0)
            inv_dist = np.delete(dist, i_1, axis=0)
            vertex1 = np.array([tri[i_1], inv_ver[0]])
            vertex2 = np.array([tri[i_1], inv_ver[1]])

            if np.count_nonzero(dist) == 1:
                inv_ver = np.delete(tri, np.argmax(abs(dist)), axis=0)
                return inv_ver
            else:
                inter1 = [vertex1[0][0] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][0] - vertex1[0][0]),
                          vertex1[0][1] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][1] - vertex1[0][1]),
                          vertex1[0][2] - dist[i_1] / (inv_dist[0] - dist[i_1]) * (vertex1[1][2] - vertex1[0][2])]

                inter2 = [vertex2[0][0] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][0] - vertex2[0][0]),
                          vertex2[0][1] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][1] - vertex2[0][1]),
                          vertex2[0][2] - dist[i_1] / (inv_dist[1] - dist[i_1]) * (vertex2[1][2] - vertex2[0][2])]

                return [inter1, inter2]

# ****************************************************************************************************************
    '''
    Acceptre une liste de droite : 
        inter
            droite_1
                point_a
                    x y z
                point_b
                    x y z
            droite_2
    Retourne une listede droite dans laquelle a été supprimé :
        - Les droites de longueurs nulles
        - Les droites identiques (non signé)
            Exemple :
                Dans le cas suivant la droite_2 est supprimée
                inter
                    droite_1
                        point_a
                            (0, 0, 0)
                        point_b
                            (0, 0, 1)
                    droite_2
                        point_a
                            (0, 0, 1)
                        point_b
                            (0, 0, 0)
    '''

    def __clean_intersection(self, inter):
        '''
        ******************************************
        Algo stable - complexité 2*n^2
        ******************************************

        for i in range(len(inter)):
            if np.all(inter[i][0] == inter[i][1]):
                arg_list.append(i)
                inter = np.delete(inter, arg_list, axis=0)
        arg_list = []

        for i in range(len(inter)):
            for j in range(len(inter)):
                if j not in arg_list and i != j:
                    if np.array_equal(inter[i][0], inter[j][0]) and np.array_equal(inter[i][1], inter[j][1]):
                        # arg_list.append(i)
                    if np.array_equal(inter[i][1], inter[j][0]) and np.array_equal(inter[i][0], inter[j][1]):
                        # arg_list.append(i)
        inter = np.delete(inter, arg_list, axis=0)

        ******************************************
        Nouvel algo complexité 0.5*n^2
        ******************************************
        '''
        arg_list = []
        i = 0
        while i < len(inter) - 1:
            if np.all(inter[i][0] == inter[i][1]):
                inter = np.delete(inter, i, axis=0)
            j = 0
            while j < len(inter) - 1:
                if i != j and np.array_equal(inter[i][0], inter[j][0]) and np.array_equal(inter[i][1], inter[j][1]):
                    inter = np.delete(inter, j, axis=0)
                if i != j and np.array_equal(inter[i][1], inter[j][0]) and np.array_equal(inter[i][0], inter[j][1]):
                    inter = np.delete(inter, j, axis=0)
                j = j + 1
            i = i + 1

        return inter

# ****************************************************************************************************************
    '''
    Retourne une liste de droite ordonnées --> toutes les droites se suivent
        Chaque point ne doit être present que 2 fois dans la liste
        La liste de droite doit definir une contour fermé
            Départ du point list[0] --> pas de retour en arrière donc si un segment est manquant l'algo s'arrete
    complexité : 0.5*n^2
    '''

    def __order_intersection(self, inter):
        inter_ordered = []
        nb_line = len(inter)
        if len(inter) == 0:
            print('ERROR')
        inter_ordered.append(inter[0])
        inter = np.delete(inter, 0, axis=0)
        i = 0
        while len(inter_ordered) < nb_line:
            for i in range(len(inter)):
                if np.all(inter_ordered[-1][1] == inter[i][0]):
                    inter_ordered.append(inter[i])
                    inter = np.delete(inter, i, axis=0)
                    i = -1
                    break
                elif np.all(inter_ordered[-1][1] == inter[i][1]):
                    inter_ordered.append(np.array([inter[i][1], inter[i][0]]))
                    inter = np.delete(inter, i, axis=0)
                    i = -1
                    break

                if i == (len(inter) - 1):
                    inter = np.delete(inter, i, axis=0)
                    nb_line = nb_line - 1
                    i = -1
                    break
        return np.array(inter_ordered)

# ****************************************************************************************************************
    '''
    Calcul l'aire défini par un contour maillé et ordonnés
    Accepte une liste de segment orientés
        Calcul la somme sur le contour de A_iB_i^B_iO
        Calcul la norme de ce vecteur et divise par 2
    Retourne un float
    '''

    def compute_area(self, intersection):
        # print('start computing area')
        area = np.array([0, 0, 0])
        for i in range(len(intersection)):
            area = area + np.cross(intersection[i][1] - intersection[i][0], - intersection[i][1])
        area = area / 2
        area = (area[0] ** 2 + area[1] ** 2 + area[2] ** 2) ** 0.5
        return area
# ****************************************************************************************************************
    '''
    Additionne tout les elements d'une liste de droite
    Retourne un float
    '''

    def compute_perimeter(self, intersection):
        perimeter = 0.
        for vertex in intersection:
            perimeter = perimeter + ((vertex[1][0] - vertex[0][0]) ** 2 + (vertex[1][1] - vertex[0][1]) ** 2 + (vertex[1][2] - vertex[0][2]) ** 2) ** 0.5

        return perimeter
# ****************************************************************************************************************
    '''
    Calcul toute les intersection entre les triangles et le plan donné
        complexité : n
    Nettoie les intersection : 
        complexité : 0.5*n^2
    Ordonne les intersection :
        complexité : 0.5*n^2
    '''

    def cut(self, plane):
        start = clock()
        intersection = []
        for t in self.tri:
            inter = self.__compute_intersection(t, plane)
            if inter is not None:
                intersection.append(inter)
        t1 = clock() - start
        print('\n***********************')
        print('find intersections : ', t1)
        intersection = np.array(intersection)
        intersection = np.round(intersection, 5)
        t2 = clock() - t1 - start
        print('trun to numpy : ', t2)
        intersection = self.__clean_intersection(intersection)
        t3 = clock() - t2 - t1 - start
        print('clean intersections : ', t3)
        intersection = self.__order_intersection(intersection)
        t4 = clock() - t3 - t2 - t1 - start
        print('order intersections : ', t4)
        print('total time to cut : ', clock() - start)
        return intersection


'''
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    # for vertex in c:
    #     for i in range(len(vertex)):
    #         pnt.append(vertex[i])

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    # print('cool')
    # print(c)
'''
