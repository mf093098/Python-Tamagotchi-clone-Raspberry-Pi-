import pygame
import  random
import signal
import  os
import  sys
from displayhatmini import DisplayHATMini
import RPi.GPIO as GPIO

#screen = pygame.display.set_mode((320, 240))




class PygameDHM():
    screen = None
    # inicjalizacja ekranu
    def __init__(self):
        self.dhm = DisplayHATMini(None)
        self._init_display()

        self.screen.fill((0, 0, 0))
        self._updatefb()

        self._running = False
        #odczytywanie przycisków i tłumaczenie dla pygame
        def button_callback(pin):
            key = {
                self.dhm.BUTTON_A: 'a',
                self.dhm.BUTTON_B: 'b',
                self.dhm.BUTTON_X: 'x',
                self.dhm.BUTTON_Y: 'y'
            }[pin]
            event = pygame.KEYDOWN if self.dhm.read_button(pin) else pygame.KEYUP
            pygame.event.post(pygame.event.Event(event, unicode=key, key=pygame.key.key_code(key)))

        self.dhm.on_button_pressed(button_callback)


    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def _init_display(self):
        os.putenv('SDL_VIDEODRIVER', 'dummy')
        pygame.display.init()  # Need to init for .convert() to work
        self.screen = pygame.Surface((320, 240))

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def _updatefb(self):
        self.dhm.st7789.set_window()
        # Grab the pygame screen as a bytes object
        pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16, 0).get_buffer()
        # Lazy (slow) byteswap:
        pixelbytes = bytearray(pixelbytes)
        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
        for i in range(0, len(pixelbytes), 4096):
            self.dhm.st7789.data(pixelbytes[i:i + 4096])





    #gra
    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        bg = pygame.image.load("tlo.png")
        sleeping= pygame.image.load("sleeping.png")
        sleeping = pygame.transform.scale(sleeping, (260, 180))
        night = pygame.image.load("night.jpg")
        night = pygame.transform.scale(night, (320, 240))
        pet = pygame.image.load("animal.png")
        pet = pygame.transform.scale(pet, (260, 180))
        sleep = pygame.image.load("moon.png")
        sleep = pygame.transform.scale(sleep, (20, 20))
        happy = pygame.image.load("happy.png")
        happy = pygame.transform.scale(happy, (20, 20))
        heart = pygame.image.load("heart.png")
        heart = pygame.transform.scale(heart, (30, 30))
        food = pygame.image.load("food.png")
        food = pygame.transform.scale(food, (80, 80))
        minigame = pygame.image.load("minigame.png")
        minigame = pygame.transform.scale(minigame, (320, 240))
        rock = pygame.image.load("rock.png")
        rock = pygame.transform.scale(rock, (100, 100))
        paper = pygame.image.load("paper.png")
        paper = pygame.transform.scale(paper, (80, 80))
        scissors = pygame.image.load("scissors.png")
        scissors = pygame.transform.scale(scissors, (80, 80))
        poop = pygame.image.load("poop.png")
        poop = pygame.transform.scale(poop, (80, 80))
        clock = pygame.time.Clock()
        delta = 0.0
        a = 0
        b = 0
        z = 0
        smutek = 1
        kpn = 0
        cleaning = 0;
        koniec = 0
        gracz = 0
        pingwin = 0
        rockpaperscissors = [1, 2, 3]
        spanko= 0
        sleeptime= 0
        self._running = True
        signal.signal(signal.SIGINT, self._exit)
        #wyłączanie gry
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        break

            # Clear the screen
            self.screen.fill((0, 0, 0))

            #uzależnienie animacji i pasków od czasu
            delta += clock.tick() / 1000.0
            while delta > 0.5:
                # print("rusz pingwina")
                delta -= 0.5
                z += 1  #
                a += 10  # ruch w x
                b += 10  # ruch w y
                if z > 20:
                    cleaning = 1
                    if (z % 10) == 0:
                        smutek+=5


                if smutek < 96 :
                    if (z % 10) == 0:
                        smutek += 5
                        spanko += 1



            self.screen.fill((255, 255, 255))
            self.screen.blit(bg, (0, 0))
            if a <= 40:  # ruch pingwina funkcja

                if (b % 20) != 0:
                    # print(b)
                    self.screen.blit(pet, (20 - a, 40 + 10))

                else:
                    self.screen.blit(pet, (20 - a, 40 - 10))
            else:
                a = 0

           #zmiana pasków
            if smutek <= 95:
                pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(195, 10, 100 - smutek, 10))
            if spanko <= 95:
                pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(30, 10, 100 - spanko, 10))

            self.screen.blit(sleep, (5, 5))
            self.screen.blit(happy, (170, 5))
            if cleaning == 1:
                self.screen.blit(poop, (240, 140))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x and 100 - smutek < 99:
                        #karmienie
                        self.screen.blit(food, (200, 40))

                        self.screen.blit(heart, (15, 120))
                        GPIO.output(19, GPIO.HIGH)
                        pygame.time.wait(40)
                        GPIO.output(19, GPIO.LOW)
                        pygame.time.wait(1000)
                        smutek -= 20
                    elif event.key == pygame.K_y:
                        cleaning = 0
                        z= 0
                        GPIO.output(19, GPIO.HIGH)
                        pygame.time.wait(40)
                        GPIO.output(19, GPIO.LOW)
                        # Grab the pygame screen as a bytes object
                        pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16, 0).get_buffer()
                        # Lazy (slow) byteswap:
                        pixelbytes = bytearray(pixelbytes)
                        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                        for i in range(0, len(pixelbytes), 4096):
                            self.dhm.st7789.data(pixelbytes[i:i + 4096])
                    #spanie
                    elif event.key == pygame.K_b:
                        sleeptime=1
                        while sleeptime == 1:

                                self.screen.blit(night, (0, 0))
                                self.screen.blit(sleeping, (20, 40))
                                self.screen.blit(sleep, (5, 5))
                                self.screen.blit(happy, (170, 5))
                                pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(30, 10, 100 - spanko, 10))
                                pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(195, 10, 100 - smutek, 10))
                                self.dhm.st7789.set_window()
                                # Grab the pygame screen as a bytes object
                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16, 0).get_buffer()
                                # Lazy (slow) byteswap:
                                pixelbytes = bytearray(pixelbytes)
                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                for i in range(0, len(pixelbytes), 4096):
                                        self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                if 100 - spanko < 100:
                                    pygame.time.wait(300)
                                    spanko -= 10
                                if 100 - spanko >= 100:
                                    sleeptime=0

                                for wstan in pygame.event.get():
                                    if wstan.type == pygame.KEYDOWN:
                                        if wstan.key == pygame.K_b:
                                            sleeptime=0
                    #kamien papier nozyce
                    elif event.key == pygame.K_a:

                        kpn +=1



                        while kpn >= 1:

                            self.screen.blit(minigame, (0, 0))
                            self.screen.blit(sleep, (5, 5))
                            self.screen.blit(happy, (170, 5))
                            self.screen.blit(pet, (140, 160))
                            pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(195, 10, 100 - smutek, 10))
                            pygame.draw.rect(self.screen, (250, 0, 0), pygame.Rect(30, 10, 100 - spanko, 10))
                            self.dhm.st7789.set_window()
                            # Grab the pygame screen as a bytes object
                            pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16, 0).get_buffer()
                            # Lazy (slow) byteswap:
                            pixelbytes = bytearray(pixelbytes)
                            pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                            # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                            for i in range(0, len(pixelbytes), 4096):
                                self.dhm.st7789.data(pixelbytes[i:i + 4096])



                            # screen.blit(rock, (15, 50))


                            for finisz in pygame.event.get():
                                if finisz.type == pygame.KEYDOWN:
                                    if finisz.key == pygame.K_a:

                                        kpn = 0

                                        # print("koniec")
                                    elif finisz.key == pygame.K_x:

                                        gracz = 1
                                        pingwin = random.choice(rockpaperscissors)
                                        print("pingwin=", pingwin)
                                        print("gracz =", gracz)
                                        self.screen.blit(rock, (15, 50))
                                        self.dhm.st7789.set_window()
                                        # Grab the pygame screen as a bytes object
                                        pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                       0).get_buffer()
                                        # Lazy (slow) byteswap:
                                        pixelbytes = bytearray(pixelbytes)
                                        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                        for i in range(0, len(pixelbytes), 4096):
                                            self.dhm.st7789.data(pixelbytes[i:i + 4096])

                                        if gracz == pingwin or pingwin == 2:


                                            if pingwin == 1:
                                                self.screen.blit(rock, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                            if pingwin == 2:
                                                self.screen.blit(paper, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])

                                        else:
                                            if 100 - smutek < 99:
                                                smutek -= 20

                                            self.screen.blit(scissors, (200, 50))
                                            print("wygrana")
                                            GPIO.output(19, GPIO.HIGH)
                                            pygame.time.wait(40)
                                            GPIO.output(19, GPIO.LOW)
                                    elif finisz.key == pygame.K_b:
                                        gracz = 2
                                        pingwin = random.choice(rockpaperscissors)
                                        self.screen.blit(paper, (15, 50))
                                        self.dhm.st7789.set_window()
                                        # Grab the pygame screen as a bytes object
                                        pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                       0).get_buffer()
                                        # Lazy (slow) byteswap:
                                        pixelbytes = bytearray(pixelbytes)
                                        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                        for i in range(0, len(pixelbytes), 4096):
                                            self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                        print("pingwin=", pingwin)
                                        print("gracz =", gracz)
                                        if gracz == pingwin or pingwin == 3:
                                            if pingwin == 2:
                                                self.screen.blit(paper, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                            if pingwin == 3:
                                                self.screen.blit(scissors, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])

                                        else:
                                            if 100 - smutek < 99:
                                                smutek -= 20
                                            self.screen.blit(rock, (200, 50))
                                            self.dhm.st7789.set_window()
                                            # Grab the pygame screen as a bytes object
                                            pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                           0).get_buffer()
                                            # Lazy (slow) byteswap:
                                            pixelbytes = bytearray(pixelbytes)
                                            pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                            # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                            for i in range(0, len(pixelbytes), 4096):
                                                self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                            print("wygrana")
                                            GPIO.output(19, GPIO.HIGH)
                                            pygame.time.wait(40)
                                            GPIO.output(19, GPIO.LOW)
                                    elif finisz.key == pygame.K_y:

                                        gracz = 3
                                        pingwin = random.choice(rockpaperscissors)
                                        print("pingwin=", pingwin)
                                        print("gracz =", gracz)
                                        self.screen.blit(scissors, (15, 50))
                                        self.dhm.st7789.set_window()
                                        # Grab the pygame screen as a bytes object
                                        pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                       0).get_buffer()
                                        # Lazy (slow) byteswap:
                                        pixelbytes = bytearray(pixelbytes)
                                        pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                        # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                        for i in range(0, len(pixelbytes), 4096):
                                            self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                        if gracz == pingwin or pingwin == 1:
                                            if pingwin == 3:
                                                self.screen.blit(scissors, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                            elif pingwin == 1:
                                                self.screen.blit(rock, (200, 50))
                                                self.dhm.st7789.set_window()
                                                # Grab the pygame screen as a bytes object
                                                pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                               0).get_buffer()
                                                # Lazy (slow) byteswap:
                                                pixelbytes = bytearray(pixelbytes)
                                                pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                                # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                                for i in range(0, len(pixelbytes), 4096):
                                                    self.dhm.st7789.data(pixelbytes[i:i + 4096])

                                        else:
                                            self.screen.blit(paper, (200, 50))
                                            self.dhm.st7789.set_window()
                                            # Grab the pygame screen as a bytes object
                                            pixelbytes = pygame.transform.rotate(self.screen, 180).convert(16,
                                                                                                           0).get_buffer()
                                            # Lazy (slow) byteswap:
                                            pixelbytes = bytearray(pixelbytes)
                                            pixelbytes[0::2], pixelbytes[1::2] = pixelbytes[1::2], pixelbytes[0::2]
                                            # Bypass the ST7789 PIL image RGB888->RGB565 conversion
                                            for i in range(0, len(pixelbytes), 4096):
                                                self.dhm.st7789.data(pixelbytes[i:i + 4096])
                                            if 100 - smutek < 99:
                                                smutek -= 20
                                            GPIO.output(19, GPIO.HIGH)
                                            pygame.time.wait(40)
                                            GPIO.output(19, GPIO.LOW)
                                            print("wygrana")

            #dotyk
            print(GPIO.input(8))
            if (GPIO.input(8) == True) and 100 - smutek < 99:

                #print("Dotknoles pingwinka")
                smutek-=10
                self.screen.blit(heart, (15, 120))
                GPIO.output(19, GPIO.HIGH)
                pygame.time.wait(90)
                GPIO.output(19, GPIO.LOW)

            self._updatefb()

        pygame.quit()
        sys.exit(0)

display = PygameDHM()
display.run()


