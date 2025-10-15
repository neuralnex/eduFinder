import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import METTA_ENDPOINT, METTA_SPACE, METTA_USE_MOCK

try:
    from hyperon import MeTTa, E, S, V, ValueAtom, GroundedAtom, OperationAtom, ExpressionAtom
    HYPERON_AVAILABLE = True
except ImportError:
    HYPERON_AVAILABLE = False
    print("hyperon package not installed.")
    print("   Install with: pip install hyperon")
    print("   Documentation: https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html")

class MeTTaKnowledgeGraph:
    def __init__(self, space_name: str = METTA_SPACE):
        self.space_name = space_name
        self.metta = None
        self.use_real_metta = HYPERON_AVAILABLE and not METTA_USE_MOCK
    
    async def __aenter__(self):
        if self.use_real_metta:
            try:
                self.metta = MeTTa()
                await self._initialize_knowledge_graph()
                print("✅ Connected to Real MeTTa Knowledge Graph")
            except Exception as e:
                print(f"⚠️ Real MeTTa initialization failed: {e}, falling back to mock data")
                self.use_real_metta = False
        else:
            if not HYPERON_AVAILABLE:
                print("📚 Using Mock MeTTa (hyperon not installed)")
            else:
                print("📚 Using Mock MeTTa (METTA_USE_MOCK=true)")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.metta:
            self.metta.close()
    
    async def _initialize_knowledge_graph(self):
        if not self.metta:
            return
            
        try:
            concepts_data = [
                ("machine_learning", "Machine Learning", "ai_engineering"),
                ("deep_learning", "Deep Learning", "ai_engineering"),
                ("neural_networks", "Neural Networks", "ai_engineering"),
                ("blockchain", "Blockchain", "web3_development"),
                ("smart_contracts", "Smart Contracts", "web3_development"),
                ("cryptocurrency", "Cryptocurrency", "web3_development"),
                ("data_analysis", "Data Analysis", "data_science"),
                ("statistics", "Statistics", "data_science"),
            ]
            
            for concept_name, display_name, domain in concepts_data:
                self.metta.space().add_atom(E(S("learning_concept"), S(concept_name), S(domain)))
                self.metta.space().add_atom(E(S("concept_name"), S(concept_name), ValueAtom(display_name)))
            
            prerequisites = [
                ("prerequisite", "deep_learning", "machine_learning"),
                ("prerequisite", "deep_learning", "linear_algebra"),
                ("prerequisite", "deep_learning", "calculus"),
                ("prerequisite", "machine_learning", "linear_algebra"),
                ("prerequisite", "machine_learning", "statistics"),
                ("prerequisite", "machine_learning", "python_programming"),
                ("prerequisite", "neural_networks", "linear_algebra"),
                ("prerequisite", "neural_networks", "calculus"),
                ("prerequisite", "neural_networks", "python_programming"),
                ("prerequisite", "smart_contracts", "blockchain"),
                ("prerequisite", "smart_contracts", "solidity"),
                ("prerequisite", "smart_contracts", "ethereum"),
                ("prerequisite", "blockchain", "cryptography"),
                ("prerequisite", "blockchain", "distributed_systems"),
                ("prerequisite", "blockchain", "javascript"),
                ("prerequisite", "data_analysis", "statistics"),
                ("prerequisite", "data_analysis", "python"),
                ("prerequisite", "data_analysis", "sql"),
            ]
            
            for prereq_type, concept, prereq in prerequisites:
                self.metta.space().add_atom(E(S(prereq_type), S(concept), S(prereq)))
            
            related_concepts = [
                ("related_concept", "machine_learning", "supervised_learning"),
                ("related_concept", "machine_learning", "unsupervised_learning"),
                ("related_concept", "machine_learning", "deep_learning"),
                ("related_concept", "deep_learning", "neural_networks"),
                ("related_concept", "deep_learning", "cnn"),
                ("related_concept", "deep_learning", "rnn"),
                ("related_concept", "deep_learning", "transformers"),
                ("related_concept", "blockchain", "consensus_mechanisms"),
                ("related_concept", "blockchain", "smart_contracts"),
                ("related_concept", "blockchain", "cryptocurrency"),
                ("related_concept", "smart_contracts", "defi"),
                ("related_concept", "smart_contracts", "nfts"),
                ("related_concept", "smart_contracts", "daos"),
                ("related_concept", "data_analysis", "data_visualization"),
                ("related_concept", "data_analysis", "statistical_analysis"),
                ("related_concept", "data_analysis", "data_cleaning"),
            ]
            
            for related_type, concept, related in related_concepts:
                self.metta.space().add_atom(E(S(related_type), S(concept), S(related)))
            
            learning_paths = [
                ("learning_step", "machine_learning", 1, "Mathematical Foundations"),
                ("learning_step", "machine_learning", 2, "Programming Skills"),
                ("learning_step", "machine_learning", 3, "ML Algorithms"),
                ("learning_step", "machine_learning", 4, "Model Evaluation"),
                ("learning_step", "machine_learning", 5, "Production Deployment"),
                ("learning_step", "deep_learning", 1, "Neural Network Basics"),
                ("learning_step", "deep_learning", 2, "Backpropagation"),
                ("learning_step", "deep_learning", 3, "Convolutional Networks"),
                ("learning_step", "deep_learning", 4, "Recurrent Networks"),
                ("learning_step", "deep_learning", 5, "Advanced Architectures"),
                ("learning_step", "blockchain", 1, "Cryptography Basics"),
                ("learning_step", "blockchain", 2, "Distributed Systems"),
                ("learning_step", "blockchain", 3, "Blockchain Architecture"),
                ("learning_step", "blockchain", 4, "Consensus Algorithms"),
                ("learning_step", "blockchain", 5, "Smart Contract Development"),
            ]
            
            for path_type, concept, step_num, step_name in learning_paths:
                self.metta.space().add_atom(E(S(path_type), S(concept), ValueAtom(step_num), ValueAtom(step_name)))
            
            definitions = {
                "machine_learning": "A subset of artificial intelligence that enables computers to learn and make decisions from data",
                "deep_learning": "A subset of machine learning using neural networks with multiple layers",
                "neural_networks": "Computing systems inspired by biological neural networks",
                "blockchain": "A distributed ledger technology that maintains a continuously growing list of records",
                "smart_contracts": "Self-executing contracts with terms directly written into code",
                "cryptocurrency": "Digital or virtual currency secured by cryptography",
                "data_analysis": "The process of inspecting, cleaning, and modeling data to discover useful information",
                "statistics": "The science of collecting, analyzing, and interpreting data",
            }
            
            for concept, definition in definitions.items():
                self.metta.space().add_atom(E(S("definition"), S(concept), ValueAtom(definition)))
            
            difficulties = {
                "machine_learning": "Intermediate",
                "deep_learning": "Advanced",
                "neural_networks": "Intermediate",
                "blockchain": "Intermediate",
                "smart_contracts": "Intermediate",
                "cryptocurrency": "Beginner",
                "data_analysis": "Beginner",
                "statistics": "Beginner",
            }
            
            for concept, difficulty in difficulties.items():
                self.metta.space().add_atom(E(S("difficulty"), S(concept), ValueAtom(difficulty)))
            
            time_estimates = {
                "machine_learning": "3-6 months",
                "deep_learning": "4-8 months",
                "neural_networks": "2-4 months",
                "blockchain": "2-4 months",
                "smart_contracts": "3-5 months",
                "cryptocurrency": "1-3 months",
                "data_analysis": "2-4 months",
                "statistics": "2-3 months",
            }
            
            for concept, time_est in time_estimates.items():
                self.metta.space().add_atom(E(S("time_estimate"), S(concept), ValueAtom(time_est)))
            
            print(f"✅ Initialized MeTTa knowledge graph with {len(concepts_data)} concepts")
            
        except Exception as e:
            print(f"Error initializing MeTTa knowledge graph: {e}")
            self.use_real_metta = False
    
    async def query_learning_concepts(self, domain: str, concept: str) -> Dict[str, Any]:
        if self.use_real_metta:
            return await self._real_metta_query(domain, concept)
        else:
            return await self._mock_metta_query(domain, concept)
    
    async def _real_metta_query(self, domain: str, concept: str) -> Dict[str, Any]:
        try:
            concept_key = concept.lower().replace(" ", "_")
            
            definition_query = f'!(match &self (definition {concept_key} $def) $def)'
            definition_result = self.metta.run(definition_query)
            if definition_result and len(definition_result) > 0:
                definition = str(definition_result[0])
            else:
                definition = "No definition available"
            
            prereq_query = f'!(match &self (prerequisite {concept_key} $prereq) $prereq)'
            prereq_result = self.metta.run(prereq_query)
            prerequisites = [str(atom) for atom in prereq_result] if prereq_result else []
            
            related_query = f'!(match &self (related_concept {concept_key} $related) $related)'
            related_result = self.metta.run(related_query)
            related_concepts = [str(atom) for atom in related_result] if related_result else []
            
            path_query = f'!(match &self (learning_step {concept_key} $step_num $step_name) ($step_num $step_name))'
            path_result = self.metta.run(path_query)
            learning_path = []
            if path_result:
                learning_path = [str(step) for step in path_result]
            
            difficulty_query = f'!(match &self (difficulty {concept_key} $diff) $diff)'
            difficulty_result = self.metta.run(difficulty_query)
            difficulty = str(difficulty_result[0]) if difficulty_result and len(difficulty_result) > 0 else "Not specified"
            
            time_query = f'!(match &self (time_estimate {concept_key} $time) $time)'
            time_result = self.metta.run(time_query)
            time_estimate = str(time_result[0]) if time_result and len(time_result) > 0 else "Not specified"
            
            return {
                "concept": concept,
                "definition": definition,
                "prerequisites": prerequisites,
                "related_concepts": related_concepts,
                "learning_path": learning_path,
                "difficulty_level": difficulty,
                "estimated_time": time_estimate,
                "source": "MeTTa Knowledge Graph (hyperon)"
            }
            
        except Exception as e:
            print(f"Real MeTTa query error: {e}")
            return await self._mock_metta_query(domain, concept)
    
    async def _mock_metta_query(self, domain: str, concept: str) -> Dict[str, Any]:
        knowledge_graph = {
            "ai_engineering": {
                "machine_learning": {
                    "concept": "Machine Learning",
                    "definition": "A subset of artificial intelligence that enables computers to learn and make decisions from data",
                    "prerequisites": ["Linear Algebra", "Statistics", "Python Programming"],
                    "related_concepts": ["Supervised Learning", "Unsupervised Learning", "Deep Learning"],
                    "learning_path": [
                        "Mathematical Foundations",
                        "Programming Skills",
                        "ML Algorithms",
                        "Model Evaluation",
                        "Production Deployment"
                    ],
                    "difficulty_level": "Intermediate",
                    "estimated_time": "3-6 months"
                },
                "deep_learning": {
                    "concept": "Deep Learning",
                    "definition": "A subset of machine learning using neural networks with multiple layers",
                    "prerequisites": ["Machine Learning", "Linear Algebra", "Calculus"],
                    "related_concepts": ["Neural Networks", "CNN", "RNN", "Transformers"],
                    "learning_path": [
                        "Neural Network Basics",
                        "Backpropagation",
                        "Convolutional Networks",
                        "Recurrent Networks",
                        "Advanced Architectures"
                    ],
                    "difficulty_level": "Advanced",
                    "estimated_time": "4-8 months"
                },
                "neural_networks": {
                    "concept": "Neural Networks",
                    "definition": "Computing systems inspired by biological neural networks",
                    "prerequisites": ["Linear Algebra", "Calculus", "Python Programming"],
                    "related_concepts": ["Deep Learning", "Backpropagation", "Activation Functions"],
                    "learning_path": [
                        "Perceptron",
                        "Multi-layer Perceptron",
                        "Backpropagation Algorithm",
                        "Activation Functions",
                        "Network Architectures"
                    ],
                    "difficulty_level": "Intermediate",
                    "estimated_time": "2-4 months"
                }
            },
            "web3_development": {
                "blockchain": {
                    "concept": "Blockchain",
                    "definition": "A distributed ledger technology that maintains a continuously growing list of records",
                    "prerequisites": ["Cryptography", "Distributed Systems", "JavaScript"],
                    "related_concepts": ["Consensus Mechanisms", "Smart Contracts", "Cryptocurrency"],
                    "learning_path": [
                        "Cryptography Basics",
                        "Distributed Systems",
                        "Blockchain Architecture",
                        "Consensus Algorithms",
                        "Smart Contract Development"
                    ],
                    "difficulty_level": "Intermediate",
                    "estimated_time": "2-4 months"
                },
                "smart_contracts": {
                    "concept": "Smart Contracts",
                    "definition": "Self-executing contracts with terms directly written into code",
                    "prerequisites": ["Blockchain", "Solidity", "Ethereum"],
                    "related_concepts": ["DeFi", "NFTs", "DAOs", "Gas Optimization"],
                    "learning_path": [
                        "Solidity Language",
                        "Ethereum Platform",
                        "Contract Development",
                        "Testing and Deployment",
                        "Security Best Practices"
                    ],
                    "difficulty_level": "Intermediate",
                    "estimated_time": "3-5 months"
                },
                "cryptocurrency": {
                    "concept": "Cryptocurrency",
                    "definition": "Digital or virtual currency secured by cryptography",
                    "prerequisites": ["Cryptography", "Economics", "Computer Science"],
                    "related_concepts": ["Bitcoin", "Ethereum", "Mining", "Wallets"],
                    "learning_path": [
                        "Cryptographic Principles",
                        "Consensus Mechanisms",
                        "Mining and Validation",
                        "Wallet Technology",
                        "Market Dynamics"
                    ],
                    "difficulty_level": "Beginner",
                    "estimated_time": "1-3 months"
                }
            },
            "data_science": {
                "data_analysis": {
                    "concept": "Data Analysis",
                    "definition": "The process of inspecting, cleaning, and modeling data to discover useful information",
                    "prerequisites": ["Statistics", "Python/R", "SQL"],
                    "related_concepts": ["Data Visualization", "Statistical Analysis", "Data Cleaning"],
                    "learning_path": [
                        "Statistical Foundations",
                        "Data Manipulation",
                        "Exploratory Data Analysis",
                        "Data Visualization",
                        "Statistical Modeling"
                    ],
                    "difficulty_level": "Beginner",
                    "estimated_time": "2-4 months"
                },
                "statistics": {
                    "concept": "Statistics",
                    "definition": "The science of collecting, analyzing, and interpreting data",
                    "prerequisites": ["Mathematics", "Probability"],
                    "related_concepts": ["Probability", "Hypothesis Testing", "Regression Analysis"],
                    "learning_path": [
                        "Descriptive Statistics",
                        "Probability Theory",
                        "Inferential Statistics",
                        "Hypothesis Testing",
                        "Regression Analysis"
                    ],
                    "difficulty_level": "Beginner",
                    "estimated_time": "2-3 months"
                },
                "machine_learning": {
                    "concept": "Machine Learning",
                    "definition": "A subset of artificial intelligence that enables computers to learn and make decisions from data",
                    "prerequisites": ["Statistics", "Linear Algebra", "Python Programming"],
                    "related_concepts": ["Data Analysis", "Deep Learning", "Neural Networks"],
                    "learning_path": [
                        "Data Preprocessing",
                        "Supervised Learning",
                        "Unsupervised Learning",
                        "Model Evaluation",
                        "Feature Engineering"
                    ],
                    "difficulty_level": "Intermediate",
                    "estimated_time": "3-6 months"
                }
            }
        }
        
        domain_data = knowledge_graph.get(domain, {})
        concept_data = domain_data.get(concept.lower().replace(" ", "_"), {})
        
        if not concept_data:
            for key, value in domain_data.items():
                if concept.lower() in key or key in concept.lower():
                    concept_data = value
                    break
        
        if concept_data:
            concept_data["source"] = "Mock MeTTa (Demo Mode)"
        
        return concept_data
    
    async def get_learning_prerequisites(self, domain: str, concept: str) -> List[str]:
        concept_data = await self.query_learning_concepts(domain, concept)
        return concept_data.get("prerequisites", [])
    
    async def get_related_concepts(self, domain: str, concept: str) -> List[str]:
        concept_data = await self.query_learning_concepts(domain, concept)
        return concept_data.get("related_concepts", [])
    
    async def get_learning_path(self, domain: str, concept: str) -> List[str]:
        concept_data = await self.query_learning_concepts(domain, concept)
        return concept_data.get("learning_path", [])
    
    async def get_concept_definition(self, domain: str, concept: str) -> str:
        concept_data = await self.query_learning_concepts(domain, concept)
        return concept_data.get("definition", "No definition available")
    
    async def suggest_learning_order(self, domain: str, concepts: List[str]) -> List[str]:
        learning_order = []
        remaining_concepts = concepts.copy()
        
        while remaining_concepts:
            for concept in remaining_concepts[:]:
                prerequisites = await self.get_learning_prerequisites(domain, concept)
                
                if all(prereq in learning_order for prereq in prerequisites):
                    learning_order.append(concept)
                    remaining_concepts.remove(concept)
                    break
            else:
                if remaining_concepts:
                    learning_order.append(remaining_concepts.pop(0))
        
        return learning_order

    async def add_knowledge(self, domain: str, concept: str, knowledge_data: Dict[str, Any]):
        if self.use_real_metta and self.metta:
            try:
                concept_key = concept.lower().replace(" ", "_")
                
                self.metta.space().add_atom(E(S("learning_concept"), S(concept_key), S(domain)))
                
                if "definition" in knowledge_data:
                    self.metta.space().add_atom(E(S("definition"), S(concept_key), ValueAtom(knowledge_data["definition"])))
                
                for prereq in knowledge_data.get("prerequisites", []):
                    prereq_key = prereq.lower().replace(" ", "_")
                    self.metta.space().add_atom(E(S("prerequisite"), S(concept_key), S(prereq_key)))
                
                for related in knowledge_data.get("related_concepts", []):
                    related_key = related.lower().replace(" ", "_")
                    self.metta.space().add_atom(E(S("related_concept"), S(concept_key), S(related_key)))
                
                for i, step in enumerate(knowledge_data.get("learning_path", []), 1):
                    self.metta.space().add_atom(E(S("learning_step"), S(concept_key), ValueAtom(i), ValueAtom(step)))
                
                if "difficulty_level" in knowledge_data:
                    self.metta.space().add_atom(E(S("difficulty"), S(concept_key), ValueAtom(knowledge_data["difficulty_level"])))
                
                if "estimated_time" in knowledge_data:
                    self.metta.space().add_atom(E(S("time_estimate"), S(concept_key), ValueAtom(knowledge_data["estimated_time"])))
                
                print(f"✅ Added knowledge for {concept} to MeTTa")
                return True
                
            except Exception as e:
                print(f"Error adding knowledge: {e}")
                return False
        else:
            print(f"📝 Mock mode: Would add knowledge for {concept}")
            return True

async def test_metta_integration():
    print("Testing MeTTa Knowledge Graph Integration")
    print("=" * 50)
    
    async with MeTTaKnowledgeGraph() as metta:
        print(f"Using {'Real MeTTa (hyperon)' if metta.use_real_metta else 'Mock MeTTa'}")
        
        concept_data = await metta.query_learning_concepts("ai_engineering", "machine learning")
        print(f"Machine Learning Concept: {concept_data}")
        
        prerequisites = await metta.get_learning_prerequisites("ai_engineering", "deep learning")
        print(f"Deep Learning Prerequisites: {prerequisites}")
        
        learning_path = await metta.get_learning_path("web3_development", "smart contracts")
        print(f"Smart Contracts Learning Path: {learning_path}")
        
        concepts = ["deep learning", "machine learning", "neural networks"]
        order = await metta.suggest_learning_order("ai_engineering", concepts)
        print(f"Suggested Learning Order: {order}")

if __name__ == "__main__":
    asyncio.run(test_metta_integration())