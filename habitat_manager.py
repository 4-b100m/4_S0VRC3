#!/usr/bin/env python3
"""
HABITAT_MANAGER.py

Management interface for the Experimental Habitat system.
This script provides a command-line interface for spawning, managing,
and monitoring experimental systems within nested containment environments.

Usage:
    python3 habitat_manager.py spawn <experiment_name> --hypothesis "test hypothesis"
    python3 habitat_manager.py run <experiment_name>
    python3 habitat_manager.py status [experiment_name]
    python3 habitat_manager.py graduate <experiment_name>
    python3 habitat_manager.py compost <experiment_name> --reason "failure reason"
    python3 habitat_manager.py nest <parent_exp> <child_name>
    python3 habitat_manager.py list-habitats
    python3 habitat_manager.py cleanup
"""

import argparse
import json
import os
import sys
from datetime import datetime
from experimental_habitat_implementation import ExperimentalHabitat, ExperimentalSystem, RecursiveMythEngine

class HabitatManager:
    """Manager for experimental habitat operations"""
    
    def __init__(self, config_file: str = "habitat_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.habitats = {}
        self.initialize_habitats()
    
    def load_config(self) -> dict:
        """Load or create habitat configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Default configuration
            default_config = {
                "default_habitat": {
                    "name": "main_lab",
                    "isolation_level": 3,
                    "default_containment": {
                        "resources": {"cpu": "50%", "memory": "512M"},
                        "network_isolation": True,
                        "time_limit": 1800,
                        "recursive_depth_limit": 5
                    }
                },
                "experiment_types": {
                    "recursive_myth": "RecursiveMythEngine",
                    "pattern_test": "PatternTestSystem",
                    "symbolic_loop": "SymbolicLoopSystem"
                }
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: dict = None):
        """Save habitat configuration"""
        if config is None:
            config = self.config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def initialize_habitats(self):
        """Initialize habitat instances"""
        default_config = self.config["default_habitat"]
        main_habitat = ExperimentalHabitat(
            name=default_config["name"],
            isolation_level=default_config["isolation_level"]
        )
        self.habitats["main"] = main_habitat
    
    def spawn_experiment(self, name: str, experiment_type: str = "recursive_myth", 
                        hypothesis: str = "Default experiment hypothesis", 
                        containment_rules: dict = None) -> dict:
        """Spawn a new experimental system"""
        
        if containment_rules is None:
            containment_rules = self.config["default_habitat"]["default_containment"]
        
        # Create experiment instance based on type
        if experiment_type == "recursive_myth":
            experiment = RecursiveMythEngine()
            experiment.name = name  # Override name
            experiment.hypothesis = hypothesis
        else:
            # Generic experimental system
            experiment = ExperimentalSystem(name, hypothesis)
        
        # Spawn in main habitat
        habitat = self.habitats["main"]
        exp_data = habitat.spawn_experiment(experiment, containment_rules)
        
        print(f"🧪 Spawned experiment '{name}' in habitat '{habitat.name}'")
        print(f"   Hypothesis: {hypothesis}")
        print(f"   Containment Level: {habitat.isolation_level}")
        print(f"   Boundary: {experiment.boundary.get_full_path()}")
        
        return exp_data
    
    def run_experiment(self, name: str, habitat_name: str = "main") -> dict:
        """Run a spawned experiment"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"🚀 Running experiment '{name}' in habitat '{habitat_name}'...")
        
        try:
            result = habitat.run_experiment(name)
            print(f"✅ Experiment '{name}' completed successfully")
            print("Result summary:")
            if isinstance(result, dict):
                for key, value in result.items():
                    if key != "nested":  # Don't print nested recursion
                        print(f"   {key}: {value}")
            else:
                print(f"   {result}")
            return result
        except Exception as e:
            print(f"❌ Experiment '{name}' failed: {e}")
            raise
    
    def get_status(self, experiment_name: str = None, habitat_name: str = "main") -> dict:
        """Get habitat or experiment status"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        if experiment_name:
            # Get specific experiment status
            if experiment_name in habitat.active_experiments:
                exp_data = habitat.active_experiments[experiment_name]
                experiment = exp_data['experiment']
                status = {
                    'name': experiment_name,
                    'status': experiment.status,
                    'hypothesis': experiment.hypothesis,
                    'created': experiment.created,
                    'boundary': experiment.boundary.get_full_path() if experiment.boundary else None,
                    'workspace': exp_data.get('workspace'),
                    'containment_rules': exp_data.get('containment_rules')
                }
                print(f"📊 Status for experiment '{experiment_name}':")
                print(json.dumps(status, indent=2))
                return status
            elif experiment_name in habitat.graduated_patterns:
                print(f"🎓 Experiment '{experiment_name}' has graduated to Code Forge")
                return habitat.graduated_patterns[experiment_name]
            elif experiment_name in habitat.failed_experiments:
                print(f"💀 Experiment '{experiment_name}' has been composted")
                return habitat.failed_experiments[experiment_name]
            else:
                print(f"❓ Experiment '{experiment_name}' not found in habitat '{habitat_name}'")
                return {}
        else:
            # Get habitat status
            status = habitat.get_habitat_status()
            print(f"🏠 Status for habitat '{habitat_name}':")
            print(json.dumps(status, indent=2))
            return status
    
    def graduate_experiment(self, name: str, habitat_name: str = "main") -> dict:
        """Graduate an experiment to the Code Forge"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"🎓 Graduating experiment '{name}' to Code Forge...")
        
        try:
            forge_package = habitat.graduate_to_forge(name)
            print(f"✅ Experiment '{name}' successfully graduated!")
            print("Forge package contents:")
            print(f"   Code patterns: {forge_package['code_patterns']}")
            print(f"   Symbolic mappings: {forge_package['symbolic_mappings']}")
            print(f"   Integration hooks: {forge_package['integration_hooks']}")
            return forge_package
        except Exception as e:
            print(f"❌ Failed to graduate experiment '{name}': {e}")
            raise
    
    def compost_experiment(self, name: str, reason: str, habitat_name: str = "main") -> dict:
        """Compost a failed experiment"""
        habitat = self.habitats.get(habitat_name)
        if not habitat:
            raise ValueError(f"Habitat '{habitat_name}' not found")
        
        print(f"♻️  Composting experiment '{name}' - Reason: {reason}")
        
        try:
            lessons = habitat.contain_failure(name, reason)
            print(f"✅ Experiment '{name}' safely composted")
            print("Lessons learned:")
            for lesson_type, lesson_data in lessons.items():
                print(f"   {lesson_type}: {lesson_data}")
            return lessons
        except Exception as e:
            print(f"❌ Failed to compost experiment '{name}': {e}")
            raise
    
    def create_nested_habitat(self, parent_experiment: str, child_name: str, 
                            parent_habitat: str = "main") -> 'ExperimentalHabitat':
        """Create a nested habitat"""
        parent_hab = self.habitats.get(parent_habitat)
        if not parent_hab:
            raise ValueError(f"Parent habitat '{parent_habitat}' not found")
        
        print(f"🪆 Creating nested habitat '{child_name}' under experiment '{parent_experiment}'...")
        
        try:
            nested_habitat = parent_hab.nest_habitat(parent_experiment, child_name)
            habitat_key = f"{parent_habitat}_{child_name}"
            self.habitats[habitat_key] = nested_habitat
            
            print(f"✅ Nested habitat '{child_name}' created successfully")
            print(f"   Nesting depth: {nested_habitat.nesting_depth}")
            print(f"   Isolation level: {nested_habitat.isolation_level}")
            print(f"   Access key: {habitat_key}")
            
            return nested_habitat
        except Exception as e:
            print(f"❌ Failed to create nested habitat: {e}")
            raise
    
    def list_habitats(self):
        """List all active habitats"""
        print("🏠 Active Habitats:")
        print("=" * 50)
        
        for key, habitat in self.habitats.items():
            status = habitat.get_habitat_status()
            print(f"📍 {key} ({habitat.name})")
            print(f"   Isolation Level: {status['isolation_level']}")
            print(f"   Nesting Depth: {status['nesting_depth']}")
            print(f"   Active Experiments: {status['active_experiments']}")
            print(f"   Graduated Patterns: {status['graduated_patterns']}")
            print(f"   Failed Experiments: {status['failed_experiments']}")
            print(f"   Workspace: {status['workspace']}")
            print()
    
    def cleanup_all(self):
        """Cleanup all habitats"""
        print("🧹 Cleaning up all habitats...")
        
        for key, habitat in self.habitats.items():
            try:
                habitat.cleanup()
                print(f"✅ Cleaned up habitat '{key}'")
            except Exception as e:
                print(f"❌ Failed to cleanup habitat '{key}': {e}")
        
        print("🎉 Cleanup complete!")

def main():
    """Main command-line interface"""
    parser = argparse.ArgumentParser(description="Experimental Habitat Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Spawn command
    spawn_parser = subparsers.add_parser('spawn', help='Spawn a new experiment')
    spawn_parser.add_argument('name', help='Experiment name')
    spawn_parser.add_argument('--type', default='recursive_myth', help='Experiment type')
    spawn_parser.add_argument('--hypothesis', default='Default experimental hypothesis', help='Experiment hypothesis')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run an experiment')
    run_parser.add_argument('name', help='Experiment name')
    run_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Get status')
    status_parser.add_argument('name', nargs='?', help='Experiment name (optional)')
    status_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Graduate command
    grad_parser = subparsers.add_parser('graduate', help='Graduate experiment to Code Forge')
    grad_parser.add_argument('name', help='Experiment name')
    grad_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Compost command
    compost_parser = subparsers.add_parser('compost', help='Compost failed experiment')
    compost_parser.add_argument('name', help='Experiment name')
    compost_parser.add_argument('--reason', required=True, help='Failure reason')
    compost_parser.add_argument('--habitat', default='main', help='Habitat name')
    
    # Nest command
    nest_parser = subparsers.add_parser('nest', help='Create nested habitat')
    nest_parser.add_argument('parent_experiment', help='Parent experiment name')
    nest_parser.add_argument('child_name', help='Child habitat name')
    nest_parser.add_argument('--parent-habitat', default='main', help='Parent habitat name')
    
    # List command
    subparsers.add_parser('list-habitats', help='List all habitats')
    
    # Cleanup command
    subparsers.add_parser('cleanup', help='Cleanup all habitats')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize manager
    manager = HabitatManager()
    
    try:
        if args.command == 'spawn':
            manager.spawn_experiment(args.name, args.type, args.hypothesis)
            
        elif args.command == 'run':
            manager.run_experiment(args.name, args.habitat)
            
        elif args.command == 'status':
            manager.get_status(args.name, args.habitat)
            
        elif args.command == 'graduate':
            manager.graduate_experiment(args.name, args.habitat)
            
        elif args.command == 'compost':
            manager.compost_experiment(args.name, args.reason, args.habitat)
            
        elif args.command == 'nest':
            manager.create_nested_habitat(args.parent_experiment, args.child_name, args.parent_habitat)
            
        elif args.command == 'list-habitats':
            manager.list_habitats()
            
        elif args.command == 'cleanup':
            manager.cleanup_all()
            
    except Exception as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()