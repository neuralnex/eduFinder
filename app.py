import asyncio
import multiprocessing
import time
import os
from typing import Dict, List, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import subprocess
import signal
import sys

app = FastAPI(
    title="EduFinder Multi-Agent System",
    description="AI-powered learning path system with specialized agents",
    version="2.0.0"
)

class AgentStatus(BaseModel):
    name: str
    address: str
    port: int
    status: str
    agentverse_url: str

class SystemStatus(BaseModel):
    status: str
    agents: List[AgentStatus]
    total_agents: int
    active_agents: int

agent_processes = {}
agent_addresses = {
    "curriculum": "agent1q2t29q262rsp660k727g3nhejn2sftdesfrc4k6dttydwzs2nsp2ypfzww8",
    "materials": "agent1qdq2ynx5e5qcyyhnzzr4cmvpg4wufvqskqp2dl9nldm9w7da6lvysdxwnuf", 
    "enhanced": "agent1qdeqahn3pr4ta7zxgtwee5ts0klrkeh30an7wmsdhagsfyy28udtqs2tsk4",
    "main": "agent1q2ygnhcc5xj3davnvu0g0p0qytuyc7dsz8dh538ks49y7sru5t9skwn5gne"
}

agent_ports = {
    "curriculum": 8001,
    "materials": 8002,
    "enhanced": 8003,
    "main": 8000
}

def start_agent(agent_name: str, delay: int = 0):
    """Start a specific agent with delay"""
    time.sleep(delay)
    try:
        if agent_name == "main":
            process = subprocess.Popen([
                sys.executable, "agent.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            process = subprocess.Popen([
                sys.executable, f"agents/{agent_name}_agent.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        agent_processes[agent_name] = process
        print(f"Started {agent_name} agent with PID {process.pid}")
    except Exception as e:
        print(f"Failed to start {agent_name} agent: {e}")

def start_all_agents():
    """Start all agents in sequence"""
    print("Starting EduFinder Multi-Agent System...")
    
    processes = []
    
    processes.append(multiprocessing.Process(target=start_agent, args=("curriculum", 0)))
    processes.append(multiprocessing.Process(target=start_agent, args=("materials", 3)))
    processes.append(multiprocessing.Process(target=start_agent, args=("enhanced", 6)))
    processes.append(multiprocessing.Process(target=start_agent, args=("main", 9)))
    
    for process in processes:
        process.start()
    
    for process in processes:
        process.join()
    
    print("All agents started successfully!")

def stop_all_agents():
    """Stop all running agents"""
    print("Stopping all agents...")
    for agent_name, process in agent_processes.items():
        try:
            process.terminate()
            process.wait(timeout=5)
            print(f"Stopped {agent_name} agent")
        except Exception as e:
            print(f"Error stopping {agent_name} agent: {e}")
    agent_processes.clear()

@app.on_event("startup")
async def startup_event():
    """Start all agents when the FastAPI app starts"""
    print("🚀 Starting EduFinder Multi-Agent System...")
    start_all_agents()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop all agents when the FastAPI app shuts down"""
    print("🛑 Shutting down EduFinder Multi-Agent System...")
    stop_all_agents()

@app.get("/")
async def root():
    """Main API endpoint with system information"""
    return {
        "name": "EduFinder Multi-Agent System",
        "version": "2.0.0",
        "description": "AI-powered learning path system with specialized agents",
        "status": "running",
        "agents": {
            "curriculum": {
                "name": "Curriculum Agent",
                "address": agent_addresses["curriculum"],
                "port": agent_ports["curriculum"],
                "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['curriculum']}&address={agent_addresses['curriculum']}"
            },
            "materials": {
                "name": "Materials Agent",
                "address": agent_addresses["materials"],
                "port": agent_ports["materials"],
                "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['materials']}&address={agent_addresses['materials']}"
            },
            "enhanced": {
                "name": "Enhanced Agent",
                "address": agent_addresses["enhanced"],
                "port": agent_ports["enhanced"],
                "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['enhanced']}&address={agent_addresses['enhanced']}"
            },
            "main": {
                "name": "Main Learning Agent",
                "address": agent_addresses["main"],
                "port": agent_ports["main"],
                "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['main']}&address={agent_addresses['main']}"
            }
        },
        "endpoints": {
            "status": "/status",
            "agents": "/agents",
            "health": "/health",
            "docs": "/docs"
        },
        "technology": {
            "framework": "uAgents",
            "ai_service": "Gemini AI",
            "knowledge_graph": "MeTTa",
            "api_framework": "FastAPI",
            "deployment": "Gunicorn"
        }
    }

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get overall system status"""
    agents = []
    active_count = 0
    
    for agent_name, address in agent_addresses.items():
        port = agent_ports[agent_name]
        agentverse_url = f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{port}&address={address}"
        
        status = "active" if agent_name in agent_processes else "inactive"
        if status == "active":
            active_count += 1
            
        agents.append(AgentStatus(
            name=agent_name.title() + " Agent",
            address=address,
            port=port,
            status=status,
            agentverse_url=agentverse_url
        ))
    
    return SystemStatus(
        status="running" if active_count > 0 else "stopped",
        agents=agents,
        total_agents=len(agent_addresses),
        active_agents=active_count
    )

@app.get("/agents")
async def get_agents():
    """Get detailed agent information"""
    return {
        "curriculum_agent": {
            "name": "Curriculum Agent",
            "address": agent_addresses["curriculum"],
            "port": agent_ports["curriculum"],
            "description": "Creates comprehensive educational plans with step-by-step resources",
            "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['curriculum']}&address={agent_addresses['curriculum']}",
            "capabilities": ["Educational plan creation", "Step-by-step learning paths", "Resource integration"]
        },
        "materials_agent": {
            "name": "Materials Agent", 
            "address": agent_addresses["materials"],
            "port": agent_ports["materials"],
            "description": "Finds targeted learning resources, courses, and YouTube videos",
            "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['materials']}&address={agent_addresses['materials']}",
            "capabilities": ["Resource discovery", "YouTube integration", "Course recommendations"]
        },
        "enhanced_agent": {
            "name": "Enhanced Agent",
            "address": agent_addresses["enhanced"], 
            "port": agent_ports["enhanced"],
            "description": "Provides deep insights and concept explanations",
            "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['enhanced']}&address={agent_addresses['enhanced']}",
            "capabilities": ["Deep insights", "Concept analysis", "Learning dependencies"]
        },
        "main_agent": {
            "name": "Main Learning Agent",
            "address": agent_addresses["main"],
            "port": agent_ports["main"], 
            "description": "Routes requests and coordinates responses from specialized agents",
            "agentverse_url": f"https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{agent_ports['main']}&address={agent_addresses['main']}",
            "capabilities": ["Request routing", "Response coordination", "Inter-agent communication"]
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "agents_running": len(agent_processes),
        "total_agents": len(agent_addresses)
    }

@app.post("/restart-agents")
async def restart_agents():
    """Restart all agents"""
    try:
        stop_all_agents()
        time.sleep(2)
        start_all_agents()
        return {"status": "success", "message": "All agents restarted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart agents: {str(e)}")

@app.get("/logs/{agent_name}")
async def get_agent_logs(agent_name: str):
    """Get logs for a specific agent"""
    if agent_name not in agent_processes:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        process = agent_processes[agent_name]
        stdout, stderr = process.communicate(timeout=1)
        return {
            "agent": agent_name,
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else ""
        }
    except Exception as e:
        return {"agent": agent_name, "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info"
    )
