#!/usr/bin/env python3
"""
EXPERIMENTAL_HABITAT_IMPLEMENTATION.py

A practical implementation of the Experimental Habitat system for containing
and managing experimental systems in nested, isolated environments.

This is the "hat on a hat on a" containment engine - each layer provides
additional isolation and structure for safe experimentation.
"""

import json
import os
import subprocess
import tempfile
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContainmentBoundary:
    """Represents an isolation boundary for experimental systems"""
    
    def __init__(self, name: str, level: int, parent: Optional['ContainmentBoundary'] = None):
        self.name = name
        self.level = level
        self.parent = parent
        self.children: List['ContainmentBoundary'] = []
        self.created = datetime.now().isoformat()
        self.active = True
        
        if parent:
            parent.children.append(self)
    
    def get_full_path(self) -> str:
        """Get the full containment path (hat stack)"""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name
    
    def breach_detected(self) -> bool:
        """Check for containment breaches"""
        # Placeholder for actual breach detection logic
        return False

class ExperimentalSystem:
    """Base class for experimental systems"""
    
    def __init__(self, name: str, hypothesis: str):
        self.name = name
        self.hypothesis = hypothesis
        self.status = "spawning"
        self.created = datetime.now().isoformat()
        self.results = {}
        self.failures = []
        self.resource_usage = {}
        self.boundary: Optional[ContainmentBoundary] = None
        
    def run(self) -> Dict[str, Any]:
        """Run the experimental system"""
        try:
            self.status = "running"
            logger.info(f"Running experiment: {self.name}")
            
            # This would be overridden by specific experiments
            result = self._execute_experiment()
            
            self.status = "completed"
            self.results = result
            return result
            
        except Exception as e:
            self.status = "failed"
            self.failures.append({
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "context": "experiment_execution"
            })
            raise
    
    def _execute_experiment(self) -> Dict[str, Any]:
        """Override this method in specific experiments"""
        return {"message": "Base experiment completed", "success": True}

class RecursiveMythEngine(ExperimentalSystem):
    """Example experimental system: A recursive myth generation engine"""
    
    def __init__(self):
        super().__init__(
            name="recursive_myth_engine",
            hypothesis="Myths can be recursively generated using self-referential patterns"
        )
        self.depth = 0
        self.max_depth = 3
        
    def _execute_experiment(self) -> Dict[str, Any]:
        """Generate recursive mythic patterns"""
        logger.info(f"Generating myth at depth {self.depth}")
        
        if self.depth >= self.max_depth:
            return {"myth": f"At depth {self.depth}, the mirror reflects itself infinitely", "depth": self.depth}
        
        # Recursive myth generation
        self.depth += 1
        nested_result = self._execute_experiment()
        
        return {
            "myth": f"In the beginning was the word, and the word contained: {nested_result['myth']}",
            "depth": self.depth,
            "nested": nested_result
        }

