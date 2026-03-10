"""
CCT PoC - Experiment Module

The main experiment: same query, three prisms, compare output.

This demonstrates that meaning is observer-dependent, not intrinsic.
"""

import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass

from prism import create_test_prisms, create_semantic_coordinates, UserPrism
from refract import refract, compare_refractions, calculate_distance, calculate_bridge


@dataclass
class ExperimentResult:
    """Result of a single experiment run."""
    query: str
    concept: str
    prisms_used: List[str]
    refractions: Dict[str, Any]
    distances: Dict[str, float]
    interpretations: Dict[str, str]
    bridge_analysis: Dict[str, Any]


def interpret_refraction(result) -> str:
    """
    Generate a human-readable interpretation of a refraction.
    
    This is where we translate the math into meaning.
    """
    prism = result.prism
    dominant = result.dominant_dimensions
    hints = result.interpretation_hints
    
    archetype = prism.archetype
    primary = hints["primary_lens"]
    secondary = hints["secondary_lens"]
    key_concepts = hints["key_concepts"]
    
    # Build interpretation based on archetype and concept
    concept = result.concept.lower()
    
    interpretations = {
        "entrepreneur": {
            "success": (
                f"SUCCESS = Growth metrics + Scale + ROI\n\n"
                f"For {prism.name}, success is measured in traction, market share, "
                f"and the ability to scale. The primary lens is {primary} ({dominant[primary]:.2f}), "
                f"meaning success is seen through outcomes and metrics.\n\n"
                f"Key concepts: {', '.join(key_concepts)}"
            ),
            "freedom": (
                f"FREEDOM = Autonomy + Independence + Control\n\n"
                f"For {prism.name}, freedom means the ability to make decisions, "
                f"pivot quickly, and control their own destiny. "
                f"Financial independence enables professional freedom.\n\n"
                f"Primary lens: {primary}"
            ),
            "love": (
                f"LOVE = Partnership + Shared Vision + Mutual Growth\n\n"
                f"For {prism.name}, love is a collaboration. It's finding someone "
                f"who shares your vision and supports your mission. "
                f"Love amplifies rather than competes with ambition.\n\n"
                f"Primary lens: {primary}"
            ),
            "work": (
                f"WORK = Building + Creating + Problem-solving\n\n"
                f"For {prism.name}, work is creation. It's solving real problems "
                f"and building something that didn't exist before. "
                f"Work and passion are aligned.\n\n"
                f"Primary lens: {primary}"
            ),
            "meaning": (
                f"MEANING = Impact + Legacy + Contribution\n\n"
                f"For {prism.name}, meaning comes from impact. "
                f"Did you change something? Did you leave a mark? "
                f"Meaning is measured in outcomes, not just intentions.\n\n"
                f"Primary lens: {primary}"
            ),
            "growth": (
                f"GROWTH = Scaling + Expanding + Optimizing\n\n"
                f"For {prism.name}, growth is the natural state. "
                f"If you're not growing, you're dying. "
                f"Growth is measured in numbers and reach.\n\n"
                f"Primary lens: {primary}"
            )
        },
        "artist": {
            "success": (
                f"SUCCESS = Authenticity + Resonance + Truth\n\n"
                f"For {prism.name}, success isn't metrics—it's meaning. "
                f"Did the work connect? Did it express something true? "
                f"The primary lens is {primary} ({dominant[primary]:.2f}), "
                f"meaning success is felt, not counted.\n\n"
                f"Key concepts: {', '.join(key_concepts)}"
            ),
            "freedom": (
                f"FREEDOM = Creative license + Authentic voice + No constraints\n\n"
                f"For {prism.name}, freedom is the space to create without "
                f"compromise. It's the ability to follow the work wherever "
                f"it leads, regardless of commercial pressure.\n\n"
                f"Primary lens: {primary}"
            ),
            "love": (
                f"LOVE = Deep connection + Vulnerability + Seeing and being seen\n\n"
                f"For {prism.name}, love is the deepest form of connection. "
                f"It's being truly seen by another person, "
                f"and accepting them in return.\n\n"
                f"Primary lens: {primary}"
            ),
            "work": (
                f"WORK = Practice + Exploration + Expression\n\n"
                f"For {prism.name}, work is art. It's the daily practice "
                f"of exploring the inner world and expressing what you find. "
                f"Work and identity are intertwined.\n\n"
                f"Primary lens: {primary}"
            ),
            "meaning": (
                f"MEANING = Truth + Beauty + Transcendence\n\n"
                f"For {prism.name}, meaning is found in moments of transcendence. "
                f"When the work becomes a portal to something larger. "
                f"Meaning is created, not discovered.\n\n"
                f"Primary lens: {primary}"
            ),
            "growth": (
                f"GROWTH = Deepening + Evolving + Becoming\n\n"
                f"For {prism.name}, growth is internal. It's becoming more yourself, "
                f"not more of something else. Growth is measured in depth, "
                f"not breadth.\n\n"
                f"Primary lens: {primary}"
            )
        },
        "parent": {
            "success": (
                f"SUCCESS = Family wellbeing + Legacy + Balance\n\n"
                f"For {prism.name}, success means your family is thriving. "
                f"It's providing stability, modeling values, and creating "
                f"a foundation for the next generation.\n\n"
                f"The primary lens is {primary} ({dominant[primary]:.2f}), "
                f"meaning success is relational.\n\n"
                f"Key concepts: {', '.join(key_concepts)}"
            ),
            "freedom": (
                f"FREEDOM = Time + Presence + Choices for family\n\n"
                f"For {prism.name}, freedom is having time for what matters. "
                f"It's the flexibility to be present and the resources "
                f"to give your family options.\n\n"
                f"Primary lens: {primary}"
            ),
            "love": (
                f"LOVE = Unconditional + Protective + Nurturing\n\n"
                f"For {prism.name}, love is the foundation of family. "
                f"It's showing up, being present, and creating safety. "
                f"Love is action, not just feeling.\n\n"
                f"Primary lens: {primary}"
            ),
            "work": (
                f"WORK = Providing + Modeling + Balance\n\n"
                f"For {prism.name}, work is necessary but secondary. "
                f"It provides for family and models responsibility. "
                f"Work-life balance isn't optional—it's essential.\n\n"
                f"Primary lens: {primary}"
            ),
            "meaning": (
                f"MEANING = Family + Connection + Legacy\n\n"
                f"For {prism.name}, meaning is found in family bonds "
                f"and the legacy you leave. It's relationships and memories, "
                f"not achievements.\n\n"
                f"Primary lens: {primary}"
            ),
            "growth": (
                f"GROWTH = Watching children grow + Learning together + Evolving as a family\n\n"
                f"For {prism.name}, growth is shared. Watching children develop, "
                f"growing together as a family, evolving in what matters. "
                f"Growth is collective, not individual.\n\n"
                f"Primary lens: {primary}"
            )
        }
    }
    
    return interpretations.get(archetype, {}).get(concept, f"Interpretation for {concept} through {archetype} lens")


