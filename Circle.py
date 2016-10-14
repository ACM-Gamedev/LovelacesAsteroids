
class Circle:

    def __init__(self, center, radius):

        self.center = center
        self.radius = radius

    # takes in another circle
    def overlaps(self, other):

        distance = (self.center - other.center).magnitude()

        sum_radii = self.radius + other.radius

        return distance <= sum_radii
