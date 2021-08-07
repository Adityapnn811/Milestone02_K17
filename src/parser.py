def parsermsg(text, kata_kunci):
    arr_text = text.split(' ')
    for word in arr_text:
        if word == kata_kunci:
            return word

# contoh penggunaan
'''
text = "Aku stress banget nih"
kata_kunci = parsermsg(text, "makan")
if kata_kunci == "stress":
    print("Ini nih biar lu ga stress")
else:
    print("Ngomong apaan sih lu")
'''
