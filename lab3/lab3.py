import numpy as np
import matplotlib.pyplot as plt
element_files = ["Cd109.Txt", "Co57.Txt", "Co60.Txt", "Cs137.Txt", "Mn54.Txt", "Na22.Txt", "Zn65.Txt"]
data = ["data/" + i for i in element_files]

E_CONST = 1.972973

class Element():
    def __init__(self, file) -> None:
        self.__name = self.__set_name(file)
        self.__e = self.__set_energy(file) # energy array in keV
        self.__counts = self.__set_counts(file) # array of counts (usually 5 columns)
        self.__avg_counts = self.__set_avg_counts(self.get_counts()) # average of the columns in the counts
    def __set_name(self, file) -> str:
        with open(file, "r") as f:
            lines = f.readlines()
            for l in range(len(lines)):
                if lines[l] == "Sample description:\n":
                    n = lines[l + 1]
                    break
        return n.strip()
    def get_name(self) -> str:
        return self.__name
    def __set_energy(self, file) -> np.array(list()):
        e = np.array([])
        with open(file, "r") as f:
            lines = f.readlines()
            d_start = 0
            for l in range(len(lines)):
                if lines[l] == "SPECTRUM\n":
                    d_start = l + 1
                    break
            for l in lines[d_start:]:
                e = np.append(e, int(l.split()[0][:-1]) * E_CONST)
        return e
    def get_energy(self) -> np.array(list()):
        return self.__e
    def __set_counts(self, file) -> np.array(list()):
        with open(file, "r") as f:
            lines = f.readlines()
            for l in range(len(lines)):
                if lines[l] == "SPECTRUM\n":
                    d_start = l + 1
                    break
            col_counts = []
            for l in lines[d_start:]:
                l = l.split()[1:]
                line_len = len(l)
                col_val = []
                for i in range(line_len):
                    col_val.append(int(l[i]))
                col_counts.append(col_val)
        return col_counts
    def get_counts(self) -> np.array(list()):
        return self.__counts               
    def __set_avg_counts(self, counts) -> np.array(list()):
        avg_counts = np.array([])
        for c in counts:
            avg_counts = np.append(avg_counts, np.mean(c))
        return avg_counts
    def get_avg_counts(self) -> np.array(list()):
        return self.__avg_counts
    def __str__(self) -> str:
        return self.get_name()
elements = np.array([])
for d in data:
    elements = np.append(elements, Element(d))
for e in elements:
    fig, ax = plt.subplots(1, 1)
    ax.plot(e.get_energy(), e.get_avg_counts())
    ax.set_xlim([0, 1.5e3])
    ax.set_title(e.get_name())
    fig.show()
plt.show()