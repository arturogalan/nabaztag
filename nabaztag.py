import sys
import nabaztagActions
# import recognizerActionsGoogle
import recognizerActionsWit
import time

def main():
    # nabaztagActions.sayMan("eh niño... que haces, quieres jugar?. No te voy a hacer daño")
    # nabaztagActions.sayWoman("eh niño... que haces, quieres jugar?. No te voy a hacer daño")
    # nabaztagActions.earsSad()
    # nabaztagActions.earsUp()

    # nabaztagActions.earsPayAttention()
    # time.sleep(1)
    # nabaztagActions.earsActionDone()
    # nabaztagActions.whisper("eh niño... que haces, quieres jugar?. No te voy a hacer daño")
    nabaztagActions.earsUp()
    # recognizerActionsGoogle.startRecognizer()
    recognizerActionsWit.startRecognizer()

    # nabaztagActions.earsSad()
if __name__ == '__main__':
    main()

