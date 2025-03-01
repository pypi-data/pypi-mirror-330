# 🚀 How to Set Up OpenSSH on Windows and Linux  

Follow these simple steps to install and configure OpenSSH on your system, whether you're using Windows or Linux.  

---

## 🖥️ Setting Up OpenSSH on Windows  

### **Step 1: Install OpenSSH**  
1. Open **Settings** and search for **"Add Optional Features"**.  
2. Click **Add Features**.  
3. Install **OpenSSH Server** and **OpenSSH Client**.  

---

### **Step 2: Start OpenSSH Services**  
Run the following commands in **PowerShell**:  
```powershell
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```  

---

### **Step 3: Customize the SSH Port (Optional)**  
1. Open the configuration file:  
   ```
   C:\ProgramData\ssh\sshd_config
   ```
2. Locate the line `#Port 22`.  
3. Uncomment it by removing `#` and change `22` to your preferred port:  
   ```
   Port <your_custom_port>
   ```
   
---

### **Step 4: Restart OpenSSH Service**  
Run these commands in **PowerShell (Admin Mode)**:  
```powershell
net stop sshd
net start sshd
```  

---

### **Step 5: Restart OpenSSH via Services**  
1. Press `Win + R`, type `services.msc`, and press **Enter**.  
2. Find **OpenSSH Server**, right-click it, and select **Restart**.  

---

### 🎉 **Success!**  
OpenSSH is now set up and running on your Windows machine. You can start connecting via SSH! 🚀  

---

## 🐧 Setting Up OpenSSH on Linux  

### **Step 1: Check if OpenSSH is Installed**  
Run the following command:  
```bash
sudo systemctl status ssh
```  
If OpenSSH is not installed, install it with:  
```bash
sudo apt install openssh-server
```  

---

### **Step 2: Allow SSH in the Firewall (Default Port: 22)**  
```bash
sudo ufw allow 22/tcp
```  

---

### **Step 3: Verify Open Ports**  
Check if SSH is listening on the correct port:  
```bash
sudo netstat -tulnp
```  

---

### 🎉 **You're All Set!**  
Your Linux system is now ready to accept SSH connections. Start exploring securely! 🌍✨  
