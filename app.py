from time import sleep
from tkinter import *
import paho.mqtt.client as mqtt
import sys


class AppFrame(Frame):
    def __init__(self, parent):
        super(AppFrame, self).__init__(parent)  # Set __init__ to the master class
        self.parent = parent
        self.client = mqtt.Client(self.parent.client_name)
        self.user = self.parent.username
        self.passw = self.parent.password
        self.connected = False
        self.broker_address = "pcfeib425t.vsb.cz"
        self.create_main()
        self.other_users = {"all": "online"}
        self.subscribe_topics = ["/mschat/all/#", "/mschat/status/#", f"/mschat/{self.parent.client_name}/#"]

    # def get_center(self, width, height):
    # screen_width = self.parent.winfo_screenwidth()
    # screen_height = self.parent.winfo_screenheight()
    # x_coordinate = (screen_width / 2) - (width / 2)
    # y_coordinate = (screen_height / 2) - (height / 2)
    # return width, height, x_coordinate, y_coordinate

    def send_message(self, source, destination):
        publish_topic = ""
        if destination == "all":
            publish_topic = f"/mschat/all/{source}"
        else:
            publish_topic = f"/mschat/user/{destination}/{source}"
        self.client.publish(publish_topic, payload=self.current_msg.get())
        self.msg_list.insert(END, f"{source} {self.current_msg.get()}")
        self.current_msg.set("")

    def create_message_frame(self, source=None, destination="all"):
        source = self.parent.client_name
        self.messages_frame = Frame(self.ctr_mid)
        self.current_msg = StringVar()  # For the messages to be sent.
        self.current_msg.set("Type your messages here.")
        self.scrollbar = Scrollbar(self.messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        self.msg_list = Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH)
        self.msg_list.pack(side=LEFT, fill=BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        self.entry_field = Entry(self, textvariable=self.current_msg)
        self.entry_field.bind("<Return>", lambda: self.send_message(source, destination))
        self.entry_field.pack()
        self.send_button = Button(self, text="Send", command=lambda: self.send_message(source, destination))
        self.send_button.pack()


    def login_success(self):
        self.login_success_screen = Toplevel(self)
        self.login_success_screen.title("Success")
        self.log_label = Label(self.login_success_screen, text=f"Connected to broker {self.broker_address}").pack()
        self.log_button = Button(self.login_success_screen, text="OK",
                                 command=lambda: self.delete_login_success()).pack()

    def failed_login(self):
        self.login_fail = Toplevel(self)
        self.login_fail.title("Login failed")
        # self.login_fail_screen.geometry("%dx%d+%d+%d" % self.get_center(self.width, self.height))
        self.log_fail_label = Label(self.login_fail, text=f"Failed connection with broker {self.broker_address}").pack()
        self.log_fail_button = Button(self.login_fail, text="Exit the program", command=self.delete_login_fail).pack()

    def delete_login_fail(self):
        self.login_fail.destroy()
        sys.exit()

    def delete_login_success(self):
        self.login_success_screen.destroy()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.login_success()
            self.connected = True  # Signal connection
            for topic in self.subscribe_topics:
                self.client.subscribe(topic)
            self.client.publish(f"/mschat/status/{self.parent.client_name}", payload="online", retain=True)
        else:
            print("Connection failed")
            self.failed_login()

    def on_disconnect(self, client, userdata, flags, rc):
        self.listbox_left.delete('0', 'end')
        if rc == 0:
            print("Client disconnected")

    def on_message(self, client, userdata, message):
        if r := re.match(rf"^(/mschat/status/)((?P<client_id>\w+)$)", message.topic):
            msg = str(message.payload.decode("utf-8"))
            client_id = r.groupdict().get("client_id")
            self.other_users[client_id] = msg
            self.listbox_left.delete('0', 'end')
            for user in self.other_users.items():
                self.listbox_left.insert(END, " - ".join(user))
            print(f"{client_id} {msg}")

        print("message received ", message)

    def logout(self):
        self.listbox_left.delete('0', 'end')
        self.parent.switch_frame("login", self)
        print('exiting')
        self.client.disconnect()
        self.client.loop_stop()

    def create_main(self):
        self.top_frame = Frame(self.parent, bg='lavender', width=450, height=50, pady=3)
        self.center = Frame(self.parent, bg='gray2', width=50, height=40, padx=3, pady=3)
        self.btm_frame = Frame(self.parent, bg='lavender', width=450, height=45, pady=3)

        # layout all of the main containers
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.top_frame.grid(row=0, sticky="ew")
        self.center.grid(row=1, sticky="nsew")
        self.btm_frame.grid(row=3, sticky="ew")

        # create the widgets for the top frame
        self.logout_btn = Button(self.top_frame, text="Logout", fg="black",
                                 command=self.logout)

        # layout the widgets in the top frame
        self.logout_btn.pack(side=RIGHT)
        # create the center widgets
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        self.ctr_left = Frame(self.center, bg='blue', width=250, height=190)
        self.ctr_mid = Frame(self.center, bg='yellow', width=500, height=190, padx=3, pady=3)

        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_mid.grid(row=0, column=1, sticky="nsew")

        self.listbox_left = Listbox(self.ctr_left)
        self.listbox_left.pack()

        self.client.username_pw_set(username=self.user, password=self.passw)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.will_set(f"/mschat/status/{self.parent.client_name}", payload="offline", retain=True)
        self.client.connect(self.broker_address, port=1883)  # connect to broker
        self.client.loop_start()
