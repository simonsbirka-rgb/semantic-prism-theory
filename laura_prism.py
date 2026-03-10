"""
Laura Matjošaitytė Prism Extraction
===================================

Converting real profile data into a 128D semantic prism.

This demonstrates how CCT can extract a user's worldview from
their professional profile, achievements, and behavioral patterns.
"""

import numpy as np
import json
from prism import UserPrism


def extract_prism_from_profile(profile_data: dict) -> UserPrism:
    """
    Extract a prism vector from a professional profile.
    
    The prism encodes:
    - Professional values (what they amplify)
    - Emotional orientation (how they relate)
    - Intellectual stance (abstract vs concrete)
    - Behavioral patterns (what they do)
    """
    
    # Initialize base vector
    vector = np.ones(128)
    bias = np.zeros(128)
    
    # ================================================================
    # PROFESSIONAL DIMENSIONS (0-31)
    # ================================================================
    
    # Dimensions 0-7: Authority & Leadership
    # Laura: Former VRK Chair, LRT Council, survived political pressure
    authority_score = 0.0
    if "chairperson" in str(profile_data).lower():
        authority_score += 0.3
    if "survived" in str(profile_data).lower() or "resilience" in str(profile_data).lower():
        authority_score += 0.4
    if "nominated by" in str(profile_data).lower():
        authority_score += 0.2
    vector[0:8] = 1.0 + authority_score  # Strong authority amplification
    
    # Dimensions 8-15: Expertise & Specialization
    # Laura: Election law, constitutional law - niche expertise
    expertise_areas = profile_data.get("services", [])
    if len(expertise_areas) > 3:
        vector[8:16] = 1.6  # High specialization
    else:
        vector[8:16] = 1.2
    
    # Dimensions 16-23: Risk Tolerance & Resilience
    # Laura: Survived no-confidence vote, didn't resign under pressure
    if "survived" in str(profile_data).lower() or "crisis" in str(profile_data).lower():
        vector[16:24] = 1.8  # Very high resilience
    else:
        vector[16:24] = 1.0
    
    # Dimensions 24-31: Institutional Knowledge
    # Laura: Insider - VRK, LRT, academic
    institutional_roles = len([r for r in str(profile_data).lower() if "council" in r or "chair" in r or "member" in r])
    if institutional_roles > 3:
        vector[24:31] = 1.7  # Deep institutional understanding
    
    # ================================================================
    # EMOTIONAL DIMENSIONS (32-63)
    # ================================================================
    
    # Dimensions 32-39: Trust & Integrity
    # Laura: "nesilanksta" (doesn't bend) - high integrity signal
    brand_tone = profile_data.get("brand_tone", "").lower()
    if "trusted" in brand_tone or "authoritative" in brand_tone:
        vector[32:40] = 1.9  # Strong trust amplification
    
    # Dimensions 40-47: Resilience Under Pressure
    # Laura: Survived political crisis without resignation
    if "pressure" in str(profile_data).lower() or "survived" in str(profile_data).lower():
        vector[40:48] = 2.0  # Maximum resilience
    
    # Dimensions 48-55: Communication Style
    # Laura: Lecturer, trainer, media commentator - communicates
    if "lecturer" in str(profile_data).lower() or "speaker" in str(profile_data).lower():
        vector[48:56] = 1.4  # Strong communicator
    
    # Dimensions 56-63: Emotional Control
    # Laura: Precise, analytical - controlled emotional expression
    if "analytical" in brand_tone or "precise" in str(profile_data).lower():
        vector[56:63] = 0.7  # Dampen emotional expression (professional distance)
    
    # ================================================================
    # INTELLECTUAL DIMENSIONS (64-95)
    # ================================================================
    
    # Dimensions 64-71: Abstract/Conceptual Thinking
    # Laura: Constitutional law, academic - high abstraction
    if "constitutional" in str(profile_data).lower() or "lecturer" in str(profile_data).lower():
        vector[64:72] = 1.6  # Strong abstract thinking
    
    # Dimensions 72-79: Strategic Orientation
    # Laura: Strategic approach mentioned, crisis management
    if "strategic" in str(profile_data).lower():
        vector[72:80] = 1.7  # Highly strategic
    
    # Dimensions 80-87: International Perspective
    # Laura: 4 languages, Council of Europe, international conferences
    languages = len(profile_data.get("languages", []))
    if languages >= 3:
        vector[80:88] = 1.5  # International orientation
    if "council of europe" in str(profile_data).lower():
        vector[80:88] += 0.2
    
    # Dimensions 88-95: Academic Rigor
    # Laura: Lecturer since 2016, trainer
    if "lecturer" in str(profile_data).lower() or "university" in str(profile_data).lower():
        vector[88:95] = 1.5  # Academic orientation
    
    # ================================================================
    # PHYSICAL/CONCRETE DIMENSIONS (96-127)
    # ================================================================
    
    # Dimensions 96-103: Tangible Results
    # Laura: Oversaw multiple elections, concrete achievements
    achievements = profile_data.get("positive_achievements", [])
    if len(achievements) > 5:
        vector[96:104] = 1.4  # Results-oriented
    
    # Dimensions 104-111: Practical Application
    # Laura: Private practice attorney, real cases
    if "attorney" in str(profile_data).lower() or "private practice" in str(profile_data).lower():
        vector[104:112] = 1.3  # Applied practice
    
    # Dimensions 112-119: Visibility & Public Presence
    # Laura: Media commentator, public figure
    if "media" in str(profile_data).lower() or "public" in str(profile_data).lower():
        vector[112:120] = 1.4  # Public presence
    
    # Dimensions 120-127: Concrete Outcomes
    # Laura: Real election oversight, real legal cases
    vector[120:127] = 1.2  # Concrete outcomes matter
    
    # ================================================================
    # BIAS CALCULATION
    # ================================================================
    
    # Professional bias (institutional worldview)
    bias[0:31] = 0.25  # Career lens bias
    
    # Trust/integrity bias
    bias[32:47] = 0.3  # Trust lens bias
    
    # Strategic bias
    bias[64:80] = 0.2  # Strategic thinking bias
    
    # ================================================================
    # CREATE PRISM
    # ================================================================
    
    prism = UserPrism(
        user_id="laura_001",
        name=profile_data.get("name", profile_data.get("business_name", "Unknown")),
        archetype="authority_resilient",
        vector=vector,
        bias=bias,
        metadata={
            "description": f"Attorney with {profile_data.get('background', 'public-sector experience')}",
            "language_style": "precise, authoritative, strategic",
            "key_concepts": extract_key_concepts(profile_data),
            "profile_source": "extracted_from_real_data"
        }
    )
    
    return prism


