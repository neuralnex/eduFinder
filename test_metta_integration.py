#!/usr/bin/env python3

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.gemini_service import GeminiLearningService
from services.metta_integration import MeTTaKnowledgeGraph

async def test_metta_integration():
    print("Testing MeTTa Integration with EduFinder")
    print("=" * 50)
    
    print("\n1. Testing Direct MeTTa Knowledge Graph:")
    try:
        async with MeTTaKnowledgeGraph() as metta:
            print(f"   MeTTa initialized: {'Real MeTTa' if metta.use_real_metta else 'Mock MeTTa'}")
            
            concept_data = await metta.query_learning_concepts("ai_engineering", "machine learning")
            if concept_data:
                print(f"   Query successful: Found {len(concept_data.get('prerequisites', []))} prerequisites")
                print(f"   Source: {concept_data.get('source', 'Unknown')}")
            else:
                print("   No data returned from MeTTa query")
                
    except Exception as e:
        print(f"   MeTTa test failed: {e}")
    
    print("\n2. Testing Gemini Service with MeTTa Integration:")
    try:
        gemini_service = GeminiLearningService()
        
        print("   Testing curriculum generation...")
        curriculum = await gemini_service.generate_curriculum("ai_engineering", "Teach me machine learning")
        if "MeTTa Knowledge Graph" in curriculum:
            print("   MeTTa insights integrated into curriculum")
        else:
            print("   MeTTa insights not found in curriculum (using pure Gemini)")
        
        print("   Testing deep insights generation...")
        insights = await gemini_service.generate_deep_insights("machine learning", "ai_engineering", "Explain machine learning concepts")
        if "MeTTa Knowledge Graph" in insights:
            print("   MeTTa insights integrated into deep analysis")
        else:
            print("   MeTTa insights not found in deep analysis (using pure Gemini)")
            
    except Exception as e:
        print(f"   Gemini service test failed: {e}")
    
    print("\n3. Agent Integration Status:")
    try:
        from config import METTA_USE_MOCK, METTA_ENDPOINT, METTA_SPACE
        print(f"   MeTTa Configuration:")
        print(f"      - Endpoint: {METTA_ENDPOINT}")
        print(f"      - Space: {METTA_SPACE}")
        print(f"      - Use Mock: {METTA_USE_MOCK}")
        
        try:
            import hyperon
            print(f"   Hyperon library available: {hyperon.__version__}")
        except ImportError:
            print("   Hyperon library not installed - using pure Gemini")
            
    except Exception as e:
        print(f"   Configuration test failed: {e}")
    
    print("\n" + "=" * 50)
    print("MeTTa Integration Test Complete!")
    print("\nNext Steps:")
    print("1. Install hyperon: pip install hyperon")
    print("2. Set METTA_USE_MOCK=false in .env")
    print("3. Run agents to test full integration")

if __name__ == "__main__":
    asyncio.run(test_metta_integration())
