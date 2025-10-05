# Fly.io Distributed System Challenge

This repository contains my solutions and experiments for the **Fly.io Distributed Systems Challenges**, also known as the **Gossip Glomers** challenges.  
The challenges are designed to provide hands-on experience with building distributed systems concepts such as replication, fault tolerance, consistency, and coordination.
Challenge [Link](https://fly.io/dist-sys/1/)
---

## 📖 Overview

The challenges use [Maelstrom](https://github.com/jepsen-io/maelstrom), a distributed systems workbench created by Kyle Kingsbury (Jepsen).  
Maelstrom provides a simulated cluster environment, fault injection, and test harnesses to validate implementations against consistency and fault-tolerance models.

Each challenge requires building a small distributed system component in a programming language of your choice (here: **Python**).

---

## 🚀 Challenges Implemented

1. **Echo**  
   - Introduction to Maelstrom: build a node that echoes back received messages.

2. **Unique ID Generation**  
   - Ensure every request gets a globally unique ID across the cluster.

3. **Broadcast**  
   - Implement a gossip-based broadcast protocol for cluster-wide message delivery.

4. **Grow-Only Counter (G-Counter)**  
   - Design a CRDT-based counter that converges under concurrent updates.

5. **Kafka-Style Log**  
   - Implement a replicated log with partitioning and offset-based reads.

6. **Txn List-Key-Value Store**  
   - Build a transactional key-value store with linearizability guarantees.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Dependencies:** 
  - [maelstrom](https://github.com/jepsen-io/maelstrom) (binary required)
  - `asyncio` for event loop handling
  - `json` for message serialization
- **Testing:** Maelstrom workloads (e.g., `echo`, `broadcast`, `lin-kv`)

---


---

## ▶️ Running the Project

### 1. Install Maelstrom
Download and extract Maelstrom:

```bash
wget https://github.com/jepsen-io/maelstrom/releases/download/v0.2.3/maelstrom.tar.bz2
tar -xjf maelstrom.tar.bz2
```

./maelstrom/maelstrom test -w echo \
  --bin echo.py \
  --node-count 1 \
  --time-limit 10

Thanks to [](https://www.codyhiar.com/blog/reading-ddia-and-solving-gossip-glomers-in-python-part-1/)