#!/usr/bin/env python3
"""
SIMPLE_HABITAT_DEMO.py

A simple demonstration of the complete "hat on a hat on a" experimental 
containment system, showing how to safely spawn, run, and manage nested
experimental systems.
"""

from experimental_habitat_implementation import ExperimentalHabitat, RecursiveMythEngine, ExperimentalSystem
import json

def main():
    print("🎩 'A HAT ON A HAT ON A' - EXPERIMENTAL CONTAINMENT DEMO")
    print("=" * 60)
    print("Creating layered experimental environments...")
    print()
    
    # Layer 1: Base Habitat (The first "hat")
    print("🎩 Layer 1: Creating base experimental habitat...")
    base_habitat = ExperimentalHabitat("base_creative_lab", isolation_level=1)
    print(f"   ✅ Base habitat established: {base_habitat.name}")
    
    # Spawn first experiment in base layer
    myth_engine = RecursiveMythEngine()
    base_containment = {
        'resources': {'cpu': '75%', 'memory': '1G'},
        'network_isolation': True,
        'recursive_depth_limit': 4
    }
    
    exp1_data = base_habitat.spawn_experiment(myth_engine, base_containment)
    print(f"   ✅ Experiment spawned: {myth_engine.name}")
    print(f"   🔒 Containment boundary: {myth_engine.boundary.get_full_path()}")
    print()
    
    # Layer 2: Nested Habitat (The second "hat")
    print("🎩 Layer 2: Creating nested habitat within experiment...")
    nested_habitat = base_habitat.nest_habitat(myth_engine.name, "recursive_analysis_lab")
    print(f"   ✅ Nested habitat created: {nested_habitat.name}")
    print(f"   📊 Nesting depth: {nested_habitat.nesting_depth}")
    print(f"   🔒 Isolation level: {nested_habitat.isolation_level}")
    
    # Spawn experiment in nested layer
    class PatternAnalyzer(ExperimentalSystem):
        def _execute_experiment(self):
            return {
                "patterns_found": ["recursive_mirror", "infinite_word", "nested_creation"],
                "analysis": "Mythic patterns exhibit self-referential stability",
                "confidence": 0.87
            }
    
    analyzer = PatternAnalyzer("pattern_analyzer", "Analyzing patterns from parent myth engine")
    nested_containment = {
        'resources': {'cpu': '50%', 'memory': '256M'},
        'network_isolation': True,
        'parent_dependency': myth_engine.name
    }
    
    exp2_data = nested_habitat.spawn_experiment(analyzer, nested_containment)
    print(f"   ✅ Nested experiment spawned: {analyzer.name}")
    print(f"   🔒 Nested boundary: {analyzer.boundary.get_full_path()}")
    print()
    
    # Layer 3: Double-nested Habitat (The third "hat")
    print("🎩 Layer 3: Creating double-nested habitat...")
    deep_habitat = nested_habitat.nest_habitat(analyzer.name, "deep_synthesis_lab")
    print(f"   ✅ Deep habitat created: {deep_habitat.name}")
    print(f"   📊 Nesting depth: {deep_habitat.nesting_depth}")
    print(f"   🔒 Isolation level: {deep_habitat.isolation_level}")
    
    # Spawn experiment in deepest layer
    class SynthesisEngine(ExperimentalSystem):
        def _execute_experiment(self):
            return {
                "synthesis": "Recursive patterns create stable meaning containers",
                "insight": "Each containment layer adds interpretive depth",
                "meta_observation": "The observer observing the observer observing patterns"
            }
    
    synthesizer = SynthesisEngine("synthesis_engine", "Synthesizing insights from nested analysis")
    deep_containment = {
        'resources': {'cpu': '25%', 'memory': '128M'},
        'network_isolation': True,
        'max_runtime': 60
    }
    
    exp3_data = deep_habitat.spawn_experiment(synthesizer, deep_containment)
    print(f"   ✅ Deep experiment spawned: {synthesizer.name}")
    print(f"   🔒 Deep boundary: {synthesizer.boundary.get_full_path()}")
    print()
    
    # Execute experiments from deepest to shallowest
    print("🚀 RUNNING EXPERIMENTS (deepest to shallowest)...")
    print("-" * 60)
    
    # Run deepest experiment first
    print("⚡ Running Layer 3: Synthesis Engine...")
    synthesis_result = deep_habitat.run_experiment(synthesizer.name)
    print("   📊 Synthesis Results:")
    for key, value in synthesis_result.items():
        print(f"      {key}: {value}")
    print()
    
    # Run nested experiment
    print("⚡ Running Layer 2: Pattern Analyzer...")
    analysis_result = nested_habitat.run_experiment(analyzer.name)
    print("   📊 Analysis Results:")
    for key, value in analysis_result.items():
        print(f"      {key}: {value}")
    print()
    
    # Run base experiment
    print("⚡ Running Layer 1: Recursive Myth Engine...")
    myth_result = base_habitat.run_experiment(myth_engine.name)
    print("   📊 Myth Generation Results:")
    print(f"      Generated myth: {myth_result['myth'][:100]}...")
    print(f"      Recursion depth: {myth_result['depth']}")
    print()
    
    # Show the complete hat stack status
    print("🎯 COMPLETE HAT STACK STATUS")
    print("-" * 60)
    
    print("📊 Base Habitat (Layer 1):")
    base_status = base_habitat.get_habitat_status()
    print(f"   Active experiments: {base_status['active_experiments']}")
    print(f"   Containment boundaries: {len(base_status['containment_boundaries'])}")
    
    print("📊 Nested Habitat (Layer 2):")
    nested_status = nested_habitat.get_habitat_status()
    print(f"   Active experiments: {nested_status['active_experiments']}")
    print(f"   Nesting depth: {nested_status['nesting_depth']}")
    print(f"   Containment boundaries: {len(nested_status['containment_boundaries'])}")
    
    print("📊 Deep Habitat (Layer 3):")
    deep_status = deep_habitat.get_habitat_status()
    print(f"   Active experiments: {deep_status['active_experiments']}")
    print(f"   Nesting depth: {deep_status['nesting_depth']}")
    print(f"   Containment boundaries: {len(deep_status['containment_boundaries'])}")
    print()
    
    # Graduate experiments upward
    print("🎓 GRADUATION PROCESS (deepest to shallowest)...")
    print("-" * 60)
    
    # Graduate synthesis to nested habitat
    print("🎓 Graduating synthesis engine to pattern analyzer level...")
    synthesis_package = deep_habitat.graduate_to_forge(synthesizer.name)
    print(f"   ✅ Synthesis patterns ready for integration")
    
    # Graduate analyzer to base habitat  
    print("🎓 Graduating pattern analyzer to base level...")
    analysis_package = nested_habitat.graduate_to_forge(analyzer.name)
    print(f"   ✅ Analysis patterns ready for integration")
    
    # Graduate myth engine to Code Forge
    print("🎓 Graduating myth engine to Code Forge...")
    myth_package = base_habitat.graduate_to_forge(myth_engine.name)
    print(f"   ✅ Myth engine patterns ready for production")
    print()
    
    # Show final summary
    print("🎉 HAT STACK EXPERIMENT COMPLETE!")
    print("=" * 60)
    print("Successfully demonstrated:")
    print("✅ Multi-layer experimental containment")
    print("✅ Nested habitat creation and management") 
    print("✅ Safe experiment execution at each layer")
    print("✅ Graduation of successful patterns upward")
    print("✅ Complete isolation and boundary management")
    print()
    print("The 'hat on a hat on a' containment system provides:")
    print("🎯 Progressive isolation levels for risk management")
    print("🎯 Recursive experimentation without contamination")
    print("🎯 Safe graduation paths for successful patterns")
    print("🎯 Complete failure containment and composting")
    print()
    
    # Cleanup
    print("🧹 Cleaning up experimental environments...")
    base_habitat.cleanup()
    nested_habitat.cleanup() 
    deep_habitat.cleanup()
    print("✅ All habitats cleaned up successfully")

if __name__ == "__main__":
    main()