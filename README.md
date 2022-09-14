# Automated API-based bot to scan telegram's channel's posts

## Project Descriptions
I saw a time-consuming void in constantly checking channels to get new posts about programming, finance, and even News.
Eventually, I decided to create this API-based bot to run over the telegram account(in this case, my telegram account), check channels that I select, and forward them based on unique keywords to the target channel that the bot admin can.

In this project, I used the **telethon** library in *python3* and **dockerize** them so I could run it on my server without any conflict with my other projects

## How to Run Project
1. ### Prerequisites & Dependencies
    For running this project, you must have these dependencies installed and ready to use:
    * docker
    * docker-compose
    * python3

2. ### Config & Run
    after cloning this project, you have to create a `.env` file in the *root* of the project (where *Dockerfile* is) and then put these lines of code to it with the credentials that give to you when you login into this link(its telegram official page) and find your `api_id` and `api_hash` To find your_id you can go to the telegram account that you want to be your bot's admin, then start this bot `@userinfobot`, and it will send you your id:

        TEL_ID=your_api_id
        TEL_HASH='your_hash_id'
        BOT_ADMIN=your_id

    Before you run this on docker, you must create your session file(it looks like `main.session`) based on your credentials; to do so, you must run the script I wrote for an easy install.
    
    For easy installation, you have to run this command that you see below:

        python3 -m venv venv
        pip install -r localReq.txt
        python3 createSession.py
        ctrl+c (to close python file)
    
    If you run into any problems, feel free to contact me; otherwise, you will see something like the screenshot I provided below:

    ![login for create main.session ](/sc/login.png)
    
    =
    After you complete these steps, in your project root, you can find `main.session` file after that, you can run the project on docker with the commands below:

        docker-compose -f docker-compose-deploy.yml build
        docker-compose -f docker-compose-deploy.yml up

3. ### Usage
    There are several commands to configure the bot.
    
    You have to send them to the bot account.
    
    The list of commands comes below:

    | ID | Command | Job |
    | :-------------:| :-------------: | :------------- |
    |1| `Hello` | test to check bot works correctly |
    |2| `:add ch:` | add channels for listening to it |
    |3| `:rem ch:` | remove channels from list of listening|
    |4| `:list ch:` | show the list of channels |
    |5| `:add key:` | add keywords |
    |6| `:rem key:` | remove keywords |
    |7| `:list key:` | show the list of keywords |
    |8| `:add target:` | add or update target channel that post forward to it |

    To use command **2,3,5,6** you must put the command in the first line. Then for every link or keyword, you must put every one of those in one line like the snippet below: 

        :add ch:
        @test
        t.me/test
        https://t.me/test

4. ### Screenshots
    ![login for create main.session ](/sc/01.jpeg)

    ![login for create main.session ](/sc/02.jpeg)
    
    ![login for create main.session ](/sc/03.jpeg)

