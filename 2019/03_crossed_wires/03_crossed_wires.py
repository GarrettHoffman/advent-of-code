from __future__ import annotations
import typing


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x} , {self.y})'

    def __eq__(self, other_point):
        return (self.x == other_point.x) and (self.y == other_point.y)

class Line:

    def __init__(self, start: Point, direction: str, length: int):
        self.start = start
        self.direction = direction
        self.length = length

        self.direction_fn_map = {
            'U': self.move_up,
            'D': self.move_down,
            'R': self.move_right,
            'L': self.move_left
        }

        self.orientation_map = {
            'U': 'VERTICAL',
            'D': 'VERTICAL',
            'R': 'HORIZONTAL',
            'L': 'HORIZONTAL'
        }

        self.orientation_does_intersect_fn_map = {
            ('VERTICAL', 'VERTICAL'): self.vert_vert_does_intersect,
            ('VERTICAL', 'HORIZONTAL'): self.vert_horiz_does_intersect,
            ('HORIZONTAL', 'VERTICAL'): self.horiz_vert_does_intersect,
            ('HORIZONTAL', 'HORIZONTAL'): self.horiz_horiz_does_intersect
        }

        self.orientation_find_intersect_fn_map = {
            ('VERTICAL', 'VERTICAL'): self.vert_vert_find_intersect,
            ('VERTICAL', 'HORIZONTAL'): self.vert_horiz_find_intersect,
            ('HORIZONTAL', 'VERTICAL'): self.horiz_vert_find_intersect,
            ('HORIZONTAL', 'HORIZONTAL'): self.horiz_horiz_find_intersect
        }

        self.end = self.calculate_endpoint()
        self.orientation = self.orientation_map[self.direction]
        self.max_x = max(self.start.x, self.end.x)
        self.min_x = min(self.start.x, self.end.x)
        self.max_y = max(self.start.y, self.end.y)
        self.min_y = min(self.start.y, self.end.y)

    def __repr__(self):
        return f'({self.start.x} , {self.start.y}) -> ({self.end.x} , {self.end.y})'

    def calculate_endpoint(self) -> Point:
        endpoint = self.direction_fn_map[self.direction]()
        return endpoint

    def move_up(self) -> Point:
        return Point(self.start.x, self.start.y + self.length)

    def move_down(self) -> Point:
        return Point(self.start.x, self.start.y - self.length)

    def move_right(self) -> Point:
        return Point(self.start.x + self.length, self.start.y)
    
    def move_left(self) -> Point:
        return Point(self.start.x - self.length, self.start.y)

    def does_intersect(self, other_line: Line) -> bool:
        does_intersect = self.orientation_does_intersect_fn_map[(self.orientation, other_line.orientation)](other_line)
        # exclude initial lines starting at (0, 0)
        if self.start == Point(0, 0) and other_line.start == Point(0, 0):
            does_intersect = False
        return does_intersect

    def vert_vert_does_intersect(self, other_line: Line) -> bool:
        does_intersect = (self.start.x == other_line.start.x) and \
            ((self.min_y <= other_line.start.y <= self.max_y) or 
             (self.min_y <= other_line.end.y <= self.max_y))
        return does_intersect

    def vert_horiz_does_intersect(self, other_line: Line) -> bool:
        does_intersect = (self.min_y <= other_line.start.y <= self.max_y) and \
            (other_line.min_x <= self.start.x <= other_line.max_x)
        return does_intersect

    def horiz_vert_does_intersect(self, other_line: Line) -> bool:
        does_intersect = (self.min_x <= other_line.start.x <= self.max_x) and \
            (other_line.min_y <= self.start.y <= other_line.max_y)
        return does_intersect

    def horiz_horiz_does_intersect(self, other_line: Line) -> bool:
        does_intersect = (self.start.y == other_line.start.y) and \
            ((self.min_x <= other_line.start.x <= self.max_x) or 
             (self.min_x <= other_line.end.x <= self.max_x))
        return does_intersect

    def get_min_dist_intersection_point(self, other_line: Line) -> Point:
        point = self.orientation_find_intersect_fn_map[(self.orientation, other_line.orientation)](other_line)
        return point
    
    def vert_vert_find_intersect(self, other_line: Line) -> Point:
        point = None
        if (self.min_y <= other_line.start.y <= self.max_y):
            point = Point(self.min_x, self.min_y)
        else:
            point = Point(other_line.min_x, other_line.min_y)
        return point

    def vert_horiz_find_intersect(self, other_line: Line) -> Point:
        point = Point(self.start.x, other_line.start.y)
        return point

    def horiz_vert_find_intersect(self, other_line: Line) -> Point:
        point = Point(other_line.start.x, self.start.y)
        return point

    def horiz_horiz_find_intersect(self, other_line: Line) -> Point:
        point = None
        if (self.min_x <= other_line.start.x <= self.max_x):
            point = Point(other_line.min_x, other_line.min_y)
        else:
            point = Point(self.min_x, self.min_y)
        return point

    def get_steps_to_intersection(self, other_line: Line) -> int:
        intersection = self.get_min_dist_intersection_point(other_line)
        steps = abs(intersection.x - self.start.x) + abs(intersection.y - self.start.y)
        return steps

