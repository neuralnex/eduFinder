#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path

def test_imports():
    print("🧪 Testing imports...")
    
    try:
        import uagents
        print("✅ uagents imported successfully")
    except ImportError as e:
        print(f"❌ uagents import failed: {e}")
        return False
    
    try:
        from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
        print("✅ Chat protocol imported successfully")
    except ImportError as e:
        print(f"❌ Chat protocol import failed: {e}")
        return False
    
    try:
        import httpx
        print("✅ httpx imported successfully")
    except ImportError as e:
        print(f"❌ httpx import failed: {e}")
        return False
    
    try:
        from youtubesearchpython import VideosSearch
        print("✅ youtube-search-python imported successfully")
    except ImportError:
        print("⚠️ youtube-search-python not installed (optional)")
    
    return True

def test_agent_files():
    print("\n🔍 Testing agent files...")
    
    agent_files = [
        "agents/curriculum_agent.py",
        "agents/materials_agent.py", 
        "agents/enhanced_curriculum_agent.py",
        "agents/metta_integration.py"
    ]
    
    all_valid = True
    
    for agent_file in agent_files:
        if Path(agent_file).exists():
            try:
                with open(agent_file, 'r') as f:
                    code = f.read()
                compile(code, agent_file, 'exec')
                print(f"✅ {agent_file} - Valid Python syntax")
            except SyntaxError as e:
                print(f"❌ {agent_file} - Syntax error: {e}")
                all_valid = False
        else:
            print(f"❌ {agent_file} - File not found")
            all_valid = False
    
    return all_valid

async def test_metta_integration():
    print("\n🧠 Testing MeTTa integration...")
    
    try:
        from agents.metta_integration import MeTTaKnowledgeGraph
        
        async with MeTTaKnowledgeGraph() as metta:
            concept_data = await metta.query_learning_concepts("ai_engineering", "machine learning")
            if concept_data:
                print("✅ MeTTa concept query working")
            else:
                print("⚠️ MeTTa concept query returned empty data")
            
            prerequisites = await metta.get_learning_prerequisites("ai_engineering", "deep learning")
            if prerequisites:
                print("✅ MeTTa prerequisites query working")
            else:
                print("⚠️ MeTTa prerequisites query returned empty data")
        
        return True
        
    except Exception as e:
        print(f"❌ MeTTa integration test failed: {e}")
        return False

def test_youtube_search():
    print("\n🎥 Testing YouTube search...")
    
    try:
        from youtubesearchpython import VideosSearch
        
        videosSearch = VideosSearch("machine learning tutorial", limit=1)
        results = videosSearch.result()
        
        if results.get('result'):
            print("✅ YouTube search working")
            return True
        else:
            print("⚠️ YouTube search returned no results")
            return False
            
    except ImportError:
        print("⚠️ YouTube search not available (optional package)")
        return True
    except Exception as e:
        print(f"❌ YouTube search test failed: {e}")
        return False

def test_config():
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import AGENT_SEED, AGENT_NAME, AGENT_DESCRIPTION
        print("✅ Configuration loaded successfully")
        print(f"   Agent Name: {AGENT_NAME}")
        print(f"   Agent Description: {AGENT_DESCRIPTION}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    print("🎓 Learning Agents Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Files Test", test_agent_files),
        ("Configuration Test", test_config),
        ("YouTube Search Test", test_youtube_search),
        ("MeTTa Integration Test", test_metta_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your learning agents are ready to deploy!")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)