class ExperimentalHabitat:
    """Main habitat for containing experimental systems"""
    
    def __init__(self, name: str, isolation_level: int = 3):
        self.name = name
        self.isolation_level = isolation_level
        self.active_experiments: Dict[str, Any] = {}
        self.graduated_patterns: Dict[str, Any] = {}
        self.failed_experiments: Dict[str, Any] = {}
        self.nesting_depth = 0
        self.containment_boundaries: Dict[str, ContainmentBoundary] = {}
        self.temp_dir = tempfile.mkdtemp(prefix=f"habitat_{name}_")
        logger.info(f"Habitat {name} established at {self.temp_dir}")
        
    def spawn_experiment(self, experiment: ExperimentalSystem, containment_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Spawn a new experimental system within containment boundaries"""
        
        # Create containment boundary
        boundary = ContainmentBoundary(
            name=f"boundary_{experiment.name}",
            level=self.isolation_level
        )
        experiment.boundary = boundary
        self.containment_boundaries[experiment.name] = boundary
        
        # Set up resource limits
        resource_limits = containment_rules.get('resources', {})
        experiment.resource_limits = resource_limits
        
        # Create isolated workspace
        exp_dir = os.path.join(self.temp_dir, experiment.name)
        os.makedirs(exp_dir, exist_ok=True)
        
        experiment_data = {
            'experiment': experiment,
            'containment_rules': containment_rules,
            'workspace': exp_dir,
            'status': 'spawned',
            'spawned_at': datetime.now().isoformat(),
            'boundary': boundary
        }
        
        self.active_experiments[experiment.name] = experiment_data
        logger.info(f"Spawned experiment {experiment.name} in isolation level {self.isolation_level}")
        
        return experiment_data
    
    def run_experiment(self, experiment_name: str) -> Dict[str, Any]:
        """Run a contained experiment"""
        if experiment_name not in self.active_experiments:
            raise ValueError(f"Experiment {experiment_name} not found in habitat")
        
        exp_data = self.active_experiments[experiment_name]
        experiment = exp_data['experiment']
        
        # Check containment boundary
        if experiment.boundary and experiment.boundary.breach_detected():
            raise RuntimeError(f"Containment breach detected for {experiment_name}")
        
        try:
            # Monitor resource usage during execution
            start_time = time.time()
            result = experiment.run()
            execution_time = time.time() - start_time
            
            # Update experiment data
            exp_data['status'] = experiment.status
            exp_data['result'] = result
            exp_data['execution_time'] = execution_time
            exp_data['completed_at'] = datetime.now().isoformat()
            
            logger.info(f"Experiment {experiment_name} completed in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            exp_data['status'] = 'failed'
            exp_data['error'] = str(e)
            exp_data['failed_at'] = datetime.now().isoformat()
            logger.error(f"Experiment {experiment_name} failed: {e}")
            raise
    
    def nest_habitat(self, parent_experiment: str, child_name: str) -> 'ExperimentalHabitat':
        """Create a nested habitat within an existing experiment"""
        if parent_experiment not in self.active_experiments:
            raise ValueError(f"Parent experiment {parent_experiment} not found")
        
        parent_boundary = self.containment_boundaries[parent_experiment]
        
        nested_habitat = ExperimentalHabitat(
            name=f"{self.name}_nested_{child_name}",
            isolation_level=self.isolation_level + 1
        )
        nested_habitat.nesting_depth = self.nesting_depth + 1
        
        # Create nested boundary
        nested_boundary = ContainmentBoundary(
            name=f"nested_{child_name}",
            level=self.isolation_level + 1,
            parent=parent_boundary
        )
        
        logger.info(f"Created nested habitat {child_name} at depth {nested_habitat.nesting_depth}")
        return nested_habitat
    
    def graduate_to_forge(self, experiment_name: str) -> Dict[str, Any]:
        """Graduate a successful experiment to the Code Forge"""
        if experiment_name not in self.active_experiments:
            raise ValueError(f"Experiment {experiment_name} not found")
        
        exp_data = self.active_experiments.pop(experiment_name)
        exp_data['status'] = 'graduated'
        exp_data['graduated_at'] = datetime.now().isoformat()
        
        # Package for Code Forge
        forge_package = {
            'name': experiment_name,
            'experiment_data': exp_data,
            'code_patterns': self._extract_patterns(exp_data),
            'symbolic_mappings': self._extract_symbols(exp_data),
            'integration_hooks': self._create_integration_hooks(exp_data)
        }
        
        self.graduated_patterns[experiment_name] = forge_package
        logger.info(f"Experiment {experiment_name} graduated to Code Forge")
        
        return forge_package
    
    def contain_failure(self, experiment_name: str, failure_reason: str) -> Dict[str, Any]:
        """Safely contain and compost a failed experiment"""
        if experiment_name not in self.active_experiments:
            raise ValueError(f"Experiment {experiment_name} not found")
        
        exp_data = self.active_experiments.pop(experiment_name)
        exp_data['status'] = 'composted'
        exp_data['failure_reason'] = failure_reason
        exp_data['composted_at'] = datetime.now().isoformat()
        exp_data['lessons'] = self._extract_lessons(exp_data)
        
        self.failed_experiments[experiment_name] = exp_data
        logger.info(f"Experiment {experiment_name} safely contained and composted")
        
        return exp_data['lessons']
    
    def get_habitat_status(self) -> Dict[str, Any]:
        """Get current habitat status"""
        return {
            'name': self.name,
            'isolation_level': self.isolation_level,
            'nesting_depth': self.nesting_depth,
            'active_experiments': len(self.active_experiments),
            'graduated_patterns': len(self.graduated_patterns),
            'failed_experiments': len(self.failed_experiments),
            'containment_boundaries': [b.get_full_path() for b in self.containment_boundaries.values()],
            'workspace': self.temp_dir
        }
    
    def _extract_patterns(self, exp_data: Dict[str, Any]) -> List[str]:
        """Extract reusable code patterns from experiment"""
        # Placeholder for pattern extraction logic
        return ["recursive_structure", "containment_protocol", "mythic_generator"]
    
    def _extract_symbols(self, exp_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract symbolic mappings from experiment"""
        return {
            "experiment_archetype": "recursive_creator",
            "mythic_function": "pattern_generator",
            "symbolic_resonance": "mirror_infinite"
        }
    
    def _create_integration_hooks(self, exp_data: Dict[str, Any]) -> List[str]:
        """Create hooks for integrating with other systems"""
        return [
            "forge_integration_point",
            "echo_shell_connection", 
            "mirror_cabinet_link"
        ]
    
    def _extract_lessons(self, exp_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract lessons from failed experiments"""
        experiment = exp_data.get('experiment')
        return {
            'what_failed': exp_data.get('error', 'Unknown'),
            'failure_patterns': experiment.failures if experiment else [],
            'resource_issues': exp_data.get('resource_issues', []),
            'containment_breaches': exp_data.get('breaches', []),
            'wisdom_gained': [
                "Recursive depth limits are important",
                "Symbolic patterns need validation",
                "Containment boundaries must be monitored"
            ],
            'reusable_components': self._extract_patterns(exp_data)
        }
    
    def cleanup(self):
        """Clean up habitat resources"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        logger.info(f"Habitat {self.name} cleaned up")

def demonstrate_experimental_habitat():
    """Demonstrate the experimental habitat system"""
    print("🧪 EXPERIMENTAL HABITAT DEMONSTRATION")
    print("=" * 50)
    
    # Create main habitat
    main_lab = ExperimentalHabitat("main_experimental_lab", isolation_level=3)
    print(f"Created habitat: {main_lab.name}")
    
    # Create experimental system
    myth_engine = RecursiveMythEngine()
    print(f"Created experiment: {myth_engine.name}")
    
    # Spawn experiment in habitat
    containment_rules = {
        'resources': {'cpu': '50%', 'memory': '512M'},
        'network_isolation': True,
        'time_limit': 30,
        'recursive_depth_limit': 3
    }
    
    exp_data = main_lab.spawn_experiment(myth_engine, containment_rules)
    print(f"Spawned experiment in containment boundary: {myth_engine.boundary.get_full_path()}")
    
    # Create nested habitat before running experiment
    nested_lab = main_lab.nest_habitat(myth_engine.name, "recursive_sub_lab")
    print(f"Created nested habitat at depth: {nested_lab.nesting_depth}")
    
    # Run experiment
    try:
        result = main_lab.run_experiment(myth_engine.name)
        print("Experiment Result:")
        print(json.dumps(result, indent=2))
        
        # Graduate successful experiment
        forge_package = main_lab.graduate_to_forge(myth_engine.name)
        print(f"Experiment graduated to Code Forge")
        
    except Exception as e:
        # Handle failure
        lessons = main_lab.contain_failure(myth_engine.name, str(e))
        print(f"Experiment failed safely. Lessons learned: {lessons}")
    
    # Show habitat status
    status = main_lab.get_habitat_status()
    print("\nHabitat Status:")
    print(json.dumps(status, indent=2))
    
    # Cleanup
    main_lab.cleanup()
    nested_lab.cleanup()
    print("\nHabitat demonstration complete!")

if __name__ == "__main__":
    demonstrate_experimental_habitat()