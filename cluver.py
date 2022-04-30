import sys
import os
import pwd

import json
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from prettytable import PrettyTable

banner = """
██████████████████████████████████████
█─▄▄▄─█▄─▄███▄─██─▄█▄─█─▄█▄─▄▄─█▄─▄▄▀█
█─███▀██─██▀██─██─███▄▀▄███─▄█▀██─▄─▄█
▀▄▄▄▄▄▀▄▄▄▄▄▀▀▄▄▄▄▀▀▀▀▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀

Author: Fsoky
GitHub: https://github.com/Fsoky

Tool for send letter to email v1.0
~> help - get a reference
"""
print(banner)

uname = pwd.getpwuid(os.getuid()).pw_name
opts_path = f"/home/{uname}/.cluver-config.json"
temp_path = f"{os.getcwd()}/.temp-cluver-config.json"

opts = {
    "email": "",
    "passwd": ""
}
temp_opts = {
    "mode": "text",
    "html-file": "",
    "attachment": "",
    "subject": "Click Me Please",
    "message": "Just be happy.",
    "url": "smtp.gmail.com:587",
    "toaddr": ""
}
opts_help = {
    "help": "Show this message",
    "constructor": "Create your own letter. step by step",
    "attachment": "Pin attachment to letter",
    "mode": "html / text (default: text)",
    "html-file": "HTML doc for letter instead of text",
    "email": "Set your email address (email example@gmail.com)",
    "passwd": "Set password of your email address (passwd 12345)",
    "subject": "Subject for letter (default: click me please)",
    "message": "Message for letter if mode is text (default: just be happy)",
    "send": "Send a letter",
    "exit": "End the script",
    "clear": "Clear screen",
    "url": "Server url (default: smtp.gmail.com:587)",
    "toaddr": "Which address will be send message",
    "show": "Show value of option (example: show email)"
}

if not os.path.exists(opts_path):
    with open(opts_path, "w") as setfile:
        json.dump(opts, setfile)

with open(temp_path, "w") as tempfile:
    json.dump(temp_opts, tempfile)


def cmd_help():
    table = PrettyTable(["Option", "Description"])
    table.align = "l"

    for opt in opts_help:
        table.add_row([str(opt), opts_help[opt]])
    print(table)


def write_new_values(value, opt):
    with open(opts_path, "r", encoding="utf-8") as stfile:
        settings = json.load(stfile)
    settings[opt] = value

    with open(opts_path, "w", encoding="utf-8") as file:
        json.dump(settings, file)


def write_new_temp_values(value, opt):
    with open(temp_path, "r", encoding="utf-8") as stfile:
        settings = json.load(stfile)
    settings[opt] = value

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(settings, file)


def constructor():
    banner = "[constructor]"

    email = input(f"{banner} email ~> ")
    password = input(f"{banner} password ~> ")
    url = input(f"{banner} url (smtp.gmail.com) ~> ")
    port = input(f"{banner} port (587) ~> ")
    toaddr = input(f"{banner} to (address) ~> ")
    subject = input(f"{banner} subject ~> ")
    message = input(f"{banner} message ~> ")

    accept_act = input(f"{banner} Everything is ready, do you want send a letter? (y/n): ")
    if accept_act == "y":
        server = smtplib.SMTP(["smtp.gmail.com" if len(re.findall(r"[a-z]+.[a-z]+.[a-z]+", url)) == 0 else url], [587 if port is None else port])
        server.starttls()

        try:
            server.login(email, password)
            msg = MIMEText(message)
            msg["Subject"] = subject
            server.sendmail(email, toaddr, msg.as_string())
        except Exception as e:
            print("Error", e)
    else:
        print("\n")
        main()


def send_letter():
    opts = json.load(open(opts_path, "r", encoding="utf-8"))
    temp_opts = json.load(open(temp_path, "r", encoding="utf-8"))
        
    for topt in temp_opts:
        print(f"{topt} => {temp_opts[topt]}")

    print("\nMake sure everything is correct. If not you need rewrite some options")
    ans = input("Send? y/n: ")

    if ans == "y":
        url, port = temp_opts["url"].split(":")
        server = smtplib.SMTP(url, int(port))
        server.starttls()

        try:
            server.login(opts["email"], opts["passwd"])
            msg = MIMEText(temp_opts["message"])
            msg["Subject"] = temp_opts["subject"]
            msg["From"] = opts["email"]
            msg["To"] = temp_opts["toaddr"]

            if temp_opts["mode"] != "text":
                try:
                    with open(temp_opts["html-file"], "r", encoding="utf-8") as file:
                        template = file.read()
                    msg = MIMEText(template, "html")
                except IOError:
                    print("The template file doesn't found!")

            server.sendmail(opts["email"], temp_opts["toaddr"])
        except Exception as e:
            print("Error", e)


def main():
    while True:
        ui = input(f"~> ")
        save_cmd_list = ["email", "passwd"]
        temp_cmd_list = ["mode", "html-file", "attachment", "message", "subject", "url", "toaddr"]

        try:
            if ui == "help":
                cmd_help()
            elif ui == "exit":
                os.remove(temp_path)
                sys.exit()
            elif ui == "clear":
                os.system("clear")
            elif ui == "constructor":
                constructor()
            elif ui == "send":
                send_letter()
            elif "show" in ui:
                account_opts = open(opts_path, "r", encoding="utf-8")
                _temp_opts = open(temp_path, "r", encoding="utf-8")
                all_options = json.load(account_opts) | json.load(_temp_opts)

                for aopt in all_options:
                    if ui.split()[1] == aopt:
                        print(f"{aopt} => {all_options[aopt]}")

                account_opts.close()
                _temp_opts.close()
            else:
                for scmd in save_cmd_list:
                    if scmd in ui:
                        opt, value = ui.split()
                        write_new_values(value, opt)
                    else:
                        for tcmd in temp_cmd_list:
                            if tcmd in ui:
                                opt, value = ui.split()
                                write_new_temp_values(value, opt)
        except ValueError:
            print(f"The second argument needed\n{opts_help[ui]}\n")
        except IndexError:
            print(f"The second argument needed\n{opts_help[ui]}\n")


if __name__ == '__main__':
    main()
