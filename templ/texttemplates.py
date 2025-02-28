def fishlist(fishdata):
    result = ""
    i = 0
    for key, value in fishdata.items():
        i+=1
        result += f"\n🐟 - {i}) {key} - {value}%"
    return result