from mnemonic import Mnemonic
import hashlib

class mnemo_memword_gen:
    '''shortcut: need to use 12, 15, 18, 21, 24 library provided word, hard to memorize'''
    def __init__(self):
        pass

    '''if not provide any args, gen new. if provide, recall user the seed'''
    def run(self, recall:str=None):
        mnemo = Mnemonic("english")

        if (recall==None):
            # gen if empty
            input("Press enter to generate mnemonic, taken them down carefully!")
            recall = mnemo.generate(strength=256)
        else:
            if(mnemo.check(recall)):
                print("Valid mnemonic")
            else:
                exit(1)

        seed = mnemo.to_seed(recall, passphrase=input("Enter passphrase:"))

        # seed is out result, ok to use
        print(f"Mnemonic: {recall}")
        print(f"Seed: {seed.hex()}")
        return seed



class sha256_memword_gen:
    '''pro: unique word gen 1-1 password
            user provided arbitary len password
        con: possible to use social enginerring + rainbow table'''

    def __init__(self):
        pass

    def run(self):
        memword = input("Enter your memonic:")
        result = hashlib.sha256(memword.encode()).hexdigest()
        return result

testsubj = mnemo_memword_gen()
testsubj.run("slice raw idle system ticket hammer debris trumpet little before mass sock window neck cement toy tide wet reward grocery announce wine grit work")
#suggest test: "slice raw idle system ticket hammer debris trumpet little before mass sock window neck cement toy tide wet reward grocery announce wine grit work"
# passphase: 123413

