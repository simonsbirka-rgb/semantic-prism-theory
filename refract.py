"""
CCT PoC - Refraction Module

The core operation: P_u(ω) = ∂ω/∂u

Refraction is how a prism transforms a semantic coordinate into personal meaning.

This module implements the mathematical operations.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass

# Import from prism module
from prism import UserPrism, get_coordinate


@dataclass
class RefractionResult:
    """Result of a refraction operation."""
    original_coordinate: np.ndarray
    transformed_coordinate: np.ndarray
    prism: UserPrism
    concept: str
    magnitude: float
    dominant_dimensions: Dict[str, float]
    interpretation_hints: Dict[str, Any]


def refract(
    concept: str,
    prism: UserPrism,
    method: str = "standard"
) -> Optional[RefractionResult]:
    """
    Apply a prism to a semantic coordinate.
    
    This is the core CCT operation: P_u(ω) = Φ_u(ω)
    
    Args:
        concept: The concept to refract (e.g., "success", "freedom")
        prism: The user's prism (transformation)
        method: Refraction method ("standard", "nonlinear", "attention")
    
    Returns:
        RefractionResult with transformed coordinate and metadata
    """
    # Get the semantic coordinate
    coordinate = get_coordinate(concept)
    if coordinate is None:
        return None
    
    # Apply transformation based on method
    if method == "standard":
        transformed = _refract_standard(coordinate, prism)
    elif method == "nonlinear":
        transformed = _refract_nonlinear(coordinate, prism)
    elif method == "attention":
        transformed = _refract_attention(coordinate, prism)
    else:
        transformed = _refract_standard(coordinate, prism)
    
    # Calculate metrics
    magnitude = np.linalg.norm(transformed)
    
    # Find dominant dimensions
    dominant = _find_dominant_dimensions(transformed)
    
    # Generate interpretation hints
    hints = _generate_hints(transformed, prism, concept)
    
    return RefractionResult(
        original_coordinate=coordinate,
        transformed_coordinate=transformed,
        prism=prism,
        concept=concept,
        magnitude=magnitude,
        dominant_dimensions=dominant,
        interpretation_hints=hints
    )


def _refract_standard(coordinate: np.ndarray, prism: UserPrism) -> np.ndarray:
    """
    Standard refraction: element-wise modulation + bias.
    
    P_u(ω) = ω * Φ_u + bias
    
    This amplifies or dampens each dimension based on the prism.
    """
    modulated = coordinate * prism.vector
    shifted = modulated + prism.bias
    return shifted


def _refract_nonlinear(coordinate: np.ndarray, prism: UserPrism) -> np.ndarray:
    """
    Nonlinear refraction: applies tanh to bound values.
    
    P_u(ω) = tanh(ω * Φ_u + bias)
    
    This creates more extreme amplification/dampening.
    """
    modulated = coordinate * prism.vector + prism.bias
    bounded = np.tanh(modulated)
    return bounded


def _refract_attention(coordinate: np.ndarray, prism: UserPrism) -> np.ndarray:
    """
    Attention-style refraction: uses prism to "attend" to dimensions.
    
    This is more sophisticated - the prism acts as query/key.
    """
    # Normalize prism to create attention weights
    attention = prism.vector / (prism.vector.sum() + 1e-8)
    
    # Weight the coordinate
    weighted = coordinate * attention * len(coordinate)
    
    # Add residual connection
    result = coordinate + 0.5 * (weighted - coordinate)
    
    return result


def _find_dominant_dimensions(transformed: np.ndarray, top_k: int = 5) -> Dict[str, float]:
    """
    Find the most amplified dimensions after transformation.
    
    Returns dimension ranges and their average values.
    """
    # Define dimension ranges (conceptual)
    ranges = {
        "professional": (0, 31),
        "emotional": (32, 63),
        "intellectual": (64, 95),
        "physical": (96, 127)
    }
    
    dominant = {}
    for name, (start, end) in ranges.items():
        avg = transformed[start:end].mean()
        dominant[name] = float(avg)
    
    return dominant


def _generate_hints(
    transformed: np.ndarray, 
    prism: UserPrism, 
    concept: str
) -> Dict[str, Any]:
    """
    Generate interpretation hints for the transformed meaning.
    
    These help humans understand what the transformation "means".
    """
    dominant = _find_dominant_dimensions(transformed)
    
    # Sort by dominance
    sorted_dims = sorted(dominant.items(), key=lambda x: x[1], reverse=True)
    
    # Generate hints based on prism archetype and dominant dimensions
    hints = {
        "primary_lens": sorted_dims[0][0],
        "secondary_lens": sorted_dims[1][0],
        "amplified": [dim for dim, val in sorted_dims if val > 0.7],
        "dampened": [dim for dim, val in sorted_dims if val < 0.5],
        "archetype": prism.archetype,
        "language_style": prism.metadata.get("language_style", "neutral"),
        "key_concepts": prism.metadata.get("key_concepts", [])
    }
    
    return hints


def compare_refractions(
    concept: str,
    prisms: list,
    method: str = "standard"
) -> Dict[str, RefractionResult]:
    """
    Refract a concept through multiple prisms.
    
    This shows how the same semantic coordinate produces different
    personal meanings for different observers.
    """
    results = {}
    for prism in prisms:
        result = refract(concept, prism, method)
        if result:
            results[prism.archetype] = result
    return results


def calculate_distance(result1: RefractionResult, result2: RefractionResult) -> float:
    """
    Calculate semantic distance between two refractions.
    
    This measures how differently two prisms interpret the same concept.
    """
    diff = result1.transformed_coordinate - result2.transformed_coordinate
    return float(np.linalg.norm(diff))


def calculate_prism_similarity(prism1: UserPrism, prism2: UserPrism) -> float:
    """
    Calculate similarity between two prisms.
    
    Higher = more similar worldview.
    """
    # Cosine similarity of prism vectors
    v1 = prism1.vector
    v2 = prism2.vector
    
    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return float(similarity)


# ============================================================================
# BRIDGE CALCULATION (Prism Intersection)
# ============================================================================

def calculate_bridge(prism1: UserPrism, prism2: UserPrism) -> np.ndarray:
    """
    Calculate the "bridge" between two prisms.
    
    F_bridge = F₁ ∩ F₂
    
    This represents shared meaning - where both prisms align.
    
    The bridge is useful for:
    - Communication between different worldviews
    - Finding common ground
    - Translation between perspectives
    """
    # Intersection: element-wise minimum
    bridge = np.minimum(prism1.vector, prism2.vector)
    
    # Also consider shared bias
    shared_bias = (prism1.bias + prism2.bias) / 2
    
    # Combined bridge
    bridge_vector = bridge + 0.3 * shared_bias
    
    return bridge_vector


def bridge_refract(
    concept: str,
    prism1: UserPrism,
    prism2: UserPrism
) -> Tuple[Optional[RefractionResult], np.ndarray]:
    """
    Refract a concept through the bridge of two prisms.
    
    This shows what meaning is shared between two observers.
    """
    bridge = calculate_bridge(prism1, prism2)
    
    # Create a temporary "bridge prism"
    bridge_prism = UserPrism(
        user_id="bridge",
        name=f"Bridge({prism1.name}, {prism2.name})",
        archetype="bridge",
        vector=bridge,
        bias=np.zeros(128),
        metadata={"type": "intersection"}
    )
    
    result = refract(concept, bridge_prism)
    return result, bridge


if __name__ == "__main__":
    from prism import create_test_prisms
    
    print("=" * 60)
    print("CCT PoC - Refraction Module Test")
    print("=" * 60)
    
    prisms = create_test_prisms()
    
    print("\n" + "-" * 60)
    print("Test 1: Single refraction")
    print("-" * 60)
    
    result = refract("success", prisms["entrepreneur"])
    if result:
        print(f"Concept: {result.concept}")
        print(f"Prism: {result.prism.name}")
        print(f"Magnitude: {result.magnitude:.3f}")
        print(f"Dominant dimensions: {result.dominant_dimensions}")
        print(f"Interpretation hints: {result.interpretation_hints}")
    
    print("\n" + "-" * 60)
    print("Test 2: Compare refractions")
    print("-" * 60)
    
    results = compare_refractions("success", list(prisms.values()))
    for archetype, res in results.items():
        print(f"\n{archetype}:")
        print(f"  Magnitude: {res.magnitude:.3f}")
        print(f"  Primary lens: {res.interpretation_hints['primary_lens']}")
    
    print("\n" + "-" * 60)
    print("Test 3: Distance calculation")
    print("-" * 60)
    
    dist = calculate_distance(results["entrepreneur"], results["artist"])
    print(f"Distance between entrepreneur and artist (on 'success'): {dist:.3f}")
    
    print("\n" + "-" * 60)
    print("Test 4: Bridge calculation")
    print("-" * 60)
    
    bridge_result, bridge_vector = bridge_refract(
        "success",
        prisms["entrepreneur"],
        prisms["artist"]
    )
    print(f"Bridge vector mean: {bridge_vector.mean():.3f}")
    if bridge_result:
        print(f"Bridge interpretation: {bridge_result.dominant_dimensions}")
