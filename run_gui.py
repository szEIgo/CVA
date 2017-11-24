from tkinter import *


def main():
    root = Tk()
    root.title('CVA - Computer Vision App')
    root.minsize(width=450, height=450)
    root.maxsize(width=450, height=450)

    buttonStart = Button(root, text='Start')
    buttonStart.pack(fill=X)
    buttonSettings = Button(root, text='Settings')
    buttonSettings.pack(fill=X)

    settings = Tk()
    settings.title('CVA - Settings')
    settings.minsize(width=450, height=450)
    settings.maxsize(width=450, height=450)

    label_name = Label(settings, text='Name')
    label_source = Label(settings, text='Source')
    buttonAdd = Button(settings, text='add')
    entry_name = Entry(settings)
    entry_source = Entry(settings)

    label_name.grid(row=0)
    label_source.grid(row=1)
    entry_name.grid(row=0, column=1)
    entry_source.grid(row=1, column=1)
    buttonAdd.grid(columnspan=2)





    root.mainloop()


if __name__ == '__main__':
    main()
