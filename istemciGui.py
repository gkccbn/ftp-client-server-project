import tkinter as tk
from tkinter import messagebox
from ftplib import FTP
from tkinter import simpledialog
ftp = FTP("")

def connect_ftp():
    hostname = entry_hostname.get()
    username = entry_username.get()
    password = entry_password.get()

    try:
        ftp.connect(hostname,3000)  
        ftp.login(username, password)
        messagebox.showinfo("Bağlantı Başarılı", "FTP Sunucusuna Bağlanıldı.")
        return ftp
    except Exception as e:
        messagebox.showerror("Bağlantı Hatası", str(e))
        return None

def download():
    if ftp:
        remote_path = simpledialog.askstring("","indirilecek dosyanin sunucudaki pathi: ")
        local_path = simpledialog.askstring("", "localde yükleneceği yerin pathi:: ")
        try:
            with open(remote_path, 'rb') as remote_file:
                file_name = remote_path.split('/')
                ftp.storbinary('STOR ' + local_path + file_name[-1], remote_file)
            messagebox.showinfo("Yükleme Başarılı", f"{local_path} dosyası başarıyla indirildi.")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", str(e))

def upload():
    if ftp:
        local_path = simpledialog.askstring("","yüklenecek dosyanin local pathi: ")
        remote_path = simpledialog.askstring("", "sunucuda yükleneceği yerin pathi:: ")
        try:
            with open(local_path, 'rb') as local_file:
                file_name = local_path.split('/')
                ftp.storbinary('STOR ' + remote_path + file_name[-1], local_file)
            messagebox.showinfo("Yükleme Başarılı", f"{local_path} dosyası başarıyla yüklendi.")
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", str(e))

def create_directory():
    if ftp:
        directory = simpledialog.askstring("","oluşturulacak dosyanın pathi: ")
        try:
            ftp.mkd(directory)
            messagebox.showinfo("Dizin Oluşturma Başarılı", f"{directory} dizini başarıyla oluşturuldu.")
        except Exception as e:
            messagebox.showerror("Dizin Oluşturma Hatası", str(e))

def delete_directory():
    if ftp:
        delete_directory = simpledialog.askstring("","silinecek dosyanın mevcut adı: ")
        try:
            ftp.delete(delete_directory)
            messagebox.showinfo("Dizin Silme Başarılı", f"{delete_directory} dizini başarıyla silindi.")
        except Exception as e:
            messagebox.showerror("Dizin Silme Hatası", str(e))

def rename_file():
    if ftp:
        old_name = simpledialog.askstring("","Değiştirilecek dosyanın mevcut adı: ")
        new_name = simpledialog.askstring("", "Yeni dosya adı: ")

        try:
            ftp.rename(old_name, new_name)
            messagebox.showinfo("Dosya Adı Değiştirme Başarılı", f"{old_name} dosyası başarıyla {new_name} olarak değiştirildi.")
        except Exception as e:
            messagebox.showerror("Dosya Adı Değiştirme Hatası", str(e))
def list_files():
    if ftp:
        try:
            files = ftp.nlst()
            messagebox.showinfo("Sunucu Dosyaları", "\n".join(files))
        except Exception as e:
            messagebox.showerror("Dosya Listeleme Hatası", str(e))

# Arayüzü oluştur
root = tk.Tk()
root.title("FTP İstemci")

frame_login = tk.Frame(root)
frame_login.pack()

label_hostname = tk.Label(frame_login, text="FTP Sunucu Adresi:")
label_hostname.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_hostname = tk.Entry(frame_login)
entry_hostname.grid(row=0, column=1, padx=5, pady=5)

label_username = tk.Label(frame_login, text="Kullanıcı Adı:")
label_username.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_username = tk.Entry(frame_login)
entry_username.grid(row=1, column=1, padx=5, pady=5)

label_password = tk.Label(frame_login, text="Şifre:")
label_password.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_password = tk.Entry(frame_login, show="*")
entry_password.grid(row=2, column=1, padx=5, pady=5)

button_connect = tk.Button(frame_login, text="Bağlan", command=connect_ftp)
button_connect.grid(row=3, columnspan=2, padx=5, pady=5)

frame_actions = tk.Frame(root)
frame_actions.pack()

button_download = tk.Button(frame_actions, text="Dosya İndir", command=download)
button_download.grid(row=0, column=0, padx=5, pady=5)

button_upload = tk.Button(frame_actions, text="Dosya Yükle", command=upload)
button_upload.grid(row=0, column=1, padx=5, pady=5)

button_create_dir = tk.Button(frame_actions, text="Dizin Oluştur", command=create_directory)
button_create_dir.grid(row=0, column=2, padx=5, pady=5)

button_delete_dir = tk.Button(frame_actions, text="Dizin Sil", command=delete_directory)
button_delete_dir.grid(row=0, column=3, padx=5, pady=5)

button_rename_file = tk.Button(frame_actions, text="Dosya Adı Değiştir", command=rename_file)
button_rename_file.grid(row=0, column=4, padx=5, pady=5)

button_list_files = tk.Button(frame_actions, text="Sunucu Dosyalarını Listele", command=list_files)
button_list_files.grid(row=0, column=5, padx=5, pady=5)

root.mainloop()
