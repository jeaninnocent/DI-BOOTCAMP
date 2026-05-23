import math
import turtle

class Circle:
    def __init__(self, radius=1.0):
        # The base attribute is the radius
        self.radius = radius

    # --- DECORATORS FOR DIAMETER ---
    
    @property
    def diameter(self):
        """Allows querying the diameter (e.g., print(c.diameter))"""
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        """Allows setting the circle via diameter (e.g., c.diameter = 10)"""
        self.radius = value / 2

    @property
    def area(self):
        """Computes the area dynamically."""
        return math.pi * (self.radius ** 2)

    # --- DUNDER (MAGIC) METHODS ---

    def __str__(self):
        """User-friendly print output."""
        return f"Circle(radius={self.radius:.1f}, diameter={self.diameter:.1f})"

    def __repr__(self):
        """Developer-friendly representation (useful in lists)."""
        return f"Circle({self.radius})"

    def __add__(self, other):
        """Adds two circles together to return a new Circle."""
        if isinstance(other, Circle):
            return Circle(self.radius + other.radius)
        raise TypeError("Can only add another Circle.")

    def __gt__(self, other):
        """Greater than: compares two circles (c1 > c2)."""
        if isinstance(other, Circle):
            return self.radius > other.radius
        return NotImplemented

    def __lt__(self, other):
        """Less than: compares two circles (c1 < c2). Crucial for sorting!"""
        if isinstance(other, Circle):
            return self.radius < other.radius
        return NotImplemented

    def __eq__(self, other):
        """Equal to: checks if two circles are identical in size (c1 == c2)."""
        if isinstance(other, Circle):
            return self.radius == other.radius
        return NotImplemented


# ==========================================
# TEST AND DEMONSTRATION
# ==========================================
def main():
    # 1. Create circles using radius or diameter
    c1 = Circle(radius=50)
    
    c2 = Circle()
    c2.diameter = 60  # Using the @diameter.setter decorator

    c3 = Circle(radius=15)

    # 2. Print attributes
    print(f"C1: {c1} | Area: {c1.area:.2f}")
    print(f"C2: {c2} | Area: {c2.area:.2f}")

    # 3. Add two circles
    c4 = c1 + c2
    print(f"\nAdding C1 and C2 creates C4: {c4}")

    # 4. Compare circles
    print(f"\nIs C1 greater than C2? {c1 > c2}")
    print(f"Is C1 equal to C3? {c1 == c3}")

    # 5. Store in a list and sort
    # (Sorting works automatically because we defined __lt__ and __gt__)
    circle_list = [c1, c2, c3, c4]
    circle_list.sort()
    
    print("\nSorted Circles (from smallest to largest):")
    print(circle_list)

    # ==========================================
    # BONUS CHALLENGE: DRAWING WITH TURTLE
    # ==========================================
    print("\nDrawing circles... Look for the new window!")
    
    # Setup turtle screen
    screen = turtle.Screen()
    screen.title("Sorted Circles Visualized")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(3)
    t.pensize(2)
    
    # Start position for drawing
    x_offset = -250
    
    for circle in circle_list:
        # Move turtle to the correct starting point (bottom of the circle)
        t.penup()
        t.goto(x_offset, -circle.radius)
        t.pendown()
        
        # Draw the circle
        t.circle(circle.radius)
        
        # Move right for the next circle (diameter + a little gap)
        x_offset += circle.diameter + 20

    # Wait for the user to close the window
    turtle.done()

if __name__ == "__main__":
    main()