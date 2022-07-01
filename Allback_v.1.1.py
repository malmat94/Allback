import shutil
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import time
import datetime

root = Tk()
root.title('AutoBackup for Allplan')
root.geometry('600x300')

c = Canvas(root, height=500, width=1500)
c.place(relwidth=1, relheight=1)

class PathUtil:

    def __init__(self):
        pass


class Backup:

    def __init__(self, load_path="", save_path="", factor=5, interval=5, counter = 0, overall = 0):
        self.load_path = load_path
        self.save_path = save_path
        self.factor = factor     # factor used to compensate saving time, prevents to skip files saving
        self.interval = interval
        self.counter = counter
        self.overall = overall

    def search_file(self):
        pass

    def should_be_copied(self, file, interval, project):
        """
        Return True if input file was edited since last backup, otherwise return false
        """
        print("checking file: " + str(file) + "    from project:" + str(project)[4:10] + ",   current time: " + str(datetime.datetime.now())[11:19])
        path = self.load_path + "\\" + project
        factor = int(self.factor)

        file_path = str(path + "\\" + file)
        current_day = str(datetime.datetime.now())[0:10]
        current_hour = str(datetime.datetime.now())[11:13]
        current_minute = str(datetime.datetime.now())[14:16]
        current_time_in_minutes = int(current_hour) * 60 + int(current_minute)

        file_mod_day = str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))[0:10]
        file_mod_hour = str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))[11:13]
        file_mod_minute = str(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))[14:16]
        file_mod_time_in_minutes = int(file_mod_hour) * 60 + int(file_mod_minute)

        if file_mod_time_in_minutes > current_time_in_minutes - interval - factor and current_day == file_mod_day:
            print('allowed, copying in progress ...')
            self.counter += 1
            self.overall += 1
            return True
        else:
            print('rejected')
            return False

    def target_path(self):
        """
        Open choose save directory dialog window, return save path
        """

        file_path = filedialog.askdirectory()
        save_path = str(file_path)

        target_label = Label(c, text='Kopiuję do:     \n' + str(file_path))
        target_label.pack()
        target_label.place(relwidth=1, relheight=0.1, rely=0.88)

        self.save_path = save_path

    def source_path(self):
        """
        Open choose save directory dialog window, return save path
        """

        load_path = filedialog.askdirectory()

        SourceLabel = Label(c, text='Kopiuję z:     \n' + str(load_path))
        SourceLabel.pack()
        SourceLabel.place(relwidth=1, relheight=0.1, rely=0.75)

        self.load_path = load_path

    def do_backup(self, ndw_file, project_name):
        day_folder = str(datetime.datetime.now())[0:10]
        ndw_name = str(ndw_file)
        file_path = str(self.load_path + "\\" + project_name + "\\" + ndw_name)

        save_path = str(self.save_path + "\\" + project_name +"\\" + day_folder + "\\" + ndw_name)
        if not os.path.exists(save_path):
            new_directory = str(os.makedirs(save_path))
        current_time = "h" + str(datetime.datetime.now())[11:13] + "m" + str(datetime.datetime.now())[14:16] + "_"

        GetFile = shutil.copy(file_path, save_path)
        os.rename(save_path + "\\" + ndw_name, str(self.save_path + "\\" + project_name  + "\\" + day_folder + "\\" + ndw_name + "\\" + current_time + ndw_name))

    def main_process(self):

        load_path = self.load_path
        while True:
            dir_list = [f for f in os.listdir(load_path)]
            project_dir_list = []
            for file in dir_list:
                self.get_only_projects(file, project_dir_list)

            for project in project_dir_list:
                project_load_path = load_path + "\\" + project

                file_list = [f for f in os.listdir(project_load_path) if os.path.isfile(os.path.join(project_load_path, f))]

                for f in file_list:
                    if str(f)[-3:] == "ndw" or str(f)[-3:] == "npl":
                        if self.interval == 'Wybierz interwał zapisu':
                            
                            return

                        else:
                            if self.interval == '5 minut':
                                if self.should_be_copied(f, 5, project):
                                    self.do_backup(f, project)
                            elif self.interval == '15 minut':
                                if self.should_be_copied(f, 15, project):
                                    self.do_backup(f, project)
                            elif self.interval == '30 minut':
                                if self.should_be_copied(f, 30, project):
                                    self.do_backup(f, project)
                            elif self.interval == '1 godzina':
                                if self.should_be_copied(f, 60, project):
                                    self.do_backup(f, project)

            breaktime = str(datetime.datetime.now())[0:16]
            if self.interval == '5 minut':
                print("BREAK on time:  " + breaktime + " "*10 + str(self.counter) + " files was copied." + " Files from start: " + str(self.overall))
                self.counter = 0
                time.sleep(300)
            elif self.interval == '15 minut':
                print("BREAK on time:  " + breaktime + " "*10 + str(self.counter) + "  files was copied." + " Files from start: " + str(self.overall))
                self.counter = 0
                time.sleep(600)
            elif self.interval == '30 minut':
                print("BREAK on time:  " + breaktime + " "*10 + str(self.counter) + "  files was copied." + " Files from start: " + str(self.overall))
                self.counter = 0
                time.sleep(1800)
            elif self.interval == '1 godzina':
                print("BREAK on time:  " + breaktime + " "*10 + str(self.counter) + "  files was copied." + " Files from start: " + str(self.overall))
                self.counter = 0
                time.sleep(3600)
            else:
                break


    def get_only_projects(self, file, project_dir_list):
        """
        Checks whether given file is a project directory, if it is, appends it to project_dir_list
        """
        try:
            x = int(file[0:4])
            project_dir_list.append(file)
        except:
            print("cant do that")
            x = file[0:4]

    def graphic_interface(self):

        n = StringVar()
        delay = ttk.Combobox(c, width=27, font='calibri', textvariable=n)
        delay.pack()
        delay.place(relwidth=1, relheight=0.2, rely=0)

        # global choose
        # Delay.bind("Wybierz interwał zapisu", choose = 0)

        # Adding combobox drop down list
        delay['values'] = ('Wybierz interwał zapisu', '5 minut', '15 minut', '30 minut', '1 godzina')
        delay.current(3)

        target_path = Button(c, text='Dokąd kopiować?', font='calibri', border=5, command=self.target_path)
        target_path.place(relwidth=1, relheight=0.2, rely=0.4)

        source_path = Button(c, text='Skąd kopiować?', font='calibri', border=5, command=self.source_path)
        source_path.pack()
        source_path.place(relwidth=1, relheight=0.2, rely=0.2)

        # testowy = Button(c,text='GetFiles', command=GetFiles)
        # testowy.pack()

        def check_data():
            self.interval = n.get()
            if self.interval == 'Wybierz interwał zapisu':
                messagebox.showinfo("Info", n.get())
                return
            if self.load_path == '':
                messagebox.showinfo("Info", "Wybierz lokalizację projektu, dla którego wykanać backup")
                return
            if self.save_path == '':
                messagebox.showinfo("Info", "Wybierz lokalizację, w której zapisać backup")
                return

        backup = Button(c, text='ROZPOCZNIJ', font='calibri', border=5, command=lambda: [check_data(), self.main_process()])
        backup.pack()
        backup.place(relwidth=1, relheight=0.2, rely=0.6)
        #
        root.mainloop()


x = Backup()
x.graphic_interface()

print(str(datetime.datetime.now())[0:10])

# str(datetime.datetime.now()) [0:10]   --> YEAR-MONTH-DAY
# str(datetime.datetime.now()) [11:13]  --> HOUR
# str(datetime.datetime.now()) [14:16]  --> MINUTE
