"""
CCT PoC - Prism Module

The Prism is the user's semantic transformation vector.
It refracts raw semantic coordinates into personal meaning.

Formula: P_u(ω) = Φ_u(ω)

Where:
- ω is a semantic coordinate (the "objective" meaning)
- Φ_u is the user's prism (transformation)
- P_u(ω) is the personal meaning
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class UserPrism:
    """
    A user's semantic prism.
    
    The prism encodes:
    - Worldview (how they categorize reality)
    - Values (what they amplify/dampen)
    - History (their semantic trajectory)
    """
    user_id: str
    name: str
    archetype: str
    vector: np.ndarray  # 128D transformation vector
    bias: np.ndarray    # 128D bias vector
    metadata: Dict
    
    def transform(self, coordinate: np.ndarray) -> np.ndarray:
        """
        Apply prism transformation to a semantic coordinate.
        
        The core operation: P_u(ω) = Φ_u · ω + bias
        """
        # Element-wise modulation (amplify/dampen)
        modulated = coordinate * self.vector
        
        # Add personal bias (worldview shift)
        shifted = modulated + self.bias
        
        return shifted


# ============================================================================
# HARD-CODED TEST USERS
# ============================================================================

def create_test_prisms() -> Dict[str, UserPrism]:
    """
    Create 3 test users with hand-crafted prisms.
    
    Each prism is 128 dimensions, encoding different worldviews.
    """
    
    np.random.seed(42)  # Reproducibility
    
    # Base dimensions (what each dimension "means")
    # In a real system, these would be learned from user data
    # For PoC, we hand-craft the semantics
    
    # Dimension indices and their "meanings" (conceptual, not literal)
    # 0-31: Professional/Career orientation
    # 32-63: Emotional/Relational orientation  
    # 64-95: Intellectual/Abstract orientation
    # 96-127: Physical/Concrete orientation
    
    # --------------------------------------------------------------------
    # USER 1: THE ENTREPRENEUR
    # --------------------------------------------------------------------
    entrepreneur_vector = np.ones(128)
    
    # Amplify: Growth, metrics, scale, efficiency (dims 0-31)
    entrepreneur_vector[0:8] = 2.0    # Growth focus
    entrepreneur_vector[8:16] = 1.8   # Scale orientation
    entrepreneur_vector[16:24] = 1.5  # Efficiency drive
    entrepreneur_vector[24:31] = 1.6  # Risk tolerance
    
    # Neutral: Emotional dimensions
    entrepreneur_vector[32:63] = 1.0
    
    # Dampen: Abstract philosophy, theoretical concepts
    entrepreneur_vector[64:95] = 0.6
    
    # Amplify: Concrete results, tangible outcomes
    entrepreneur_vector[96:127] = 1.7
    
    entrepreneur_bias = np.zeros(128)
    entrepreneur_bias[0:31] = 0.3    # Career bias
    entrepreneur_bias[96:127] = 0.2  # Results bias
    
    entrepreneur = UserPrism(
        user_id="user_001",
        name="Alex Chen",
        archetype="entrepreneur",
        vector=entrepreneur_vector,
        bias=entrepreneur_bias,
        metadata={
            "description": "Serial entrepreneur, values growth and metrics",
            "language_style": "direct, action-oriented",
            "key_concepts": ["scale", "efficiency", "ROI", "traction"]
        }
    )
    
    # --------------------------------------------------------------------
    # USER 2: THE ARTIST
    # --------------------------------------------------------------------
    artist_vector = np.ones(128)
    
    # Dampen: Traditional career metrics
    artist_vector[0:31] = 0.5
    
    # Amplify: Emotional depth, authenticity, expression (dims 32-63)
    artist_vector[32:40] = 2.2    # Emotional depth
    artist_vector[40:48] = 1.9    # Authenticity
    artist_vector[48:56] = 1.8    # Creative expression
    artist_vector[56:63] = 1.7    # Aesthetic sensitivity
    
    # Amplify: Abstract, philosophical, theoretical
    artist_vector[64:95] = 1.6
    
    # Neutral: Physical/concrete
    artist_vector[96:127] = 1.0
    
    artist_bias = np.zeros(128)
    artist_bias[32:63] = 0.4    # Emotional bias
    artist_bias[64:95] = 0.2    # Abstract bias
    
    artist = UserPrism(
        user_id="user_002",
        name="Maya Rivers",
        archetype="artist",
        vector=artist_vector,
        bias=artist_bias,
        metadata={
            "description": "Painter and poet, values authenticity and beauty",
            "language_style": "evocative, metaphorical",
            "key_concepts": ["authenticity", "expression", "beauty", "truth"]
        }
    )
    
    # --------------------------------------------------------------------
    # USER 3: THE PARENT
    # --------------------------------------------------------------------
    parent_vector = np.ones(128)
    
    # Moderate: Career (important but not primary)
    parent_vector[0:31] = 0.8
    
    # Amplify: Relationships, care, nurturing (dims 32-63)
    parent_vector[32:40] = 2.0    # Care/nurturing
    parent_vector[40:48] = 1.9    # Protection
    parent_vector[48:56] = 1.7    # Legacy/future
    parent_vector[56:63] = 1.6    # Community
    
    # Moderate: Abstract concepts
    parent_vector[64:95] = 0.9
    
    # Amplify: Concrete, practical, daily life
    parent_vector[96:127] = 1.4
    
    parent_bias = np.zeros(128)
    parent_bias[32:63] = 0.35   # Relational bias
    parent_bias[96:127] = 0.15  # Practical bias
    
    parent = UserPrism(
        user_id="user_003",
        name="Sam Jordan",
        archetype="parent",
        vector=parent_vector,
        bias=parent_bias,
        metadata={
            "description": "Parent of two, values family and stability",
            "language_style": "warm, practical, protective",
            "key_concepts": ["family", "safety", "growth", "connection"]
        }
    )
    
    return {
        "entrepreneur": entrepreneur,
        "artist": artist,
        "parent": parent
    }


def get_prism(archetype: str) -> Optional[UserPrism]:
    """Get a prism by archetype."""
    prisms = create_test_prisms()
    return prisms.get(archetype)


def list_prisms() -> List[str]:
    """List available prism archetypes."""
    return list(create_test_prisms().keys())


# ============================================================================
# SEMANTIC COORDINATES (The "Objective" Space Ω)
# ============================================================================

def create_semantic_coordinates() -> Dict[str, np.ndarray]:
    """
    Create test semantic coordinates.
    
    These represent "objective" meanings in the semantic space.
    They exist independently of any observer.
    
    In a real system, these would come from an embedding model.
    For PoC, we hand-craft them.
    """
    np.random.seed(42)
    
    coordinates = {}
    
    # SUCCESS - a coordinate in semantic space
    success = np.zeros(128)
    success[0:8] = 1.0    # Achievement dimension
    success[8:16] = 0.8   # Recognition
    success[16:24] = 0.6  # Financial
    success[32:40] = 0.5  # Emotional fulfillment
    success[64:72] = 0.4  # Philosophical meaning
    success[96:104] = 0.7 # Tangible outcomes
    coordinates["success"] = success
    
    # FREEDOM
    freedom = np.zeros(128)
    freedom[0:8] = 0.6    # Professional autonomy
    freedom[24:31] = 0.9  # Independence
    freedom[32:40] = 0.8  # Emotional liberation
    freedom[64:72] = 0.7  # Philosophical liberty
    freedom[96:104] = 0.5 # Physical movement
    coordinates["freedom"] = freedom
    
    # LOVE
    love = np.zeros(128)
    love[32:40] = 1.0    # Emotional connection
    love[40:48] = 0.9    # Intimacy
    love[48:56] = 0.7    # Commitment
    love[56:63] = 0.8    # Community
    love[64:72] = 0.5    # Spiritual dimension
    coordinates["love"] = love
    
    # WORK
    work = np.zeros(128)
    work[0:8] = 0.9     # Effort/exertion
    work[8:16] = 0.7    # Professional identity
    work[16:24] = 0.6   # Financial exchange
    work[32:40] = 0.4   # Emotional engagement
    work[96:104] = 0.8  # Concrete output
    coordinates["work"] = work
    
    # MEANING
    meaning = np.zeros(128)
    meaning[32:40] = 0.6   # Emotional resonance
    meaning[64:72] = 1.0   # Philosophical depth
    meaning[72:80] = 0.9   # Purpose
    meaning[80:88] = 0.8   # Significance
    meaning[96:104] = 0.3  # Tangible manifestation
    coordinates["meaning"] = meaning
    
    # GROWTH
    growth = np.zeros(128)
    growth[0:8] = 0.8    # Professional development
    growth[8:16] = 0.7   # Expansion
    growth[32:40] = 0.6  # Personal evolution
    growth[48:56] = 0.5  # Maturity
    growth[96:104] = 0.7 # Visible progress
    coordinates["growth"] = growth
    
    return coordinates


def get_coordinate(concept: str) -> Optional[np.ndarray]:
    """Get a semantic coordinate by concept name."""
    coordinates = create_semantic_coordinates()
    return coordinates.get(concept.lower())


def list_concepts() -> List[str]:
    """List available semantic concepts."""
    return list(create_semantic_coordinates().keys())


if __name__ == "__main__":
    # Test the prisms
    print("=" * 60)
    print("CCT PoC - Prism Module Test")
    print("=" * 60)
    
    prisms = create_test_prisms()
    coordinates = create_semantic_coordinates()
    
    print(f"\nAvailable prisms: {list_prisms()}")
    print(f"Available concepts: {list_concepts()}")
    
    print("\n" + "-" * 60)
    print("Testing: SUCCESS coordinate through each prism")
    print("-" * 60)
    
    success_coord = coordinates["success"]
    
    for archetype, prism in prisms.items():
        transformed = prism.transform(success_coord)
        print(f"\n{prism.name} ({archetype}):")
        print(f"  Original sum: {success_coord.sum():.2f}")
        print(f"  Transformed sum: {transformed.sum():.2f}")
        print(f"  Top amplified dims: {np.argmax(transformed[:32])}, {np.argmax(transformed[32:64])}")
