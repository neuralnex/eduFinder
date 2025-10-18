#!/usr/bin/env python3

import subprocess
import time
import sys
import os
import json
from multiprocessing import Process

def start_agent(agent_file, delay=0):
    if delay > 0:
        time.sleep(delay)
    
    try:
        print(f"Starting {agent_file}...")
        subprocess.Popen([sys.executable, agent_file], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        print(f"{agent_file} started")
    except Exception as e:
        print(f"Failed to start {agent_file}: {e}")

def start_all_agents():
    """Start all EduFinder agents"""
    print("Starting EduFinder Multi-Agent System...")
    
    agents = [
        ("agents/curriculum_agent.py", 0),
        ("agents/materials_agent.py", 3),
        ("agents/enhanced_agent.py", 6),
        ("agent.py", 9)
    ]
    
    processes = []
    for agent_file, delay in agents:
        process = start_agent(agent_file, delay)
        if process:
            processes.append(process)
    
    print("All agents started!")
    return processes

def application(environ, start_response):
    """WSGI application for gunicorn"""
    # Start agents if not already running
    if not hasattr(application, 'agents_started'):
        application.processes = start_all_agents()
        application.agents_started = True
    
    # Simple health check endpoint
    status = '200 OK'
    headers = [('Content-type', 'application/json')]
    
    response = {
        "status": "EduFinder Multi-Agent System Running",
        "agents": {
            "main_agent": "agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne",
            "curriculum_agent": "agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8",
            "materials_agent": "agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf",
            "enhanced_agent": "agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4"
        },
        "ports": {
            "main_agent": 8000,
            "curriculum_agent": 8001,
            "materials_agent": 8002,
            "enhanced_agent": 8003
        },
    }
    
    response_body = json.dumps(response, indent=2)
    
    start_response(status, headers)
    return [response_body.encode()]

def main():
    """Main function for direct execution"""
    processes = start_all_agents()
    print("Press Ctrl+C to exit launcher")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Launcher closed. Agents continue running.")

if __name__ == "__main__":
    main()
