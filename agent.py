#!/usr/bin/env python3

import asyncio
import multiprocessing
import time
import signal
import sys
import os
from typing import List

from curriculum_agent import agent as curriculum_agent
from materials_agent import materials_agent
from enhanced_curriculum_agent import enhanced_agent
from metta_integration import MeTTaKnowledgeGraph

class LearningPathSystem:
    def __init__(self):
        self.agents = {
            "curriculum": curriculum_agent,
            "materials": materials_agent,
            "enhanced": enhanced_agent
        }
        self.processes = []
        self.running = False
    
    def start_agent(self, agent_name: str, agent_instance):
        print(f"Starting {agent_name} agent...")
        try:
            agent_instance.run()
        except Exception as e:
            print(f"Error starting {agent_name} agent: {e}")
    
    def start_all_agents(self):
        print("Learning Path Agents System")
        print("=" * 50)
        
        for name, agent in self.agents.items():
            process = multiprocessing.Process(
                target=self.start_agent,
                args=(name, agent)
            )
            process.start()
            self.processes.append(process)
            print(f"Started {name} agent (PID: {process.pid})")
            time.sleep(2)
        
        self.running = True
        print("\nAll agents started successfully!")
        print("\nAgent Addresses:")
        print(f"Curriculum Agent: {curriculum_agent.address}")
        print(f"Materials Agent: {materials_agent.address}")
        print(f"Enhanced Agent: {enhanced_agent.address}")
        
        print("\nSystem Status: RUNNING")
        print("Press Ctrl+C to stop all agents")
    
    def stop_all_agents(self):
        print("\nStopping all agents...")
        self.running = False
        
        for process in self.processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
                print(f"Stopped agent (PID: {process.pid})")
        
        print("All agents stopped.")
    
    def test_system(self):
        print("\nTesting system components...")
        
        try:
            print("Testing MeTTa integration...")
            async def test_metta():
                async with MeTTaKnowledgeGraph() as metta:
                    result = await metta.query_learning_concepts("ai_engineering", "machine_learning")
                    print(f"MeTTa test result: {result.get('concept', 'Unknown')}")
            
            asyncio.run(test_metta())
            print("MeTTa integration: OK")
            
        except Exception as e:
            print(f"MeTTa test failed: {e}")
        
        try:
            print("Testing YouTube integration...")
            from youtubesearchpython import VideosSearch
            videosSearch = VideosSearch("machine learning", limit=1)
            results = videosSearch.result()
            if results.get('result'):
                print("YouTube integration: OK")
            else:
                print("YouTube integration: Failed")
        except Exception as e:
            print(f"YouTube test failed: {e}")
        
        print("System test completed.")
    
    def show_status(self):
        print("\nSystem Status:")
        print("-" * 30)
        
        for i, process in enumerate(self.processes):
            status = "RUNNING" if process.is_alive() else "STOPPED"
            agent_name = list(self.agents.keys())[i]
            print(f"{agent_name.capitalize()} Agent: {status} (PID: {process.pid})")
        
        print(f"\nOverall Status: {'RUNNING' if self.running else 'STOPPED'}")
    
    def show_help(self):
        print("\nLearning Path Agents System - Help")
        print("=" * 40)
        print("Commands:")
        print("  start    - Start all agents")
        print("  stop     - Stop all agents")
        print("  restart  - Restart all agents")
        print("  status   - Show system status")
        print("  test     - Test system components")
        print("  help     - Show this help")
        print("  quit     - Exit the system")
        print("\nAgent Capabilities:")
        print("  Curriculum Agent  - Creates structured learning paths")
        print("  Materials Agent   - Discovers educational resources")
        print("  Enhanced Agent    - Provides deep insights via MeTTa")
        print("\nUsage:")
        print("  python agent.py start    # Start the system")
        print("  python agent.py test     # Test components")
        print("  python agent.py status   # Check status")

def signal_handler(signum, frame):
    print("\nReceived interrupt signal. Stopping system...")
    if hasattr(signal_handler, 'system'):
        signal_handler.system.stop_all_agents()
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print("Learning Path Agents System")
        print("Usage: python agent.py <command>")
        print("Commands: start, stop, restart, status, test, help, quit")
        print("Run 'python agent.py help' for detailed information")
        return
    
    command = sys.argv[1].lower()
    system = LearningPathSystem()
    signal_handler.system = system
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if command == "start":
        system.start_all_agents()
        try:
            while system.running:
                time.sleep(1)
        except KeyboardInterrupt:
            system.stop_all_agents()
    
    elif command == "stop":
        system.stop_all_agents()
    
    elif command == "restart":
        system.stop_all_agents()
        time.sleep(2)
        system.start_all_agents()
        try:
            while system.running:
                time.sleep(1)
        except KeyboardInterrupt:
            system.stop_all_agents()
    
    elif command == "status":
        system.show_status()
    
    elif command == "test":
        system.test_system()
    
    elif command == "help":
        system.show_help()
    
    elif command == "quit":
        print("Exiting system...")
        sys.exit(0)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: start, stop, restart, status, test, help, quit")

if __name__ == "__main__":
    main()
