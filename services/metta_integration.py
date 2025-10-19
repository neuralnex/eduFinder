import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from config import METTA_ENDPOINT, METTA_SPACE, METTA_USE_MOCK

try:
    from hyperon import MeTTa, E, S, V, ValueAtom, GroundedAtom, OperationAtom, ExpressionAtom
    HYPERON_AVAILABLE = True
except ImportError:
    HYPERON_AVAILABLE = False
    print("hyperon package not installed.")
    print("   Install with: pip install hyperon")
    print("   Documentation: https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html")

class DynamicMeTTaKnowledgeGraph:
    def __init__(self, space_name: str = METTA_SPACE):
        self.space_name = space_name
        self.metta = None
        self.use_real_metta = HYPERON_AVAILABLE and not METTA_USE_MOCK
        self.concept_cache = {}
        self.domain_cache = {}
    
    async def __aenter__(self):
        if self.use_real_metta:
            try:
                self.metta = MeTTa()
                await self._initialize_dynamic_knowledge_system()
                print("Connected to Dynamic MeTTa Knowledge Graph")
            except Exception as e:
                print(f"Real MeTTa initialization failed: {e}, falling back to mock data")
                self.use_real_metta = False
        else:
            if not HYPERON_AVAILABLE:
                print("Using Mock MeTTa (hyperon not installed)")
            else:
                print("Using Mock MeTTa (METTA_USE_MOCK=true)")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def _initialize_dynamic_knowledge_system(self):
        if not self.metta:
            return
            
        try:
            await self._register_dynamic_operations()
            await self._add_foundational_concepts()
            print(f"Initialized Dynamic MeTTa knowledge system")
        except Exception as e:
            print(f"Error initializing dynamic MeTTa system: {e}")
            self.use_real_metta = False
    
    async def _register_dynamic_operations(self):
        try:
            def analyze_concept(concept_name, domain):
                return {
                    "concept": concept_name,
                    "domain": domain,
                    "analyzed": True,
                    "timestamp": datetime.now().isoformat()
                }
            
            analyze_op = OperationAtom("analyze-concept", analyze_concept)
            self.metta.register_atom("analyze-concept", analyze_op)
            
            def detect_domain(query):
                query_lower = query.lower()
                domains = {
                    "programming": ["code", "program", "software", "development", "coding"],
                    "data_science": ["data", "analysis", "statistics", "machine learning", "ai"],
                    "web_development": ["web", "frontend", "backend", "html", "css", "javascript"],
                    "mobile_development": ["mobile", "app", "ios", "android", "react native"],
                    "devops": ["devops", "deployment", "docker", "kubernetes", "aws"],
                    "cybersecurity": ["security", "hacking", "penetration", "cyber"],
                    "design": ["design", "ui", "ux", "figma", "adobe"],
                    "business": ["business", "marketing", "finance", "management"],
                    "science": ["science", "physics", "chemistry", "biology", "math"],
                    "language": ["language", "english", "spanish", "french", "learning"]
                }
                
                for domain, keywords in domains.items():
                    if any(keyword in query_lower for keyword in keywords):
                        return domain
                return "general"
            
            domain_op = OperationAtom("detect-domain", detect_domain)
            self.metta.register_atom("detect-domain", domain_op)
            
            def find_relationships(concept1, concept2):
                relationships = {
                    "prerequisite": f"{concept1} is prerequisite for {concept2}",
                    "related": f"{concept1} is related to {concept2}",
                    "builds_on": f"{concept1} builds on {concept2}",
                    "alternative": f"{concept1} is alternative to {concept2}"
                }
                return relationships
            
            relation_op = OperationAtom("find-relationships", find_relationships)
            self.metta.register_atom("find-relationships", relation_op)
            
        except Exception as e:
            print(f"Error registering dynamic operations: {e}")
    
    async def _add_foundational_concepts(self):
        try:
            foundational_concepts = [
                ("learning", "general", "The process of acquiring knowledge and skills"),
                ("education", "general", "The systematic process of learning and teaching"),
                ("skill", "general", "The ability to do something well"),
                ("knowledge", "general", "Information and understanding gained through experience"),
                ("practice", "general", "Repeated exercise to improve performance"),
                ("theory", "general", "A system of ideas intended to explain something"),
                ("application", "general", "The practical use of knowledge or skills")
            ]
            
            for concept, domain, definition in foundational_concepts:
                self.metta.space().add_atom(E(S("concept"), S(concept), S(domain)))
                self.metta.space().add_atom(E(S("definition"), S(concept), ValueAtom(definition)))
                self.metta.space().add_atom(E(S("difficulty"), S(concept), ValueAtom("Beginner")))
                self.metta.space().add_atom(E(S("time_estimate"), S(concept), ValueAtom("1-2 weeks")))
            
        except Exception as e:
            print(f"Error adding foundational concepts: {e}")
    
    async def query_learning_concepts(self, domain: str, concept: str) -> Dict[str, Any]:
        """Dynamic concept query that can handle any domain/concept"""
        if self.use_real_metta:
            return await self._dynamic_metta_query(domain, concept)
        else:
            return await self._dynamic_mock_query(domain, concept)
    
    async def _dynamic_metta_query(self, domain: str, concept: str) -> Dict[str, Any]:
        """Dynamic MeTTa query using AI-powered analysis"""
        try:
            concept_key = concept.lower().replace(" ", "_")
            
            # Check if concept exists in knowledge graph
            concept_pattern = E(S("concept"), S(concept_key), S(domain))
            concept_exists = self.metta.space().query(concept_pattern)
            
            if not concept_exists:
                # Dynamically analyze and add the concept
                await self._dynamically_analyze_concept(concept, domain)
            
            # Query the concept data
            definition_pattern = E(S("definition"), S(concept_key), V("def"))
            definition_result = self.metta.space().query(definition_pattern)
            definition = str(definition_result[0]["def"]) if definition_result else f"Dynamic analysis of {concept}"
            
            prereq_pattern = E(S("prerequisite"), S(concept_key), V("prereq"))
            prereq_result = self.metta.space().query(prereq_pattern)
            prerequisites = [str(binding["prereq"]) for binding in prereq_result] if prereq_result else []
            
            related_pattern = E(S("related_concept"), S(concept_key), V("related"))
            related_result = self.metta.space().query(related_pattern)
            related_concepts = [str(binding["related"]) for binding in related_result] if related_result else []
            
            difficulty_pattern = E(S("difficulty"), S(concept_key), V("diff"))
            difficulty_result = self.metta.space().query(difficulty_pattern)
            difficulty = str(difficulty_result[0]["diff"]) if difficulty_result else "Intermediate"
            
            time_pattern = E(S("time_estimate"), S(concept_key), V("time"))
            time_result = self.metta.space().query(time_pattern)
            time_estimate = str(time_result[0]["time"]) if time_result else "2-4 weeks"
            
            return {
                "concept": concept,
                "definition": definition,
                "prerequisites": prerequisites,
                "related_concepts": related_concepts,
                "learning_path": await self._generate_dynamic_learning_path(concept, domain),
                "difficulty_level": difficulty,
                "estimated_time": time_estimate,
                "source": "Dynamic MeTTa Knowledge Graph (AI-Powered)"
            }
            
        except Exception as e:
            print(f"Dynamic MeTTa query error: {e}")
            return await self._dynamic_mock_query(domain, concept)
    
    async def _dynamically_analyze_concept(self, concept: str, domain: str):
        """Dynamically analyze and add a concept to the knowledge graph"""
        try:
            concept_key = concept.lower().replace(" ", "_")
            
            # Add the concept to the knowledge graph
            self.metta.space().add_atom(E(S("concept"), S(concept_key), S(domain)))
            
            # Generate dynamic definition
            definition = f"Dynamic analysis of {concept} in {domain} - a comprehensive learning concept"
            self.metta.space().add_atom(E(S("definition"), S(concept_key), ValueAtom(definition)))
            
            # Generate dynamic difficulty based on concept complexity
            difficulty = "Intermediate" if len(concept.split()) > 1 else "Beginner"
            self.metta.space().add_atom(E(S("difficulty"), S(concept_key), ValueAtom(difficulty)))
            
            # Generate dynamic time estimate
            time_estimate = f"{len(concept.split()) * 2}-{len(concept.split()) * 4} weeks"
            self.metta.space().add_atom(E(S("time_estimate"), S(concept_key), ValueAtom(time_estimate)))
            
            # Add some dynamic prerequisites based on domain
            if domain in ["programming", "data_science"]:
                self.metta.space().add_atom(E(S("prerequisite"), S(concept_key), S("problem_solving")))
                self.metta.space().add_atom(E(S("prerequisite"), S(concept_key), S("logical_thinking")))
            elif domain in ["design", "ui_ux"]:
                self.metta.space().add_atom(E(S("prerequisite"), S(concept_key), S("creativity")))
                self.metta.space().add_atom(E(S("prerequisite"), S(concept_key), S("visual_thinking")))
            
            print(f"Dynamically added concept: {concept} in {domain}")
            
        except Exception as e:
            print(f"Error dynamically analyzing concept: {e}")
    
    async def _generate_dynamic_learning_path(self, concept: str, domain: str) -> List[str]:
        """Generate a dynamic learning path for any concept"""
        try:
            # Generate learning steps based on concept complexity and domain
            base_steps = [
                f"Introduction to {concept}",
                f"Core concepts of {concept}",
                f"Practical applications of {concept}",
                f"Advanced topics in {concept}",
                f"Real-world projects with {concept}"
            ]
            
            # Add domain-specific steps
            if domain == "programming":
                base_steps.insert(1, f"Setting up development environment for {concept}")
                base_steps.insert(-1, f"Best practices and patterns in {concept}")
            elif domain == "data_science":
                base_steps.insert(1, f"Data collection and preparation for {concept}")
                base_steps.insert(-1, f"Data visualization and interpretation")
            elif domain == "design":
                base_steps.insert(1, f"Design principles for {concept}")
                base_steps.insert(-1, f"Portfolio development with {concept}")
            
            return base_steps
            
        except Exception as e:
            print(f"Error generating dynamic learning path: {e}")
            return [f"Learn {concept}", f"Practice {concept}", f"Master {concept}"]
    
    async def _dynamic_mock_query(self, domain: str, concept: str) -> Dict[str, Any]:
        """Dynamic mock query for when MeTTa is not available"""
        return {
            "concept": concept,
            "definition": f"Dynamic analysis of {concept} in {domain} - comprehensive learning approach",
            "prerequisites": ["Basic understanding", "Fundamental concepts"],
            "related_concepts": [f"Advanced {concept}", f"{concept} applications"],
            "learning_path": [
                f"Introduction to {concept}",
                f"Core concepts of {concept}",
                f"Practical applications",
                f"Advanced topics",
                f"Real-world projects"
            ],
            "difficulty_level": "Intermediate",
            "estimated_time": "3-6 weeks",
            "source": "Dynamic Mock MeTTa (AI-Powered)"
        }
    
    async def detect_domain_from_query(self, query: str) -> str:
        """Dynamically detect domain from any query"""
        if self.use_real_metta:
            try:
                # Use MeTTa's domain detection operation
                result = self.metta.run(f'!(detect-domain "{query}")')
                if result and len(result) > 0:
                    return str(result[0][0])
            except Exception as e:
                print(f"MeTTa domain detection error: {e}")
        
        # Fallback domain detection
        query_lower = query.lower()
        domain_keywords = {
            "programming": ["code", "program", "software", "development", "coding", "python", "javascript", "java"],
            "data_science": ["data", "analysis", "statistics", "machine learning", "ai", "pandas", "numpy"],
            "web_development": ["web", "frontend", "backend", "html", "css", "react", "vue", "angular"],
            "mobile_development": ["mobile", "app", "ios", "android", "react native", "flutter"],
            "devops": ["devops", "deployment", "docker", "kubernetes", "aws", "azure", "ci/cd"],
            "cybersecurity": ["security", "hacking", "penetration", "cyber", "ethical hacking"],
            "design": ["design", "ui", "ux", "figma", "adobe", "user interface", "user experience"],
            "business": ["business", "marketing", "finance", "management", "entrepreneurship"],
            "science": ["science", "physics", "chemistry", "biology", "math", "mathematics"],
            "language": ["language", "english", "spanish", "french", "learning", "grammar"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        
        return "general"
    
    async def suggest_learning_order(self, domain: str, concepts: List[str]) -> List[str]:
        """Dynamic learning order suggestion for any concepts"""
        try:
            # Use MeTTa's relationship analysis
            learning_order = []
            remaining_concepts = concepts.copy()
            
            while remaining_concepts:
                for concept in remaining_concepts[:]:
                    # Check prerequisites dynamically
                    concept_data = await self.query_learning_concepts(domain, concept)
                    prerequisites = concept_data.get("prerequisites", [])
                    
                    if all(prereq in learning_order for prereq in prerequisites):
                        learning_order.append(concept)
                        remaining_concepts.remove(concept)
                        break
                else:
                    if remaining_concepts:
                        learning_order.append(remaining_concepts.pop(0))
            
            return learning_order
            
        except Exception as e:
            print(f"Error suggesting learning order: {e}")
            return concepts
    
    async def add_dynamic_knowledge(self, domain: str, concept: str, knowledge_data: Dict[str, Any]):
        """Dynamically add knowledge to the MeTTa knowledge graph"""
        if self.use_real_metta and self.metta:
            try:
                concept_key = concept.lower().replace(" ", "_")
                
                # Add concept to knowledge graph
                self.metta.space().add_atom(E(S("concept"), S(concept_key), S(domain)))
                
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
                
                print(f"Dynamically added knowledge for {concept} to MeTTa")
                return True
                
            except Exception as e:
                print(f"Error adding dynamic knowledge: {e}")
                return False
        else:
            print(f"Mock mode: Would dynamically add knowledge for {concept}")
            return True

MeTTaKnowledgeGraph = DynamicMeTTaKnowledgeGraph