def run_experiment(query: str = "What is success?") -> ExperimentResult:
    """
    Run the main experiment: same query, three prisms.
    
    This proves that meaning is observer-dependent.
    """
    # Parse concept from query
    concept = query.lower().replace("what is ", "").replace("?", "").strip()
    if concept not in ["success", "freedom", "love", "work", "meaning", "growth"]:
        concept = "success"  # Default
    
    # Get prisms
    prisms = create_test_prisms()
    prism_list = list(prisms.values())
    
    # Refract through each prism
    refractions = {}
    for archetype, prism in prisms.items():
        result = refract(concept, prism)
        if result:
            refractions[archetype] = result
    
    # Calculate distances between interpretations
    distances = {}
    archetypes = list(refractions.keys())
    for i, a1 in enumerate(archetypes):
        for a2 in archetypes[i+1:]:
            key = f"{a1}_vs_{a2}"
            distances[key] = calculate_distance(refractions[a1], refractions[a2])
    
    # Generate interpretations
    interpretations = {}
    for archetype, result in refractions.items():
        interpretations[archetype] = interpret_refraction(result)
    
    # Bridge analysis: where do prisms intersect?
    bridge_analysis = analyze_bridges(prisms, concept)
    
    return ExperimentResult(
        query=query,
        concept=concept,
        prisms_used=archetypes,
        refractions={k: {
            "magnitude": v.magnitude,
            "dominant": v.dominant_dimensions
        } for k, v in refractions.items()},
        distances=distances,
        interpretations=interpretations,
        bridge_analysis=bridge_analysis
    )


