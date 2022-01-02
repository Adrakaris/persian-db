from tkinter import Button, Frame, Grid, Label, StringVar, Tk, Toplevel, Text
from tkinter.constants import E, N, S, W
from typing import List, Tuple
from functions import read_csv, linearly_find, write_csv, Table

# column names
TARG_LANG = 0
TARG_WORD = 1
ARIYA_SOURCE = 2
DEF = 3
TAVERNIER = 4
VARIANTS = 5
TYPE = 6
TRANSMISSION = 7
MED = 9
MEDIAN = 10

dictionary: Table[str]
HEADERS: List[str]
try:
    dictionary, HEADERS = read_csv("persianDict.csv")
except FileNotFoundError as e:
    print("Error: persianDict.csv not found")
    tryagain:str = input("Enter the file name of the dictionary (including the .csv extension): ")
    try:
        dictionary, HEADERS = read_csv(tryagain)
    except FileNotFoundError as e:
        with open("error-file-not-found.log", "w") as fn:
            fn.write("File not found: persianDict.csv\n")
        exit(1)

# write_csv("test.csv", HEADERS, dictionary)  # working

# for i in range(20):
#     print(dictionary[i])


class ResultsWindow:
    def __init__(self, base: Tk, data: Table[str]):
        self.base = base
        self.base.title("Results")
        
        self._assemble_table()    
        self.write_data(data)    
        
    def _assemble_table(self):
        # make target language box
        self.targLLabel = Label(self.base, text="Target Language:", font = ("Georgia", 10))
        self.targLLabel.grid(row=0, column=0, sticky=E+W)
        self.targLang = Text(self.base, height=50, width=20, font=("Georgia", 10))
        self.targLang.grid(row=1, column=0, sticky=W)
        
        # target word
        self.targWLabel = Label(self.base, text="Target Word:", font = ("Georgia", 10))
        self.targWLabel.grid(row=0, column=1, sticky=E+W)
        self.targWord = Text(self.base, height=50, width=20, font=("Georgia", 10))
        self.targWord.grid(row=1, column=1, sticky=W)
        
        # ariya source
        self.ariyaSLabel = Label(self.base, text="Ariya Source:", font = ("Georgia", 10))
        self.ariyaSLabel.grid(row=0, column=2, sticky=E+W)
        self.ariyaSource = Text(self.base, height=50, width=20, font=("Georgia", 10))
        self.ariyaSource.grid(row=1, column=2, sticky=W)
        
        # definition
        self.defLabel = Label(self.base, text="Definition:", font = ("Georgia", 10))
        self.defLabel.grid(row=0, column=4, sticky=E+W)
        self.definition = Text(self.base, height=50, width=30, font=("Georgia", 10))
        self.definition.grid(row=1, column=3, sticky=W)
        
        # tavernier
        self.tavenierLabel = Label(self.base, text="Tavernier:", font = ("Georgia", 10))
        self.tavenierLabel.grid(row=0, column=4, sticky=E+W)
        self.tavernier = Text(self.base, height=50, width=10, font=("Georgia", 10))
        self.tavernier.grid(row=1, column=4, sticky=W)
        
        # variants
        self.variantsLabel = Label(self.base, text="Variants:", font = ("Georgia", 10))
        self.variantsLabel.grid(row=0, column=5, sticky=E+W)
        self.variants = Text(self.base, height=50, width=30, font=("Georgia", 10))
        self.variants.grid(row=1, column=5, sticky=W)
        
        # type
        self.typeLabel = Label(self.base, text="Type:", font = ("Georgia", 10))
        self.typeLabel.grid(row=0, column=6, sticky=E+W)
        self.types = Text(self.base, height=50, width=20, font=("Georgia", 10))
        self.types.grid(row=1, column=6, sticky=W)
        
        # transmission
        self.transLabel = Label(self.base, text="Transmission:", font = ("Georgia", 10))
        self.transLabel.grid(row=0, column=7, sticky=E+W)
        self.transmission = Text(self.base, height=50, width=20, font=("Georgia", 10))
        self.transmission.grid(row=1, column=7, sticky=W)

    def write_data(self, data: Table[str]):
        # aggregate and write data into the text boxes
        aggregate_data: List[str] = ["" for i in range(len(data[0]))]
        for j, row in enumerate(data):
            for i, coln in enumerate(row):
                aggregate_data[i] += f"{j}) {coln}\n" 
        self.targLang.insert(1.0, aggregate_data[TARG_LANG])
        self.targWord.insert(1.0, aggregate_data[TARG_WORD])
        self.ariyaSource.insert(1.0, aggregate_data[ARIYA_SOURCE])
        self.definition.insert(1.0, aggregate_data[DEF])
        self.tavernier.insert(1.0, aggregate_data[TAVERNIER])
        self.variants.insert(1.0, aggregate_data[VARIANTS])
        self.types.insert(1.0, aggregate_data[TYPE])
        self.transmission.insert(1.0, aggregate_data[TRANSMISSION])
        
        

