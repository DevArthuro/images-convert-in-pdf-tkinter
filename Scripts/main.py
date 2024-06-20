import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
#Library convert to pdf 
import os
import shutil
from PIL import Image
from PyPDF2 import PdfMerger

#save functions 
class Functions_window():
    #address save files
    paths = {
        "download" : [],
        "photos" : [],
        "name" : []
            }
    #Select directory
    def open_fileExplorer(self, root, entry):
        root.filename =  filedialog.askdirectory(initialdir = "c:/",title = "Select directory")
        entry.delete(0, 999)
        entry.insert(999, root.filename)
        if((len(entry.get())>0)):
            #save path directory
            self.paths["download"].append(entry.get())
            entry.config(state="disabled")
    #select files
    def selector_files(self,root, entry):
        root.filename = filedialog.askopenfilenames(initialdir="c:/", title="Select File", filetypes=(("imagenes jpg", "*.jpeg"),("arvivos png", "*.png")))
        entry.delete(0, 999)
        entry.insert(999, root.filename)
        if((len(entry.get())>0)):
            #save path photos
            self.paths["photos"].append(entry.get())
            entry.config(state="disabled")
            
    def convert_to_PDF(self, entry_name, entry_path, entry_photos):
        if not(entry_name.get() == "" or "." in entry_name.get()):
            self.paths["name"].append(entry_name.get())
            entry_name.config(state="disabled")
        else:
            self.paths["name"].append("generic_name")
            entry_name.delete(0, 999)
            entry_name.insert(999, "generic_name")
            entry_name.config(state="disabled")
        #verificamos que el archivo tenga su ruta de descarga y imagenes
        if ((len(self.paths["download"])>0) and (len(self.paths["photos"])>0)):
            name_pdf = self.paths["name"][0]
            #pass the images to a list
            image_list = self.paths["photos"]
            images = " ".join(image_list)
            #organize the paths
            """Podemos encontrar rutas con espacion, estas deben ser organizadas para una correcta lectura y evitar     errores"""
            word = "" #con este buscaremos dejar las rutas limpias
            list_path = [] #guardaremos las rutas 1 x 1 
            entrada = False # con este haremos la limpieza de las rutas con espacios
            for i in images: #recorremos el join (str) para organizar las rutas
                # Las direccion con espacios se almacenan en {} usamos esto para saber cuales debemos arreglar
                if entrada == True:
                    #cuando inicia por "{" sabemos que empezara una nueva ruta
                    if i == "{":
                        continue #damos salto y evitamos agregar "{"
                    #cuando nos encontramos "}" finaliza la ruta agregamos y reiniciamos
                    if i == '}':
                        #si hay una palabra tendremos una ruta la agregamos y reiniciamos
                        if len(word) > 0:
                            list_path.append(word)
                            word = ""
                        entrada = False
                        continue
                    word += i #vamos armando la ruta
                # esta entrada ya son las rutas que no estan entre "{}"
                if entrada == False:
                    # si empieza con "{" sabemos que es una ruta con espacios, reiniciamos y mandamos la ruta para el   primer if
                    if i == '{':
                        entrada = True
                        word = ""
                        continue
                    #cuando encontremos un espacio sabremos que la ruta se completos reiniciamos y continuamos 
                    if i == " ":
                        if len(word) > 0:
                            list_path.append(word)
                            word = ""
                        continue
                    word += i #Organizar el enlace - interpretacion de datos 
                    #Este if evalua conversiones de una sola imagen 
                    if (" " not in (self.paths["photos"][0])): #sabemos que las direccion de una imagen no tiene espacio 
                        if (len(self.paths["photos"][0])) == (len(word)):  #verificamos el tamaño de la ruta original con la organizacion
                            #si es correcta procedemos a guardarla
                            list_path.append(word)
                            word = ""
                            continue
                    #vamos armando la ruta
                    
            # copiaremos las imagenes en una carpeta local
            #copiamos cada imagen en una carpeta diferente
            
            for i in list_path:
                path_current = os.getcwd()
                path_copy = f"{path_current}/carpeta"
                if not os.path.exists(path_copy):
                    os.mkdir(f"{path_current}/carpeta")
                shutil.copy(i, path_copy)
            #renombramos las imagenes 
            #quede arreglando renombramiento pero el problema es la extenciion del archivo
            count = 0
            
            for i in os.listdir(path_copy):
                #averiguamos cua es el tipo de extencion para que la imagen se guarde correctamente 
                if (".png" in i) or (".PNG" in i):
                    extention = ".png"
                elif (".jpeg" in i) or (".jpg" in i):
                    extention = ".jpg"
                os.rename(f"{path_copy}/{i}", f"{path_copy}\{str(count)}{extention}")
                count += 1
            
            """Convertidor pdf """
            #direccion de imagenes
            #primero convertimos cada imagen a pdf
            if not (os.path.exists(f"{os.getcwd()}/carpeta/pdf")):
                os.mkdir(f"{os.getcwd()}/carpeta/pdf")
            
            output_dir = f"{os.getcwd()}/carpeta/pdf"
            sourse_dir = f"{os.getcwd()}/carpeta"
            for file in os.listdir(sourse_dir):
                if file.split(".")[-1] in ("png", "PNG", "jpeg", "jpg"):
                    image = Image.open(os.path.join(sourse_dir, file))
                    image_convert = image.convert("RGB")
                    image_convert.save(os.path.join(output_dir, f"{file.split('.')[-2]}.pdf"))
            list_pdf = os.listdir(output_dir)
            merger = PdfMerger()
            for i in list_pdf:
                merger.append(f"{output_dir}/{i}")
            merger.write(f"{os.getcwd()}/{name_pdf}.pdf")
            merger.close()
            #eliminamos las rutas (carpetas) que creamos 
            for i in list_pdf:
                os.remove(f"{output_dir}/{i}")
            os.rmdir(output_dir)
            for i in os.listdir(sourse_dir):
                os.remove(f"{sourse_dir}/{i}")
            os.rmdir(sourse_dir)
            path_download = self.paths['download'][0]
            #evitamos tener archivos repetidos
            count = 1 #buscaremos agragarle un nombre al pdf agregandole un numero de mas cada que vez que este     repetido
            if (os.path.exists(f"{path_download}/{name_pdf}.pdf")):
                while True:
                    if not(os.path.exists(f"{path_download}/{name_pdf}{str(count)}.pdf")):
                        os.rename(f"{os.getcwd()}/{name_pdf}.pdf", f"{os.getcwd()}/{name_pdf}{str(count)}.pdf")
                        shutil.copy(f"{os.getcwd()}/{name_pdf}{str(count)}.pdf", path_download)
                        name_pdf = f"{name_pdf}{str(count)}"
                        self.clean_all(entry_name, entry_path, entry_photos)
                        break
                    count += 1
            else:    
                shutil.copy(f"{os.getcwd()}/{name_pdf}.pdf", path_download)
            os.remove(f"{os.getcwd()}/{name_pdf}.pdf")
            self.clean_all(entry_name, entry_path, entry_photos)
            if (os.path.exists(f"{path_download}/{name_pdf}.pdf")):
                messagebox.showinfo("Correctamente", f"Tu archivo se encuentra en:\n {path_download}/{name_pdf}.pdf")
                self.paths["name"].pop()
                self.paths["photos"] = []
                self.paths["download"] = []
        else:
            messagebox.showwarning("Alerta", "Uno de los campos no fue correctamente diligenciado")
            self.clean_all(entry_name, entry_path, entry_photos)
            messagebox.showinfo("Error Inesperado", "Intentalo nuevamente")
            self.paths["name"].pop()
        
    def clean_all(self, entry_1, entry_2, entry_3):
        #habilitamos las entradas
        list_entrys = [entry_1, entry_2, entry_3]
        for i in list_entrys:
            i.config(state="activate")
            #Hacemos cinco eliminacion ya que en el campo de (entry_selectFiles) puede sobrepasar el rango de caracteres
            i.delete(0,999)
            tamaño = len(i.get())
            if (tamaño > 0):
                while 1:
                    tamaño = len(i.get())
                    if (tamaño > 0):
                        i.delete(0,999)
                    else:
                        break
    
