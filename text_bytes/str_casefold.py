import unicodedata

if __name__ == "__main__":
    micro = "µ"
    print(">>>", unicodedata.name(micro))
    micro_cf = micro.casefold()
    print(">>>", unicodedata.name(micro_cf))
    print(">>>", micro, micro_cf)
    eszett = "ß"
    eszett_cf = eszett.casefold()
    print(">>>", unicodedata.name(eszett))
    print(">>>", eszett, eszett_cf)
