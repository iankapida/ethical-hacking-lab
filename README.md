# Full-Stack Python Ethical Hacking & Telemetry Analysis Lab

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Focus-Red%20%2F%20Blue%20Team-red.svg)]()
[![Platform](https://img.shields.io/badge/Environment-Linux%20%2F%20Termux-brightgreen.svg)]()

## 📌 Executive Summary

This repository contains a lightweight, modular ethical hacking and security telemetry pipeline built from scratch in Python. Designed to demonstrate end-to-end cyber operations, the lab covers offensive attack techniques—such as TCP port reconnaissance, web endpoint fuzzing, and multi-threaded Command-and-Control (C2) session handling—alongside defensive Security Operations Center (SOC) log correlation and threat detection.

---

## 🏗️ Core Architecture & Modules

### 🔴 Red Team (Offensive Modules)
* **`recon_toolkit.py`**: A multi-threaded TCP port scanner designed for network host discovery, service enumeration, and open port identification.
* **`web_fuzzer.py`**: An automated HTTP directory and endpoint brute-forcing tool that tests for hidden sensitive paths (`.env`, `robots.txt`, admin panels) and exports structured JSON findings (`fuzz_report.json`).
* **`c2_simulator.py`**: A concurrent multi-threaded TCP listener simulating Command-and-Control infrastructure, featuring socket management and agent session persistence.

### 🔵 Blue Team (Defensive & Telemetry Modules)
* **`detect_recon.py`**: A SOC telemetry parser that ingests web access logs (`attack_telemetry.log`), correlates HTTP status codes, and alerts on anomalous enumeration scans and sensitive file exposure (`.env`).

---

## 💻 Tech Stack & Environment

* **Language:** Python 3 (Standard Library: `socket`, `threading`, `json`, `sys`, `os`, `datetime`)
* **Environment:** Linux / Termux terminal environment
* **Formats:** JSON reports, standard W3C access logs, Git version control

---

## ⚡ Quick Start & Usage

### 1. Network Reconnaissance (Port Scanning)
```bash
python3 recon_toolkit.py 127.0.0.1
