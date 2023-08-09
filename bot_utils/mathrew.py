from .apibtc import get_difficulty, get_rewards

def api_rew():
    t=86400
    R=get_rewards()
    H=1000000000000
    D=get_difficulty()
    step=4294967296
    threw=(t*R*H)/(D*step)
    otv='{:0.8f}'.format(threw)
    return otv