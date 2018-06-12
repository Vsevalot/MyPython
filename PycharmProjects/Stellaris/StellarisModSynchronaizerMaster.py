import os

if __name__ == "__main__":
    path_to_settings = os.path.join(os.path.expanduser("~"), "Documents\Paradox Interactive\Stellaris\settings.txt")
    while not os.path.exists(path_to_settings):
        print("Please print path to the Documents folder: ", end='')
        path_to_settings = os.path.join(input(), "Paradox Interactive\Stellaris\settings.txt")

    mod_list = []
    with open(path_to_settings, 'r') as file:
        mod_lines = False
        for line in file:
            if line == "last_mods={\n":
                mod_lines = True
                continue
            if line == "}\n" and mod_lines: # the closing bracket
                break
            if mod_lines:
                mod_list.append(line.split('_')[-1].split('.')[0])
        file.close()

    with open("master_mod_list.txt", 'w') as file:
        for mod in mod_list:
            file.write("{}\n".format(mod))
        file.close()