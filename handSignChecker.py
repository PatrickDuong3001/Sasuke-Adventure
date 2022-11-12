class handSignChecker:    
    def compareHandSign(self, handsigns):
        if handsigns[0] == "three" and handsigns[1] == "four" and handsigns[2] == "one" and handsigns[3] == "five": #fire style
            return 1
        return -1