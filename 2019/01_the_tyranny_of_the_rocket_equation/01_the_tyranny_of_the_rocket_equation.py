import math
import typing

class Module:

    def __init__(self, mass: int):
        self.mass = mass

class FuelCounterUpper:

    def __init__(self, input_file: str, fuel_func: typing.Callable[[int], int]):
        self.modules = self.read_modules(input_file)
        self.fuel_func = fuel_func

    def get_total_module_fuel(self, inc_fuel: bool) -> int:
        total_fuel_required = 0
        for module in self.modules:
            fuel_req = module.mass
            while fuel_req > 0:
                fuel_req = self.fuel_func(fuel_req)
                total_fuel_required += max(0, fuel_req)
                if not inc_fuel:
                    break
        return total_fuel_required
    
    def read_modules(self, input_file: str) -> [Module]:
        modules = []
        with open(input_file) as f:
            for line in f.readlines():
                module = Module(mass=int(line))
                modules.append(module)
        return modules

def fuel_by_mass(mass: int) -> int:
    return math.floor(mass / 3) - 2

if __name__ == '__main__':
    fuel_counter_upper = FuelCounterUpper('input.txt', fuel_by_mass)
    total_fuel_req = fuel_counter_upper.get_total_module_fuel(inc_fuel=False)
    print("Required Fuel for Part 1: ", total_fuel_req)
    total_fuel_req = fuel_counter_upper.get_total_module_fuel(inc_fuel=True)
    print("Required Fuel for Part 2: ", total_fuel_req)
    