class Window(Functions_window):
    def __init__(self):
        #ventana de configuración
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title("Convertidor convencional")
        self.root.iconbitmap("logo.ico")
        #navigation menu
        self.sections = ttk.Notebook(self.root, )
        self.sections_Notebook_one()
        self.sections.grid(column=0, row=0, padx=10, pady=0)
        self.root.mainloop()
    #
    def sections_Notebook_one(self):
        #Interface converter
        self.page_frame1 = ttk.Frame(self.sections)
        self.sections.add(self.page_frame1, text="convertidor")
        
        #collector path
        self.converter = ttk.Labelframe(self.page_frame1, text="Elegir Carpetas")
        self.converter.grid(column=0, row=0, padx=5, pady=10)
        
        #collector path where file will go
        self.Label_goFile = ttk.Label(self.converter, text="Ruta de Descarga")
        self.Label_goFile.grid(column=0, row=0, padx=5)
        self.Entry_goFile = ttk.Entry(self.converter, justify="right", font=("Times New Roman", 8))
        self.Entry_goFile.grid(column=1, row=0)
        self.Button_goFile = ttk.Button(self.converter, text="Elegir", command=lambda:self.open_fileExplorer(self.root, self.Entry_goFile))
        self.Button_goFile.grid(column=2, row=0, padx=5)
        
        #select files to convert
        self.Label_SelectFiles = ttk.Label(self.converter, text="Seleccionar archivos")
        self.Label_SelectFiles.grid(column=0, row=1, padx=5)
        self.Entry_SelectFiles = ttk.Entry(self.converter, justify="right", font=("Times New Roman", 8))
        self.Entry_SelectFiles.grid(column=1, row=1)
        self.Button_SelectFiles = ttk.Button(self.converter, text="Elegir", command=lambda:self.selector_files(self.root,self.Entry_SelectFiles))
        self.Button_SelectFiles.grid(column=2, row=1, padx=5)

        #name pdf
        self.label_name = ttk.Label(self.converter, text="Dale un nombre a tu pdf")
        self.label_name.grid(column=0, row= 2, padx=5)
        self.Entry_name = ttk.Entry(self.converter, font=("Times New Roman", 8))
        self.Entry_name.grid(column=1, row=2)
        
        #button to convert
        self.button_convert = ttk.Button(self.converter, text="Convertir", command=lambda: self.convert_to_PDF(self.Entry_name, self.Entry_goFile, self.Entry_SelectFiles))
        self.button_convert.grid(column=0, row=3, pady=5, padx=50)
        
        #clean button
        self.button_clean = ttk.Button(self.converter, text="Reiniciar", command=lambda: self.clean_all(self.Entry_name, self.Entry_goFile, self.Entry_SelectFiles))
        self.button_clean.grid(column=1, row=3, pady=5)

if __name__ == "__main__":
    ventanita = Window()