def extract_key_concepts(profile_data: dict) -> list:
    """Extract key concepts from profile for interpretation."""
    concepts = []
    
    if "constitutional" in str(profile_data).lower():
        concepts.append("constitutional_expertise")
    if "election" in str(profile_data).lower():
        concepts.append("electoral_authority")
    if "survived" in str(profile_data).lower() or "resilience" in str(profile_data).lower():
        concepts.append("unbending_resilience")
    if "lecturer" in str(profile_data).lower():
        concepts.append("academic_rigor")
    if "international" in str(profile_data).lower() or "council of europe" in str(profile_data).lower():
        concepts.append("international_recognition")
    if "crisis" in str(profile_data).lower():
        concepts.append("crisis_management")
    
    return concepts if concepts else ["authority", "expertise", "trust"]


# ================================================================
# LAURA'S ACTUAL PROFILE DATA
# ================================================================

LAURA_PROFILE = {
    "name": "Laura Matjošaitytė",
    "business_name": "Laura Matjošaitytė",
    "location": "Lithuania",
    "industry": "Attorney-at-Law & Election Expert",
    "background": "Former Chairwoman of VRK (Central Electoral Commission). LRT Council Member. Lecturer at Mykolas Romeris University.",
    "services": [
        "Administrative & Constitutional Law",
        "Election Law & Consulting",
        "Civil & Commercial Litigation",
        "Labor Law & Contract Negotiation",
        "Crisis Management & Reputation Defense"
    ],
    "brand_tone": "Highly Authoritative, Analytical, Trusted, Public-Sector Tested",
    "languages": ["Lithuanian", "English", "Russian", "German"],
    "keywords": [
        "Constitutional law",
        "Election expert",
        "VRK pirmininkė",
        "Legal thought leadership",
        "Crisis management"
    ],
    "key_achievements": [
        "VRK Chairperson (2017-2021)",
        "Survived no-confidence vote without resignation",
        "LRT Council Member (until 2028)",
        "Council of Europe electoral bodies roster",
        "MRU Lecturer since 2016"
    ]
}


