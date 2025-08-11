#!/usr/bin/env python3
"""
Containment Validation Script
INTERNAL_ENV_ONLY - This script is for internal use within 4_S0VRC3 environment only.

This script validates that all markdown files within the repository comply with
the environment containment policy by checking for required internal banners
and detecting prohibited global phrases that could lead to unintended propagation.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Tuple, Set

# Required banner text for internal documents
REQUIRED_BANNER = "INTERNAL_ENV_ONLY"

# Prohibited phrases that might indicate uncontrolled export
PROHIBITED_PHRASES = [
    "use globally",
    "apply everywhere", 
    "standard practice",
    "global pattern",
    "universal rule",
    "export this",
    "use in all repos",
    "cross-repo standard"
]

# Files and directories to skip during validation
SKIP_PATTERNS = [
    ".git/",
    ".github/workflows/",
    "node_modules/",
    ".obsidian/",
    ".makemd/",
    ".space/",
    ".trash/",
    "README.md"  # Skip main README as it's public-facing
]

class ContainmentValidator:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def should_skip(self, file_path: Path) -> bool:
        """Check if a file should be skipped during validation."""
        path_str = str(file_path.relative_to(self.repo_path))
        
        for pattern in SKIP_PATTERNS:
            if pattern in path_str:
                return True
                
        return False
    
    def check_banner_presence(self, file_path: Path) -> bool:
        """Check if a markdown file contains the required internal banner."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if banner is present in the first few lines
            lines = content.split('\n')[:10]  # Check first 10 lines
            for line in lines:
                if REQUIRED_BANNER in line:
                    return True
                    
            return False
            
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            return False
    
    def check_prohibited_phrases(self, file_path: Path) -> List[str]:
        """Check for prohibited phrases that might indicate uncontrolled export."""
        found_phrases = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            for phrase in PROHIBITED_PHRASES:
                if phrase.lower() in content:
                    found_phrases.append(phrase)
                    
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            
        return found_phrases
    
    def check_symlinks(self) -> List[Path]:
        """Detect symlinks that might bypass containment."""
        symlinks = []
        
        for path in self.repo_path.rglob("*"):
            if path.is_symlink() and not self.should_skip(path):
                symlinks.append(path)
                
        return symlinks
    
    def validate_policy_files(self) -> None:
        """Validate that policy and documentation files have required banners."""
        policy_patterns = [
            "docs/policies/*.md",
            "*POLICY*.md",
            "*MANIFEST*.md", 
            "*PLAYBOOK*.md"
        ]
        
        policy_files = set()
        for pattern in policy_patterns:
            policy_files.update(self.repo_path.glob(pattern))
            policy_files.update(self.repo_path.rglob(pattern))
            
        for file_path in policy_files:
            if self.should_skip(file_path):
                continue
                
            if not self.check_banner_presence(file_path):
                self.errors.append(
                    f"Missing INTERNAL_ENV_ONLY banner: {file_path.relative_to(self.repo_path)}"
                )
    
    def validate_all_markdown(self) -> None:
        """Validate all markdown files for prohibited phrases."""
        for file_path in self.repo_path.rglob("*.md"):
            if self.should_skip(file_path):
                continue
                
            prohibited = self.check_prohibited_phrases(file_path)
            for phrase in prohibited:
                self.warnings.append(
                    f"Prohibited phrase '{phrase}' found in: {file_path.relative_to(self.repo_path)}"
                )
    
    def validate_symlinks(self) -> None:
        """Check for symlinks that might bypass containment."""
        symlinks = self.check_symlinks()
        
        for symlink in symlinks:
            target = symlink.resolve()
            if not str(target).startswith(str(self.repo_path)):
                self.warnings.append(
                    f"External symlink detected (potential containment bypass): {symlink.relative_to(self.repo_path)} -> {target}"
                )
    
    def run_validation(self) -> bool:
        """Run all validation checks."""
        print("🔍 Running containment validation...")
        print(f"Repository: {self.repo_path}")
        print()
        
        # Run validation checks
        self.validate_policy_files()
        self.validate_all_markdown()
        self.validate_symlinks()
        
        # Report results
        print("📋 Validation Results:")
        print("=" * 50)
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
            print()
            
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
            
        if not self.errors and not self.warnings:
            print("✅ All containment checks passed!")
            print()
            
        # Summary
        total_issues = len(self.errors) + len(self.warnings)
        if total_issues > 0:
            print(f"📊 Summary: {len(self.errors)} errors, {len(self.warnings)} warnings")
        else:
            print("📊 Summary: No issues detected")
            
        return len(self.errors) == 0

def main():
    """Main entry point for the validation script."""
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = os.getcwd()
        
    validator = ContainmentValidator(repo_path)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()