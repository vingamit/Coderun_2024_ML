import math
import random
 
SMALL = 1e-10
 
class CircleIntersection:
    @staticmethod
    def intersection_area(circles, stats=None):
        # Получаем все точки пересечения кругов
        intersection_points = CircleIntersection.get_intersection_points(circles)
        
        # Фильтруем точки, которые не включены во все круги
        inner_points = [p for p in intersection_points if CircleIntersection.contained_in_circles(p, circles)]
 
        arc_area = 0
        polygon_area = 0
        arcs = []
 
        # Если у нас есть точки пересечения, которые находятся внутри всех кругов,
        # то вычисляем площадь, содержащуюся в них
        if len(inner_points) > 1:
            # Сортируем точки по углу от центра многоугольника, что позволяет
            # нам просто итерироваться по точкам, чтобы получить рёбра
            center = CircleIntersection.get_center(inner_points)
            for p in inner_points:
                p['angle'] = math.atan2(p['x'] - center['x'], p['y'] - center['y'])
            inner_points.sort(key=lambda a: a['angle'], reverse=True)
 
            # Итерируемся по всем точкам, получаем дугу между точками
            # и обновляем площади
            p2 = inner_points[-1]
            for p1 in inner_points:
                # Площадь многоугольника обновляется легко ...
                polygon_area += (p2['x'] + p1['x']) * (p1['y'] - p2['y'])
    
                # Обновление площади дуги немного сложнее
                mid_point = {'x': (p1['x'] + p2['x']) / 2,
                             'y': (p1['y'] + p2['y']) / 2}
                arc = None
 
                for j in p1['parent_index']:
                    if j in p2['parent_index']:
                        # Вычисляем угол между двумя точками
                        # на текущем круге
                        circle = circles[j]
                        a1 = math.atan2(p1['x'] - circle['x'], p1['y'] - circle['y'])
                        a2 = math.atan2(p2['x'] - circle['x'], p2['y'] - circle['y'])
 
                        angle_diff = (a2 - a1)
                        if angle_diff < 0:
                            angle_diff += 2 * math.pi
                        
                        # И используем этот угол для вычисления ширины
                        # дуги
                        a = a2 - angle_diff / 2
                        width = CircleIntersection.distance(mid_point, {
                            'x': circle['x'] + circle['radius'] * math.sin(a),
                            'y': circle['y'] + circle['radius'] * math.cos(a)
                        })
                        
                        # Выбираем круг, чья дуга имеет наименьшую ширину
                        if arc is None or arc['width'] > width:
                            arc = {'circle': circle,    
                                   'width': width,
                                   'p1': p1,
                                   'p2': p2}
                
                arcs.append(arc)
                arc_area += CircleIntersection.circle_area(arc['circle']['radius'], arc['width'])
                p2 = p1
        else:
            # Нет точек пересечения, либо круги не пересекаются, либо полностью
            # перекрываются. Определяем, что именно, рассматривая наименьший круг
            smallest = min(circles, key=lambda c: c['radius'])
           
            # Убеждаемся, что наименьший круг полностью содержится во всех
            # остальных кругах
            disjoint = any(CircleIntersection.distance(circle, smallest) > abs(smallest['radius'] - circle['radius']) for circle in circles)
 
            if disjoint:
                arc_area = polygon_area = 0
            else:
                arc_area = smallest['radius'] ** 2 * math.pi
                arcs.append({
                    'circle': smallest,
                    'p1': {'x': smallest['x'], 'y': smallest['y'] + smallest['radius']},
                    'p2': {'x': smallest['x'] - SMALL, 'y': smallest['y'] + smallest['radius']},
                    'width': smallest['radius'] * 2
                })
 
        polygon_area /= 2
        if stats is not None:
            stats['area'] = arc_area + polygon_area
            stats['arc_area'] = arc_area
            stats['polygon_area'] = polygon_area
            stats['arcs'] = arcs
            stats['inner_points'] = inner_points
            stats['intersection_points'] = intersection_points
 
        return arc_area + polygon_area
 
    @staticmethod
    def monte_carlo_estimate(circles, count=10000):
        contained = 0
        bound = CircleIntersection.get_bounding_rectangle(circles)
        for _ in range(count):
            p = CircleIntersection.random_point(bound)
            if CircleIntersection.contained_in_circles(p, circles):
                contained += 1
        return bound['width'] * bound['height'] * contained / count
 
    @staticmethod
    def subdivide_rectangle(current, output):
        w = current['width'] / 2
        h = current['height'] / 2
        level = current.get('level', 0)
 
        output({
            'x': current['x'],
            'y': current['y'],
            'width': w,
            'height': h,
            'level': level + 1
        })
 
        output({
            'x': current['x'] + w,
            'y': current['y'],
            'width': w,
            'height': h,
            'level': level + 1
        })
 
        output({
            'x': current['x'],
            'y': current['y'] + h,
            'width': w,
            'height': h,
            'level': level + 1
        })
 
        output({
            'x': current['x'] + w,
            'y': current['y'] + h,
            'width': w,
            'height': h,
            'level': level + 1
        })
 
    @staticmethod
    def rectangle_contained(current, circles):
        x, y, w, h = current['x'], current['y'], current['width'], current['height']
 
        point_values = [
            CircleIntersection.contained_in_circles({'x': x, 'y': y}, circles),
            CircleIntersection.contained_in_circles({'x': x + w, 'y': y}, circles),
            CircleIntersection.contained_in_circles({'x': x, 'y': y + h}, circles),
            CircleIntersection.contained_in_circles({'x': x + w, 'y': y + h}, circles)
        ]
 
        if all(v == point_values[0] for v in point_values):
            return 1 if point_values[0] else -1
        return 0
 
    @staticmethod
    def quadtree_estimate(circles, depth=8):
        bound = CircleIntersection.get_bounding_rectangle(circles)
        area = 0
        outside_area = 0
 
        if bound['width'] <= 0 or bound['height'] <= 0:
            return [0, 0]
 
        def examine_rectangle(r):
            nonlocal area, outside_area
            in_or_out = CircleIntersection.rectangle_contained(r, circles)
            if in_or_out == 0:
                if r['level'] <= depth:
                    CircleIntersection.subdivide_rectangle(r, examine_rectangle)
            elif in_or_out > 0:
                area += r['width'] * r['height']
            else:
                outside_area += r['width'] * r['height']
 
        bound['level'] = 0
        CircleIntersection.subdivide_rectangle(bound, examine_rectangle)
 
        uncertain = (bound['width'] * bound['height'] - area - outside_area) / 2
        return [area + uncertain, uncertain]
 
    @staticmethod
    def contained_in_circles(point, circles):
        return all(CircleIntersection.distance(point, circle) <= circle['radius'] + SMALL for circle in circles)
 
    @staticmethod
    def get_intersection_points(circles):
        ret = []
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                intersect = CircleIntersection.circle_circle_intersection(circles[i], circles[j])
                for p in intersect:
                    p['parent_index'] = [i, j]
                    ret.append(p)
        return ret
 
    @staticmethod
    def circle_integral(r, x):
        y = math.sqrt(r * r - x * x)
        return x * y + r * r * math.atan2(x, y)
 
    @staticmethod
    def circle_area(r, width):
        return CircleIntersection.circle_integral(r, width - r) - CircleIntersection.circle_integral(r, -r)
 
    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2)
 
    @staticmethod
    def circle_overlap(r1, r2, d):
        if d >= r1 + r2:
            return 0
        if d <= abs(r1 - r2):
            return math.pi * min(r1, r2) ** 2
 
        w1 = r1 - (d * d - r2 * r2 + r1 * r1) / (2 * d)
        w2 = r2 - (d * d - r1 * r1 + r2 * r2) / (2 * d)
        return CircleIntersection.circle_area(r1, w1) + CircleIntersection.circle_area(r2, w2)
 
    @staticmethod
    def circle_circle_intersection(p1, p2):
        d = CircleIntersection.distance(p1, p2)
        r1, r2 = p1['radius'], p2['radius']
 
        if d >= (r1 + r2) or d <= abs(r1 - r2):
            return []
 
        a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
        h = math.sqrt(r1 * r1 - a * a)
        x0 = p1['x'] + a * (p2['x'] - p1['x']) / d
        y0 = p1['y'] + a * (p2['y'] - p1['y']) / d
        rx = -(p2['y'] - p1['y']) * (h / d)
        ry = -(p2['x'] - p1['x']) * (h / d)
 
        return [{'x': x0 + rx, 'y': y0 - ry},
                {'x': x0 - rx, 'y': y0 + ry}]
 
    @staticmethod
    def get_center(points):
        x_sum = sum(p['x'] for p in points)
        y_sum = sum(p['y'] for p in points)
        n = len(points)
        return {'x': x_sum / n, 'y': y_sum / n}
 
    @staticmethod
    def random_point(rect):
        return {
            'x': rect['x'] + random.random() * rect['width'],
            'y': rect['y'] + random.random() * rect['height']
        }
 
    @staticmethod
    def get_bounding_rectangle(circles):
        def contained(p):
            return CircleIntersection.contained_in_circles(p, circles)
        
        intersection_points = CircleIntersection.get_intersection_points(circles)
        inner = [p for p in intersection_points if contained(p)]
 
        x1 = min(p['x'] for p in inner)
        y1 = min(p['y'] for p in inner)
        x2 = max(p['x'] for p in inner)
        y2 = max(p['y'] for p in inner)
        
        for p in circles:
            if p['x'] - p['radius'] < x1 and contained({'x': p['x'] - p['radius'], 'y': p['y']}):
                x1 = p['x'] - p['radius']
            if p['x'] + p['radius'] > x2 and contained({'x': p['x'] + p['radius'], 'y': p['y']}):
                x2 = p['x'] + p['radius']
            if p['y'] - p['radius'] < y1 and contained({'y': p['y'] - p['radius'], 'x': p['x']}):
                y1 = p['y'] - p['radius']
            if p['y'] + p['radius'] > y2 and contained({'y': p['y'] + p['radius'], 'x': p['x']}):
                y2 = p['y'] + p['radius']
 
        return {'x': x1, 'y': y1, 'height': y2 - y1, 'width': x2 - x1}