if __name__ == "__main__":
    from prism import create_test_prisms, create_semantic_coordinates
    from refract import refract, compare_refractions, calculate_distance
    
    print("=" * 70)
    print("CCT EXPERIMENT: LAURA MATJOŠAITYTĖ PRISM")
    print("=" * 70)
    
    # Extract Laura's prism from profile
    laura_prism = extract_prism_from_profile(LAURA_PROFILE)
    
    print(f"\nExtracted Prism for: {laura_prism.name}")
    print(f"Archetype: {laura_prism.archetype}")
    print(f"Key Concepts: {laura_prism.metadata['key_concepts']}")
    
    # Get test prisms for comparison
    test_prisms = create_test_prisms()
    
    # Compare with test prisms
    print("\n" + "-" * 70)
    print("PRISM SIMILARITY ANALYSIS")
    print("-" * 70)
    
    for name, prism in test_prisms.items():
        # Cosine similarity
        v1 = laura_prism.vector
        v2 = prism.vector
        similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        print(f"\nLaura ↔ {prism.name} ({prism.archetype}):")
        print(f"  Similarity: {similarity:.3f}")
        print(f"  Interpretation: {'Similar worldview' if similarity > 0.9 else 'Different worldview'}")
    
    # Test refraction on key concepts
    print("\n" + "-" * 70)
    print("REFRACTION TEST: 'SUCCESS' THROUGH LAURA'S PRISM")
    print("-" * 70)
    
    result = refract("success", laura_prism)
    if result:
        print(f"\nConcept: {result.concept}")
        print(f"Magnitude: {result.magnitude:.3f}")
        print(f"Dominant Dimensions: {result.dominant_dimensions}")
        print(f"\nInterpretation:")
        print(f"  Primary Lens: {result.interpretation_hints['primary_lens']}")
        print(f"  Secondary Lens: {result.interpretation_hints['secondary_lens']}")
        
        # Generate Laura-specific interpretation
        print(f"\n  For Laura, SUCCESS = Authority + Resilience + Recognition")
        print(f"  Magnitude {result.magnitude:.2f} indicates strong resonance with this concept")
        print(f"  Primary lens '{result.interpretation_hints['primary_lens']}' = professional achievement")
    
    # Test on other concepts
    print("\n" + "-" * 70)
    print("MULTI-CONCEPT REFRACTION")
    print("-" * 70)
    
    concepts = ["success", "freedom", "authority", "trust", "meaning"]
    print(f"\n{'Concept':<15} {'Magnitude':<12} {'Primary Lens':<20}")
    print("-" * 50)
    
    for concept in concepts:
        r = refract(concept, laura_prism)
        if r:
            print(f"{concept:<15} {r.magnitude:<12.3f} {r.interpretation_hints['primary_lens']:<20}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(f"""
Laura's prism shows:
- High authority/resilience amplification (survived political crisis)
- Strong professional orientation (institutional insider)
- Intellectual rigor (academic, constitutional law)
- Trust and integrity as core values

The prism extraction captures her real-world profile:
{', '.join(laura_prism.metadata['key_concepts'])}
""")
