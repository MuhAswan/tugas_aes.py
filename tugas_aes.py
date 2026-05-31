from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256
import os

def get_key(pwd):
    b_pwd = pwd.encode('utf-8')
    h_obj = SHA256.new(data=b_pwd)
    return h_obj.digest()

def enc_file(fpath, pwd):
    try:
        key = get_key(pwd)
        mode = AES.MODE_CBC
        cipher = AES.new(key, mode)
        
        with open(fpath, 'rb') as f:
            pt = f.read()
        
        bs = AES.block_size
        padded_pt = pad(pt, bs)
        ct = cipher.encrypt(padded_pt)
        
        out_f = fpath + ".enc"
        with open(out_f, 'wb') as f:
            f.write(cipher.iv)
            f.write(ct)
        print("[+] Sukses enkripsi!")
    except Exception as e:
        print("[-] Gagal:", e)

def dec_file(fpath, pwd, out_f):
    try:
        key = get_key(pwd)
        with open(fpath, 'rb') as f:
            iv = f.read(16)
            ct = f.read()
        
        mode = AES.MODE_CBC
        cipher = AES.new(key, mode, iv)
        
        pt_pad = cipher.decrypt(ct)
        bs = AES.block_size
        pt = unpad(pt_pad, bs)
        
        with open(out_f, 'wb') as f:
            f.write(pt)
        print("[+] Sukses dekripsi!")
    except Exception as e:
        print("[-] Gagal:", e)

if __name__ == "__main__":
    print("=== AES ===")
    print("1: Enkripsi, 2: Dekripsi")
    pil = input("Pilih: ")
    
    if pil == '1':
        f_in = input("Nama file: ")
        pwd = input("Password: ")
        
   
        if not os.path.exists(f_in):
            print(f"[!] Membuat file {f_in} otomatis...")
            with open(f_in, 'w') as f:
                f.write("Ini dokumen rahasia UTS Kriptografi Aswan.")
                
        enc_file(f_in, pwd)
            
    elif pil == '2':
        f_in = input("File .enc: ")
        f_out = input("Nama output: ")
        pwd = input("Password: ")
        if os.path.exists(f_in):
            dec_file(f_in, pwd, f_out)
        else:
            print("File tidak ada.")
