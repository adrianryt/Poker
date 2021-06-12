# Poker
Authors: Mateusz Pieróg, Adrian Ryt

This project is a desktop aplication enabling you to play Poker online with friends. We did it as a project for our python course at AGH.

## How to play
First run this command:

    pip install -r requirements.txt

By default server starts on local IP address, you can change server IP in line 12 in server.py
    
    SERVER = "192.168.65.128"

You can also configure small blind and start tokens in server.py

When the server starts running, you are asked to input number of players in the console

![server_screen](https://user-images.githubusercontent.com/72470330/121773796-8b667e80-cb7e-11eb-9bff-3e4846836b0e.png)

After that you need to configure line 11 in client.py - copy there your server's IP.
Then you have to launch clients and give you name.
![login_client](https://user-images.githubusercontent.com/72470330/121773925-7ccc9700-cb7f-11eb-90ea-b8c90f8bfa95.png)
When all the players are connected the game stars:

![table](https://user-images.githubusercontent.com/72470330/121774104-dd100880-cb80-11eb-862b-81554458c727.png)


<b>Adrian Ryt</b><br> 
The project turned out to be quite time consuming due to many specific rules in Poker. Project taught me that making a good scheme before writing the code is very important and helpful.
My skills in python has expanded, I learned about client - server conenction, pickles and threads.
Overall, the project was very fun to write, python is very friendly language and the documentation in great.

Mateusz Pieróg:
