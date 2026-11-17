from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None

    if request.method == "POST":
        router_device = {
            'device_type': 'cisco_ios_telnet',
            'ip': '192.168.10.108',
            'port': 32770,
            'username': 'admin',
            'password': 'eve123',
            'secret': 'eve123',
        }

        commands_to_run = [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]

        try:
            # Connect to the router
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()


            # Run commands and store outputs in a dictionary
            for cmd in commands_to_run:
                output = net_connect.send_command(cmd)
                results[cmd] = output

            net_connect.disconnect()
        except Exception as e:

            error = f"Connection failed: {e}"

    return render_template("index.html", results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)