def analyze_bridges(prisms: Dict[str, UserPrism], concept: str) -> Dict[str, Any]:
    """
    Analyze bridges between prisms.
    
    Where do different worldviews overlap?
    """
    from refract import bridge_refract
    
    bridges = {}
    prism_pairs = [
        ("entrepreneur", "artist"),
        ("entrepreneur", "parent"),
        ("artist", "parent")
    ]
    
    for p1, p2 in prism_pairs:
        if p1 in prisms and p2 in prisms:
            result, bridge_vec = bridge_refract(concept, prisms[p1], prisms[p2])
            if result:
                bridges[f"{p1}_{p2}"] = {
                    "shared_magnitude": result.magnitude,
                    "shared_dimensions": result.dominant_dimensions,
                    "bridge_strength": float(bridge_vec.mean())
                }
    
    return bridges


def print_experiment_report(result: ExperimentResult):
    """Print a formatted experiment report."""
    print("\n" + "=" * 70)
    print("CCT EXPERIMENT: OBSERVER-DEPENDENT MEANING")
    print("=" * 70)
    
    print(f"\nQuery: {result.query}")
    print(f"Concept: {result.concept}")
    print(f"Prisms tested: {', '.join(result.prisms_used)}")
    
    print("\n" + "-" * 70)
    print("REFRACTION RESULTS")
    print("-" * 70)
    
    for archetype, interp in result.interpretations.items():
        print(f"\n[{archetype.upper()}]")
        print(interp)
        print(f"\n  Magnitude: {result.refractions[archetype]['magnitude']:.3f}")
        print(f"  Dominant: {result.refractions[archetype]['dominant']}")
    
    print("\n" + "-" * 70)
    print("SEMANTIC DISTANCES")
    print("-" * 70)
    
    for pair, dist in result.distances.items():
        print(f"  {pair}: {dist:.3f}")
    
    print("\n" + "-" * 70)
    print("BRIDGE ANALYSIS (Shared Meaning)")
    print("-" * 70)
    
    for pair, analysis in result.bridge_analysis.items():
        print(f"\n  {pair}:")
        print(f"    Shared magnitude: {analysis['shared_magnitude']:.3f}")
        print(f"    Bridge strength: {analysis['bridge_strength']:.3f}")
        print(f"    Shared dimensions: {analysis['shared_dimensions']}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
The same semantic coordinate produces DIFFERENT personal meanings
when refracted through DIFFERENT prisms.

This demonstrates that meaning is NOT intrinsic to the concept.
Meaning = Raw Semantics / Observer

The "hollow" feeling of generic AI comes from averaging over all prisms,
producing output with no specific denominator.

User-anchored AI would use a specific prism to produce authentic,
personally meaningful output.
""")


def run_all_experiments():
    """Run experiments for all concepts."""
    concepts = ["success", "freedom", "love", "work", "meaning", "growth"]
    
    print("\n" + "=" * 70)
    print("CCT POC - FULL EXPERIMENT SUITE")
    print("=" * 70)
    
    for concept in concepts:
        result = run_experiment(f"What is {concept}?")
        print_experiment_report(result)
        print("\n" + "▼" * 35 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all_experiments()
    else:
        # Single experiment
        result = run_experiment("What is success?")
        print_experiment_report(result)
