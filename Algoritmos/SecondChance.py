class SecondChance:
    def __init__(self):
        pass

    def marks(self, x, arr, second_chance, frames):
        for i in range(frames):
              
            if arr[i] == x:
                second_chance[i] = True
                return True
          
        return False
      
    def paging(self, x, arr, second_chance, frames, pointer):
        while(True):
            if not second_chance[pointer]:
                arr[pointer] = x

                return (pointer+1)%frames

            second_chance[pointer] = False
              
            pointer = (pointer + 1) % frames
      
    def simular(self, reference_string, frames):
          
        pointer = 0
        pf = 0
        arr = [0]*frames
        for s in range(frames):
            arr[s] = -1

        second_chance = [False]*frames
        Str = reference_string.split(' ')
          
        l = len(Str)
          
        for i in range(l):
            x = Str[i]

            if not self.marks(x,arr,second_chance,frames):
                pointer = self.paging(x,arr,second_chance,frames,pointer)
                pf += 1
