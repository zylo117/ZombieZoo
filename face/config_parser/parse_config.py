import configparser, os, pathlib


class Config:
    def __init__(self, conf_path):
        self.conf_path = conf_path

        file_path = pathlib.Path(conf_path)
        if not file_path.exists():
            parent_path = "/".join(self.conf_path.split("/")[:-1])
            if not pathlib.Path(parent_path).exists():
                os.mkdir(parent_path)
            conf_file = open(self.conf_path, "w")
            conf_file.close()

        self.conf = configparser.ConfigParser()
        self.conf.read(conf_path)

    def _section_exist(self, section_name):
        self.section = self.conf.sections()
        for section in self.section:
            if section == section_name:
                return True

    def get_value(self, section_name, option_name, type="str"):
        value = self.conf.get(section_name, option_name)

        # pre-classify data type and remove annotation
        if type == "str":
            return str(value).split("  #")[0]
        elif type == "bool":
            v = str(value).split("  #")[0]
            if v.lower() == "true":
                return True
            else:
                return False
        elif type == "int":
            return int(str(value).split("  #")[0])
        elif type == "float":
            return float(str(value).split("  #")[0])

    def set_value(self, section_name, option_name, new_value, annotation=None, write_to_file=True):
        if not self._section_exist(section_name):
            self.conf.add_section(section_name)

        # add annotation
        if annotation is not None:
            annotation = str(annotation)
            annotation = annotation.strip("#")
            new_value += "  # " + annotation

        self.conf.set(section_name, option_name, new_value)

        if write_to_file:
            self.conf.write(open(self.conf_path, "w"))

    def remove(self, section, option=None):
        if option is None:
            self.conf.remove_section(section)
        else:
            self.conf.remove_option(section, option)
        self.conf.write(open(self.conf_path, "w"))

    def remove_all(self):
        self.section = self.conf.sections()
        for section in self.section:
            self.conf.remove_section(section)
        self.conf.write(open(self.conf_path, "w"))

    def list_items(self):
        self.conf.items()

if __name__ == "__main__":
    current_module_path = os.path.dirname(os.path.abspath(__file__))

    conf = Config("./main_config.conf")
    conf.remove_all()

    conf.set_value("Category", "Granite-C", "Q", "set the header for every category")
    conf.set_value("Category", "Granite-D", "Q")
    conf.set_value("Category", "Granite-E", "Q")
    conf.set_value("Category", "BlueBerry", "Q")
    conf.set_value("Category", "Angel-P", "A")
    conf.set_value("Category", "Angel-R", "A")
    conf.set_value("Category", "Lumber", "H")
    conf.set_value("Category", "Syrup-A", "Y")
    conf.set_value("Category", "Syrup-S", "Y")
    conf.set_value("MachineType", "gfc-up", "GU", "set the short version for every machine type")
    conf.set_value("MachineType", "gfc-down", "GD")
    conf.set_value("MachineType", "oqc-up", "QU")
    conf.set_value("MachineType", "oqc-down", "QU")
    conf.set_value("MachineType", "cube-up", "CU")
    conf.set_value("MachineType", "cube-down", "CU")
    conf.set_value("MachineType", "rel-up", "RU")
    conf.set_value("MachineType", "rel-down", "RU")
    conf.set_value("Default", "GFC_Data_Path", "./000.csv")



    print(conf.get_value("Category", "Lumber", type="str"))
