#!/usr/bin/env python3

import subprocess
import time
import sys
import os
import json
import signal
import atexit
import threading
from multiprocessing import Process

running_processes = []

def cleanup_processes():
    print("\nCleaning up processes...")
    for process in running_processes:
        if process and process.poll() is None:
            print(f"Terminating process {process.pid}")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"Force killing process {process.pid}")
                process.kill()
    print("Cleanup complete.")

def start_agent(agent_file, delay=0):
    if delay > 0:
        time.sleep(delay)
    
    try:
        print(f"Starting {agent_file}...")
        process = subprocess.Popen([sys.executable, agent_file], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)
        running_processes.append(process)
        print(f"{agent_file} started (PID: {process.pid})")
        
        def log_reader():
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"[{agent_file}] {line.rstrip()}")
        
        log_thread = threading.Thread(target=log_reader, daemon=True)
        log_thread.start()
        
        return process
    except Exception as e:
        print(f"Failed to start {agent_file}: {e}")
        return None

def start_all_agents():
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

def check_agent_health():
    healthy_agents = 0
    total_agents = len(running_processes)
    
    for i, process in enumerate(running_processes):
        if process and process.poll() is None:
            healthy_agents += 1
        else:
            print(f"Agent {i+1} is not running")
    
    return healthy_agents, total_agents

def application(environ, start_response):
    if not hasattr(application, 'agents_started'):
        application.processes = start_all_agents()
        application.agents_started = True
    
    path = environ.get('PATH_INFO', '/')
    
    if path == '/' or path == '':
        status = '200 OK'
        headers = [('Content-type', 'application/json')]
        
        healthy_agents, total_agents = check_agent_health()
        
        response = {
            "status": "EduFinder Multi-Agent System Running",
            "message": "Welcome to EduFinder! Your AI-powered learning companion with MeTTa Knowledge Graph.",
            "system_health": {
                "healthy_agents": healthy_agents,
                "total_agents": total_agents,
                "status": "healthy" if healthy_agents == total_agents else "degraded"
            },
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
            "profile_links": {
                "main_agent": "https://agentverse.ai/agents/details/agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne/profile",
                "curriculum_agent": "https://agentverse.ai/agents/details/agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8/profile",
                "materials_agent": "https://agentverse.ai/agents/details/agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf/profile",
                "enhanced_agent": "https://agentverse.ai/agents/details/agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4/profile"
            },
            "features": {
                "metta_knowledge_graph": "Dynamic concept analysis and unlimited domain support",
                "gemini_ai": "Advanced content generation and natural language understanding",
                "unlimited_domains": "Technology, Arts, Sciences, Languages, Life Skills, Business, and more"
            }
        }
        
        response_body = json.dumps(response, indent=2)
        start_response(status, headers)
        return [response_body.encode()]
    
    elif path == '/health':
        status = '200 OK'
        headers = [('Content-type', 'application/json')]
        
        healthy_agents, total_agents = check_agent_health()
        
        response = {
            "status": "healthy" if healthy_agents == total_agents else "degraded",
            "agents_running": healthy_agents,
            "total_agents": total_agents,
            "timestamp": time.time(),
            "metta_integration": "active",
            "unlimited_domains": True
        }
        
        response_body = json.dumps(response, indent=2)
        start_response(status, headers)
        return [response_body.encode()]
    
    elif path == '/stop':
        status = '200 OK'
        headers = [('Content-type', 'application/json')]
        
        cleanup_processes()
        
        response = {
            "status": "stopped",
            "message": "All agents have been stopped",
            "timestamp": time.time()
        }
        
        response_body = json.dumps(response, indent=2)
        start_response(status, headers)
        return [response_body.encode()]
    
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'application/json')]
        
        response = {
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": ["/", "/health", "/stop"]
        }
        
        response_body = json.dumps(response, indent=2)
        start_response(status, headers)
        return [response_body.encode()]

def main():
    atexit.register(cleanup_processes)
    
    def signal_handler(sig, frame):
        print("\nReceived interrupt signal. Cleaning up...")
        cleanup_processes()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    processes = start_all_agents()
    print("EduFinder Multi-Agent System is now ACTIVE!")
    print("All agents are running with live logs")
    print("MeTTa Knowledge Graph integration: ACTIVE")
    print("Unlimited domain support: ENABLED")
    
    try:
        while True:
            time.sleep(30)
            healthy_agents, total_agents = check_agent_health()
            if healthy_agents < total_agents:
                print(f"Warning: {total_agents - healthy_agents} agents are not running")
            else:
                print(f"All {total_agents} agents are healthy")
    except KeyboardInterrupt:
        print("\nStopping EduFinder Multi-Agent System...")
        cleanup_processes()
    except Exception as e:
        print(f"Unexpected error: {e}")
        cleanup_processes()
        sys.exit(1)

if __name__ == "__main__":
    main()