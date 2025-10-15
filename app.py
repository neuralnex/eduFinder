#!/usr/bin/env python3

import asyncio
import multiprocessing
import time
import signal
import sys
from typing import List

def run_agent(agent_name: str, port: int):
    """Run a specific agent"""
    print(f"Starting {agent_name} on port {port}...")
    
    if agent_name == "curriculum":
        from agents.curriculum_agent import curriculum_agent
        curriculum_agent.run()
    elif agent_name == "materials":
        from agents.materials_agent import materials_agent
        materials_agent.run()
    elif agent_name == "enhanced":
        from agents.enhanced_agent import enhanced_agent
        enhanced_agent.run()

def main():
    print("Learning Path Agents System")
    print("=" * 60)
    
    agents = [
        ("curriculum", 8001),
        ("materials", 8002),
        ("enhanced", 8003)
    ]
    
    processes = []
    
    # Start all agents
    for agent_name, port in agents:
        process = multiprocessing.Process(target=run_agent, args=(agent_name, port))
        process.start()
        processes.append(process)
        time.sleep(2)  # Stagger startup
    
    print("\nAll agents started successfully!")
    print("Agent Addresses:")
    print("- Curriculum Agent: agent1q... (port 8001)")
    print("- Materials Agent: agent1q... (port 8002)")
    print("- Enhanced Agent: agent1q... (port 8003)")
    print("\nPress Ctrl+C to stop all agents")
    
    def signal_handler(sig, frame):
        print("\nStopping all agents...")
        for process in processes:
            process.terminate()
            process.join()
        print("All agents stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
