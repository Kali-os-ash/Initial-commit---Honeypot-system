1. Install Dependencies

Run the following command to install required packages:

sudo apt update && sudo apt install python3 python3-pip sqlite3 iptables -y
pip3 install flask requests

-------------------------------------------------------------------------------------------------------------------------------------------

2. Create the Project Folder

mkdir ~/honeypot && cd ~/honeypot
------------------------------------------------------------------------------------------------------------------------------------------

3. Create the Honeypot Python Script

nano honeypot.py

Paste the following code inside and save (CTRL+X, then Y, then Enter):


which is in the python file you can copy it.

--------------------------------------------------------------------------------------------------------------------------------------------

4. Create the Fake Login Page

mkdir templates && nano templates/login.html

Paste the following HTML code and save (CTRL+X, then Y, then Enter):

which is also given in the folder you can copy it.
---------------------------------------------------------------------------------------------------------------------------------------------

5. Run the Honeypot

python3 honeypot.py

    Your honeypot will now be available at:
        http://127.0.0.1:8080 (Local)
        http://192.168.X.X:8080 (Network)

you can see that your honeypot is working properly and click on the link to see that it working properly or not .

--------------------------------------------------------------------------------------------------------------------------------------------------
6. Redirect SSH Traffic to the Honeypot

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-port 8080

Now, any SSH login attempts will be redirected to the honeypot.

----------------------------------------------------------------------------------------------------------------------------------------------------
View Captured Credentials

Check the log file:

cat honeypot.log

View credentials in SQLite:

sqlite3 honeypot.db "SELECT * FROM attacks;"


-------------------------------------------------------------------------------------------------------------------------------------------------------
