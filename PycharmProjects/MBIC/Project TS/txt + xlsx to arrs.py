import os

def txt_to_list(path_to_txt):
    lines = []
    with open(path_to_txt, 'r') as file:
        data = False
        for line in file:
            if line[:2] == "0\t":
                data = True
            if data:
                lines.append(line)
    return lines


path_to_data = "data"
txt_names = [os.path.join(path_to_data, f) for f in os.listdir(path_to_data) if
                        os.path.isfile(os.path.join(path_to_data, f))]

data_dict = {txt.split('\\')[-1]: txt_to_list(txt) for txt in txt_names}
print(data_dict.keys())