class Window:
    
    def __init__(self, base: Tk):
        self.base = base
        self.base.title("Persian Dictionary")
        
        self.mainFrame = Frame(self.base)
        self.mainFrame.grid(row=0, column=0, sticky=N+S+E+W)
        
        self.buttonFrame = Frame(self.base)
        self.buttonFrame.grid(row=1, column=0, sticky=N+S+E+W)
        Grid.rowconfigure(self.buttonFrame, 0, weight=1)
        Grid.columnconfigure(self.buttonFrame, 1, weight=1)
        Grid.columnconfigure(self.buttonFrame, 0, weight=1)
        
        # title stuff
        self.title = Label(self.mainFrame, text="Persian Dictionary", font=("Georgia", 20))
        self.title.grid(row=0, column=0, columnspan=2, sticky=E+W)
        
        self.status = StringVar()
        self.statusLabel = Label(self.mainFrame, textvariable=self.status, font=("Georgia", 10))
        self.statusLabel.grid(row=1, column=0, columnspan=2, sticky=E+W)
        
        self._ass_search()
        
        # submit button stuff
        # have a search button on the left
        self.searchButton = Button(self.buttonFrame, text="Search", command=self.search)
        self.searchButton.grid(row=0, column=0, sticky=E+W+N+S)
        
        self.saveButton = Button(self.buttonFrame, text="Save", command=self.save)
        self.saveButton.grid(row=0, column=1, sticky=E+W+N+S)
        
    def _ass_search(self):
        """
        Assembes the buttons of search window
        Ha ha very funny
        Two columns
        """
        # make target language box
        self.targLLabel = Label(self.mainFrame, text="Target Language:",font = ("Georgia", 10))
        self.targLLabel.grid(row=2, column=0, sticky=E)
        self.targLang = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.targLang.grid(row=2, column=1, sticky=W)
        
        # target word
        self.targWLabel = Label(self.mainFrame, text="Target Word:",font = ("Georgia", 10))
        self.targWLabel.grid(row=3, column=0, sticky=E)
        self.targWord = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.targWord.grid(row=3, column=1, sticky=W)
        
        # ariya source
        self.ariyaSLabel = Label(self.mainFrame, text="Ariya Source:",font = ("Georgia", 10))
        self.ariyaSLabel.grid(row=4, column=0, sticky=E)
        self.ariyaSource = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.ariyaSource.grid(row=4, column=1, sticky=W)
        
        # definition
        self.defLabel = Label(self.mainFrame, text="Definition:",font = ("Georgia", 10))
        self.defLabel.grid(row=5, column=0, sticky=E)
        self.definition = Text(self.mainFrame, height=3, width=20, font=("Georgia", 10))
        self.definition.grid(row=5, column=1, sticky=W)
        
        # tavernier
        self.tavenierLabel = Label(self.mainFrame, text="Tavernier:",font = ("Georgia", 10))
        self.tavenierLabel.grid(row=6, column=0, sticky=E)
        self.tavernier = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.tavernier.grid(row=6, column=1, sticky=W)
        
        # variants
        self.variantsLabel = Label(self.mainFrame, text="Variants:",font = ("Georgia", 10))
        self.variantsLabel.grid(row=7, column=0, sticky=E)
        self.variants = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.variants.grid(row=7, column=1, sticky=W)
        
        # type
        self.typeLabel = Label(self.mainFrame, text="Type:",font = ("Georgia", 10))
        self.typeLabel.grid(row=8, column=0, sticky=E)
        self.types = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.types.grid(row=8, column=1, sticky=W)
        
        # transmission
        self.transLabel = Label(self.mainFrame, text="Transmission:",font = ("Georgia", 10))
        self.transLabel.grid(row=9, column=0, sticky=E)
        self.transmission = Text(self.mainFrame, height=1, width=20, font=("Georgia", 10))
        self.transmission.grid(row=9, column=1, sticky=W)
    
    def _extract_data(self) -> List[Tuple[str, int]]:
        # extract data from text boxes
        data: List[Tuple[str, int]] = []
        buffer: str = ""
        
        if (buffer := self.targLang.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], TARG_LANG))
        if (buffer := self.targWord.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], TARG_WORD))
        if (buffer := self.ariyaSource.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], ARIYA_SOURCE))
        if (buffer := self.definition.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], DEF))
        if (buffer := self.tavernier.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], TAVERNIER))
        if (buffer := self.variants.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], VARIANTS))
        if (buffer := self.types.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], TYPE))
        if (buffer := self.transmission.get("1.0", "end")) != "\n":
            data.append((buffer[:-1], TRANSMISSION))
            
        # print(data)
            
        return data
    
    def search(self):
        data: List[Tuple[str, int]] = self._extract_data()
        
        result: Table[str] = linearly_find(data, dictionary)
        if not result:
            self.status.set("No results found")
            return
        self.status.set("Found results")
        # print(result[0])
        
        # open a results window
        resultWindow: ResultsWindow = ResultsWindow(Toplevel(self.base), result)
        
    def save(self):
        pass


if __name__ == '__main__':
    root:Tk = Tk()
    gui:Window = Window(root)
    root.mainloop()
