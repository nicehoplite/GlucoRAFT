
# GlucoRAFT
GlucoRAFT uses the RAFT algorithm to run servers for connecting T1D patient records and their endocrinologist with real time CGM updates. 
If you want more context to this repo, here's my Medium article that explains RAFT and why this repo exists.

I aim to model the RAFT algorithm's properties - leader elections, heartbeats, log updation and replication in a very simple skeletal as closely as possible in Python...sigh global interpreter lock say hi :) The implementation has been simplified here for open sourcing using a "fake patient" - a python client script acting as our CGM user emitting random physiological readings every 5 seconds which is recieved by our servers through PUT requests. The client side of the doctor primarily issues GET requests to retrieve existing patient data by searching up their name.

This is an effort to help anyone starting with RAFT,Distributed Systems or Open Source contributions in general and most of it is open ended so that PRs can be raised by people reading/practicing this.

You can get started by first running the servers in different terminal windows.
python3 server.py 0 servers.txt

Any contributions are welcome! I am actively working on this and will accept contributions within 1-2 days. Some possible contributions include:
TODO: Creating websockets to livesteam the script and show it in a dashboard (HTML + Flask)
TODO: Extend client.py to send more value fields (percentage of hypo/hyper/in range, age and other patient related information)
Feel free to propose your own changes or optimize the code!

Here's where you can find the original RAFT paper and github.io page for your reference.

https://raft.github.io/raft.pdf
https://raft.github.io
