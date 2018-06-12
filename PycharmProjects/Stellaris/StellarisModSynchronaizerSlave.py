import os

if __name__ == "__main__":

    path_to_master_list = "master_mod_list.txt"
    while not os.path.exists(path_to_master_list):
        print("Please print path to the master_mod_list.txt: ", end='')
        path_to_master_list = input()

    mod_list = []
    with open(path_to_master_list, 'r') as file:
        for mod in file:
            mod_list.append(mod[:-1]) # without \n

    path_to_settings = os.path.join(os.path.expanduser("~"), "Documents\Paradox Interactive\Stellaris\settings.txt")
    while not os.path.exists(path_to_settings):
        print("Please print path to the Documents folder: ", end='')
        path_to_settings = os.path.join(input(), "Paradox Interactive\Stellaris\settings.txt")

    settings_lines = []
    with open(path_to_settings, 'r') as file:
        for line in file:
            settings_lines.append(line)
        file.close()

    new_settings = []
    for i in range(len(settings_lines)):
        if settings_lines[i] == "last_mods={\n":
            new_settings = settings_lines[:i + 1]
            for mod in mod_list:
                new_settings.append('\t"mod/ugc_{}.mod"\n'.format(mod))
            for k in range(i, len(settings_lines), 1):
                if settings_lines[k] == "}\n":
                    new_settings += settings_lines[k:]
                    break
        if settings_lines[i][:8] == "autosave":
            new_settings = settings_lines[:i]
            new_settings.append("last_mods={\n")
            for mod in mod_list:
                new_settings.append('\t"mod/ugc_{}.mod"\n'.format(mod))
            new_settings.append("}\n")
            new_settings += settings_lines[i:]
            break

    with open(path_to_settings, 'w') as file:
        for line in new_settings:
            file.write(line)
        file.close()




