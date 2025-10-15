#!/usr/bin/env python3

import asyncio
import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, description: str):
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_dependencies():
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "uagents",
        "httpx",
        "pydantic",
        "python-dotenv",
        "youtube-search-python",
        "requests",
        "aiohttp"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        install_cmd = f"pip install {' '.join(missing_packages)}"
        run_command(install_cmd, "Installing dependencies")
    
    return len(missing_packages) == 0

def setup_environment():
    print("⚙️ Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as f:
            content = f.read()
        
        import secrets
        unique_seed = secrets.token_hex(16)
        content = content.replace("your-unique-seed-here", unique_seed)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Created .env file with seed: {unique_seed}")
    else:
        print("✅ Environment file already exists")

def test_agents():
    print("🧪 Testing agents...")
    
    agents = [
        ("agents/curriculum_agent.py", "Curriculum Agent"),
        ("agents/materials_agent.py", "Materials Agent"),
        ("agents/enhanced_curriculum_agent.py", "Enhanced Curriculum Agent")
    ]
    
    for agent_file, agent_name in agents:
        if Path(agent_file).exists():
            print(f"🔍 Testing {agent_name}...")
            try:
                exec(f"import {agent_file.replace('.py', '').replace('/', '.')}")
                print(f"✅ {agent_name} - Import successful")
            except Exception as e:
                print(f"❌ {agent_name} - Import failed: {e}")
        else:
            print(f"❌ {agent_file} not found")

def deploy_to_agentverse():
    print("🚀 Deploying to Agentverse...")
    
    agents = [
        "agents/curriculum_agent.py",
        "agents/materials_agent.py", 
        "agents/enhanced_curriculum_agent.py"
    ]
    
    for agent_file in agents:
        if Path(agent_file).exists():
            print(f"📤 Deploying {agent_file}...")
            print(f"✅ {agent_file} - Deployment simulated")
        else:
            print(f"❌ {agent_file} not found")

def main():
    print("🎓 Learning Agents Deployment Script")
    print("=" * 50)
    
    if not check_dependencies():
        print("❌ Dependency check failed")
        return False
    
    setup_environment()
    
    test_agents()
    
    deploy_to_agentverse()
    
    print("\n🎉 Deployment completed!")
    print("\n📋 Next Steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Run individual agents:")
    print("   python agents/curriculum_agent.py")
    print("   python agents/materials_agent.py")
    print("   python agents/enhanced_curriculum_agent.py")
    print("3. Test agent communication")
    print("4. Register agents on Agentverse")
    print("5. Enable Chat Protocol for ASI:One compatibility")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)