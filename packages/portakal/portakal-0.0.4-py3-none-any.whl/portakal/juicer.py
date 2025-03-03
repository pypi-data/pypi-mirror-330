import random

class OrangeJuicer:
    def __init__(self):
        self.total_juice = 0
        self.total_oranges_squeezed = 0
        self.new_orange()

    def new_orange(self):
        self.remaining_squeezes = random.randint(3,5)
        self.current_juice = 0
        print(f"🍊 Yeni portakal geldi! {self.remaining_squeezes} kez SIKILAbilir.")

    def squeeze(self):

        if self.remaining_squeezes > 0:
            juice = random.randint(30,80) #30ml - 80ml
            self.current_juice += juice
            self.total_juice += juice
            self.remaining_squeezes -= 1
            print(f"🧃 {juice} ml portakal suyu SIKILDI! KALAN SIKMA HAKKI: {self.remaining_squeezes}")

            if self.remaining_squeezes == 0:
                self.total_oranges_squeezed +=1
                print(f"✅ Portakal tamamen SIKILDI! Bu portakaldan {self.current_juice} ml su elde ettin.\n")
                self.new_orange()

        else:
            self.new_orange()

    def get_total_juice(self):
        print(f"🔢 Toplam {self.total_juice} ml portakal suyu SIKTIN!")

    def get_total_oranges(self):
        print(f"🍊 Toplam {self.total_oranges_squeezed} portakal SIKTIN!")
