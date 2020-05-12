class Capture(object):
    
    speedLimit=30

    def __init__(self, number_plate, Speed):
        self.num_plate = number_plate
        self.speed = Speed
        self.fineTBP = 0
    
    def fine(self):
        excess = self.speed - self.speedLimit
        
        excess = round(excess, 3)
        
        if (excess <= 10):
            self.fineTBP= 0
            print("The fine to be paid is {self.fineTBP}")

        elif (excess > 10):
            exceeded = excess - 10
            self.fineTBP = 100+ (0.50*exceeded*50)
            self.fineTBP = round(self.fineTBP, 2)
            return self.fineTBP
        
    def changeSpd(self, new_speed):
        self.speed = new_speed

    def speed_lim(self):
        print(self.speedLimit)

caught = Capture("GN-2737-20", 45.7)
caught.fine()