class Wire:

    def __init__(self, input_str: str):
        self.lines = self.parse_input_str(input_str)

    def parse_input_str(self, input_str: str) -> [Line]:
        lines = []
        move_list = input_str.split(',')
        next_line_start = Point(0, 0)
        for move in move_list:
            direction = move[0]
            length = int(move[1:])
            line = Line(next_line_start, direction, length)
            lines.append(line)

            next_line_start = line.end
            
        return lines

class FrontPanel:
    
    def __init__(self, input_file: str): 

        self.wires = self.parse_wires(input_file)

    def parse_wires(self, input_file: str) -> [Wire]:
        wires = []
        with open(input_file) as f:
            for line in f.readlines():
                wire = Wire(line)
                wires.append(wire)
        return wires    

    def find_closest_intersection_by_dist(self):
        min_intersection_distance = float('inf')
        wire1 = self.get_wire_at_idx(0)
        wire2 = self.get_wire_at_idx(1)
        for line1 in wire1.lines:
            for line2 in wire2.lines:
                if line1.does_intersect(line2):
                    intersection = line1.get_min_dist_intersection_point(line2)
                    distance = abs(intersection.x) + abs(intersection.y)
                    if distance < min_intersection_distance:
                        min_intersection_distance = distance
        
        return min_intersection_distance

    def find_clostest_intersection_by_steps(self):
        min_intersection_steps = float('inf')
        wire1 = self.get_wire_at_idx(0)
        wire2 = self.get_wire_at_idx(1)
        
        wire1_steps = 0
        wire2_steps = 0
        for line1 in wire1.lines:
            wire2_steps = 0
            for line2 in wire2.lines:
                if line1.does_intersect(line2):
                    intersect = line1.get_min_dist_intersection_point(line2)
                    total_steps_to_intersection = wire1_steps + wire2_steps + line1.get_steps_to_intersection(line2) + line2.get_steps_to_intersection(line1)
                    if total_steps_to_intersection < min_intersection_steps:
                        min_intersection_steps = total_steps_to_intersection
                    
                wire2_steps += line2.length
            wire1_steps += line1.length
        
        return min_intersection_steps

    def get_wire_at_idx(self, i: int) -> Wire:
        return self.wires[i]

if __name__ == '__main__':
    front_panel = FrontPanel('input.txt')
    part_1_solution = front_panel.find_closest_intersection_by_dist()
    print(f'The minimum distance intersection for part 1 is {part_1_solution}')
    part_2_solution = front_panel.find_clostest_intersection_by_steps()
    print(f'The minimum steps intersection for part 2 is {part_2_solution}')
        