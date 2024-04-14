# GlucoRAFT

GlucoRAFT is a Python implementation of the RAFT algorithm for running servers that connect Type 1 Diabetes (T1D) patient records with their endocrinologists, providing real-time Continuous Glucose Monitoring (CGM) updates. The project aims to simplify the implementation of RAFT's properties such as leader election, heartbeats, log updation, and replication, making it accessible for those interested in distributed systems and open-source contributions.

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/GlucoRAFT.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd GlucoRAFT/src/
   ```

3. **Run servers in different terminal windows:**

   ```bash
   python3 server.py 0 servers.txt
   python3 server.py 1 servers.txt
   python3 server.py 2 servers.txt
   python3 server.py 3 servers.txt
   python3 server.py 4 servers.txt
   ```

4. **Run the automated script to simulate CGM updates:**

   ```bash
   python3 random_cgm.py
   ```

5. **Use `client.py` to submit GET or PUT requests:**

   ```bash
   python3 client.py <ip> <key>
   python3 client.py <ip> <key> <value>
   ```

## Contributing

Contributions to GlucoRAFT are welcomed! Here are some ideas for contributions:

- Implement websockets to livestream data and visualize it in a dashboard using HTML and Flask.
- Extend `client.py` to support additional value fields such as percentage of hypo/hyper/in-range values, patient age, and other relevant patient information.
- Propose and implement your own optimizations or improvements to the codebase.

## References

- [RAFT Paper](https://raft.github.io/raft.pdf)
- [RAFT GitHub Page](https://raft.github.io)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
